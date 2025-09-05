"""
Allow OpportuniBot to be executable as a module with python -m opportunibot.
"""

from .main import cli

if __name__ == "__main__":
    cli()
