"""
OpportuniBot Data Models

Defines the core data structures used throughout the application.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum


class JobSource(Enum):
    """Supported job sources"""
    INDEED = "indeed"
    GREENHOUSE = "greenhouse"
    LEVER = "lever"
    CUSTOM = "custom"


@dataclass
class JobListing:
    """Represents a single job listing"""
    
    # Basic job information
    title: str
    company: str
    location: str
    url: str
    description: str
    source: JobSource
    job_id: str
    
    # Optional fields
    posted_date: Optional[str] = None
    salary_range: Optional[str] = None
    requirements: Optional[List[str]] = None
    benefits: Optional[List[str]] = None
    job_type: Optional[str] = None  # full-time, contract, etc.
    experience_level: Optional[str] = None  # junior, senior, etc.
    
    # Metadata
    scraped_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Validate and clean data after initialization"""
        # Ensure job_id is unique and clean
        if not self.job_id:
            self.job_id = f"{self.source.value}_{hash(self.url)}"
        
        # Clean text fields
        self.title = self._clean_text(self.title)
        self.company = self._clean_text(self.company)
        self.location = self._clean_text(self.location)
        self.description = self._clean_text(self.description)
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        # Remove extra whitespace and normalize
        import re
        return re.sub(r'\s+', ' ', text.strip())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'title': self.title,
            'company': self.company,
            'location': self.location,
            'url': self.url,
            'description': self.description,
            'source': self.source.value,
            'job_id': self.job_id,
            'posted_date': self.posted_date,
            'salary_range': self.salary_range,
            'requirements': self.requirements,
            'benefits': self.benefits,
            'job_type': self.job_type,
            'experience_level': self.experience_level,
            'scraped_at': self.scraped_at.isoformat()
        }


@dataclass
class JobAnalysis:
    """Analysis results for a job listing"""
    
    job: JobListing
    match_score: float  # 0.0 to 1.0
    matched_keywords: List[str]
    fit_reasons: List[str]
    concerns: List[str] = field(default_factory=list)
    cover_letter: str = ""
    
    # Analysis details
    skill_matches: List[str] = field(default_factory=list)
    experience_match: bool = False
    location_match: bool = False
    industry_match: bool = False
    
    # Metadata
    analyzed_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Validate analysis data"""
        # Ensure match score is within bounds
        self.match_score = max(0.0, min(1.0, self.match_score))
        
        # Remove duplicates from lists
        self.matched_keywords = list(set(self.matched_keywords))
        self.fit_reasons = list(dict.fromkeys(self.fit_reasons))  # Preserve order
        self.skill_matches = list(set(self.skill_matches))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'job': self.job.to_dict(),
            'match_score': self.match_score,
            'matched_keywords': self.matched_keywords,
            'fit_reasons': self.fit_reasons,
            'concerns': self.concerns,
            'cover_letter': self.cover_letter,
            'skill_matches': self.skill_matches,
            'experience_match': self.experience_match,
            'location_match': self.location_match,
            'industry_match': self.industry_match,
            'analyzed_at': self.analyzed_at.isoformat()
        }


@dataclass
class UserProfile:
    """User's professional profile and preferences"""
    
    # Personal information
    name: str
    email: str
    phone: str = ""
    linkedin: str = ""
    location: str = ""
    
    # Professional background
    summary: str = ""
    technical_skills: List[str] = field(default_factory=list)
    soft_skills: List[str] = field(default_factory=list)
    experience_years: int = 0
    industries: List[str] = field(default_factory=list)
    
    # Education
    education_degree: str = ""
    education_school: str = ""
    education_year: Optional[int] = None
    
    def __post_init__(self):
        """Validate and clean profile data"""
        # Clean skill lists
        self.technical_skills = [skill.strip() for skill in self.technical_skills if skill.strip()]
        self.soft_skills = [skill.strip() for skill in self.soft_skills if skill.strip()]
        self.industries = [industry.strip() for industry in self.industries if industry.strip()]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'linkedin': self.linkedin,
            'location': self.location,
            'summary': self.summary,
            'technical_skills': self.technical_skills,
            'soft_skills': self.soft_skills,
            'experience_years': self.experience_years,
            'industries': self.industries,
            'education_degree': self.education_degree,
            'education_school': self.education_school,
            'education_year': self.education_year
        }


@dataclass
class SearchCriteria:
    """Job search criteria and filters"""
    
    # Keywords
    required_keywords: List[str] = field(default_factory=list)
    preferred_keywords: List[str] = field(default_factory=list)
    excluded_keywords: List[str] = field(default_factory=list)
    
    # Location preferences
    locations: List[str] = field(default_factory=list)
    remote_ok: bool = True
    
    # Job preferences
    job_types: List[str] = field(default_factory=lambda: ["full-time"])
    experience_levels: List[str] = field(default_factory=list)
    
    # Salary expectations
    min_salary: Optional[int] = None
    max_salary: Optional[int] = None
    
    # Filtering
    min_match_score: float = 0.6
    max_results: int = 15
    max_age_days: int = 14
    exclude_applied: bool = True
    excluded_companies: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate search criteria"""
        # Ensure match score is within bounds
        self.min_match_score = max(0.0, min(1.0, self.min_match_score))
        
        # Validate salary range
        if self.min_salary and self.max_salary:
            if self.min_salary > self.max_salary:
                self.min_salary, self.max_salary = self.max_salary, self.min_salary
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'required_keywords': self.required_keywords,
            'preferred_keywords': self.preferred_keywords,
            'excluded_keywords': self.excluded_keywords,
            'locations': self.locations,
            'remote_ok': self.remote_ok,
            'job_types': self.job_types,
            'experience_levels': self.experience_levels,
            'min_salary': self.min_salary,
            'max_salary': self.max_salary,
            'min_match_score': self.min_match_score,
            'max_results': self.max_results,
            'max_age_days': self.max_age_days,
            'exclude_applied': self.exclude_applied,
            'excluded_companies': self.excluded_companies
        }


@dataclass
class TargetCompanies:
    """Companies to specifically target for job searches"""
    
    greenhouse_companies: List[str] = field(default_factory=list)
    lever_companies: List[str] = field(default_factory=list)
    custom_companies: List[Dict[str, str]] = field(default_factory=list)
    
    def get_all_companies(self) -> List[str]:
        """Get all company names as a flat list"""
        companies = []
        companies.extend(self.greenhouse_companies)
        companies.extend(self.lever_companies)
        companies.extend([c.get('name', '') for c in self.custom_companies])
        return companies
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'greenhouse_companies': self.greenhouse_companies,
            'lever_companies': self.lever_companies,
            'custom_companies': self.custom_companies
        }


@dataclass 
class JobSearchConfig:
    """Complete configuration for job search"""
    
    user_profile: UserProfile
    search_criteria: SearchCriteria
    target_companies: TargetCompanies
    
    # Job source settings
    job_sources: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    
    # Output settings
    output_format: str = "pdf"
    output_directory: str = "./reports"
    open_report: bool = True
    
    def __post_init__(self):
        """Set default job source settings if not provided"""
        if not self.job_sources:
            self.job_sources = {
                'indeed': {'enabled': True, 'max_results_per_search': 20},
                'greenhouse': {'enabled': True},
                'lever': {'enabled': True}
            }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'user_profile': self.user_profile.to_dict(),
            'search_criteria': self.search_criteria.to_dict(),
            'target_companies': self.target_companies.to_dict(),
            'job_sources': self.job_sources,
            'output_format': self.output_format,
            'output_directory': self.output_directory,
            'open_report': self.open_report
        }