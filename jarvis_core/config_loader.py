"""
JARVIS Configuration Loader
Loads and manages configuration from config.yaml
"""

import os
import yaml # pyright: ignore[reportMissingModuleSource]
import logging
from typing import Any, Dict, Optional
from dotenv import load_dotenv # pyright: ignore[reportMissingImports]

logger = logging.getLogger(__name__)


class Config:
    """JARVIS Configuration Manager"""
    
    _instance = None
    _config: Dict[str, Any] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._config:
            self.load_config()
    
    def load_config(self, config_path: str = "config.yaml") -> None:
        """
        Load configuration from YAML file
        
        Args:
            config_path: Path to config.yaml
        """
        # Load environment variables first
        load_dotenv()
        
        if not os.path.exists(config_path):
            logger.warning(f"Config file {config_path} not found. Using defaults.")
            self._set_defaults()
            return
        
        try:
            with open(config_path, 'r') as f:
                config_data = yaml.safe_load(f)
            
            # Process environment variable substitutions
            self._process_env_vars(config_data)
            self._config = config_data
            
            logger.info(f"Configuration loaded from {config_path}")
            
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            self._set_defaults()
    
    def _process_env_vars(self, config: Dict) -> None:
        """Recursively process environment variable substitutions"""
        for key, value in config.items():
            if isinstance(value, dict):
                self._process_env_vars(value)
            elif isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                env_key = value[2:-1]
                config[key] = os.getenv(env_key, value)
    
    def _set_defaults(self) -> None:
        """Set default configuration"""
        self._config = {
            'assistant': {
                'name': 'JARVIS',
                'wake_word': 'jarvis',
                'voice_rate': 175,
                'voice_volume': 1.0,
            },
            'speech': {
                'language': 'en-US',
                'ambient_noise_adjustment': True,
            },
            'tts': {
                'engine': 'pyttsx3',
                'use_edge': False,
                'use_gtts': False,
            },
            'ai': {
                'provider': None,
                'model': None,
                'api_key': None,
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by dot-notation key
        
        Args:
            key: Dot-notation key (e.g., 'assistant.name')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_required(self, key: str) -> Any:
        """
        Get required configuration value
        
        Args:
            key: Dot-notation key
            
        Returns:
            Configuration value
            
        Raises:
            ValueError: If key not found
        """
        value = self.get(key)
        if value is None:
            raise ValueError(f"Required configuration key '{key}' not found")
        return value
    
    def update(self, key: str, value: Any) -> None:
        """
        Update configuration value
        
        Args:
            key: Dot-notation key
            value: New value
        """
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save(self, config_path: str = "config.yaml") -> None:
        """Save current configuration to file"""
        try:
            with open(config_path, 'w') as f:
                yaml.dump(self._config, f, default_flow_style=False)
            logger.info(f"Configuration saved to {config_path}")
        except Exception as e:
            logger.error(f"Error saving config: {e}")
    
    def reload(self) -> None:
        """Reload configuration from file"""
        self.load_config()


# Singleton instance
config = Config()


def get_config() -> Config:
    """Get the global configuration instance"""
    return config
