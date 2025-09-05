"""
OpportuniBot Configuration Management

Handles loading, validation, and management of configuration files.
"""

import os
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from .models import (
    JobSearchConfig, UserProfile, SearchCriteria, 
    TargetCompanies
)

logger = logging.getLogger(__name__)


class ConfigurationError(Exception):
    """Raised when there's an issue with configuration"""
    pass


class ConfigManager:
    """Manages configuration loading, validation, and creation"""
    
    DEFAULT_CONFIG_FILE = "job_search_config.yaml"
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize configuration manager
        
        Args:
            config_file: Path to configuration file. If None, uses default.
        """
        self.config_file = config_file or self.DEFAULT_CONFIG_FILE
        self._config_data: Optional[Dict[str, Any]] = None
        self._job_search_config: Optional[JobSearchConfig] = None
    
    def load_config(self) -> JobSearchConfig:
        """Load configuration from file
        
        Returns:
            JobSearchConfig object
            
        Raises:
            ConfigurationError: If config file doesn't exist or is invalid
        """
        if not os.path.exists(self.config_file):
            raise ConfigurationError(
                f"Configuration file not found: {self.config_file}\n"
                f"Create a job_search_config.yaml file first!"
            )
        
        try:
            with open(self.config_file, 'r') as f:
                self._config_data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ConfigurationError(f"Invalid YAML in config file: {e}")
        except Exception as e:
            raise ConfigurationError(f"Error reading config file: {e}")
        
        if not self._config_data:
            raise ConfigurationError("Configuration file is empty")
        
        # Validate and parse configuration
        self._job_search_config = self._parse_config(self._config_data)
        logger.info(f"Configuration loaded from {self.config_file}")
        
        return self._job_search_config
    
    def _parse_config(self, config_data: Dict[str, Any]) -> JobSearchConfig:
        """Parse raw config data into JobSearchConfig object
        
        Args:
            config_data: Raw configuration dictionary
            
        Returns:
            JobSearchConfig object
            
        Raises:
            ConfigurationError: If configuration is invalid
        """
        try:
            # Parse user profile
            user_profile_data = config_data.get('user_profile', {})
            personal_info = user_profile_data.get('personal_info', {})
            background = user_profile_data.get('background', {})
            education = background.get('education', {})
            skills = background.get('skills', {})
            
            user_profile = UserProfile(
                name=personal_info.get('name', ''),
                email=personal_info.get('email', ''),
                phone=personal_info.get('phone', ''),
                linkedin=personal_info.get('linkedin', ''),
                location=personal_info.get('location', ''),
                summary=background.get('summary', ''),
                technical_skills=skills.get('technical', []),
                soft_skills=skills.get('soft', []),
                experience_years=background.get('experience_years', 0),
                industries=background.get('industries', []),
                education_degree=education.get('degree', ''),
                education_school=education.get('school', ''),
                education_year=education.get('year')
            )
            
            # Parse search criteria
            search_data = config_data.get('search_criteria', {})
            keywords = search_data.get('keywords', {})
            salary_range = search_data.get('salary_range', {})
            filters = config_data.get('filters', {})
            
            search_criteria = SearchCriteria(
                required_keywords=keywords.get('required', []),
                preferred_keywords=keywords.get('preferred', []),
                excluded_keywords=keywords.get('excluded', []),
                locations=search_data.get('locations', []),
                remote_ok='remote' in [loc.lower() for loc in search_data.get('locations', [])],
                job_types=search_data.get('job_types', ['full-time']),
                experience_levels=search_data.get('experience_levels', []),
                min_salary=salary_range.get('min'),
                max_salary=salary_range.get('max'),
                min_match_score=filters.get('min_match_score', 0.6),
                max_results=filters.get('max_results', 15),
                max_age_days=filters.get('max_age_days', 14),
                exclude_applied=filters.get('exclude_applied', True),
                excluded_companies=filters.get('excluded_companies', [])
            )
            
            # Parse target companies
            companies_data = config_data.get('target_companies', {})
            target_companies = TargetCompanies(
                greenhouse_companies=companies_data.get('greenhouse_companies', []),
                lever_companies=companies_data.get('lever_companies', []),
                custom_companies=companies_data.get('custom_companies', [])
            )
            
            # Parse output settings
            output_data = config_data.get('output', {})
            
            # Create final config
            job_search_config = JobSearchConfig(
                user_profile=user_profile,
                search_criteria=search_criteria,
                target_companies=target_companies,
                job_sources=config_data.get('job_sources', {}),
                output_format=output_data.get('report_format', 'pdf'),
                output_directory=output_data.get('report_directory', './reports'),
                open_report=output_data.get('open_report', True)
            )
            
            return job_search_config
            
        except Exception as e:
            raise ConfigurationError(f"Error parsing configuration: {e}")
    
    def validate_config(self, config: Optional[JobSearchConfig] = None) -> bool:
        """Validate configuration
        
        Args:
            config: Configuration to validate. If None, uses loaded config.
            
        Returns:
            True if valid
            
        Raises:
            ConfigurationError: If configuration is invalid
        """
        if config is None:
            if self._job_search_config is None:
                raise ConfigurationError("No configuration loaded")
            config = self._job_search_config
        
        errors = []
        
        # Validate user profile
        if not config.user_profile.name:
            errors.append("User name is required")
        if not config.user_profile.email:
            errors.append("User email is required")
        
        # Validate search criteria
        if not config.search_criteria.required_keywords:
            errors.append("At least one required keyword must be specified")
        if not config.search_criteria.locations:
            errors.append("At least one location must be specified")
        
        # Validate target companies - optional warning
        total_companies = len(config.target_companies.get_all_companies())
        if total_companies == 0:
            logger.warning("No target companies specified - will only search general job boards")
        
        # Validate job sources
        enabled_sources = [
            source for source, settings in config.job_sources.items()
            if settings.get('enabled', False)
        ]
        if not enabled_sources:
            errors.append("At least one job source must be enabled")
        
        if errors:
            raise ConfigurationError("Configuration validation failed:\n" + "\n".join(f"- {error}" for error in errors))
        
        logger.info("Configuration validation passed")
        return True


def load_config(config_file: Optional[str] = None) -> JobSearchConfig:
    """Convenience function to load configuration
    
    Args:
        config_file: Path to configuration file
        
    Returns:
        JobSearchConfig object
    """
    manager = ConfigManager(config_file)
    return manager.load_config()


def create_example_config(output_path: Optional[str] = None) -> str:
    """Convenience function to create example configuration
    
    Args:
        output_path: Where to save the example config
        
    Returns:
        Path to created file
    """
    manager = ConfigManager()
    return manager.create_example_config(output_path)