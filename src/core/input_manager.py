"""
Input manager module for "When Society Falls".

This module provides the InputManager class for handling user input.
"""
import pygame
from pygame.locals import (
    KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION
)


class InputManager:
    """
    Input manager for handling user input.
    
    This class tracks keyboard and mouse input and provides methods
    for checking input states and registering callbacks.
    """
    
    def __init__(self):
        """Initialize the input manager."""
        # Keyboard state tracking
        self.keys_pressed = set()
        self.keys_down = set()
        self.keys_up = set()
        
        # Mouse state tracking
        self.mouse_position = (0, 0)
        self.mouse_buttons_pressed = set()
        self.mouse_buttons_down = set()
        self.mouse_buttons_up = set()
        self.mouse_wheel_y = 0
        
        # Callback registrations
        self.key_callbacks = {}
        self.mouse_button_callbacks = {}
        self.mouse_motion_callbacks = []
    
    def process_event(self, event):
        """
        Process an input event.
        
        Args:
            event: Pygame event to process.
        """
        # Keyboard events
        if event.type == KEYDOWN:
            self.keys_pressed.add(event.key)
            self.keys_down.add(event.key)
            
            # Call registered callbacks for this key
            if event.key in self.key_callbacks:
                for callback in self.key_callbacks[event.key]:
                    callback(event.key, True)
                    
        elif event.type == KEYUP:
            if event.key in self.keys_pressed:
                self.keys_pressed.remove(event.key)
            self.keys_up.add(event.key)
            
            # Call registered callbacks for this key
            if event.key in self.key_callbacks:
                for callback in self.key_callbacks[event.key]:
                    callback(event.key, False)
        
        # Mouse events
        elif event.type == MOUSEMOTION:
            self.mouse_position = event.pos
            
            # Call registered mouse motion callbacks
            for callback in self.mouse_motion_callbacks:
                callback(event.pos, event.rel)
                
        elif event.type == MOUSEBUTTONDOWN:
            self.mouse_buttons_pressed.add(event.button)
            self.mouse_buttons_down.add(event.button)
            
            # Call registered callbacks for this button
            if event.button in self.mouse_button_callbacks:
                for callback in self.mouse_button_callbacks[event.button]:
                    callback(event.button, True, event.pos)
                    
        elif event.type == MOUSEBUTTONUP:
            if event.button in self.mouse_buttons_pressed:
                self.mouse_buttons_pressed.remove(event.button)
            self.mouse_buttons_up.add(event.button)
            
            # Call registered callbacks for this button
            if event.button in self.mouse_button_callbacks:
                for callback in self.mouse_button_callbacks[event.button]:
                    callback(event.button, False, event.pos)
    
    def update(self):
        """Update input state at the end of the frame."""
        # Clear one-frame states
        self.keys_down.clear()
        self.keys_up.clear()
        self.mouse_buttons_down.clear()
        self.mouse_buttons_up.clear()
        self.mouse_wheel_y = 0
    
    def is_key_pressed(self, key):
        """
        Check if a key is currently pressed.
        
        Args:
            key: The key code to check.
            
        Returns:
            bool: True if the key is currently pressed, False otherwise.
        """
        return key in self.keys_pressed
    
    def is_key_down(self, key):
        """
        Check if a key was pressed this frame.
        
        Args:
            key: The key code to check.
            
        Returns:
            bool: True if the key was pressed this frame, False otherwise.
        """
        return key in self.keys_down
    
    def is_key_up(self, key):
        """
        Check if a key was released this frame.
        
        Args:
            key: The key code to check.
            
        Returns:
            bool: True if the key was released this frame, False otherwise.
        """
        return key in self.keys_up
    
    def is_mouse_button_pressed(self, button):
        """
        Check if a mouse button is currently pressed.
        
        Args:
            button: The button code to check.
            
        Returns:
            bool: True if the button is currently pressed, False otherwise.
        """
        return button in self.mouse_buttons_pressed
    
    def is_mouse_button_down(self, button):
        """
        Check if a mouse button was pressed this frame.
        
        Args:
            button: The button code to check.
            
        Returns:
            bool: True if the button was pressed this frame, False otherwise.
        """
        return button in self.mouse_buttons_down
    
    def is_mouse_button_up(self, button):
        """
        Check if a mouse button was released this frame.
        
        Args:
            button: The button code to check.
            
        Returns:
            bool: True if the button was released this frame, False otherwise.
        """
        return button in self.mouse_buttons_up
    
    def get_mouse_position(self):
        """
        Get the current mouse position.
        
        Returns:
            tuple: The (x, y) position of the mouse.
        """
        return self.mouse_position
    
    def register_key_callback(self, key, callback):
        """
        Register a callback for a key event.
        
        Args:
            key: The key code to register for.
            callback: The function to call when the key state changes.
                The callback should accept two arguments: the key code and
                a boolean indicating whether the key is pressed.
        """
        if key not in self.key_callbacks:
            self.key_callbacks[key] = []
        self.key_callbacks[key].append(callback)
    
    def register_mouse_button_callback(self, button, callback):
        """
        Register a callback for a mouse button event.
        
        Args:
            button: The button code to register for.
            callback: The function to call when the button state changes.
                The callback should accept three arguments: the button code,
                a boolean indicating whether the button is pressed, and the
                mouse position.
        """
        if button not in self.mouse_button_callbacks:
            self.mouse_button_callbacks[button] = []
        self.mouse_button_callbacks[button].append(callback)
    
    def register_mouse_motion_callback(self, callback):
        """
        Register a callback for mouse motion events.
        
        Args:
            callback: The function to call when the mouse moves.
                The callback should accept two arguments: the mouse position
                and the relative movement.
        """
        self.mouse_motion_callbacks.append(callback)