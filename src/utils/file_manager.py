"""
File Manager Utility
Handles file operations like saving text and updating history.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from rich.console import Console

console = Console()


def save_text_to_file(text: str, prefix: str) -> None:
    """
    Save text to a file with timestamp.
    
    Args:
        text: The text content to save
        prefix: Prefix for the filename
    """
    try:
        output_dir = Path("outputs")
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}.txt"
        filepath = output_dir / filename
        
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(text)
        
        console.print(f"✅ Text saved to: {filepath}", style="green")
        
    except Exception as e:
        console.print(f"❌ Failed to save file: {str(e)}", style="red")


def update_history_file(history_file: str, data: Dict[str, Any]) -> None:
    """
    Update history file with new data.
    
    Args:
        history_file: Path to the history file
        data: Data to add to history
    """
    try:
        history_path = Path(history_file)
        
        # Load existing history
        if history_path.exists():
            with open(history_path, "r", encoding="utf-8") as file:
                history = json.load(file)
        else:
            history = []
        
        # Add timestamp if not present
        if "timestamp" not in data:
            data["timestamp"] = datetime.now().isoformat()
        
        # Add new entry
        history.append(data)
        
        # Keep only last 100 entries
        if len(history) > 100:
            history = history[-100:]
        
        # Save updated history
        with open(history_path, "w", encoding="utf-8") as file:
            json.dump(history, file, indent=2, ensure_ascii=False)
            
    except Exception as e:
        console.print(f"⚠️ Warning: Could not update history: {str(e)}", style="yellow")


def create_output_directory() -> None:
    """Create the outputs directory if it doesn't exist."""
    Path("outputs").mkdir(exist_ok=True) 