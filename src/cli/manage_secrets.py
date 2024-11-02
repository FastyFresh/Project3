#!/usr/bin/env python3
import click
import json
from pathlib import Path

class SecretsManager:
    def __init__(self):
        self.secrets_file = Path('.env')

    def store_secret(self, key: str, value: str) -> None:
        """Store a secret in .env file"""
        secrets = self.get_secrets()
        secrets[key] = value
        
        # Write to .env file
        with open(self.secrets_file, 'w') as f:
            for k, v in secrets.items():
                f.write(f'{k}={v}\n')

    def get_secrets(self) -> dict:
        """Get all secrets from .env file"""
        secrets = {}
        if self.secrets_file.exists():
            with open(self.secrets_file) as f:
                for line in f:
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        secrets[key] = value
        return secrets

@click.group()
def cli():
    """CLI tool for managing API keys"""
    pass

@cli.command()
def init():
    """Initialize the secrets manager"""
    SecretsManager()
    click.echo("Secrets manager initialized!")

@cli.command()
def add():
    """Add a new API key"""
    secrets = SecretsManager()
    
    click.echo("\nEnter Alpaca API credentials:")
    key = click.prompt("API Key")
    secret = click.prompt("API Secret")
    
    secrets.store_secret("ALPACA_API_KEY", key)
    secrets.store_secret("ALPACA_API_SECRET", secret)
    secrets.store_secret("ALPACA_PAPER_TRADING", "true")
    
    click.echo("API keys stored successfully!")

if __name__ == "__main__":
    cli()