"""
Text Humanization Service
Handles AI text humanization using UndetectableAI API.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

import requests
from rich.console import Console

from src.core.base_api import BaseAPI
from src.utils.error_handler import handle_api_error
from src.utils.file_manager import save_text_to_file, update_history_file

console = Console()


class TextHumanizer(BaseAPI):
    """Service for humanizing AI-generated text."""
    
    # Constants
    MIN_TEXT_LENGTH = 50
    MAX_TEXT_LENGTH = 10000
    HISTORY_FILE = "history.json"
    DEFAULT_CONFIG_FILE = "default.env"
    
    def __init__(self, api_key: str):
        """
        Initialize the text humanizer.
        
        Args:
            api_key: The UndetectableAI API key
        """
        super().__init__(api_key)
        self.base_url = "https://humanize.undetectable.ai"
    
    def validate_response(self, response: requests.Response) -> bool:
        """Validate API response."""
        return response.status_code == 200
    
    def humanize_text(self, text: str, readability: str = "University", 
                     purpose: str = "General Writing", strength: str = "More Human") -> Optional[Dict[str, Any]]:
        """
        Humanize AI-generated text.
        
        Args:
            text: The text to humanize
            readability: The readability level
            purpose: The purpose of the text
            strength: The humanization strength
            
        Returns:
            Dictionary containing the humanized text and metadata, or None if failed
        """
        if not self._validate_input_text(text):
            return None
        
        console.print("🚀 Submitting text for humanization...", style="blue")
        
        # Submit text for humanization
        task_id = self._submit_text(text, readability, purpose, strength)
        if not task_id:
            return None
        
        # Poll for results
        console.print("⏳ Processing your text...", style="blue")
        result = self._poll_for_results(task_id)
        
        if result and result.get("status") == "done":
            console.print("✅ Text humanization completed!", style="green")
            self._save_result_to_history(result)
            return result
        else:
            console.print("❌ Text humanization failed", style="red")
            return None
    
    def _validate_input_text(self, text: str) -> bool:
        """Validate input text length."""
        if len(text) < self.MIN_TEXT_LENGTH:
            console.print(f"❌ Text too short! Minimum {self.MIN_TEXT_LENGTH} characters required.", style="red")
            return False
        if len(text) > self.MAX_TEXT_LENGTH:
            console.print(f"❌ Text too long! Maximum {self.MAX_TEXT_LENGTH} characters allowed.", style="red")
            return False
        return True
    
    def _submit_text(self, text: str, readability: str, purpose: str, strength: str) -> Optional[str]:
        """Submit text for humanization and get task ID."""
        try:
            payload = {
                "content": text,
                "readability": readability,
                "purpose": purpose,
                "strength": strength,
                "model": "v11",
            }
            
            response = self._make_request("POST", f"{self.base_url}/submit", json=payload)
            response.raise_for_status()
            
            return response.json().get("id")
            
        except requests.exceptions.HTTPError as e:
            handle_api_error(e.response.status_code)
            return None
        except Exception as e:
            console.print(f"❌ Request failed: {str(e)}", style="red")
            return None
    
    def _poll_for_results(self, task_id: str, max_attempts: int = 60) -> Optional[Dict[str, Any]]:
        """Poll for humanization results."""
        for attempt in range(max_attempts):
            try:
                response = self._make_request("POST", f"{self.base_url}/document", json={"id": task_id})
                response.raise_for_status()
                
                result = response.json()
                status = result.get("status", "")
                
                if status == "done":
                    return result
                elif status == "failed":
                    error_msg = result.get("error", "Unknown error")
                    console.print(f"Error: {error_msg}", style="red")
                    return None
                elif status == "processing":
                    console.print(f"⏳ Still processing... ({attempt + 1}/{max_attempts})", style="yellow")
                    time.sleep(5)
                else:
                    console.print(f"⚠️ Unknown status: {status}", style="yellow")
                    time.sleep(5)
                    
            except requests.exceptions.HTTPError as e:
                handle_api_error(e.response.status_code)
                return None
            except Exception as e:
                console.print(f"❌ Failed to retrieve result: {str(e)}", style="red")
                return None
        
        console.print("⏱️ Processing timed out. Please try again later.", style="red")
        return None
    
    def _save_result_to_history(self, result: Dict[str, Any]) -> None:
        """Save result to history file."""
        if "timestamp" not in result:
            result["timestamp"] = datetime.now().isoformat()
        
        update_history_file(self.HISTORY_FILE, result)
    
    def display_result(self, result: Dict[str, Any]) -> None:
        """Display humanization results."""
        output_text = result.get("output", "")
        
        console.print("\n" + "=" * 80, style="cyan")
        console.print("📝 HUMANIZED TEXT", style="bold cyan", justify="center")
        console.print("=" * 80, style="cyan")
        console.print(f"\n{output_text}\n", style="white")
        console.print("=" * 80, style="cyan")
        console.print(f"📊 Word count: {len(output_text.split())}", style="green")
        console.print(f"📊 Character count: {len(output_text)}", style="green")
        console.print(f"🎯 Readability: {result.get('readability', 'N/A')}", style="blue")
        console.print(f"🎯 Purpose: {result.get('purpose', 'N/A')}", style="blue")
        console.print("=" * 80, style="cyan")
    
    def save_to_file(self, text: str) -> None:
        """Save humanized text to file."""
        save_text_to_file(text, "humanized_text")
    
    @staticmethod
    def display_history() -> None:
        """Display humanization history."""
        history_file = Path(TextHumanizer.HISTORY_FILE)
        if not history_file.exists():
            console.print("📝 No history found", style="yellow")
            input("Press Enter to continue...")
            return
        
        try:
            with open(history_file, "r", encoding="utf-8") as file:
                history = json.load(file)
            
            if not history:
                console.print("📝 No history found", style="yellow")
                input("Press Enter to continue...")
                return
            
            console.print("📚 Humanization History", style="bold cyan")
            console.print("=" * 80)
            
            for entry in history[-10:]:
                date_str = entry.get("createdDate", "N/A")[:10]
                input_preview = entry.get("input", "")[:50] + "..." if len(entry.get("input", "")) > 50 else entry.get("input", "")
                output_preview = entry.get("output", "")[:50] + "..." if len(entry.get("output", "")) > 50 else entry.get("output", "")
                settings = f"{entry.get('readability', 'N/A')}\n{entry.get('purpose', 'N/A')}"
                console.print(f"{date_str} | {input_preview} | {output_preview} | {settings}")
            
            console.print(f"\nShowing last 10 entries (Total: {len(history)})")
            
        except Exception as e:
            console.print(f"❌ Error reading history: {str(e)}", style="red")
        
        input("\nPress Enter to continue...") 