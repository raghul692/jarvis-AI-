"""
JARVIS Conversation AI
Handles AI-powered conversations using OpenAI GPT
"""

import os
import logging
from typing import Optional, List, Dict
from datetime import datetime

try:
    import openai # pyright: ignore[reportMissingImports]
except ImportError:
    openai = None

from .config_loader import get_config

logger = logging.getLogger(__name__)


class ConversationAI:
    """
    JARVIS AI Conversation Handler
    Integrates with OpenAI GPT for intelligent responses
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the conversation AI
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        
        # Get settings from config or use defaults
        self.api_key = self.config.get('api_key') or os.getenv('OPENAI_API_KEY')
        self.model = self.config.get('model', 'gpt-3.5-turbo')
        self.max_tokens = self.config.get('max_tokens', 500)
        self.temperature = self.config.get('temperature', 0.7)
        
        # Initialize OpenAI client
        if self.api_key and openai:
            openai.api_key = self.api_key
            self.client = openai.OpenAI()
        else:
            self.client = None
            logger.warning("OpenAI API key not set. AI features will be limited.")
        
        # Conversation history
        self.conversation_history: List[Dict[str, str]] = []
        
        # System prompt for JARVIS personality
        self.system_prompt = """You are JARVIS, an advanced AI assistant inspired by Marvel's J.A.R.V.I.S.
        You are helpful, witty, and professional. You provide concise but informative responses.
        You have access to various system functions and web services.
        Your responses should be natural and conversational, not overly formal.
        Always be ready to help with coding, research, daily tasks, and general questions."""
        
        logger.info("Conversation AI initialized")
    
    def add_to_history(self, role: str, content: str) -> None:
        """
        Add a message to conversation history
        
        Args:
            role: 'user', 'assistant', or 'system'
            content: Message content
        """
        self.conversation_history.append({
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only last 20 messages to manage context window
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
    
    def get_response(self, user_input: str) -> str:
        """
        Get AI response for user input
        
        Args:
            user_input: User's message
            
        Returns:
            AI's response
        """
        if not self.client:
            return self._fallback_response(user_input)
        
        try:
            # Add user input to history
            self.add_to_history('user', user_input)
            
            # Build messages list
            messages = [{'role': 'system', 'content': self.system_prompt}]
            messages.extend(self.conversation_history)
            
            # Make API call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )
            
            # Extract response
            assistant_message = response.choices[0].message.content
            
            # Add to history
            self.add_to_history('assistant', assistant_message)
            
            logger.info(f"AI Response generated: {len(assistant_message)} chars")
            return assistant_message
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return self._fallback_response(user_input)
    
    def _fallback_response(self, user_input: str) -> str:
        """
        Provide fallback responses when AI is unavailable
        
        Args:
            user_input: User's message
            
        Returns:
            Fallback response
        """
        user_input_lower = user_input.lower()
        
        # Basic keyword-based responses
        if 'time' in user_input_lower:
            from datetime import datetime
            return f"The current time is {datetime.now().strftime('%I:%M %p')}."
        
        elif 'date' in user_input_lower:
            from datetime import datetime
            return f"Today's date is {datetime.now().strftime('%B %d, %Y')}."
        
        elif 'weather' in user_input_lower:
            return "I can check the weather if you specify a location. Try saying 'weather in [city]'."
        
        elif 'search' in user_input_lower or 'what is' in user_input_lower:
            return "I'd be happy to help with that. Enable web search feature for detailed information."
        
        elif 'how are you' in user_input_lower:
            return "I'm functioning perfectly, thank you for asking! How can I assist you today?"
        
        elif 'your name' in user_input_lower:
            return "I am JARVIS, your AI assistant. How may I help you?"
        
        else:
            return "I understand you're saying: " + user_input + ". My AI capabilities are currently limited without an API key. Configure OPENAI_API_KEY in your .env file for full functionality."
    
    def clear_history(self) -> None:
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("Conversation history cleared")
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get conversation history"""
        return self.conversation_history
    
    def is_available(self) -> bool:
        """Check if AI is available"""
        return self.client is not None


# Quick test function
if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    
    print("\n=== JARVIS Conversation AI Test ===\n")
    
    ai = ConversationAI()
    
    # Test basic interaction
    responses = [
        "Hello JARVIS, how are you?",
        "What can you do?",
        "What time is it?",
    ]
    
    for user_input in responses:
        print(f"You: {user_input}")
        response = ai.get_response(user_input)
        print(f"JARVIS: {response}\n")
    
    if not ai.is_available():
        print("\nNote: AI is not available. Set OPENAI_API_KEY for full functionality.")
