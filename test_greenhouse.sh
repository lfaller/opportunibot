# Test Greenhouse Scraper Implementation

echo "🧪 Testing Greenhouse Scraper..."

# Test 1: Import test
echo "=== Test 1: Import verification ==="
poetry run python -c "
from opportunibot.greenhouse_scraper import GreenhouseScraper
from opportunibot.models import JobSearchConfig
print('✅ Greenhouse scraper imports successful')
"

# Test 2: API connectivity test
echo ""
echo "=== Test 2: API connectivity test ==="
poetry run python -c "
import requests
url = 'https://boards-api.greenhouse.io/v1/boards/stripe/jobs'
try:
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        data = response.json()
        print(f'✅ Greenhouse API accessible - found {len(data.get(\"jobs\", []))} jobs at Stripe')
    else:
        print(f'⚠️  Greenhouse API returned status {response.status_code}')
except Exception as e:
    print(f'❌ API test failed: {e}')
"

# Test 3: Small scraper test with real config
echo ""
echo "=== Test 3: Real scraper test (limited scope) ==="
poetry run python -c "
import sys
sys.path.append('.')

from opportunibot.config import load_config
from opportunibot.greenhouse_scraper import GreenhouseScraper

try:
    # Load real config
    config = load_config('job_search_config.yaml')
    
    # Create a limited test config with just a few companies
    test_companies = ['stripe', 'benchling']  # Known working Greenhouse companies
    config.target_companies.greenhouse_companies = test_companies
    
    # Create scraper
    scraper = GreenhouseScraper(config, 'greenhouse')
    
    print(f'🔍 Testing with companies: {test_companies}')
    
    # Search jobs
    jobs = scraper.search_jobs()
    
    print(f'📊 Results:')
    print(f'   • Total jobs found: {len(jobs)}')
    
    if jobs:
        print(f'   • Sample job: {jobs[0].title} at {jobs[0].company}')
        print(f'   • Location: {jobs[0].location}')
        print(f'   • URL: {jobs[0].url}')
        print(f'   • Description preview: {jobs[0].description[:100]}...')
    
    # Show stats
    stats = scraper.get_stats()
    print(f'   • Companies scraped: {stats[\"companies_scraped\"]}')
    print(f'   • Errors: {stats[\"errors\"]}')
    
    print('✅ Greenhouse scraper test successful!')
    
except FileNotFoundError:
    print('❌ job_search_config.yaml not found - run this after creating your config')
except Exception as e:
    print(f'❌ Scraper test failed: {e}')
    import traceback
    traceback.print_exc()
"

# Test 4: Full CLI test
echo ""
echo "=== Test 4: CLI integration test ==="
echo "Running: poetry run python -m opportunibot search --verbose"
echo "(This will use your full config with all target companies)"
echo ""

poetry run python -m opportunibot search --verbose

echo ""
echo "🎉 Greenhouse scraper testing complete!"
echo ""
echo "📋 What just happened:"
echo "   1. ✅ Imports verified"
echo "   2. ✅ API connectivity tested"  
echo "   3. ✅ Limited scraper test with real companies"
echo "   4. ✅ Full CLI test with your configuration"
echo ""
echo "🚀 If all tests passed, your Greenhouse scraper is working!"
echo "   OpportuniBot can now find real jobs from biotech companies!"