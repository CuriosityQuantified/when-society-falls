"""
Application class for "When Society Falls".

This module provides the main Application class that handles the game loop,
window management, and scene transitions.
"""
import sys
import logging
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
from OpenGL.GL import glViewport

from .config import Config
from .game_clock import GameClock
from .input_manager import InputManager
from ..ecs.world import World


class Application:
    """
    Main application class managing the game's execution.
    
    This class is responsible for initializing SDL/OpenGL contexts,
    managing the main game loop, and coordinating systems and scenes.
    """
    
    def __init__(self, config=None):
        """
        Initialize the application.
        
        Args:
            config (Config, optional): Configuration for the application.
                If None, default configuration is used.
        """
        self.config = config or Config()
        self.logger = self._setup_logger()
        self.logger.info("Initializing application")
        
        self._initialize_pygame()
        
        self.clock = GameClock(self.config.target_fps)
        self.input_manager = InputManager()
        self.world = World()
        
        self.current_scene = None
        self.quit_requested = False
        self.logger.info("Application initialized")
        
    def _setup_logger(self):
        """Set up and configure the logger."""
        logger = logging.getLogger("WhenSocietyFalls")
        logger.setLevel(logging.DEBUG if self.config.debug_mode else logging.INFO)
        
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
        
    def _initialize_pygame(self):
        """Initialize Pygame and create the game window."""
        self.logger.info("Initializing Pygame")
        pygame.init()
        
        flags = pygame.DOUBLEBUF | pygame.OPENGL
        if self.config.fullscreen:
            flags |= pygame.FULLSCREEN
            
        self.screen = pygame.display.set_mode(
            (self.config.window_width, self.config.window_height),
            flags
        )
        pygame.display.set_caption(self.config.window_title)
        
        # Set up the viewport
        glViewport(0, 0, self.config.window_width, self.config.window_height)
        
    def set_scene(self, scene):
        """
        Set the current scene.
        
        Args:
            scene: The scene to set as current.
        """
        if self.current_scene:
            self.current_scene.on_exit()
            
        self.current_scene = scene
        scene.on_enter(self)
        self.logger.info(f"Scene changed to {scene.__class__.__name__}")
    
    def process_events(self):
        """Process SDL events."""
        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit_requested = True
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                if self.config.escape_quits:
                    self.quit_requested = True
            
            self.input_manager.process_event(event)
            
            if self.current_scene:
                self.current_scene.process_event(event)
    
    def update(self, dt):
        """
        Update the game state.
        
        Args:
            dt (float): Time delta in seconds.
        """
        self.input_manager.update()
        
        if self.current_scene:
            self.current_scene.update(dt)
    
    def render(self):
        """Render the current frame."""
        if self.current_scene:
            self.current_scene.render()
            
        pygame.display.flip()
    
    def run(self):
        """Run the main game loop."""
        self.logger.info("Starting main loop")
        
        while not self.quit_requested:
            dt = self.clock.tick()
            
            self.process_events()
            self.update(dt)
            self.render()
            
        self.logger.info("Main loop ended")
        self.shutdown()
        
    def shutdown(self):
        """Clean up and shut down the application."""
        self.logger.info("Shutting down application")
        
        if self.current_scene:
            self.current_scene.on_exit()
            
        pygame.quit()
        self.logger.info("Application shut down complete")