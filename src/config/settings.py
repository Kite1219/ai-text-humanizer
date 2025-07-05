"""
Settings Configuration
Handles application settings and configuration management.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional

from dotenv import load_dotenv, set_key, dotenv_values
from rich.console import Console

console = Console()


class Settings:
    """Manages application settings and configuration."""
    
    DEFAULT_CONFIG_FILE = "default.env"
    ENV_FILE = ".env"
    
    def __init__(self):
        """Initialize settings manager."""
        self._load_environment()
        self._validate_api_key()
    
    def _load_environment(self) -> None:
        """Load environment variables."""
        load_dotenv()
    
    def _validate_api_key(self) -> None:
        """Validate that API key is set."""
        api_key = os.getenv("UNDETECTABLE_API_KEY")
        if not api_key:
            console.print("❌ UNDETECTABLE_API_KEY not found in environment variables", style="red")
            console.print("Please create a .env file with your API key:", style="yellow")
            console.print("UNDETECTABLE_API_KEY=your_api_key_here", style="cyan")
            console.print("\nGet your API key from: https://undetectable.ai/", style="blue")
            sys.exit(1)
    
    def get_api_key(self) -> str:
        """
        Get the API key from environment.
        
        Returns:
            The API key
        """
        return os.getenv("UNDETECTABLE_API_KEY", "")
    
    def create_default_settings(self) -> Dict[str, str]:
        """
        Create or load default settings.
        
        Returns:
            Dictionary containing default settings
        """
        config_file = Path(self.DEFAULT_CONFIG_FILE)
        
        if not config_file.exists():
            # Create default settings
            set_key(str(config_file), "READABILITY", "University")
            set_key(str(config_file), "PURPOSE", "General Writing")
            set_key(str(config_file), "STRENGTH", "More Human")
            console.print("✅ Default settings created", style="green")
        
        return {k: v or "" for k, v in dotenv_values(str(config_file)).items()}
    
    def get_default_settings(self) -> Dict[str, str]:
        """
        Get default settings without creating them.
        
        Returns:
            Dictionary containing default settings
        """
        return {
            "READABILITY": "University",
            "PURPOSE": "General Writing",
            "STRENGTH": "More Human"
        }
    
    def create_directories(self) -> None:
        """Create necessary directories."""
        Path("outputs").mkdir(exist_ok=True)
        Path("errors").mkdir(exist_ok=True)
    
    def validate_api_key_format(self, api_key: str) -> bool:
        """
        Validate API key format.
        
        Args:
            api_key: The API key to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not api_key:
            return False
        
        # Basic validation - check if it's not empty and has reasonable length
        if len(api_key.strip()) < 10:
            return False
        
        return True 