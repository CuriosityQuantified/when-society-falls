"""
Configuration module for "When Society Falls".

This module provides the Config class for managing application settings.
"""
import json
import os


class Config:
    """
    Configuration class for managing application settings.
    
    This class stores configuration settings for the game and provides
    methods for loading and saving settings to a file.
    """
    
    def __init__(self, config_file=None):
        """
        Initialize the configuration with default values.
        
        Args:
            config_file (str, optional): Path to a configuration file to load.
                If None, default configuration is used.
        """
        # Window settings
        self.window_title = "When Society Falls"
        self.window_width = 1280
        self.window_height = 720
        self.fullscreen = False
        
        # Graphics settings
        self.vsync = True
        self.target_fps = 60
        self.render_distance = 10
        
        # Audio settings
        self.master_volume = 1.0
        self.music_volume = 0.7
        self.sfx_volume = 0.8
        
        # Game settings
        self.debug_mode = True
        self.escape_quits = True
        
        # If a config file was provided, load it
        if config_file and os.path.exists(config_file):
            self.load(config_file)
    
    def load(self, config_file):
        """
        Load configuration from a file.
        
        Args:
            config_file (str): Path to the configuration file.
        
        Returns:
            bool: True if the configuration was loaded successfully, False otherwise.
        """
        try:
            with open(config_file, 'r') as f:
                config_data = json.load(f)
                
            # Update attributes from the loaded data
            for key, value in config_data.items():
                if hasattr(self, key):
                    setattr(self, key, value)
                    
            return True
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading configuration: {e}")
            return False
    
    def save(self, config_file):
        """
        Save configuration to a file.
        
        Args:
            config_file (str): Path to the configuration file.
        
        Returns:
            bool: True if the configuration was saved successfully, False otherwise.
        """
        try:
            # Create a dictionary from instance attributes
            config_data = {key: value for key, value in self.__dict__.items()}
            
            with open(config_file, 'w') as f:
                json.dump(config_data, f, indent=4)
                
            return True
        except IOError as e:
            print(f"Error saving configuration: {e}")
            return False