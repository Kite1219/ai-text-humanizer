"""
Streaming Humanization Service
Handles real-time text humanization using WebSocket streaming.
"""

import json
import time
import uuid
from datetime import datetime
from typing import Optional, Dict, Any, Callable
from websocket._app import WebSocketApp
import threading
from rich.console import Console

from src.core.base_api import BaseAPI
from src.utils.error_handler import handle_api_error

console = Console()


class StreamingHumanizer(BaseAPI):
    """Service for streaming text humanization using WebSocket."""
    
    def __init__(self, api_key: str):
        """
        Initialize the streaming humanizer.
        
        Args:
            api_key: The UndetectableAI API key
        """
        super().__init__(api_key)
        self.base_url = "https://humanize.undetectable.ai"
        self.ws_url = "wss://humanize.undetectable.ai/ws"
        self.ws = None
        self.document_id = None
        self.is_connected = False
        self.is_processing = False
        self.chunks = []
        self.on_chunk_received = None
        self.on_complete = None
        self.on_error = None
    
    def validate_response(self, response) -> bool:
        """Validate API response."""
        return response.status_code == 200
    
    def humanize_text_streaming(self, text: str, readability: str = "University",
                               purpose: str = "General Writing", strength: str = "More Human",
                               model: str = "v11", on_chunk: Optional[Callable] = None,
                               on_complete: Optional[Callable] = None,
                               on_error: Optional[Callable] = None) -> Optional[Dict[str, Any]]:
        """
        Humanize text using streaming WebSocket connection.
        
        Args:
            text: The text to humanize
            readability: The readability level
            purpose: The purpose of the text
            strength: The humanization strength
            model: The AI model to use
            on_chunk: Callback function for each chunk received
            on_complete: Callback function when complete
            on_error: Callback function for errors
            
        Returns:
            Dictionary containing the complete result or None if failed
        """
        self.on_chunk_received = on_chunk
        self.on_complete = on_complete
        self.on_error = on_error
        self.chunks = []
        self.is_processing = True
        
        try:
            # Generate user ID for WebSocket connection
            user_id = f"{int(time.time() * 1000)}x{str(uuid.uuid4()).replace('-', '')}"
            
            # Connect to WebSocket
            ws_url = f"{self.ws_url}/{user_id}"
            self.ws = WebSocketApp(
                ws_url,
                on_open=self._on_ws_open,
                on_message=self._on_ws_message,
                on_error=self._on_ws_error,
                on_close=self._on_ws_close
            )
            
            # Start WebSocket connection in a separate thread
            ws_thread = threading.Thread(target=self.ws.run_forever)
            ws_thread.daemon = True
            ws_thread.start()
            
            # Wait for connection
            timeout = 10
            while not self.is_connected and timeout > 0:
                time.sleep(0.1)
                timeout -= 0.1
            
            if not self.is_connected:
                raise Exception("Failed to connect to WebSocket")
            
            # Send document watch request
            self._send_document_watch()
            
            # Wait for document ID
            timeout = 10
            while not self.document_id and timeout > 0:
                time.sleep(0.1)
                timeout -= 0.1
            
            if not self.document_id:
                raise Exception("Failed to get document ID")
            
            # Submit document for humanization
            self._submit_document(text, readability, purpose, strength, model)
            
            # Wait for completion
            while self.is_processing:
                time.sleep(0.1)
            
            # Close WebSocket
            if self.ws:
                self.ws.close()
            
            # Return complete result
            if self.chunks:
                complete_text = "".join(self.chunks)
                return {
                    "output": complete_text,
                    "input": text,
                    "readability": readability,
                    "purpose": purpose,
                    "strength": strength,
                    "model": model,
                    "timestamp": datetime.now().isoformat(),
                    "chunks": self.chunks
                }
            
            return None
            
        except Exception as e:
            console.print(f"❌ Streaming humanization failed: {str(e)}", style="red")
            if self.on_error:
                self.on_error(str(e))
            return None
    
    def _on_ws_open(self, ws):
        """Handle WebSocket connection open."""
        console.print("🔗 WebSocket connected", style="green")
        self.is_connected = True
    
    def _on_ws_message(self, ws, message):
        """Handle WebSocket messages."""
        try:
            data = json.loads(message)
            event_type = data.get("event_type")
            
            if event_type == "document_id":
                self.document_id = data.get("document_id")
                console.print(f"📄 Document ID received: {self.document_id}", style="blue")
                
            elif event_type == "document_chunk":
                chunk = data.get("chunk", "")
                self.chunks.append(chunk)
                console.print(f"📝 Chunk received: {chunk[:50]}...", style="cyan")
                
                if self.on_chunk_received:
                    self.on_chunk_received(chunk, data)
                    
            elif event_type == "document_done":
                console.print("✅ Document processing completed", style="green")
                self.is_processing = False
                
                if self.on_complete:
                    self.on_complete("".join(self.chunks))
                    
            elif event_type == "document_error":
                error_code = data.get("error_code", "UNKNOWN")
                error_message = data.get("message", "Unknown error")
                console.print(f"❌ Document error: {error_code} - {error_message}", style="red")
                self.is_processing = False
                
                if self.on_error:
                    self.on_error(f"{error_code}: {error_message}")
                    
        except json.JSONDecodeError:
            console.print(f"❌ Invalid JSON message: {message}", style="red")
        except Exception as e:
            console.print(f"❌ Error processing message: {str(e)}", style="red")
    
    def _on_ws_error(self, ws, error):
        """Handle WebSocket errors."""
        console.print(f"❌ WebSocket error: {str(error)}", style="red")
        self.is_connected = False
        self.is_processing = False
        
        if self.on_error:
            self.on_error(str(error))
    
    def _on_ws_close(self, ws, close_status_code, close_msg):
        """Handle WebSocket connection close."""
        console.print("🔌 WebSocket connection closed", style="yellow")
        self.is_connected = False
        self.is_processing = False
    
    def _send_document_watch(self):
        """Send document watch request."""
        if self.ws and self.is_connected:
            message = {
                "event_type": "document_watch",
                "api_key": self.api_key
            }
            self.ws.send(json.dumps(message))
            console.print("👀 Document watch request sent", style="blue")
    
    def _submit_document(self, text: str, readability: str, purpose: str, strength: str, model: str):
        """Submit document for humanization."""
        try:
            payload = {
                "content": text,
                "readability": readability,
                "purpose": purpose,
                "strength": strength,
                "model": model,
                "id": self.document_id
            }
            
            response = self._make_request("POST", f"{self.base_url}/submit", json=payload)
            response.raise_for_status()
            
            result = response.json()
            console.print("📤 Document submitted for streaming humanization", style="blue")
            
        except Exception as e:
            console.print(f"❌ Failed to submit document: {str(e)}", style="red")
            self.is_processing = False
    
    def cancel_processing(self):
        """Cancel ongoing processing."""
        if self.ws and self.is_connected and self.document_id:
            message = {
                "event_type": "document_halt",
                "document_id": self.document_id
            }
            self.ws.send(json.dumps(message))
            console.print("⏹️ Processing cancelled", style="yellow")
        
        self.is_processing = False
        if self.ws:
            self.ws.close() 