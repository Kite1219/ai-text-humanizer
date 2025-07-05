"""
Menu Manager
Handles all menu operations and user interface interactions.
"""

import time
from typing import Optional, Dict, Any

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn

from src.services.text_humanizer import TextHumanizer
from src.services.ai_detector import AIDetector
from src.utils.file_manager import create_output_directory

console = Console()


class MenuManager:
    """Handles all menu operations and user interface."""
    
    def __init__(self):
        """Initialize the menu manager."""
        create_output_directory()
    
    def display_main_menu(self) -> int:
        """
        Display main menu and get user choice.
        
        Returns:
            User's menu choice
        """
        console.print("\n")
        menu_content = """
[bold cyan]🤖 AI TEXT HUMANIZER[/bold cyan]

[green]1.[/green] 📝 Humanize Text
[green]2.[/green] 🔍 AI Detector
[green]3.[/green] 💳 Check Credits
[green]4.[/green] 🚪 Exit
        """
        
        console.print(Panel(menu_content, title="Main Menu", border_style="cyan"))
        
        while True:
            try:
                choice = IntPrompt.ask("Choose an option", choices=["1", "2", "3", "4"])
                return choice
            except KeyboardInterrupt:
                return 4
    
    def display_humanize_menu(self) -> int:
        """
        Display humanize menu and get user choice.
        
        Returns:
            User's menu choice
        """
        console.print("\n")
        menu_content = """
[bold cyan]📝 HUMANIZE TEXT[/bold cyan]

[green]1.[/green] ⚡ Use Default Settings
[green]2.[/green] ⚙️  Configure Custom Settings
[green]3.[/green] 🔙 Back to Main Menu
[green]4.[/green] 📚 View History
        """
        
        console.print(Panel(menu_content, title="Humanize Menu", border_style="green"))
        
        while True:
            try:
                choice = IntPrompt.ask("Choose an option", choices=["1", "2", "3", "4"])
                return choice
            except KeyboardInterrupt:
                return 3
    
    def get_user_input(self, min_length: int = 10, max_length: int = 5000, 
                      prompt_text: str = "Enter your text") -> Optional[str]:
        """
        Get user input with validation.
        
        Args:
            min_length: Minimum text length
            max_length: Maximum text length
            prompt_text: Text to display as prompt
            
        Returns:
            User input text or None if cancelled
        """
        console.print(f"Please enter text (minimum {min_length} characters, maximum {max_length} characters)")
        console.print('Type "quit" or "q" to return to main menu\n', style="dim")
        
        while True:
            try:
                user_input = Prompt.ask(prompt_text).strip()
                
                if user_input.lower() in ["quit", "q"]:
                    return None
                
                if len(user_input) < min_length:
                    console.print(f"❌ Text too short! Minimum {min_length} characters required.", style="red")
                    continue
                
                if len(user_input) > max_length:
                    console.print(f"❌ Text too long! Maximum {max_length} characters allowed.", style="red")
                    continue
                
                return user_input
                
            except KeyboardInterrupt:
                return None
    
    def show_progress(self, message: str = "Processing", duration: int = 2) -> None:
        """
        Show progress spinner.
        
        Args:
            message: Progress message
            duration: Duration in seconds
        """
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True,
        ) as progress:
            task = progress.add_task(f"[cyan]{message}...", total=None)
            time.sleep(duration)
    
    def show_credit_info(self) -> None:
        """Show credit information and instructions."""
        console.print("\n" + "=" * 50, style="cyan")
        console.print("💳 CREDIT INFORMATION", style="bold cyan", justify="center")
        console.print("=" * 50, style="cyan")
        console.print("📱 To check your credit balance, visit:", style="yellow")
        console.print("🌐 https://undetectable.ai/dashboard", style="blue")
        console.print("\n💡 You can also check your credits by:", style="green")
        console.print("   • Logging into your account at undetectable.ai", style="dim")
        console.print("   • Looking at your dashboard", style="dim")
        console.print("   • Checking your billing/usage section", style="dim")
        console.print("\n⚠️  If you get a 402 error, you're out of credits", style="red")
        console.print("=" * 50, style="cyan")
        
        input("\nPress Enter to continue...")
    
    def get_humanization_settings(self) -> Optional[Dict[str, str]]:
        """
        Get humanization settings through interactive prompts.
        
        Returns:
            Dictionary with settings or None if cancelled
        """
        console.print("⚙️ Interactive Settings Configuration", style="bold cyan")
        console.print("Configure your humanization preferences:\n")
        
        # Readability options
        readability_options = {
            'h': 'High School',
            'u': 'University', 
            'd': 'Doctorate',
            'j': 'Journalist',
            'm': 'Marketing'
        }
        
        console.print("📚 Readability Level Options:")
        for key, value in readability_options.items():
            console.print(f"  {key} - {value}")
        
        readability_choice = Prompt.ask(
            "Choose readability level",
            choices=list(readability_options.keys()),
            default="u"
        )
        readability = readability_options[readability_choice]
        
        # Purpose options
        purpose_options = {
            'g': 'General Writing',
            'e': 'Essay',
            'a': 'Article',
            'm': 'Marketing Material',
            's': 'Story',
            'c': 'Cover Letter',
            'r': 'Report',
            'b': 'Business Material',
            'l': 'Legal Material'
        }
        
        console.print("\n🎯 Purpose Options:")
        for key, value in purpose_options.items():
            console.print(f"  {key} - {value}")
        
        purpose_choice = Prompt.ask(
            "Choose purpose",
            choices=list(purpose_options.keys()),
            default="g"
        )
        purpose = purpose_options[purpose_choice]
        
        # Strength options
        strength_options = {
            'q': 'Quality',
            'b': 'Balanced',
            'h': 'More Human'
        }
        
        console.print("\n💪 Strength Options:")
        for key, value in strength_options.items():
            console.print(f"  {key} - {value}")
        
        strength_choice = Prompt.ask(
            "Choose strength",
            choices=list(strength_options.keys()),
            default="h"
        )
        strength = strength_options[strength_choice]
        
        # Display selected configuration
        console.print("✅ Configuration Summary:", style="bold green")
        console.print(f"📚 Readability: {readability}")
        console.print(f"🎯 Purpose: {purpose}")
        console.print(f"💪 Strength: {strength}")
        
        if not Confirm.ask("\nProceed with these settings?"):
            return None
        
        return {
            "readability": readability,
            "purpose": purpose,
            "strength": strength
        } 