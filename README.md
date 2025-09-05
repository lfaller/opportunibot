# OpportuniBot 🤖

**Your AI-powered job search assistant that never sleeps**

OpportuniBot is an automated job search tool that scrapes job boards and company ATS systems, analyzes job fit based on your profile, and generates personalized cover letters. Say goodbye to manual job hunting and hello to intelligent opportunity discovery.

## 🌟 Features

## 🚀 Quick Start

## 📋 Versioning

OpportuniBot follows [Semantic Versioning](https://semver.org/) (SemVer) with a phase-based development approach:

### Version Format: `MAJOR.MINOR.PATCH`

- **MAJOR** version: Incompatible API changes or complete rewrites
- **MINOR** version: New features and phase completions (backward compatible)
- **PATCH** version: Bug fixes and small improvements (backward compatible)

### Development Phases

- **v1.0.x**: Initial setup and project foundation
- **v1.1.x**: Phase 1 - CLI framework and configuration system ✅
- **v1.2.x**: Phase 2 - Job scraping implementation (In Progress)
- **v1.3.x**: Phase 3 - Job analysis and matching algorithms
- **v1.4.x**: Phase 4 - Cover letter generation
- **v1.5.x**: Phase 5 - PDF reporting system
- **v1.6.x**: Phase 6 - Docker deployment and production features
- **v2.0.x**: Major feature additions (web interface, ML improvements)

### Managing Versions

OpportuniBot uses Poetry for version management:

```bash
# Check current version
poetry version

# Bump version types
poetry version patch    # Bug fixes (1.1.0 -> 1.1.1)
poetry version minor    # New features (1.1.0 -> 1.2.0)
poetry version major    # Breaking changes (1.1.0 -> 2.0.0)

# Set specific version
poetry version 1.2.0
```

### Current Status

**Latest Release**: v1.1.0 - Phase 1 Complete  
**Next Target**: v1.2.0 - Job Scraping Implementation

See [CHANGELOG.md](CHANGELOG.md) for detailed release notes and [GitHub Releases](https://github.com/yourusername/opportunibot/releases) for version downloads.

### Prerequisites

- Python 3.10+

### Installation

#### Local Installation

```bash
# Clone the repository
git clone https://github.com/lfaller/opportunibot.git
cd opportunibot

poetry install
```

### Configuration

### Usage

```bash
poetry run python -m opportunibot --help
```

Will output:

```
Usage: python -m opportunibot [OPTIONS] COMMAND [ARGS]...

  OpportuniBot - Your AI-powered job search assistant 🤖

  OpportuniBot automates job searching by scraping job boards, analyzing job
  fit, and generating personalized cover letters.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  config  Configuration management
  search  Run a job search
```

#### Basic Job Search

#### Scheduled Searches

#### Configuration Management

## 🔧 Supported Job Sources

### Currently Supported
- **CLI Framework**: Complete command-line interface with configuration management

## 📊 How It Works

## 📋 Roadmap

### Version 1.0 (Current)
- [ ] Basic job scraping (Greenhouse, Lever, Indeed)
- [ ] Keyword-based matching
- [ ] PDF report generation
- [ ] Docker support
- [ ] Configuration management

### Version 1.1 (Next)
- [ ] LinkedIn Jobs integration
- [ ] Email notifications
- [ ] Improved matching algorithms
- [ ] Application tracking
- [ ] Web interface

### Version 2.0 (Future)
- [ ] Machine learning-based matching
- [ ] Automated application submission
- [ ] Interview scheduling integration
- [ ] Analytics dashboard
- [ ] Multi-user support

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python and love for job seekers everywhere
- Inspired by the need to automate the tedious parts of job searching
- Thanks to the open source community for the amazing libraries that make this possible

## 🆘 Support

- 📖 [Documentation](docs/)
- 🐛 [Issue Tracker](https://github.com/lfaller/opportunibot/issues)
- 💬 [Discussions](https://github.com/lfaller/opportunibot/discussions)

---

**Happy job hunting!** 🎯

*OpportuniBot - Because your next opportunity shouldn't be left to chance.*