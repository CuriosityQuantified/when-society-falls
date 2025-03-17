"""
Component module for Entity Component System.

This module provides the base Component class used in the ECS architecture.
"""


class Component:
    """
    Base class for all components in the ECS.
    
    Components are data containers that can be attached to entities.
    They should generally not contain behavior, only state.
    """
    
    def __init__(self):
        """Initialize the component."""
        self.entity = None
        
    def _set_entity(self, entity):
        """
        Set the owning entity for this component.
        
        This method is called by the entity when the component is added.
        
        Args:
            entity: The entity that owns this component.
        """
        self.entity = entity
        
    def get_entity(self):
        """
        Get the entity that owns this component.
        
        Returns:
            The entity that owns this component.
        """
        return self.entity
        
    def on_add(self):
        """
        Called when the component is added to an entity.
        
        Override this method to perform initialization that requires
        the owning entity to be set.
        """
        pass
        
    def on_remove(self):
        """
        Called when the component is removed from an entity.
        
        Override this method to perform cleanup before the component
        is removed from its entity.
        """
        pass
        
    @classmethod
    def get_component_type(cls):
        """
        Get the type identifier for this component class.
        
        This method returns the class itself as a type identifier,
        which allows components to be identified by their class.
        
        Returns:
            The component class.
        """
        return cls