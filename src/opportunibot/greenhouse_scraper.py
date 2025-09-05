"""
Greenhouse ATS Scraper

Scrapes jobs from companies using Greenhouse ATS via their public API.
"""

import logging
import json
from typing import List, Dict, Any
from datetime import datetime
from .models import JobListing, JobSource
from .scrapers import BaseScraper

logger = logging.getLogger(__name__)


class GreenhouseScraper(BaseScraper):
    """Scraper for Greenhouse ATS jobs"""
    
    API_BASE_URL = "https://boards-api.greenhouse.io/v1/boards"
    
    def search_jobs(self) -> List[JobListing]:
        """Search for jobs from Greenhouse companies
        
        Returns:
            List of JobListing objects
        """
        logger.info("Starting Greenhouse job search...")
        
        all_jobs = []
        companies = self.config.target_companies.greenhouse_companies
        
        if not companies:
            logger.warning("No Greenhouse companies configured")
            return []
        
        logger.info(f"Searching {len(companies)} Greenhouse companies")
        
        for company in companies:
            try:
                jobs = self._scrape_company_jobs(company)
                filtered_jobs = [job for job in jobs if self._should_include_job(job)]
                
                all_jobs.extend(filtered_jobs)
                
                logger.info(f"{company}: {len(jobs)} jobs found, {len(filtered_jobs)} after filtering")
                self.stats.companies_scraped += 1
                
            except Exception as e:
                logger.error(f"Error scraping {company}: {e}")
                self.stats.errors += 1
                continue
        
        self.stats.total_jobs_found = len(all_jobs)
        logger.info(f"Greenhouse search complete: {len(all_jobs)} jobs from {self.stats.companies_scraped} companies")
        
        return all_jobs
    
    def _scrape_company_jobs(self, company: str) -> List[JobListing]:
        """Scrape jobs from a specific Greenhouse company
        
        Args:
            company: Company identifier (e.g., 'moderna', 'ginkgo-bioworks')
            
        Returns:
            List of JobListing objects
        """
        url = f"{self.API_BASE_URL}/{company}/jobs"
        
        try:
            response = self._make_request(url)
            data = response.json()
            
            jobs = []
            jobs_data = data.get('jobs', [])
            
            for job_data in jobs_data:
                try:
                    job = self._parse_job_data(job_data, company)
                    if job:
                        jobs.append(job)
                except Exception as e:
                    logger.debug(f"Error parsing job from {company}: {e}")
                    continue
            
            return jobs
            
        except Exception as e:
            logger.error(f"Failed to fetch jobs for {company}: {e}")
            raise
    
    def _parse_job_data(self, job_data: Dict[str, Any], company: str) -> JobListing:
        """Parse job data from Greenhouse API response
        
        Args:
            job_data: Raw job data from API
            company: Company identifier
            
        Returns:
            JobListing object or None if parsing fails
        """
        try:
            # Extract basic job information
            job_id = str(job_data.get('id', ''))
            title = self._clean_text(job_data.get('title', ''))
            
            # Handle location data
            location_data = job_data.get('location', {})
            if isinstance(location_data, dict):
                location = location_data.get('name', 'Location not specified')
            else:
                location = str(location_data) if location_data else 'Location not specified'
            
            # Clean and extract description
            content = job_data.get('content', '')
            if content:
                # Remove HTML tags for cleaner text
                description = self._clean_html_content(content)
            else:
                description = ''
            
            # Build job URL
            absolute_url = job_data.get('absolute_url', '')
            if not absolute_url:
                # Fallback: construct URL from ID
                absolute_url = f"https://boards.greenhouse.io/{company}/jobs/{job_id}"
            
            # Extract additional metadata
            posted_date = job_data.get('updated_at', datetime.now().isoformat())
            
            # Create JobListing object
            job = JobListing(
                title=title,
                company=self._format_company_name(company),
                location=self._clean_text(location),
                url=absolute_url,
                description=description,
                source=JobSource.GREENHOUSE,
                job_id=f"gh_{company}_{job_id}",
                posted_date=posted_date
            )
            
            return job
            
        except Exception as e:
            logger.debug(f"Error parsing job data: {e}")
            return None
    
    def _clean_html_content(self, html_content: str) -> str:
        """Clean HTML content and extract text
        
        Args:
            html_content: Raw HTML content
            
        Returns:
            Cleaned text content
        """
        try:
            from bs4 import BeautifulSoup
            
            # Parse HTML and extract text
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text and clean it
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text
            
        except Exception as e:
            logger.debug(f"Error cleaning HTML content: {e}")
            # Fallback: return raw content
            return self._clean_text(html_content)
    
    def _format_company_name(self, company_id: str) -> str:
        """Format company identifier to readable name
        
        Args:
            company_id: Company identifier from config (e.g., 'ginkgo-bioworks')
            
        Returns:
            Formatted company name (e.g., 'Ginkgo Bioworks')
        """
        # Handle common company formatting
        company_map = {
            'ginkgo-bioworks': 'Ginkgo Bioworks',
            '10x-genomics': '10x Genomics',
            'twist-bioscience': 'Twist Bioscience',
            'pacific-biosciences': 'Pacific Biosciences',
            'guardant-health': 'Guardant Health',
            'exact-sciences': 'Exact Sciences',
            'flatiron-health': 'Flatiron Health',
            'foundation-medicine': 'Foundation Medicine',
        }
        
        if company_id in company_map:
            return company_map[company_id]
        
        # Default: title case with hyphens replaced by spaces
        return company_id.replace('-', ' ').title()
    
    def _should_include_job(self, job: JobListing) -> bool:
        """Enhanced job filtering specific to Greenhouse jobs
        
        Args:
            job: JobListing to evaluate
            
        Returns:
            True if job should be included
        """
        # Use base filtering first
        if not super()._should_include_job(job):
            return False
        
        # NOTE: Greenhouse main API doesn't include job descriptions,
        # so we can't filter on description length. We'll rely on 
        # title and company filtering for now.
        
        # Additional Greenhouse-specific filtering could go here
        # For example, checking for specific departments, job types, etc.
        
        return True
    
    def get_stats(self) -> Dict[str, Any]:
        """Get scraping statistics
        
        Returns:
            Dictionary with scraping stats
        """
        return {
            'source': 'greenhouse',
            'companies_scraped': self.stats.companies_scraped,
            'total_jobs_found': self.stats.total_jobs_found,
            'errors': self.stats.errors,
            'api_base_url': self.API_BASE_URL
        }
