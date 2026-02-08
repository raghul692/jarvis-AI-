"""
JARVIS Speech Engine
Handles both Speech-to-Text (STT) and Text-to-Speech (TTS)
"""

import speech_recognition as sr # pyright: ignore[reportMissingImports]
import pyttsx3 # pyright: ignore[reportMissingImports]
import threading
import tempfile
import os
import logging
from typing import Optional
from datetime import datetime

try:
    from gtts import gTTS # pyright: ignore[reportMissingImports]
except ImportError:
    gTTS = None

try:
    import edge_tts # pyright: ignore[reportMissingImports]
except ImportError:
    edge_tts = None

logger = logging.getLogger(__name__)


class SpeechEngine:
    """JARVIS Speech Engine for recognition and synthesis"""
    
    def __init__(self, config: dict):
        self.config = config
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # TTS Engine setup
        self.tts_engine = pyttsx3.init()
       
        
        # Voice settings
        self.voice_rate = self.config.get('voice_rate', 170)
        self.voice_volume = self.config.get('voice_volume', 1.0)
        self._setup_tts_engine()
        
        # Recognition settings
        self.language = config.get('language', 'en-US')
        self.ambient_adjustment = config.get('ambient_noise_adjustment', True)
        
        # For Edge TTS
        self.edge_voice = config.get('edge_voice', 'en-US-GuyNeural')
        
        logger.info("Speech Engine initialized successfully")
    
    def _setup_tts_engine(self):
        """Configure the pyttsx3 engine"""
        voices = self.tts_engine.getProperty('voices')
        voice_id = self.config.get('voice_id')
        
        if voice_id is None and voices:
            # Try to find a male voice for JARVIS
            for voice in voices:
                if 'male' in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    break
            else:
                self.tts_engine.setProperty('voice', voices[0].id)
        elif voice_id is not None:
            self.tts_engine.setProperty('voice', voice_id)
        
        self.tts_engine.setProperty('voice_rate:', self.voice_rate)
        self.tts_engine.setProperty('volume', self.voice_volume)
    
    def listen(self, timeout: int = 5, phrase_time_limit: int = 10) -> Optional[str]:
        """
        Listen for voice input and convert to text
        
        Args:
            timeout: Maximum seconds to wait for phrase start
            phrase_time_limit: Maximum seconds for the phrase
            
        Returns:
            Recognized text or None
        """
        try:
            with self.microphone as source:
                if self.ambient_adjustment:
                    logger.debug("Adjusting for ambient noise...")
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                logger.info("Listening for voice input...")
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_time_limit
                )
            
            # Recognize using Google Speech Recognition
            text = self._recognize_google(audio)
            
            if text:
                logger.info(f"Recognized: {text}")
                return text.lower()
            
            return None
            
        except sr.WaitTimeoutError:
            logger.debug("Listening timeout - no speech detected")
            return None
        except Exception as e:
            logger.error(f"Speech recognition error: {e}")
            return None
    
    def _recognize_google(self, audio: sr.AudioData) -> Optional[str]:
        """Recognize speech using Google Speech Recognition"""
        try:
            text = self.recognizer.recognize_google(audio, language=self.language)
            return text
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Speech recognition service error: {e}")
            return None
    
    def listen_for_wake_word(self, wake_word: str = "jarvis") -> bool:
        """
        Listen specifically for wake word
        
        Args:
            wake_word: Word to detect (default: "jarvis")
            
        Returns:
            True if wake word detected
        """
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=3)
            
            text = self._recognize_google(audio)
            
            if text and wake_word.lower() in text.lower():
                logger.info(f"Wake word '{wake_word}' detected")
                return True
            
            return False
            
        except Exception as e:
            logger.debug(f"Wake word detection error: {e}")
            return False
    
    def speak(self, text: str, use_edge: bool = True, use_gtts: bool = False) -> None:
        """
        Convert text to speech and play audio
        
        Args:
            text: Text to speak
            use_edge: Use Edge TTS (neural voices)
            use_gtts: Use Google TTS
        """
        if not text:
            return
        
        logger.info(f"JARVIS speaking: {text}")
        
        # Priority: Edge TTS > gTTS > pyttsx3
        if use_edge and edge_tts:
            self._speak_edge(text)
        elif use_gtts and gTTS:
            self._speak_gtts(text)
        else:
            self._speak_pyttsx3(text)
    
    def _speak_pyttsx3(self, text: str) -> None:
        """Use pyttsx3 for offline TTS"""
        def speak_thread():
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                logger.error(f"pyttsx3 TTS error: {e}")
        
        thread = threading.Thread(target=speak_thread)
        thread.start()
        thread.join()
    
    def _speak_gtts(self, text: str) -> None:
        """Use Google Text-to-Speech"""
        try:
            tts = gTTS(text=text, lang=self.language.split('-')[0])
            
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
                temp_file = f.name
            
            tts.save(temp_file)
            
            # Play audio
            import playsound # pyright: ignore[reportMissingImports]
            playsound.playsound(temp_file)
            
            # Clean up
            os.unlink(temp_file)
            
        except Exception as e:
            logger.error(f"gTTS error: {e}")
            # Fallback to pyttsx3
            self._speak_pyttsx3(text)
    
    def _speak_edge(self, text: str) -> None:
        """Use Edge Text-to-Speech (Neural voices)"""
        import asyncio
        
        async def edge_speak():
            try:
                communicate = edge_tts.Communicate(text, self.edge_voice)
                
                with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
                    temp_file = f.name
                
                await communicate.save(temp_file)
                
                # Play audio
                import playsound # pyright: ignore[reportMissingImports]
                playsound.playsound(temp_file)
                
                # Clean up
                os.unlink(temp_file)
                
            except Exception as e:
                logger.error(f"Edge TTS error: {e}")
                # Fallback to pyttsx3
                self._speak_pyttsx3(text)
        
        asyncio.run(edge_speak())
    
    def get_available_voices(self) -> list:
        """Get list of available pyttsx3 voices"""
        return [voice.name for voice in self.tts_engine.getProperty('voices')]
    
    def set_voice(self, voice_id: str) -> None:
        """Set a specific voice by ID"""
        self.tts_engine.setProperty('voice', voice_id)
    
    def set_rate(self, rate: int) -> None:
        """Set speech rate (words per minute)"""
        self.voice_rate = rate
        self.tts_engine.setProperty('rate', rate)
    
    def set_volume(self, volume: float) -> None:
        """Set volume (0.0 to 1.0)"""
        self.voice_volume = volume
        self.tts_engine.setProperty('volume', volume)


# Quick test function
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    config = {
        'voice_rate': 175,
        'voice_volume': 1.0,
        'language': 'en-US',
        'ambient_noise_adjustment': True,
    }
    
    engine = SpeechEngine(config)
    
    print("\n=== JARVIS Speech Engine Test ===\n")
    print("Available voices:", engine.get_available_voices())
    
    engine.speak("Hello, I am JARVIS. How can I assist you today?")
    
    print("\nListening for command (say 'hello jarvis')...")
    result = engine.listen(timeout=3, phrase_time_limit=3)
    
    if result:
        print(f"You said: {result}")
    else:
        print("No speech detected")
