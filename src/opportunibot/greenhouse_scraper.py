"""
Greenhouse ATS Scraper

Scrapes jobs from companies using Greenhouse ATS.
"""

import logging
from typing import List
from .models import JobListing, JobSource
from .scrapers import BaseScraper

logger = logging.getLogger(__name__)


class GreenhouseScraper(BaseScraper):
    """Scraper for Greenhouse ATS jobs"""
    
    def search_jobs(self) -> List[JobListing]:
        """Search for jobs from Greenhouse companies
        
        Returns:
            List of JobListing objects
        """
        # Placeholder - will implement in next step
        logger.info("Greenhouse scraper: Implementation coming soon!")
        return []
