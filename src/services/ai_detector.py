"""
AI Detection Service
Analyzes text to determine if it was written by AI using heuristic analysis.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional

from rich.console import Console

from src.core.base_api import BaseAPI
from src.utils.file_manager import save_text_to_file

console = Console()


class AIDetector(BaseAPI):
    """Service for detecting AI-generated text using heuristic analysis."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the AI detector.
        
        Args:
            api_key: Optional API key (not used for local detection)
        """
        super().__init__(api_key or "local")
    
    def validate_response(self, response) -> bool:
        """Validate response - not used for local detection."""
        return True
    
    def detect_ai(self, text: str) -> Dict[str, Any]:
        """
        Detect if text was written by AI using heuristic analysis.
        
        Args:
            text: The text to analyze
            
        Returns:
            Dictionary containing detection results
        """
        try:
            score = self._analyze_text_patterns(text)
            
            return {
                "score": score,
                "result": self._get_result_category(score),
                "details": self._get_analysis_details(text, score),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            console.print(f"❌ Error in AI detection: {str(e)}", style="red")
            return {
                "score": 0.0,
                "result": "ERROR",
                "details": f"Analysis failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def _analyze_text_patterns(self, text: str) -> float:
        """
        Analyze text patterns to determine AI probability.
        
        Args:
            text: The text to analyze
            
        Returns:
            Score between 0.0 and 1.0 indicating AI probability
        """
        score = 0.0
        text_lower = text.lower()
        words = text.split()
        
        if len(words) < 5:
            return 0.0  # Too short to analyze
        
        # Check for repetitive patterns
        if len(words) > 10:
            word_freq = {}
            for word in words:
                word_freq[word] = word_freq.get(word, 0) + 1
            
            max_freq = max(word_freq.values()) if word_freq else 0
            if max_freq > len(words) * 0.1:  # More than 10% repetition
                score += 0.2
        
        # Check for formal/robotic language patterns
        formal_indicators = [
            "furthermore", "moreover", "additionally", "in conclusion",
            "it is important to note", "it should be mentioned",
            "as previously stated", "in summary", "to summarize",
            "therefore", "thus", "hence", "consequently"
        ]
        
        for indicator in formal_indicators:
            if indicator in text_lower:
                score += 0.1
        
        # Check for perfect grammar and structure (AI tends to be too perfect)
        sentences = text.split('.')
        if len(sentences) > 3:
            sentence_lengths = [len(s.split()) for s in sentences if s.strip()]
            if sentence_lengths:
                avg_length = sum(sentence_lengths) / len(sentence_lengths)
                if 15 <= avg_length <= 25:  # Very consistent sentence length
                    score += 0.15
        
        # Check for lack of contractions (AI often doesn't use them)
        contractions = ["don't", "can't", "won't", "it's", "that's", "you're", "we're", "they're"]
        contraction_count = sum(1 for c in contractions if c in text_lower)
        if contraction_count == 0 and len(words) > 20:
            score += 0.1
        
        # Check for overly complex vocabulary
        complex_words = ["utilize", "implement", "facilitate", "methodology", "paradigm", 
                        "comprehensive", "systematic", "methodological", "theoretical"]
        complex_count = sum(1 for word in complex_words if word in text_lower)
        if complex_count > 2:
            score += 0.1
        
        # Check for repetitive sentence structures
        if len(sentences) > 5:
            starting_words = []
            for s in sentences:
                if s.strip():
                    words_in_sentence = s.strip().split()
                    if words_in_sentence:
                        starting_words.append(words_in_sentence[0].lower())
            
            if starting_words:
                unique_starts = len(set(starting_words))
                if unique_starts < len(starting_words) * 0.6:  # Too many sentences start the same way
                    score += 0.15
        
        # Check for lack of personal pronouns (AI often avoids them)
        personal_pronouns = ["i", "me", "my", "mine", "myself", "we", "us", "our", "ours"]
        pronoun_count = sum(1 for pronoun in personal_pronouns if pronoun in text_lower)
        if pronoun_count == 0 and len(words) > 30:
            score += 0.1
        
        return min(score, 1.0)  # Cap at 1.0
    
    def _get_result_category(self, score: float) -> str:
        """
        Get result category based on score.
        
        Args:
            score: The AI detection score
            
        Returns:
            Result category string
        """
        if score > 0.7:
            return "AI-GENERATED"
        elif score < 0.3:
            return "HUMAN-WRITTEN"
        else:
            return "UNCERTAIN"
    
    def _get_analysis_details(self, text: str, score: float) -> str:
        """
        Get detailed analysis information.
        
        Args:
            text: The analyzed text
            score: The detection score
            
        Returns:
            Detailed analysis string
        """
        details = []
        
        if score > 0.7:
            details.append("High probability of AI generation")
        elif score < 0.3:
            details.append("Likely human-written")
        else:
            details.append("Uncertain - mixed indicators")
        
        # Add specific observations
        words = text.split()
        if len(words) > 0:
            details.append(f"Text length: {len(words)} words")
        
        return "; ".join(details)
    
    def display_detection_result(self, result: Dict[str, Any]) -> None:
        """Display AI detection results."""
        console.print("\n" + "=" * 60, style="cyan")
        console.print("🤖 AI DETECTION RESULTS", style="bold cyan", justify="center")
        console.print("=" * 60, style="cyan")
        
        # Get detection score
        score = result.get("score", 0)
        percentage = score * 100
        
        # Determine result and color
        if percentage < 30:
            color = "green"
        elif percentage < 70:
            color = "yellow"
        else:
            color = "red"
        
        console.print(f"📊 AI Detection Score: {percentage:.1f}%", style=color)
        console.print(f"🎯 Result: {result.get('result', 'Unknown')}", style=f"bold {color}")
        
        # Additional details if available
        if "details" in result:
            console.print(f"\n📝 Details: {result['details']}", style="blue")
        
        console.print("=" * 60, style="cyan")
    
    def save_detection_result(self, result: Dict[str, Any]) -> None:
        """Save detection result to file."""
        try:
            content = "AI DETECTION RESULTS\n"
            content += "=" * 50 + "\n"
            content += f"Score: {result.get('score', 0) * 100:.1f}%\n"
            content += f"Result: {result.get('result', 'Unknown')}\n"
            if "details" in result:
                content += f"Details: {result['details']}\n"
            content += f"Timestamp: {result.get('timestamp', datetime.now().isoformat())}\n"
            
            save_text_to_file(content, "ai_detection")
            
        except Exception as e:
            console.print(f"❌ Failed to save file: {str(e)}", style="red") 