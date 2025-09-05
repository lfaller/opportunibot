# Debug script to see what jobs are being found before filtering

import sys
sys.path.append('.')

from opportunibot.config import load_config
from opportunibot.greenhouse_scraper import GreenhouseScraper

# Load config
config = load_config('job_search_config.yaml')

# Temporarily modify config to see ALL jobs (no filtering)
original_required = config.search_criteria.required_keywords.copy()
original_excluded = config.search_criteria.excluded_keywords.copy()

# Remove all keyword filtering temporarily
config.search_criteria.required_keywords = []
config.search_criteria.excluded_keywords = []

print("🔍 Debug: Finding ALL jobs without keyword filtering...")
print(f"Original required keywords: {original_required[:3]}...")
print()

# Create scraper and search just a few companies
scraper = GreenhouseScraper(config, 'greenhouse')

# Test with just 2-3 companies to see job titles
test_companies = ['stripe', 'benchling', 'insitro']
config.target_companies.greenhouse_companies = test_companies

jobs = scraper.search_jobs()

print(f"📊 Found {len(jobs)} total jobs without filtering")
print()

if jobs:
    print("📋 Sample job titles found:")
    for i, job in enumerate(jobs[:15], 1):
        print(f"   {i:2}. {job.title}")
        print(f"       🏢 {job.company}")
        print(f"       📍 {job.location}")
        print()
    
    if len(jobs) > 15:
        print(f"   ... and {len(jobs) - 15} more jobs")
    
    print("🎯 Now let's see keyword matching:")
    print("Required keywords:", original_required[:5])
    print()
    
    # Test keyword matching on first few jobs
    for job in jobs[:5]:
        job_text = f"{job.title} {job.description}".lower()
        matches = []
        for keyword in original_required:
            if keyword.lower() in job_text:
                matches.append(keyword)
        
        print(f"'{job.title}' at {job.company}")
        if matches:
            print(f"   ✅ Matched: {matches}")
        else:
            print(f"   ❌ No required keyword matches")
            # Show what words ARE in the job title for debugging
            title_words = job.title.lower().split()
            interesting_words = [w for w in title_words if len(w) > 3]
            print(f"   📝 Title contains: {interesting_words}")
        print()

else:
    print("❌ No jobs found even without filtering - there may be another issue")

print("💡 Recommendations:")
print("1. Add broader keywords like 'software engineer', 'engineer', 'developer'")
print("2. Make required keywords less specific")  
print("3. Use preferred keywords instead of required for specific terms")