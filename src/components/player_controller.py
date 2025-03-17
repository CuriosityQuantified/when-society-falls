"""
Player controller component for the ECS framework.

This module provides a component for controlling player entities.
"""
import logging
from typing import Tuple, Optional, Callable, Dict, Any
import pygame
from dataclasses import dataclass, field

from src.ecs.component import Component


@dataclass
class PlayerController(Component):
    """
    Player controller component for player-controlled entities.
    
    This component handles player input for movement and interactions.
    
    Attributes:
        move_speed: Movement speed in pixels per second
        sprint_multiplier: Speed multiplier when sprinting
        interaction_range: Maximum distance for interactions in pixels
        move_keys: Keyboard keys for movement
        sprint_key: Key for sprinting
        interact_key: Key for interactions
    """
    move_speed: float = 150.0
    sprint_multiplier: float = 1.5
    interaction_range: float = 100.0
    move_keys: Dict[str, int] = field(default_factory=lambda: {
        'up': pygame.K_w,
        'down': pygame.K_s,
        'left': pygame.K_a,
        'right': pygame.K_d
    })
    sprint_key: int = pygame.K_LSHIFT
    interact_key: int = pygame.K_e
    
    # State variables
    is_moving: bool = False
    is_sprinting: bool = False
    move_direction: Tuple[float, float] = (0.0, 0.0)
    facing_direction: Tuple[float, float] = (0.0, 1.0)  # Default facing down
    
    # Interaction callback
    on_interact: Optional[Callable[[], None]] = None
    
    def __post_init__(self):
        """Initialize the component after initialization."""
        super().__init__()
        self.logger = logging.getLogger('PlayerController')
    
    def process_input(self, dt: float, keys_pressed: Dict[int, bool]) -> Tuple[float, float]:
        """
        Process input and return the movement vector.
        
        Args:
            dt: Delta time in seconds
            keys_pressed: Dictionary of pressed keys
            
        Returns:
            Tuple containing the x and y movement in pixels
        """
        # Reset movement direction
        self.move_direction = (0.0, 0.0)
        
        # Check movement keys
        if keys_pressed.get(self.move_keys['up'], False):
            self.move_direction = (self.move_direction[0], self.move_direction[1] - 1.0)
            self.facing_direction = (0.0, -1.0)
        if keys_pressed.get(self.move_keys['down'], False):
            self.move_direction = (self.move_direction[0], self.move_direction[1] + 1.0)
            self.facing_direction = (0.0, 1.0)
        if keys_pressed.get(self.move_keys['left'], False):
            self.move_direction = (self.move_direction[0] - 1.0, self.move_direction[1])
            self.facing_direction = (-1.0, 0.0)
        if keys_pressed.get(self.move_keys['right'], False):
            self.move_direction = (self.move_direction[0] + 1.0, self.move_direction[1])
            self.facing_direction = (1.0, 0.0)
        
        # Normalize diagonal movement
        if self.move_direction[0] != 0.0 and self.move_direction[1] != 0.0:
            length = (self.move_direction[0]**2 + self.move_direction[1]**2)**0.5
            self.move_direction = (self.move_direction[0] / length, self.move_direction[1] / length)
        
        # Check sprint key
        self.is_sprinting = keys_pressed.get(self.sprint_key, False)
        
        # Calculate movement speed
        speed = self.move_speed
        if self.is_sprinting:
            speed *= self.sprint_multiplier
        
        # Calculate movement vector
        move_x = self.move_direction[0] * speed * dt
        move_y = self.move_direction[1] * speed * dt
        
        # Update moving state
        self.is_moving = move_x != 0.0 or move_y != 0.0
        
        return (move_x, move_y)
    
    def process_interaction(self, keys_pressed: Dict[int, bool], key_just_pressed: Dict[int, bool]) -> bool:
        """
        Process interaction input.
        
        Args:
            keys_pressed: Dictionary of pressed keys
            key_just_pressed: Dictionary of keys that were just pressed this frame
            
        Returns:
            True if an interaction was triggered, False otherwise
        """
        if key_just_pressed.get(self.interact_key, False) and self.on_interact:
            self.on_interact()
            return True
        return False
    
    def set_interaction_callback(self, callback: Callable[[], None]) -> None:
        """
        Set the callback function for interactions.
        
        Args:
            callback: Function to call when the player interacts
        """
        self.on_interact = callback