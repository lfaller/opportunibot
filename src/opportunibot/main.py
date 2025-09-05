"""
OpportuniBot Main CLI Interface

Command-line interface for the OpportuniBot job search tool.
"""

import click
import os
import logging
from pathlib import Path
from .config import ConfigManager, ConfigurationError
from .scrapers import search_jobs, ScrapingError

# Setup logging for CLI
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@click.group()
@click.version_option(version="0.3.0")
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
@click.option(
    '--dry-run', 
    is_flag=True, 
    help='Test configuration without actually scraping jobs'
)
def search(verbose, config, dry_run):
    """Run a job search
    
    Searches for jobs based on your configuration and generates a report
    with personalized cover letters.
    """
    config_path = Path(config)
    
    # Setup logging level
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger('opportunibot').setLevel(logging.DEBUG)
    
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
            click.echo(f"🎯 Required keywords: {', '.join(job_config.search_criteria.required_keywords[:3])}...")
            click.echo(f"🏢 Target companies: {len(job_config.target_companies.get_all_companies())}")
            click.echo(f"🔌 Enabled sources: {[s for s, cfg in job_config.job_sources.items() if cfg.get('enabled')]}")
            click.echo()
        
        click.echo("🤖 Starting job search...")
        
        if dry_run:
            click.echo("   🧪 Dry run mode - testing configuration only")
            click.echo("   ✅ Configuration loaded successfully")
            click.echo("   📊 Would search the following sources:")
            for source, cfg in job_config.job_sources.items():
                if cfg.get('enabled'):
                    click.echo(f"      • {source}")
            click.echo("   🎯 Use --verbose for more configuration details")
            return
        
        # Actually run the job search
        try:
            jobs = search_jobs(job_config)
            
            if jobs:
                click.echo(f"   ✅ Found {len(jobs)} jobs!")
                click.echo()
                click.echo("📋 Top matches:")
                
                # Show top 5 jobs
                for i, job in enumerate(jobs[:5], 1):
                    click.echo(f"   {i}. {job.title}")
                    click.echo(f"      🏢 {job.company}")
                    click.echo(f"      📍 {job.location}")
                    click.echo(f"      🔗 {job.url}")
                    click.echo()
                
                if len(jobs) > 5:
                    click.echo(f"   ... and {len(jobs) - 5} more jobs")
                
                # Create reports directory
                reports_dir = Path(job_config.output_directory)
                reports_dir.mkdir(exist_ok=True)
                
                click.echo(f"📊 Full results will be saved to: {reports_dir}")
                
            else:
                click.echo("   🔍 No jobs found matching your criteria")
                click.echo("   💡 Try adjusting your keywords or expanding your location preferences")
            
        except ScrapingError as e:
            click.echo(f"❌ Scraping error: {e}")
            raise click.Abort()
        
        click.echo()
        click.echo("🎯 Job search complete!")
        
    except ConfigurationError as e:
        click.echo(f"❌ Configuration error: {e}")
        raise click.Abort()
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}")
        if verbose:
            import traceback
            click.echo(traceback.format_exc())
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
            
            enabled_sources = [s for s, cfg in job_config.job_sources.items() if cfg.get('enabled')]
            click.echo(f"   • Sources: {enabled_sources}")
            
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
