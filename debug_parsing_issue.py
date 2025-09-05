# Debug why the parsing is failing

import requests
import json
import sys
sys.path.append('.')

from opportunibot.greenhouse_scraper import GreenhouseScraper
from opportunibot.config import load_config

# Get one job from Stripe to debug parsing
print("🔍 Testing job parsing with real API data...")

url = "https://boards-api.greenhouse.io/v1/boards/stripe/jobs"
response = requests.get(url)
data = response.json()
jobs_data = data.get('jobs', [])

if not jobs_data:
    print("❌ No jobs returned from API")
    exit()

# Get first job for testing
first_job = jobs_data[0]

print(f"📝 Raw job data from API:")
print(json.dumps(first_job, indent=2))
print(f"\nJob keys: {list(first_job.keys())}")

# Now test our parsing logic
config = load_config('job_search_config.yaml')
scraper = GreenhouseScraper(config, 'greenhouse')

print(f"\n🧪 Testing our parsing logic...")

try:
    parsed_job = scraper._parse_job_data(first_job, 'stripe')
    if parsed_job:
        print("✅ Parsing successful!")
        print(f"   Title: {parsed_job.title}")
        print(f"   Company: {parsed_job.company}")
        print(f"   Location: {parsed_job.location}")
        print(f"   URL: {parsed_job.url}")
        print(f"   Description length: {len(parsed_job.description)}")
        print(f"   Job ID: {parsed_job.job_id}")
    else:
        print("❌ Parsing returned None - job was rejected")
        
except Exception as e:
    print(f"❌ Parsing failed with exception: {e}")
    import traceback
    traceback.print_exc()

# Test with a few more jobs to see if it's consistent
print(f"\n🧪 Testing parsing on multiple jobs...")
success_count = 0
for i, job_data in enumerate(jobs_data[:5]):
    try:
        parsed = scraper._parse_job_data(job_data, 'stripe')
        if parsed:
            success_count += 1
            print(f"   Job {i+1}: ✅ {parsed.title}")
        else:
            print(f"   Job {i+1}: ❌ Failed to parse")
    except Exception as e:
        print(f"   Job {i+1}: ❌ Exception: {e}")

print(f"\n📊 Results: {success_count}/5 jobs parsed successfully")

if success_count == 0:
    print("\n🔍 All parsing failed - let's check specific issues:")
    
    # Check what fields are actually available
    sample_job = jobs_data[0]
    print(f"Available fields: {list(sample_job.keys())}")
    
    # Check if 'content' field exists (for job description)
    if 'content' not in sample_job:
        print("⚠️  No 'content' field - job descriptions not available in this API")
    
    # Check location structure
    location_data = sample_job.get('location', {})
    print(f"Location data type: {type(location_data)}")
    print(f"Location data: {location_data}")