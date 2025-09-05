# Changelog

All notable changes to OpportuniBot will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-09-05

### Added - Phase 1 Complete: Foundation & CLI Framework
- **CLI Framework**: Complete command-line interface using Click
  - `opportunibot status` - Configuration validation and system check
  - `opportunibot search` - Job search command (ready for Phase 2 implementation)
  - `--verbose` flag for detailed output
  - `--help` documentation for all commands

- **Configuration System**: YAML-based configuration with full validation
  - User profile management (personal info, skills, experience)
  - Search criteria configuration (keywords, locations, salary ranges)
  - Target company specification (Greenhouse, Lever, custom companies)
  - Job source settings and filters
  - Comprehensive error handling and validation

- **Data Models**: Type-safe data structures for all core entities
  - `JobListing` - Represents individual job postings
  - `JobAnalysis` - Job fit analysis and scoring
  - `UserProfile` - User's professional background and preferences
  - `SearchCriteria` - Job search parameters and filters
  - `TargetCompanies` - Company targeting configuration
  - `JobSearchConfig` - Complete configuration management

- **Development Infrastructure**:
  - Poetry-based dependency management
  - Pre-commit hooks for code quality
  - Comprehensive test fixtures and pytest configuration
  - Type checking with MyPy
  - Code formatting with Black and isort
  - Linting with Flake8

- **Personalization**: Custom configuration for bioinformatics/data engineering roles
  - 35+ technical skills configured
  - 48+ target companies (biotech, pharma, AI/ML, data platforms)
  - Salary range optimization for senior technical roles
  - Location preferences including biotech hubs

### Technical Details
- **Package Structure**: Clean `src/` layout with proper module organization
- **Error Handling**: Comprehensive exception handling with user-friendly messages
- **Validation**: Full configuration validation with detailed error reporting
- **Logging**: Structured logging system for debugging and monitoring
- **Documentation**: Inline docstrings and type hints throughout

### Developer Experience
- **Poetry Integration**: Modern Python dependency management
- **CLI Interface**: Intuitive command structure with help documentation
- **Status Checking**: Real-time configuration validation and system status
- **Verbose Mode**: Detailed output for debugging and development

## [0.1.0] - 2025-09-05

### Added - Initial Project Setup
- **Repository Structure**: Basic GitHub repository with README
- **Poetry Configuration**: Initial `pyproject.toml` with core dependencies
- **Package Foundation**: Basic Python package structure
- **Development Tools**: Black, Flake8, MyPy, pytest configuration
- **Documentation**: Initial README with project vision and setup instructions

### Dependencies
- **Core**: Click, PyYAML, requests, beautifulsoup4
- **Development**: pytest, black, flake8, mypy, isort
- **Future**: reportlab (PDF generation), additional scraping libraries
