#!/usr/bin/env python3
"""
Asset generation script.

This script generates placeholder assets for the "When Society Falls" game.
"""
import os
import sys
import pygame

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.asset_generator import (
    create_floor_tile, create_wall_tile, create_bookshelf,
    create_desk, create_book, save_asset, save_library_assets
)


def main():
    """Generate and save all placeholder assets."""
    # Initialize pygame (required for surface operations)
    pygame.init()
    
    print("Generating library assets...")
    save_library_assets()
    
    # Generate player character
    from src.components.sprite import Sprite
    player_sprite = Sprite.create_player_sprite(64)
    save_asset(player_sprite, "player.png")
    
    print("Assets generated successfully!")
    return 0


if __name__ == "__main__":
    sys.exit(main())