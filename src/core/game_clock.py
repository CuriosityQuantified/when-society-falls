"""
Game clock module for "When Society Falls".

This module provides the GameClock class for managing time and frame rate.
"""
import time


class GameClock:
    """
    Game clock for managing time and frame rate.
    
    This class tracks the time between frames and provides methods for
    controlling the game's frame rate and tracking performance metrics.
    """
    
    def __init__(self, target_fps=60):
        """
        Initialize the game clock.
        
        Args:
            target_fps (int, optional): Target frames per second. Defaults to 60.
        """
        self.target_fps = target_fps
        self.target_frame_time = 1.0 / target_fps
        
        self.last_time = time.time()
        self.current_time = self.last_time
        self.delta_time = 0.0
        
        # Performance tracking
        self.frame_count = 0
        self.frame_time_accumulator = 0.0
        self.current_fps = 0.0
        self.fps_update_interval = 1.0  # Update FPS calculation every second
        self.time_since_fps_update = 0.0
    
    def tick(self):
        """
        Update the clock and return the time delta since the last frame.
        
        This method calculates the time elapsed since the last call and
        sleeps if necessary to maintain the target frame rate.
        
        Returns:
            float: Time delta in seconds since the last frame.
        """
        # Calculate time since last frame
        self.current_time = time.time()
        self.delta_time = self.current_time - self.last_time
        
        # Sleep to maintain target frame rate if we're running too fast
        if self.delta_time < self.target_frame_time:
            sleep_time = self.target_frame_time - self.delta_time
            time.sleep(sleep_time)
            
            # Recalculate delta time after sleeping
            self.current_time = time.time()
            self.delta_time = self.current_time - self.last_time
        
        # Update performance metrics
        self.frame_count += 1
        self.frame_time_accumulator += self.delta_time
        self.time_since_fps_update += self.delta_time
        
        # Update FPS calculation every second
        if self.time_since_fps_update >= self.fps_update_interval:
            self.current_fps = self.frame_count / self.time_since_fps_update
            self.frame_count = 0
            self.frame_time_accumulator = 0.0
            self.time_since_fps_update = 0.0
        
        # Update last time for next frame
        self.last_time = self.current_time
        
        return self.delta_time
    
    def get_fps(self):
        """
        Get the current frames per second.
        
        Returns:
            float: Current frames per second.
        """
        return self.current_fps
    
    def get_frame_time(self):
        """
        Get the average time per frame in milliseconds.
        
        Returns:
            float: Average frame time in milliseconds.
        """
        if self.frame_count > 0:
            return (self.frame_time_accumulator / self.frame_count) * 1000.0
        return 0.0