"""
Utilities package for "When Society Falls".

This package contains various utility functions and classes used throughout the game.
"""

from .asset_generator import (
    create_bookshelf, create_desk, create_floor_tile, 
    create_wall_tile, create_book, save_asset
)

__all__ = [
    'create_bookshelf',
    'create_desk',
    'create_floor_tile',
    'create_wall_tile',
    'create_book',
    'save_asset',
]