"""
Base API class for all API services.
Provides common functionality for API interactions.
"""

import requests
from abc import ABC, abstractmethod


class BaseAPI(ABC):
    """Base class for all API services."""
    
    def __init__(self, api_key: str, content_type: str = "application/json"):
        """
        Initialize the base API class.
        
        Args:
            api_key: The API key for authentication
            content_type: The content type for requests
        """
        self.api_key = api_key
        self.content_type = content_type
    
    def _get_headers(self) -> dict:
        """
        Get the headers for API requests.
        
        Returns:
            Dictionary containing request headers
        """
        return {
            "Content-Type": self.content_type,
            "apiKey": self.api_key,
        }
    
    def _make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        Make an HTTP request with error handling.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            url: The URL to make the request to
            **kwargs: Additional arguments for the request
            
        Returns:
            Response object from the request
        """
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self._get_headers(),
                timeout=30,
                **kwargs
            )
            return response
        except requests.exceptions.RequestException as e:
            raise e
    
    @abstractmethod
    def validate_response(self, response: requests.Response) -> bool:
        """
        Validate the API response.
        
        Args:
            response: The response to validate
            
        Returns:
            True if response is valid, False otherwise
        """
        pass 