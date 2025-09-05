"""
OpportuniBot Main CLI Interface

Command-line interface for the OpportuniBot job search tool.
"""

import click
import os
from pathlib import Path
from .config import ConfigManager, ConfigurationError


@click.group()
@click.version_option(version="0.2.0")
def cli():
    """OpportuniBot - Your AI-powered job search assistant 🤖
    
    OpportuniBot automates job searching by scraping job boards,
    analyzing job fit, and generating personalized cover letters.
    """
    pass


@click.command()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.option(
    '--config', '-c',
    default='job_search_config.yaml',
    help='Configuration file path (default: job_search_config.yaml)'
)
def search(verbose, config):
    """Run a job search
    
    Searches for jobs based on your configuration and generates a report
    with personalized cover letters.
    """
    config_path = Path(config)
    
    # Check if config file exists
    if not config_path.exists():
        click.echo(f"❌ Configuration file not found: {config_path}")
        click.echo("   Create a job_search_config.yaml file first!")
        raise click.Abort()
    
    try:
        # Load configuration
        config_manager = ConfigManager(str(config_path))
        job_config = config_manager.load_config()
        
        if verbose:
            click.echo("🔍 Verbose mode enabled")
            click.echo(f"📁 Using config: {config_path}")
            click.echo(f"👤 User: {job_config.user_profile.name}")
            click.echo(f"🎯 Keywords: {', '.join(job_config.search_criteria.required_keywords[:3])}...")
            click.echo(f"🏢 Target companies: {len(job_config.target_companies.get_all_companies())}")
            click.echo()
        
        click.echo("🤖 Starting job search...")
        
        # Phase 2 implementation will go here
        click.echo("   ✅ Configuration loaded successfully")
        click.echo("   🔄 Job scraping functionality coming in Phase 2!")
        click.echo("   📊 Analysis and reporting coming soon...")
        
        click.echo()
        click.echo("🎯 Ready for Phase 2 implementation!")
        
    except ConfigurationError as e:
        click.echo(f"❌ Configuration error: {e}")
        raise click.Abort()
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}")
        raise click.Abort()


@click.command()
@click.option(
    '--config', '-c',
    default='job_search_config.yaml',
    help='Configuration file to check (default: job_search_config.yaml)'
)
def status(config):
    """Check configuration and system status"""
    config_path = Path(config)
    
    click.echo("🤖 OpportuniBot Status Check")
    click.echo("=" * 30)
    
    # Check config file
    if config_path.exists():
        click.echo(f"✅ Configuration file: {config_path}")
        
        try:
            config_manager = ConfigManager(str(config_path))
            job_config = config_manager.load_config()
            config_manager.validate_config(job_config)
            
            click.echo(f"✅ Configuration is valid")
            click.echo(f"   • User: {job_config.user_profile.name}")
            click.echo(f"   • Skills: {len(job_config.user_profile.technical_skills)} technical skills")
            click.echo(f"   • Companies: {len(job_config.target_companies.get_all_companies())} target companies")
            click.echo(f"   • Sources: {[s for s, cfg in job_config.job_sources.items() if cfg.get('enabled')]}")
            
        except Exception as e:
            click.echo(f"❌ Configuration error: {e}")
    else:
        click.echo(f"❌ Configuration file not found: {config_path}")
    
    # Check reports directory
    reports_dir = Path("./reports")
    if reports_dir.exists():
        click.echo(f"✅ Reports directory: {reports_dir}")
    else:
        click.echo(f"📁 Reports directory will be created: {reports_dir}")
    
    click.echo()
    click.echo("🚀 System ready for job searching!")


# Add commands to main CLI
cli.add_command(search)
cli.add_command(status)


def main():
    """Entry point for the CLI"""
    cli()


if __name__ == "__main__":
    main()