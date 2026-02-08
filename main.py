#!/usr/bin/env python3
"""
JARVIS AI Assistant - Main Entry Point
Advanced Voice-Powered AI Assistant with Speech Recognition and TTS

Author: JARVIS Development Team
Version: 1.0.0
"""

import os
import sys
import logging
import signal
import time
from datetime import datetime
from typing import Optional

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from jarvis_core.config_loader import get_config
from jarvis_core.speech_engine import SpeechEngine
from jarvis_core.conversation import ConversationAI
from jarvis_core.services import SystemController, WebManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('jarvis.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class JarvisAssistant:
    """
    Main JARVIS AI Assistant Class
    Coordinates all modules for complete functionality
    """
    
    def __init__(self):
        """Initialize JARVIS assistant"""
        logger.info("Initializing JARVIS AI Assistant...")
        
        # Load configuration
        self.config = get_config()
        
        # Initialize components
        self.speech_engine = SpeechEngine(self.config.get('speech', {}))
        self.conversation_ai = ConversationAI(self.config.get('ai', {}))
        self.system_controller = SystemController(self.config.get('system', {}))
        self.web_manager = WebManager(self.config.get('services', {}))
        
        # Get assistant settings
        self.name = self.config.get('assistant.name', 'JARVIS')
        self.wake_word = self.config.get('assistant.wake_word', 'jarvis')
        self.is_listening = False
        self.is_speaking = False
        
        # Signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._shutdown_handler)
        signal.signal(signal.SIGTERM, self._shutdown_handler)
        
        logger.info(f"{self.name} AI Assistant initialized successfully")
    
    def _shutdown_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logger.info(f"Received signal {signum}, shutting down...")
        self.speak(f"Goodbye, sir. Shutting down {self.name}.")
        sys.exit(0)
    
    def greet_user(self) -> None:
        """Greet the user on startup"""
        hour = datetime.now().hour
        
        if hour < 12:
            greeting = "Good morning, sir."
        elif hour < 18:
            greeting = "Good afternoon, sir."
        else:
            greeting = "Good evening, sir."
        
        startup_msg = (
            f"{greeting} I am {self.name}, your AI assistant. "
            "I am online and ready. How may I assist you today?"
        )
        
        self.speak(startup_msg)
    
    def speak(self, text: str) -> None:
        """
        Convert text to speech
        
        Args:
            text: Text to speak
        """
        use_edge = self.config.get('tts.use_edge', False)
        use_gtts = self.config.get('tts.use_gtts', False)
        
        self.is_speaking = True
        self.speech_engine.speak(text, use_edge=use_edge, use_gtts=use_gtts)
        self.is_speaking = False
    
    def listen(self) -> Optional[str]:
        """
        Listen for voice input
        
        Returns:
            Recognized text or None
        """
        return self.speech_engine.listen(timeout=3, phrase_time_limit=5)
    
    def listen_for_wake_word(self) -> bool:
        """
        Listen specifically for wake word
        
        Returns:
            True if wake word detected
        """
        return self.speech_engine.listen_for_wake_word(self.wake_word)
    
    def process_command(self, command: str) -> str:
        """
        Process user command and return response
        
        Args:
            command: User's voice command
            
        Returns:
            Response text
        """
        command_lower = command.lower().strip()
        
        # Remove wake word from command
        for word in [self.wake_word, 'hey', 'ok']:
            if command_lower.startswith(word):
                command_lower = command_lower[len(word):].strip()
        
        # System Commands
        if not command_lower:
            return "I'm listening, sir."
        
        # Time and Date
        if any(word in command_lower for word in ['time', 'what time']):
            return datetime.now().strftime("The current time is %I:%M %p.")
        
        if any(word in command_lower for word in ['date', 'what date']):
            return datetime.now().strftime("Today's date is %B %d, %Y.")
        
        # System Statistics
        if 'system' in command_lower and 'status' in command_lower:
            return self.system_controller.format_stats_for_speech()
        
        if any(word in command_lower for word in ['cpu', 'memory', 'battery']):
            stats = self.system_controller.get_system_stats()
            return f"CPU: {stats['cpu_percent']}%, Memory: {stats['memory_percent']}%, Battery: {stats.get('battery_percent', 'N/A')}%"
        
        # Weather
        if 'weather' in command_lower:
            location = command_lower.replace('weather', '').replace('in', '').strip()
            return self.web_manager.get_weather(location if location else None)
        
        # News
        if 'news' in command_lower:
            category = "technology" if "tech" in command_lower else "general"
            return self.web_manager.get_news(category=category)
        
        # Web Search
        if 'search' in command_lower:
            query = command_lower.replace('search', '').replace('for', '').strip()
            if query:
                return self.web_manager.search_web(query)
            return "What would you like me to search for?"
        
        # YouTube
        if 'play' in command_lower and ('youtube' in command_lower or 'video' in command_lower):
            query = command_lower.replace('play', '').replace('on youtube', '').replace('video', '').strip()
            if query:
                return self.web_manager.search_youtube(query)
            return "What video would you like me to play?"
        
        # Definition
        if 'define' in command_lower or 'meaning' in command_lower:
            word = command_lower.replace('define', '').replace('meaning', '').strip()
            if word:
                return self.web_manager.get_definition(word)
            return "What word would you like me to define?"
        
        # Wolfram Alpha / Question
        if any(word in command_lower for word in ['what is', 'who is', 'how many', 'calculate']):
            # Extract the question
            query = command_lower
            for word in ['what is', 'who is', 'how many', 'calculate']:
                query = query.replace(word, '').strip()
            if query and len(query) > 2:
                return self.web_manager.get_wolfram_answer(query)
        
        # Conversation / AI
        if self.conversation_ai.is_available():
            return self.conversation_ai.get_response(command)
        else:
            # Fallback responses without AI
            return self._basic_responses(command_lower)
    
    def _basic_responses(self, command: str) -> str:
        """Provide basic responses when AI is unavailable"""
        
        # Greetings
        greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']
        if any(greet in command for greet in greetings):
            responses = [
                "Hello, sir. How can I assist you?",
                "Good to hear from you. What would you like?",
                "I'm here, sir. Ready to help."
            ]
            return responses[hash(command) % len(responses)]
        
        # Help
        if 'help' in command or 'what can you do' in command:
            return ("I can help with many tasks including: "
                   "checking system status, searching the web, "
                   "playing YouTube videos, checking weather and news, "
                   "and answering questions. "
                   "Configure OPENAI_API_KEY for full AI conversation capabilities.")
        
        # Thanks
        if 'thank' in command:
            return "You're welcome, sir. Always a pleasure to assist."
        
        # Who are you
        if 'who are you' in command:
            return (f"I am {self.name}, an AI assistant designed to help you with various tasks. "
                    "I can answer questions, control your system, search the web, and more.")
        
        # Default fallback
        return ("I understand you're saying: '" + command + "'. "
                "For full AI capabilities, please configure OPENAI_API_KEY in your .env file.")
    
    def run(self) -> None:
        """Main JARVIS interaction loop"""
        self.greet_user()
        
        logger.info("Starting JARVIS main loop...")
        
        while True:
            try:
                # Listen for wake word
                if self.listen_for_wake_word():
                    # Wake word detected - listen for command
                    self.speak("Yes, sir?")
                    
                    command = self.listen()
                    
                    if command:
                        logger.info(f"Command received: {command}")
                        
                        # Process command
                        response = self.process_command(command)
                        
                        # Speak response
                        if response:
                            self.speak(response)
                    else:
                        # No command heard
                        self.speak("I'm sorry, I didn't catch that.")
                
                # Small delay to prevent excessive CPU usage
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                self.speak("I encountered an error. Please try again.")
                time.sleep(1)
    
    def interactive_mode(self) -> None:
        """Run in interactive text mode (for testing)"""
        print(f"\n=== {self.name} Interactive Mode ===")
        print("Type 'exit' to quit, 'voice' to switch to voice mode\n")
        
        while True:
            try:
                user_input = input(f"{self.name}: ").strip()
                
                if user_input.lower() == 'exit':
                    self.speak("Goodbye, sir.")
                    break
                
                elif user_input.lower() == 'voice':
                    print("Switching to voice mode...")
                    self.run()
                    break
                
                elif user_input:
                    response = self.process_command(user_input)
                    print(f"{self.name}: {response}")
                    
                    # Also speak the response
                    self.speak(response)
            
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            
            except Exception as e:
                logger.error(f"Error: {e}")
                print("An error occurred. Please try again.")


def main():
    """Main entry point"""
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║                                                      ║
    ║   ██╗███╗   ███╗ █████╗  ██████╗ ███████╗             ║
    ║   ██║████╗ ████║██╔══██╗██╔════╝ ██╔════╝             ║
    ║   ██║██╔████╔██║███████║██║  ███╗█████╗               ║
    ║   ██║██║╚██╔╝██║██╔══██║██║   ██║██╔══╝               ║
    ║   ██║██║ ╚═╝ ██║██║  ██║╚██████╔╝███████╗             ║
    ║   ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝             ║
    ║                                                      ║
    ║   Advanced AI Assistant with Voice Recognition      ║
    ║                                                      ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    # Create JARVIS instance
    jarvis = JarvisAssistant()
    
    # Check for command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == '--text':
        jarvis.interactive_mode()
    else:
        jarvis.run()


if __name__ == "__main__":
    main()
