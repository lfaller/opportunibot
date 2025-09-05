"""
Pytest configuration and shared fixtures
"""

import pytest
import tempfile
import os
from pathlib import Path
from typing import Dict, Any

from opportunibot.models import JobListing, JobSource, UserProfile, SearchCriteria, TargetCompanies, JobSearchConfig
from opportunibot.config import ConfigManager


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_job_listing():
    """Create a sample job listing for testing"""
    return JobListing(
        title="Senior Python Developer",
        company="TechCorp Inc",
        location="San Francisco, CA",
        url="https://example.com/jobs/123",
        description="We are looking for a senior Python developer with 5+ years of experience...",
        source=JobSource.GREENHOUSE,
        job_id="test_job_123",
        posted_date="2024-01-15",
        salary_range="$120,000 - $160,000",
        job_type="full-time",
        experience_level="senior"
    )


@pytest.fixture
def sample_user_profile():
    """Create a sample user profile for testing"""
    return UserProfile(
        name="Jane Developer",
        email="jane@example.com",
        phone="(555) 123-4567",
        linkedin="https://linkedin.com/in/jane-dev",
        location="San Francisco, CA",
        summary="Experienced Python developer with 5 years of experience",
        technical_skills=["Python", "JavaScript", "React", "SQL", "AWS"],
        soft_skills=["Team Leadership", "Project Management"],
        experience_years=5,
        industries=["Technology", "SaaS"],
        education_degree="Bachelor of Science in Computer Science",
        education_school="UC Berkeley",
        education_year=2018
    )


@pytest.fixture
def sample_search_criteria():
    """Create sample search criteria for testing"""
    return SearchCriteria(
        required_keywords=["python developer", "software engineer"],
        preferred_keywords=["react", "aws", "startup"],
        excluded_keywords=["intern", "junior"],
        locations=["San Francisco", "Remote"],
        job_types=["full-time"],
        experience_levels=["mid-level", "senior"],
        min_salary=100000,
        max_salary=180000,
        min_match_score=0.6,
        max_results=10
    )


@pytest.fixture
def sample_target_companies():
    """Create sample target companies for testing"""
    return TargetCompanies(
        greenhouse_companies=["stripe", "airbnb"],
        lever_companies=["uber", "lyft"],
        custom_companies=[
            {"name": "OpenAI", "careers_url": "https://openai.com/careers", "type": "custom"}
        ]
    )


@pytest.fixture
def sample_job_search_config(sample_user_profile, sample_search_criteria, sample_target_companies):
    """Create a complete job search configuration for testing"""
    return JobSearchConfig(
        user_profile=sample_user_profile,
        search_criteria=sample_search_criteria,
        target_companies=sample_target_companies,
        job_sources={
            "indeed": {"enabled": True, "max_results_per_search": 20},
            "greenhouse": {"enabled": True},
            "lever": {"enabled": True}
        },
        output_format="pdf",
        output_directory="./test_reports",
        open_report=False
    )


@pytest.fixture
def config_manager_with_temp_file(temp_dir):
    """Create a config manager with a temporary config file"""
    config_file = temp_dir / "test_config.yaml"
    return ConfigManager(str(config_file))


@pytest.fixture
def sample_config_dict():
    """Sample configuration dictionary for testing"""
    return {
        'user_profile': {
            'personal_info': {
                'name': 'Test User',
                'email': 'test@example.com',
                'location': 'Test City'
            },
            'background': {
                'summary': 'Test summary',
                'skills': {
                    'technical': ['Python', 'JavaScript'],
                    'soft': ['Communication']
                },
                'experience_years': 3,
                'industries': ['Technology'],
                'education': {
                    'degree': 'Bachelor of Science',
                    'school': 'Test University',
                    'year': 2020
                }
            }
        },
        'search_criteria': {
            'keywords': {
                'required': ['software engineer'],
                'preferred': ['python'],
                'excluded': ['intern']
            },
            'locations': ['Remote'],
            'job_types': ['full-time'],
            'experience_levels': ['mid-level']
        },
        'target_companies': {
            'greenhouse_companies': ['testcorp'],
            'lever_companies': ['testcompany'],
            'custom_companies': []
        },
        'job_sources': {
            'indeed': {'enabled': True},
            'greenhouse': {'enabled': True},
            'lever': {'enabled': False}
        },
        'filters': {
            'min_match_score': 0.6,
            'max_results': 10,
            'exclude_applied': True,
            'max_age_days': 14
        },
        'output': {
            'report_format': 'pdf',
            'report_directory': './reports',
            'open_report': True
        }
    }
