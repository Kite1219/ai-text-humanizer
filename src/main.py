"""
AI Text Humanizer - Main Application
Main entry point for the AI Text Humanization Tool.
"""

import os
import sys
from typing import Optional

from rich.console import Console
from rich.prompt import Confirm

from src.config.settings import Settings
from src.ui.menu_manager import MenuManager
from src.services.text_humanizer import TextHumanizer
from src.services.ai_detector import AIDetector
from src.utils.file_manager import create_output_directory

console = Console()


class AIHumanizerApp:
    """Main application class for AI Text Humanizer."""
    
    def __init__(self):
        """Initialize the application."""
        self.settings = Settings()
        self.menu_manager = MenuManager()
        self.settings.create_directories()
        
        # Initialize services
        self.text_humanizer = TextHumanizer(self.settings.get_api_key())
        self.ai_detector = AIDetector()
    
    def run(self) -> None:
        """Run the main application loop."""
        self._show_welcome()
        
        while True:
            try:
                choice = self.menu_manager.display_main_menu()
                
                if choice == 4:  # Exit
                    self._exit_app()
                    break
                elif choice == 1:  # Humanize Text
                    self._handle_humanize_text()
                elif choice == 2:  # AI Detector
                    self._handle_ai_detection()
                elif choice == 3:  # Check Credits
                    self._handle_credit_check()
                    
            except KeyboardInterrupt:
                console.print("\n\nOperation cancelled by user.", style="yellow")
                break
            except Exception as e:
                console.print(f"An unexpected error occurred: {str(e)}", style="red")
                console.print("Please try again or contact support if the issue persists.", style="dim")
                input("Press Enter to continue...")
    
    def _show_welcome(self) -> None:
        """Show welcome message."""
        console.print("🤖 AI Text Humanizer", style="bold cyan")
        console.print("Welcome to the AI Text Humanization Tool!", style="green")
    
    def _handle_humanize_text(self) -> None:
        """Handle text humanization workflow."""
        humanize_choice = self.menu_manager.display_humanize_menu()
        
        if humanize_choice == 1:  # Default settings
            self._humanize_with_default_settings()
        elif humanize_choice == 2:  # Custom settings
            self._humanize_with_custom_settings()
        elif humanize_choice == 4:  # View history
            TextHumanizer.display_history()
    
    def _humanize_with_default_settings(self) -> None:
        """Humanize text with default settings."""
        configs = self.settings.create_default_settings()
        
        user_input = self.menu_manager.get_user_input(
            min_length=TextHumanizer.MIN_TEXT_LENGTH,
            max_length=TextHumanizer.MAX_TEXT_LENGTH,
            prompt_text="Enter your text"
        )
        
        if user_input:
            result = self.text_humanizer.humanize_text(
                text=user_input,
                readability=configs["READABILITY"],
                purpose=configs["PURPOSE"],
                strength=configs["STRENGTH"]
            )
            
            if result:
                self.text_humanizer.display_result(result)
                if Confirm.ask("\n💾 Would you like to save this result to a file?"):
                    self.text_humanizer.save_to_file(result.get("output", ""))
            
            input("\nPress Enter to continue...")
    
    def _humanize_with_custom_settings(self) -> None:
        """Humanize text with custom settings."""
        settings = self.menu_manager.get_humanization_settings()
        
        if settings:
            user_input = self.menu_manager.get_user_input(
                min_length=TextHumanizer.MIN_TEXT_LENGTH,
                max_length=TextHumanizer.MAX_TEXT_LENGTH,
                prompt_text="Enter your text"
            )
            
            if user_input:
                result = self.text_humanizer.humanize_text(
                    text=user_input,
                    readability=settings["readability"],
                    purpose=settings["purpose"],
                    strength=settings["strength"]
                )
                
                if result:
                    self.text_humanizer.display_result(result)
                    if Confirm.ask("\n💾 Would you like to save this result to a file?"):
                        self.text_humanizer.save_to_file(result.get("output", ""))
                
                input("\nPress Enter to continue...")
    
    def _handle_ai_detection(self) -> None:
        """Handle AI detection workflow."""
        user_input = self.menu_manager.get_user_input(
            min_length=10,
            max_length=5000,
            prompt_text="Enter text to analyze"
        )
        
        if user_input:
            self.menu_manager.show_progress("Analyzing text for AI detection", 2)
            
            result = self.ai_detector.detect_ai(user_input)
            
            if result:
                console.print("✅ AI detection completed!", style="green")
                self.ai_detector.display_detection_result(result)
                
                if Confirm.ask("\n💾 Would you like to save this result to a file?"):
                    self.ai_detector.save_detection_result(result)
            
            input("\nPress Enter to continue...")
    
    def _handle_credit_check(self) -> None:
        """Handle credit check workflow."""
        self.menu_manager.show_credit_info()
    
    def _exit_app(self) -> None:
        """Exit the application gracefully."""
        console.print("Thanks for using our service! 🙏", style="bold green")


def main() -> None:
    """Main entry point for the application."""
    try:
        app = AIHumanizerApp()
        app.run()
    except Exception as e:
        console.print(f"Fatal error: {str(e)}", style="bold red")
        sys.exit(1)


if __name__ == "__main__":
    main() 