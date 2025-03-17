"""
Player system for the ECS framework.

This module provides a system for processing player input and movement.
"""
import logging
from typing import Set, Type, List, Dict, Tuple, Optional
import pygame

from src.ecs.system import System
from src.ecs.component import Component
from src.ecs.entity import Entity
from src.components.transform import Transform
from src.components.player_controller import PlayerController
from src.components.physics import RigidBody, Collider


class PlayerSystem(System):
    """
    Player system for the ECS framework.
    
    Handles player input, movement, and interactions.
    """
    
    def __init__(self):
        """Initialize the player system."""
        required_components = {PlayerController, Transform}
        super().__init__(required_components)
        self.logger = logging.getLogger('PlayerSystem')
        
        # Input state
        self.keys_pressed = {}
        self.keys_just_pressed = {}
        self.previous_keys = {}
        
        # Player entities (should typically be just one)
        self.player_entities = []
    
    def initialize(self, world):
        """
        Initialize the system with the world.
        
        Args:
            world: The ECS world
        """
        super().initialize(world)
        self.logger.info("Player system initialized")
    
    def process(self, dt: float, entities: List[Entity]) -> None:
        """
        Process the system for all matching entities.
        
        Args:
            dt: Delta time in seconds
            entities: List of entities with required components
        """
        # Update the player entities list
        self.player_entities = entities
        
        # Update input state
        self._update_input_state()
        
        # Process player input and movement
        for entity in entities:
            self._process_entity(dt, entity)
    
    def _update_input_state(self) -> None:
        """Update the input state for this frame."""
        # Store previous keys
        self.previous_keys = self.keys_pressed.copy()
        
        # Get current keys
        key_state = pygame.key.get_pressed()
        self.keys_pressed = {key: key_state[key] for key in range(len(key_state)) if key_state[key]}
        
        # Determine keys that were just pressed this frame
        self.keys_just_pressed = {
            key: True for key in self.keys_pressed if key not in self.previous_keys
        }
    
    def _process_entity(self, dt: float, entity: Entity) -> None:
        """
        Process input and movement for a player entity.
        
        Args:
            dt: Delta time in seconds
            entity: Player entity to process
        """
        # Get components
        player_controller = entity.get_component(PlayerController)
        transform = entity.get_component(Transform)
        
        # Optional physics components
        rigid_body = entity.get_component(RigidBody)
        collider = entity.get_component(Collider)
        
        # Process input for movement
        movement = player_controller.process_input(dt, self.keys_pressed)
        
        # Apply movement to transform
        if rigid_body and rigid_body.is_kinematic:
            # For kinematic rigidbodies, we set the velocity
            rigid_body.velocity = (movement[0] / dt, movement[1] / dt)
        else:
            # Direct transform modification for non-physics entities
            transform.position = (
                transform.position[0] + movement[0],
                transform.position[1] + movement[1]
            )
        
        # Process interactions
        player_controller.process_interaction(self.keys_pressed, self.keys_just_pressed)
        
        # Log movement for debugging
        if movement[0] != 0 or movement[1] != 0:
            self.logger.debug(f"Player moved: {movement}, pos: {transform.position}")
    
    def get_player_entity(self) -> Optional[Entity]:
        """
        Get the first player entity.
        
        Returns:
            The player entity, or None if no player entities exist
        """
        if self.player_entities:
            return self.player_entities[0]
        return None