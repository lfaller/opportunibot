"""
OpportuniBot Search Engine

Orchestrates job scraping, analysis, and result compilation.
"""

import logging
from typing import List
from datetime import datetime

from .models import JobListing, JobAnalysis, JobSearchConfig
from .scrapers import ScraperFactory
from .config import ConfigurationError

logger = logging.getLogger(__name__)


class SearchEngine:
    """Main search engine that orchestrates job discovery and analysis"""
    
    def __init__(self, config: JobSearchConfig):
        """Initialize the search engine
        
        Args:
            config: Job search configuration
        """
        self.config = config
        self.scraper_factory = ScraperFactory(config)
        
    def search_jobs(self, verbose: bool = False) -> List[JobListing]:
        """Execute a complete job search
        
        Args:
            verbose: Enable verbose logging
            
        Returns:
            List of job listings found and filtered
        """
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        
        logger.info("Starting job search...")
        start_time = datetime.now()
        
        try:
            # Scrape jobs from all enabled sources
            raw_jobs = self.scraper_factory.scrape_all_sources()
            logger.info(f"Found {len(raw_jobs)} total jobs")
            
            # Apply additional filtering
            filtered_jobs = self._apply_filters(raw_jobs)
            logger.info(f"After filtering: {len(filtered_jobs)} jobs")
            
            # Sort by relevance (for now, just by company preference)
            sorted_jobs = self._sort_jobs(filtered_jobs)
            
            # Limit results
            max_results = self.config.search_criteria.max_results
            final_jobs = sorted_jobs[:max_results]
            
            duration = datetime.now() - start_time
            logger.info(f"Job search completed in {duration.total_seconds():.1f}s")
            logger.info(f"Returning {len(final_jobs)} jobs")
            
            return final_jobs
            
        except Exception as e:
            logger.error(f"Error during job search: {e}")
            raise
    
    def _apply_filters(self, jobs: List[JobListing]) -> List[JobListing]:
        """Apply additional filtering beyond scraper-level filtering
        
        Args:
            jobs: List of jobs to filter
            
        Returns:
            Filtered list of jobs
        """
        filtered_jobs = []
        
        for job in jobs:
            # Check if company is in excluded list
            excluded_companies = self.config.search_criteria.excluded_companies
            if excluded_companies:
                if job.company.lower() in [company.lower() for company in excluded_companies]:
                    logger.debug(f"Excluding job from {job.company} (in excluded list)")
                    continue
            
            # Additional filters can be added here
            # - Date filtering
            # - Salary filtering
            # - Custom keyword filtering
            
            filtered_jobs.append(job)
        
        return filtered_jobs
    
    def _sort_jobs(self, jobs: List[JobListing]) -> List[JobListing]:
        """Sort jobs by relevance/preference
        
        Args:
            jobs: List of jobs to sort
            
        Returns:
            Sorted list of jobs
        """
        # Simple sorting by source preference and company name for now
        # Later this will be replaced with actual relevance scoring
        
        def sort_key(job):
            # Prefer certain companies
            target_companies = (
                self.config.target_companies.greenhouse_companies +
                self.config.target_companies.lever_companies +
                [c.get('name', '') for c in self.config.target_companies.custom_companies]
            )
            
            company_priority = 0
            if job.company.lower().replace(' ', '-') in [c.lower() for c in target_companies]:
                company_priority = 1
            
            # Prefer certain sources
            source_priority = {
                'greenhouse': 3,
                'lever': 2,
                'indeed': 1
            }.get(job.source.value, 0)
            
            return (company_priority, source_priority, job.company.lower())
        
        return sorte