"""
Text Humanization Service
Handles AI text humanization using UndetectableAI API.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List

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
    
    def check_credits(self) -> Optional[Dict[str, Any]]:
        """
        Check user credit balance.
        
        Returns:
            Dictionary containing credit information or None if failed
        """
        try:
            response = self._make_request("GET", f"{self.base_url}/check-user-credits")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            handle_api_error(e.response.status_code)
            return None
        except Exception as e:
            console.print(f"❌ Failed to check credits: {str(e)}", style="red")
            return None
    
    def list_documents(self, offset: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """
        List user documents.
        
        Args:
            offset: Optional offset for pagination
            
        Returns:
            Dictionary containing documents list or None if failed
        """
        try:
            payload = {}
            if offset is not None:
                payload["offset"] = offset
            
            response = self._make_request("POST", f"{self.base_url}/list", json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            handle_api_error(e.response.status_code)
            return None
        except Exception as e:
            console.print(f"❌ Failed to list documents: {str(e)}", style="red")
            return None
    
    def rehumanize_document(self, document_id: str, readability: str = "University", 
                           purpose: str = "General Writing", strength: str = "More Human",
                           model: str = "v11") -> Optional[Dict[str, Any]]:
        """
        Rehumanize an existing document with new settings.
        
        Args:
            document_id: The ID of the document to rehumanize
            readability: The new readability level
            purpose: The new purpose
            strength: The new humanization strength
            model: The AI model to use
            
        Returns:
            Dictionary containing the rehumanized text or None if failed
        """
        try:
            # First, get the original document to extract the input text
            original_doc = self._get_document(document_id)
            if not original_doc:
                console.print("❌ Failed to retrieve original document", style="red")
                return None
            
            input_text = original_doc.get("input", "")
            if not input_text:
                console.print("❌ No input text found in original document", style="red")
                return None
            
            console.print("🔄 Rehumanizing document with new settings...", style="blue")
            
            # Submit the original text for rehumanization with new settings
            task_id = self._submit_text(input_text, readability, purpose, strength, model)
            if not task_id:
                return None
            
            # Poll for results
            console.print("⏳ Processing rehumanization...", style="blue")
            result = self._poll_for_results(task_id)
            
            if result and result.get("output"):
                console.print("✅ Document rehumanized successfully!", style="green")
                # Add metadata about rehumanization
                result["rehumanized_from"] = document_id
                result["original_settings"] = {
                    "readability": original_doc.get("readability"),
                    "purpose": original_doc.get("purpose"),
                    "strength": original_doc.get("strength"),
                    "model": original_doc.get("model")
                }
                self._save_result_to_history(result)
                return result
            else:
                console.print("❌ Rehumanization failed", style="red")
                return None
                
        except requests.exceptions.HTTPError as e:
            handle_api_error(e.response.status_code)
            return None
        except Exception as e:
            console.print(f"❌ Failed to rehumanize document: {str(e)}", style="red")
            return None
    
    def _get_document(self, document_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific document by ID."""
        try:
            response = self._make_request("POST", f"{self.base_url}/document", json={"id": document_id})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            handle_api_error(e.response.status_code)
            return None
        except Exception as e:
            console.print(f"❌ Failed to get document: {str(e)}", style="red")
            return None
    
    def humanize_text(self, text: str, readability: str = "University", 
                     purpose: str = "General Writing", strength: str = "More Human",
                     model: str = "v11") -> Optional[Dict[str, Any]]:
        """
        Humanize AI-generated text.
        
        Args:
            text: The text to humanize
            readability: The readability level
            purpose: The purpose of the text
            strength: The humanization strength
            model: The AI model to use (v2 or v11)
            
        Returns:
            Dictionary containing the humanized text and metadata, or None if failed
        """
        if not self._validate_input_text(text):
            return None
        
        console.print("🚀 Submitting text for humanization...", style="blue")
        
        # Submit text for humanization
        task_id = self._submit_text(text, readability, purpose, strength, model)
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
    
    def _submit_text(self, text: str, readability: str, purpose: str, strength: str, model: str = "v11") -> Optional[str]:
        """Submit text for humanization and get task ID."""
        try:
            payload = {
                "content": text,
                "readability": readability,
                "purpose": purpose,
                "strength": strength,
                "model": model,
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
        console.print(f"🤖 Model: {result.get('model', 'N/A')}", style="blue")
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
            
            input("Press Enter to continue...")
            
        except Exception as e:
            console.print(f"❌ Error reading history: {str(e)}", style="red")
            input("Press Enter to continue...") 