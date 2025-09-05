# Direct API test to see what's happening

import requests
import json

def test_company_api(company):
    """Test Greenhouse API for a specific company"""
    url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"
    
    print(f"\n🔍 Testing: {company}")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            jobs = data.get('jobs', [])
            print(f"✅ Success! Found {len(jobs)} jobs")
            
            if jobs:
                print("📋 Sample jobs:")
                for i, job in enumerate(jobs[:3], 1):
                    title = job.get('title', 'No title')
                    location = job.get('location', {})
                    if isinstance(location, dict):
                        location_name = location.get('name', 'No location')
                    else:
                        location_name = str(location)
                    print(f"   {i}. {title} - {location_name}")
                
                # Show raw structure of first job
                print(f"\n📝 Raw job data structure:")
                first_job = jobs[0]
                print(f"Keys: {list(first_job.keys())}")
                
                return True, len(jobs)
            else:
                print("⚠️  API worked but returned 0 jobs")
                return True, 0
                
        elif response.status_code == 404:
            print("❌ 404 - Company doesn't use Greenhouse or wrong identifier")
            return False, 404
        else:
            print(f"❌ HTTP {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            return False, response.status_code
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False, str(e)

# Test the companies from your config
test_companies = [
    'stripe', 'benchling', 'insitro', 'figma', 'discord'
]

print("🧪 Direct Greenhouse API Testing")
print("=" * 50)

working_companies = []
for company in test_companies:
    success, result = test_company_api(company)
    if success and isinstance(result, int) and result > 0:
        working_companies.append((company, result))
    
    print("-" * 30)

print(f"\n📊 Summary:")
print(f"Working companies with jobs: {len(working_companies)}")
for company, job_count in working_companies:
    print(f"   • {company}: {job_count} jobs")

if not working_companies:
    print("❌ No companies returned jobs!")
    print("\n🔍 Possible issues:")
    print("1. These companies might not have current job openings")
    print("2. API might be rate limited")
    print("3. Companies might use different identifiers")
    print("4. Network connectivity issues")
    
    print("\n🧪 Let's test a known-good company:")
    test_company_api('stripe')  # Stripe almost always has jobs