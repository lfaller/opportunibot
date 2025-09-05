"""
OpportuniBot Job Scrapers

Scraper infrastructure for discovering job opportunities from multiple sources.
"""

import time
import logging
import requests
import hashlib
from abc import ABC, abstractmethod
from typing import List, Dict, Set, Optional, Any
from dataclasses import dataclass
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

from .models import JobListing, JobSource, JobSearchConfig
from .config import ConfigurationError

logger = logging.getLogger(__name__)


@dataclass
class ScrapingStats:
    """Statistics for a scraping session"""
    total_jobs_found: int = 0
    jobs_after_filtering: int = 0
    companies_scraped: int = 0
    errors: int = 0
    scraping_time: float = 0.0
    source_breakdown: Dict[str, int] = None
    
    def __post_init__(self):
        if self.source_breakdown is None:
            self.source_breakdown = {}


class ScrapingError(Exception):
    """Raised when scraping encounters an error"""
    pass


class BaseScraper(ABC):
    """Base class for all job scrapers"""
    
    def __init__(self, config: JobSearchConfig, source_name: str):
        """Initialize base scraper
        
        Args:
            config: Job search configuration
            source_name: Name of the job source (e.g., 'greenhouse', 'lever')
        """
        self.config = config
        self.source_name = source_name
        self.source_config = config.job_sources.get(source_name, {})
        
        # Rate limiting settings
        self.default_delay = self.source_config.get('delay_between_requests', 2.0)
        self.max_retries = self.source_config.get('max_retries', 3)
        self.backoff_factor = self.source_config.get('backoff_factor', 1.5)
        
        # Setup session with proper headers
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        # Tracking
        self.stats = ScrapingStats()
        self.last_request_time = 0
        
        logger.info(f"Initialized {self.__class__.__name__} with {self.default_delay}s delay")
    
    @abstractmethod
    def search_jobs(self) -> List[JobListing]:
        """Search for jobs and return job listings
        
        Returns:
            List of JobListing objects
        """
        pass
    
    def _rate_limit(self):
        """Implement rate limiting between requests"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.default_delay:
            sleep_time = self.default_delay - elapsed
            logger.debug(f"Rate limiting: sleeping {sleep_time:.2f}s")
            time.sleep(sleep_time)
        self.last_request_time = time.time()
    
    def _make_request(self, url: str, **kwargs) -> requests.Response:
        """Make a rate-limited HTTP request with retry logic
        
        Args:
            url: URL to request
            **kwargs: Additional arguments for requests
            
        Returns:
            Response object
            
        Raises:
            ScrapingError: If request fails after retries
        """
        self._rate_limit()
        
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(url, timeout=30, **kwargs)
                
                if response.status_code == 200:
                    return response
                elif response.status_code == 429:
                    # Rate limited - wait longer
                    wait_time = self.default_delay * (self.backoff_factor ** attempt)
                    logger.warning(f"Rate limited (429) on {url}, waiting {wait_time:.1f}s")
                    time.sleep(wait_time)
                    continue
                elif response.status_code in [403, 404]:
                    # These are probably permanent, don't retry
                    logger.warning(f"HTTP {response.status_code} for {url}")
                    break
                else:
                    logger.warning(f"HTTP {response.status_code} for {url}, attempt {attempt + 1}")
                    
            except requests.exceptions.RequestException as e:
                logger.warning(f"Request failed for {url}: {e}, attempt {attempt + 1}")
                
                if attempt < self.max_retries - 1:
                    wait_time = self.default_delay * (self.backoff_factor ** attempt)
                    time.sleep(wait_time)
        
        # All retries failed
        self.stats.errors += 1
        raise ScrapingError(f"Failed to fetch {url} after {self.max_retries} attempts")
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text content"""
        if not text:
            return ""
        
        # Remove extra whitespace and normalize
        import re
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove common HTML entities that might slip through
        text = text.replace('&nbsp;', ' ').replace('&amp;', '&')
        
        return text
    
    def _matches_keywords(self, job_text: str, required_keywords: List[str], excluded_keywords: List[str]) -> bool:
        """Check if job text matches keyword criteria
        
        Args:
            job_text: Combined job title and description text
            required_keywords: Must have at least one of these
            excluded_keywords: Must not have any of these
            
        Returns:
            True if job matches criteria
        """
        job_text_lower = job_text.lower()
        
        # Check for excluded keywords first
        if excluded_keywords:
            for excluded in excluded_keywords:
                if excluded.lower() in job_text_lower:
                    logger.debug(f"Job excluded due to keyword: {excluded}")
                    return False
        
        # Check for required keywords
        if required_keywords:
            has_required = any(keyword.lower() in job_text_lower for keyword in required_keywords)
            if not has_required:
                logger.debug("Job excluded: no required keywords found")
                return False
        
        return True
    
    def _matches_location(self, job_location: str, target_locations: List[str]) -> bool:
        """Check if job location matches target locations
        
        Args:
            job_location: Job's location string
            target_locations: List of acceptable locations
            
        Returns:
            True if location matches
        """
        if not target_locations:
            return True
        
        job_location_lower = job_location.lower()
        
        # Check for remote work
        if 'remote' in job_location_lower and 'remote' in [loc.lower() for loc in target_locations]:
            return True
        
        # Check for location matches
        for target_location in target_locations:
            if target_location.lower() in job_location_lower:
                return True
        
        return False
    
    def _should_include_job(self, job: JobListing) -> bool:
        """Determine if job should be included based on criteria
        
        Args:
            job: JobListing to evaluate
            
        Returns:
            True if job should be included
        """
        search_criteria = self.config.search_criteria
        
        # Combine title and description for keyword matching
        job_text = f"{job.title} {job.description}"
        
        # Check keywords
        if not self._matches_keywords(job_text, search_criteria.required_keywords, search_criteria.excluded_keywords):
            return False
        
        # Check location
        if not self._matches_location(job.location, search_criteria.locations):
            return False
        
        # Check excluded companies
        if job.company.lower() in [company.lower() for company in search_criteria.excluded_companies]:
            logger.debug(f"Job excluded: company {job.company} is in excluded list")
            return False
        
        return True


class JobDeduplicator:
    """Handles deduplication of job listings"""
    
    def __init__(self):
        self.seen_jobs: Set[str] = set()
        self.job_signatures: Dict[str, JobListing] = {}
    
    def _create_signature(self, job: JobListing) -> str:
        """Create a unique signature for a job
        
        Args:
            job: JobListing to create signature for
            
        Returns:
            Unique signature string
        """
        # Create signature from normalized title + company + location
        signature_text = f"{job.title.lower().strip()} | {job.company.lower().strip()} | {job.location.lower().strip()}"
        
        # Use hash for consistent, shorter signatures
        return hashlib.md5(signature_text.encode()).hexdigest()
    
    def add_job(self, job: JobListing) -> bool:
        """Add job to deduplicator
        
        Args:
            job: JobListing to add
            
        Returns:
            True if job is new (not a duplicate), False if duplicate
        """
        signature = self._create_signature(job)
        
        if signature in self.seen_jobs:
            logger.debug(f"Duplicate job found: {job.title} at {job.company}")
            return False
        
        self.seen_jobs.add(signature)
        self.job_signatures[signature] = job
        return True
    
    def get_unique_jobs(self) -> List[JobListing]:
        """Get all unique jobs
        
        Returns:
            List of unique JobListing objects
        """
        return list(self.job_signatures.values())
    
    def get_stats(self) -> Dict[str, int]:
        """Get deduplication statistics
        
        Returns:
            Dictionary with deduplication stats
        """
        return {
            'unique_jobs': len(self.job_signatures),
            'total_processed': len(self.seen_jobs)
        }


class ScraperFactory:
    """Factory for creating and managing job scrapers"""
    
    def __init__(self, config: JobSearchConfig):
        """Initialize scraper factory
        
        Args:
            config: Job search configuration
        """
        self.config = config
        self.scrapers: List[BaseScraper] = []
        self._initialize_scrapers()
    
    def _initialize_scrapers(self):
        """Initialize all enabled scrapers"""
        # Import here to avoid circular imports
        from .greenhouse_scraper import GreenhouseScraper
        from .lever_scraper import LeverScraper
        from .indeed_scraper import IndeedScraper
        
        scraper_classes = {
            'greenhouse': GreenhouseScraper,
            'lever': LeverScraper,
            'indeed': IndeedScraper,
        }
        
        for source_name, source_config in self.config.job_sources.items():
            if source_config.get('enabled', False):
                scraper_class = scraper_classes.get(source_name)
                if scraper_class:
                    try:
                        scraper = scraper_class(self.config, source_name)
                        self.scrapers.append(scraper)
                        logger.info(f"Initialized {source_name} scraper")
                    except Exception as e:
                        logger.error(f"Failed to initialize {source_name} scraper: {e}")
                else:
                    logger.warning(f"Unknown scraper type: {source_name}")
    
    def search_all_sources(self) -> List[JobListing]:
        """Search all enabled job sources
        
        Returns:
            List of unique job listings from all sources
        """
        start_time = time.time()
        deduplicator = JobDeduplicator()
        all_jobs = []
        
        logger.info(f"Starting job search across {len(self.scrapers)} sources")
        
        for scraper in self.scrapers:
            try:
                logger.info(f"Searching {scraper.source_name}...")
                jobs = scraper.search_jobs()
                
                logger.info(f"Found {len(jobs)} jobs from {scraper.source_name}")
                
                # Add jobs to deduplicator
                unique_count = 0
                for job in jobs:
                    if deduplicator.add_job(job):
                        unique_count += 1
                        all_jobs.append(job)
                
                logger.info(f"Added {unique_count} unique jobs from {scraper.source_name}")
                
            except Exception as e:
                logger.error(f"Error searching {scraper.source_name}: {e}")
                continue
        
        total_time = time.time() - start_time
        
        # Log final statistics
        dedup_stats = deduplicator.get_stats()
        logger.info(f"Search completed in {total_time:.1f}s")
        logger.info(f"Total unique jobs: {len(all_jobs)}")
        logger.info(f"Deduplication: {dedup_stats}")
        
        return all_jobs
    
    def get_enabled_sources(self) -> List[str]:
        """Get list of enabled job sources
        
        Returns:
            List of enabled source names
        """
        return [scraper.source_name for scraper in self.scrapers]


def search_jobs(config: JobSearchConfig) -> List[JobListing]:
    """Main entry point for job searching
    
    Args:
        config: Job search configuration
        
    Returns:
        List of job listings from all enabled sources
    """
    try:
        factory = ScraperFactory(config)
        jobs = factory.search_all_sources()
        
        logger.info(f"Job search completed: {len(jobs)} jobs found")
        return jobs
        
    except Exception as e:
        logger.error(f"Job search failed: {e}")
        raise ScrapingError(f"Job search failed: {e}")