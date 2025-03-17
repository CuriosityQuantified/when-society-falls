"""
Entity module for Entity Component System.

This module provides the Entity class used in the ECS architecture.
"""
import uuid


class Entity:
    """
    Entity class for the ECS architecture.
    
    Entities are containers for components. They have a unique ID
    and methods for adding, removing, and retrieving components.
    """
    
    def __init__(self, world, entity_id=None):
        """
        Initialize a new entity.
        
        Args:
            world: The World instance this entity belongs to.
            entity_id (optional): A unique ID for this entity.
                If None, a new UUID is generated.
        """
        self.id = entity_id or str(uuid.uuid4())
        self.world = world
        self.components = {}
        self.tags = set()
        self.active = True
        
    def add_component(self, component):
        """
        Add a component to this entity.
        
        Args:
            component: The component to add.
            
        Returns:
            self: For method chaining.
        """
        component_type = component.get_component_type()
        
        # Don't allow duplicate component types
        if component_type in self.components:
            raise ValueError(f"Entity already has a component of type {component_type.__name__}")
        
        # Set the component's entity reference
        component._set_entity(self)
        
        # Add the component
        self.components[component_type] = component
        
        # Notify the world of the new component
        self.world._entity_component_added(self, component)
        
        # Notify the component that it was added
        component.on_add()
        
        return self
        
    def remove_component(self, component_type):
        """
        Remove a component from this entity.
        
        Args:
            component_type: The type of component to remove.
            
        Returns:
            The removed component, or None if no component of that type exists.
        """
        if component_type in self.components:
            component = self.components[component_type]
            
            # Notify the component that it's being removed
            component.on_remove()
            
            # Remove the component
            del self.components[component_type]
            
            # Notify the world of the removed component
            self.world._entity_component_removed(self, component)
            
            return component
            
        return None
        
    def get_component(self, component_type):
        """
        Get a component of the specified type.
        
        Args:
            component_type: The type of component to get.
            
        Returns:
            The component, or None if no component of that type exists.
        """
        return self.components.get(component_type)
        
    def has_component(self, component_type):
        """
        Check if this entity has a component of the specified type.
        
        Args:
            component_type: The type of component to check for.
            
        Returns:
            bool: True if the entity has a component of the specified type,
                False otherwise.
        """
        return component_type in self.components
        
    def has_components(self, component_types):
        """
        Check if this entity has all of the specified component types.
        
        Args:
            component_types: A list of component types to check for.
            
        Returns:
            bool: True if the entity has all of the specified component types,
                False otherwise.
        """
        return all(ct in self.components for ct in component_types)
        
    def add_tag(self, tag):
        """
        Add a tag to this entity.
        
        Args:
            tag: The tag to add.
            
        Returns:
            self: For method chaining.
        """
        self.tags.add(tag)
        self.world._entity_tag_added(self, tag)
        return self
        
    def remove_tag(self, tag):
        """
        Remove a tag from this entity.
        
        Args:
            tag: The tag to remove.
            
        Returns:
            bool: True if the tag was removed, False if it wasn't present.
        """
        if tag in self.tags:
            self.tags.remove(tag)
            self.world._entity_tag_removed(self, tag)
            return True
        return False
        
    def has_tag(self, tag):
        """
        Check if this entity has the specified tag.
        
        Args:
            tag: The tag to check for.
            
        Returns:
            bool: True if the entity has the tag, False otherwise.
        """
        return tag in self.tags
        
    def destroy(self):
        """
        Destroy this entity, removing it from the world.
        
        This method removes all components and then asks the world
        to remove this entity.
        """
        # Remove all components
        for component_type in list(self.components.keys()):
            self.remove_component(component_type)
            
        # Tell the world to remove this entity
        self.world._remove_entity(self)
        
    def is_active(self):
        """
        Check if this entity is active.
        
        Returns:
            bool: True if the entity is active, False otherwise.
        """
        return self.active
        
    def set_active(self, active):
        """
        Set whether this entity is active.
        
        Inactive entities are not processed by systems.
        
        Args:
            active: Whether the entity should be active.
            
        Returns:
            self: For method chaining.
        """
        if self.active != active:
            self.active = active
            self.world._entity_active_changed(self, active)
        return self