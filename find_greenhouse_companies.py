# Let's create a script to find working Greenhouse companies

import requests
import time

def test_greenhouse_company(company_id):
    """Test if a company has a working Greenhouse endpoint"""
    url = f"https://boards-api.greenhouse.io/v1/boards/{company_id}/jobs"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            job_count = len(data.get('jobs', []))
            return True, job_count
        else:
            return False, response.status_code
    except Exception as e:
        return False, str(e)

# Test known good Greenhouse companies first
known_working = [
    'stripe', 'airbnb', 'dropbox', 'pinterest', 'coinbase', 
    'instacart', 'doordash', 'webflow', 'figma', 'discord',
    'gitlab', 'hashicorp', 'twitch', 'roblox', 'vercel',
    'retool', 'supabase', 'planetscale', 'robinhood', 'plaid'
]

# Test biotech/healthcare companies (these are less certain)
biotech_candidates = [
    'ginkgo-bioworks', 'ginkgo', 'benchling', 'recursion-pharmaceuticals',
    'recursion', 'moderna', 'illumina', 'twist-bioscience', 'twist',
    '10x-genomics', 'tenx-genomics', 'tempus-labs', 'tempus',
    'guardant-health', 'guardant', 'exact-sciences', 'exactsciences',
    'flatiron-health', 'flatiron', 'veracyte', 'pacbio',
    'pacific-biosciences', 'dnanexus', 'insitro'
]

print("🧪 Testing Greenhouse company endpoints...")
print("=" * 50)

working_companies = []
working_biotech = []

print("\n✅ Testing known tech companies:")
for company in known_working[:10]:  # Test first 10 to not spam
    working, result = test_greenhouse_company(company)
    if working:
        print(f"   ✅ {company}: {result} jobs")
        working_companies.append(company)
    else:
        print(f"   ❌ {company}: {result}")
    time.sleep(1)  # Rate limit

print("\n🧬 Testing biotech/healthcare companies:")
for company in biotech_candidates:
    working, result = test_greenhouse_company(company)
    if working:
        print(f"   ✅ {company}: {result} jobs")
        working_biotech.append(company)
        working_companies.append(company)
    else:
        print(f"   ❌ {company}: {result}")
    time.sleep(1)  # Rate limit

print("\n📊 Results Summary:")
print(f"Working tech companies: {working_companies[:10]}")  
print(f"Working biotech companies: {working_biotech}")
print(f"Total working companies: {len(working_companies)}")

# Generate updated config section
print("\n📝 Updated config for job_search_config.yaml:")
print("target_companies:")
print("  greenhouse_companies:")
for company in working_companies:
    print(f"    - \"{company}\"")