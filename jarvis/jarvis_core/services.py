"""
JARVIS Services Package
System control and web services
"""

import os
import logging
from datetime import datetime
from typing import Optional, Dict, Any
import psutil # pyright: ignore[reportMissingModuleSource]
import requests # pyright: ignore[reportMissingModuleSource]
import pywhatkit # pyright: ignore[reportMissingImports]
from bs4 import BeautifulSoup # pyright: ignore[reportMissingImports]

try:
    import screen_brightness_control as brightness # pyright: ignore[reportMissingImports]
except ImportError:
    brightness = None

logger = logging.getLogger(__name__)


class SystemController:
    """
    JARVIS System Controller
    Monitors and controls system functions
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.check_battery = self.config.get('check_battery', True)
        self.low_battery_threshold = self.config.get('low_battery_threshold', 20)
        
        logger.info("System Controller initialized")
    
    def get_system_stats(self) -> Dict[str, Any]:
        """
        Get current system statistics
        
        Returns:
            Dictionary with CPU, memory, battery info
        """
        stats = {}
        
        # CPU Usage
        stats['cpu_percent'] = psutil.cpu_percent(interval=1)
        stats['cpu_count'] = psutil.cpu_count()
        
        # Memory Usage
        memory = psutil.virtual_memory()
        stats['memory_percent'] = memory.percent
        stats['memory_used_gb'] = round(memory.used / (1024**3), 2)
        stats['memory_total_gb'] = round(memory.total / (1024**3), 2)
        
        # Disk Usage
        disk = psutil.disk_usage('/')
        stats['disk_percent'] = disk.percent
        stats['disk_used_gb'] = round(disk.used / (1024**3), 2)
        stats['disk_total_gb'] = round(disk.total / (1024**3), 2)
        
        # Battery Status
        if self.check_battery:
            battery = psutil.sensors_battery()
            if battery:
                stats['battery_percent'] = battery.percent
                stats['battery_plugged'] = battery.power_plugged
                stats['low_battery'] = battery.percent < self.low_battery_threshold
            else:
                stats['battery_percent'] = None
                stats['battery_plugged'] = None
                stats['low_battery'] = False
        
        # Boot Time
        stats['boot_time'] = datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')
        
        return stats
    
    def get_battery_status(self) -> str:
        """Get formatted battery status"""
        battery = psutil.sensors_battery()
        if not battery:
            return "Battery information not available"
        
        status = f"{battery.percent}%"
        if battery.power_plugged:
            status += " (Charging)"
        else:
            status += " (Discharging)"
        
        return status
    
    def format_stats_for_speech(self) -> str:
        """Format system stats for speech output"""
        stats = self.get_system_stats()
        
        speech = f"CPU usage is {stats['cpu_percent']} percent. "
        speech += f"Memory is at {stats['memory_percent']} percent. "
        speech += f"Disk usage is {stats['disk_percent']} percent. "
        
        if stats.get('battery_percent') is not None:
            speech += f"Battery is at {stats['battery_percent']} percent. "
            if stats.get('low_battery'):
                speech += "Warning: Battery is low! "
        
        return speech
    
    def get_running_processes(self, limit: int = 10) -> list:
        """Get list of running processes"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Sort by CPU usage
        processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
        return processes[:limit]


class WebManager:
    """
    JARVIS Web Services Manager
    Handles web searches, weather, news, and other web-based features
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        
        # Weather API config
        self.weather_api_key = self.config.get('weather', {}).get('api_key') or os.getenv('OPENWEATHER_API_KEY')
        self.default_location = self.config.get('weather', {}).get('default_location', 'New York')
        
        # News API config
        self.news_api_key = self.config.get('news', {}).get('api_key') or os.getenv('NEWS_API_KEY')
        self.news_country = self.config.get('news', {}).get('country', 'us')
        
        # Wolfram Alpha config
        self.wolfram_api_key = self.config.get('wolfram', {}).get('api_key') or os.getenv('WOLFRAM_API_KEY')
        
        logger.info("Web Manager initialized")
    
    def search_web(self, query: str) -> str:
        """
        Perform web search using pywhatkit
        
        Args:
            query: Search query
            
        Returns:
            Status message
        """
        try:
            pywhatkit.search(query)
            return f"Searching the web for '{query}'"
        except Exception as e:
            logger.error(f"Web search error: {e}")
            return f"Sorry, I couldn't perform the search. Error: {str(e)}"
    
    def search_youtube(self, query: str) -> str:
        """
        Search YouTube for a video
        
        Args:
            query: Video search query
            
        Returns:
            Status message
        """
        try:
            pywhatkit.playonyt(query)
            return f"Playing '{query}' on YouTube"
        except Exception as e:
            logger.error(f"YouTube search error: {e}")
            return f"Sorry, I couldn't find that video. Error: {str(e)}"
    
    def get_weather(self, location: Optional[str] = None) -> str:
        """
        Get weather information
        
        Args:
            location: City name (uses default if not specified)
            
        Returns:
            Weather information string
        """
        city = location or self.default_location
        
        if not self.weather_api_key:
            return f"Weather for {city}: API key not configured. Set OPENWEATHER_API_KEY for weather functionality."
        
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.weather_api_key}&units=metric"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if data.get('cod') != 200:
                return f"Weather information not available for {city}"
            
            weather = data['weather'][0]['description']
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            wind = data['wind']['speed']
            
            return f"Weather in {city}: {weather}. Temperature: {temp}°C. Humidity: {humidity}%. Wind speed: {wind} m/s."
            
        except Exception as e:
            logger.error(f"Weather API error: {e}")
            return f"Sorry, I couldn't fetch weather information. Error: {str(e)}"
    
    def get_news(self, category: str = "general", limit: int = 3) -> str:
        """
        Get latest news headlines
        
        Args:
            category: News category
            limit: Number of headlines to return
            
        Returns:
            News headlines string
        """
        if not self.news_api_key:
            return f"News: API key not configured. Set NEWS_API_KEY for news functionality."
        
        try:
            url = f"https://newsapi.org/v2/top-headlines?country={self.news_country}&category={category}&apiKey={self.news_api_key}"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if data.get('status') != 'ok':
                return "News information not available"
            
            headlines = [article['title'] for article in data['articles'][:limit]]
            
            if not headlines:
                return "No headlines available at the moment."
            
            news_text = "Here are the latest headlines: "
            for i, headline in enumerate(headlines, 1):
                news_text += f"{i}. {headline}. "
            
            return news_text
            
        except Exception as e:
            logger.error(f"News API error: {e}")
            return f"Sorry, I couldn't fetch news. Error: {str(e)}"
    
    def get_wolfram_answer(self, query: str) -> str:
        """
        Get answer from Wolfram Alpha
        
        Args:
            query: Question for Wolfram Alpha
            
        Returns:
            Answer string
        """
        if not self.wolfram_api_key:
            return f"Wolfram Alpha: API key not configured. Set WOLFRAM_API_KEY for computational knowledge."
        
        try:
            import wolframalpha # pyright: ignore[reportMissingImports]
            
            client = wolframalpha.Client(self.wolfram_api_key)
            result = client.query(query)
            
            answer = next(result.results).text
            return answer
            
        except Exception as e:
            logger.error(f"Wolfram Alpha error: {e}")
            return f"Sorry, I couldn't get an answer. Error: {str(e)}"
    
    def get_definition(self, word: str) -> str:
        """
        Get definition of a word
        
        Args:
            word: Word to define
            
        Returns:
            Definition string
        """
        try:
            url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                definition = data[0]['meanings'][0]['definitions'][0]['definition']
                return f"Definition of {word}: {definition}"
            else:
                return f"Definition not found for {word}"
                
        except Exception as e:
            logger.error(f"Dictionary API error: {e}")
            return f"Sorry, I couldn't find a definition. Error: {str(e)}"
