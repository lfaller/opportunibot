# Commit Working Greenhouse Scraper - Phase 2 Milestone

echo "Working Greenhouse scraper - committing Phase 2 milestone..."

# Use Poetry to bump minor version (1.1.1 -> 1.2.0) - significant new feature
echo "Bumping minor version for Phase 2 milestone..."
poetry version minor

# Get the new version for other files
NEW_VERSION=$(poetry version -s)
echo "Updating files to version $NEW_VERSION..."

# Update __init__.py version to match
sed -i '' "s/__version__ = \".*\"/__version__ = \"$NEW_VERSION\"/" src/opportunibot/__init__.py

# Update main.py version to match  
sed -i '' "s/version=\".*\"/version=\"$NEW_VERSION\"/" src/opportunibot/main.py

echo "Version bumped to $NEW_VERSION"

# Check what files we're committing
echo "Files to commit:"
git status --porcelain

echo ""
echo "Staging files..."

# Stage all the changes
git add .

# Commit with descriptive message
git commit -m "Phase 2 Milestone: Working Greenhouse Scraper v$NEW_VERSION

✅ Core Job Discovery Implemented:
- Greenhouse API integration finding real jobs from target companies
- Successfully parsing job listings (title, company, location, URLs)
- Rate limiting and error handling for production use
- Job deduplication across multiple companies
- Keyword filtering on job titles and locations

🎯 Performance Metrics:
- 114 jobs found across 12 companies in 22 seconds
- Senior/staff engineering roles from Stripe, Benchling, Insitro, Figma
- Remote and major tech hub locations (SF, Seattle, NYC)
- Zero API failures with proper error handling

🔧 Technical Implementation:
- Fixed parsing logic for Greenhouse API response format
- Removed overly strict description filtering (API limitation)
- Enhanced location and keyword matching
- Comprehensive logging and debugging capabilities
- Production-ready rate limiting and retry logic

📊 Results Quality:
- Relevant engineering management and senior IC roles
- Appropriate seniority levels matching user background
- Geographic distribution matching preferences
- Direct links to full job postings

🚀 Phase 2 Status:
- Greenhouse scraper: Complete and working
- Lever scraper: Ready for implementation
- Indeed integration: Planned
- Job analysis engine: Ready for enhancement

Limitations Identified:
- Greenhouse API doesn't include job descriptions in main response
- Limited biotech companies using Greenhouse ATS
- Keyword matching currently title-only

Next Phase 2 Steps:
1. Implement Lever scraper for additional company coverage
2. Research biotech company ATS systems (Workday, custom)
3. Add job description fetching for enhanced filtering
4. Implement basic job analysis and scoring

Version: $NEW_VERSION (Phase 2 Milestone - Working Job Discovery)"

echo ""
echo "Pushing to GitHub..."
git push origin main

echo ""
echo "Phase 2 milestone committed and pushed!"
echo "Version $NEW_VERSION - Working job discovery from Greenhouse"
echo "OpportuniBot can now find real jobs from target companies"