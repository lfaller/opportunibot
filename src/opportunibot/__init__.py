"""
OpportuniBot - AI-powered job search automation tool

Your intelligent assistant for finding and applying to relevant job opportunities.
"""

__version__ = "0.3.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .models import (
    JobListing, 
    JobAnalysis, 
    UserProfile, 
    SearchCriteria, 
    JobSearchConfig,
    TargetCompanies,
    JobSource
)
from .config import ConfigManager, ConfigurationError, load_config, create_example_config
from .scrapers import BaseScraper, JobDeduplicator, ScraperFactory, search_jobs

__all__ = [
    "JobListing",
    "JobAnalysis", 
    "UserProfile",
    "SearchCriteria",
    "JobSearchConfig",
    "TargetCompanies",
    "JobSource",
    "ConfigManager",
    "ConfigurationError",
    "load_config",
    "create_example_config",
    "BaseScraper",
    "JobDeduplicator",
    "ScraperFactory",
    "search_jobs",
]
