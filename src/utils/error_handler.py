"""
Error Handler Utility
Handles API errors and provides user-friendly error messages.
"""

from rich.console import Console

console = Console()


def handle_api_error(status_code: int) -> None:
    """
    Handle API errors with user-friendly messages.
    
    Args:
        status_code: HTTP status code from the API response
    """
    error_messages = {
        400: "❌ Bad Request - Your request is invalid",
        401: "❌ Unauthorized - Your API key is incorrect",
        402: "💳 Payment Required - You're out of credits",
        403: "❌ Forbidden - API key doesn't have permission",
        404: "❌ Not Found - The requested resource doesn't exist",
        405: "❌ Method Not Allowed - Invalid request method",
        406: "❌ Not Acceptable - Invalid format requested",
        410: "❌ Gone - The resource has been removed",
        429: "⏱️ Too Many Requests - Please slow down your requests",
        500: "🔧 Internal Server Error - Try again later",
        503: "🔧 Service Unavailable - Temporarily offline for maintenance"
    }
    
    message = error_messages.get(status_code, f"❌ Unexpected error (Status: {status_code})")
    console.print(message, style="red")
    
    # Additional context for common errors
    if status_code == 401:
        console.print("💡 Check your API key in the .env file", style="yellow")
    elif status_code == 402:
        console.print("💡 Visit https://undetectable.ai/ to purchase more credits", style="yellow")
    elif status_code == 429:
        console.print("💡 Wait a moment before trying again", style="yellow") 