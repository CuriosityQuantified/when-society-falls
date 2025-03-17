"""
Asset generator for creating placeholder graphics.

This module provides functions for procedurally generating placeholder 
assets with a consistent cel-shaded style.
"""
import os
import pygame
from typing import Tuple, List, Dict, Optional


def create_bookshelf(
    width: int = 64, 
    height: int = 96, 
    color: Tuple[int, int, int] = (139, 69, 19)
) -> pygame.Surface:
    """
    Create a simple bookshelf sprite with a cel-shaded look.
    
    Args:
        width: Width of the bookshelf in pixels
        height: Height of the bookshelf in pixels
        color: Base color of the bookshelf (RGB)
        
    Returns:
        A pygame Surface with the bookshelf sprite
    """
    # Create a surface with alpha channel
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))  # Fill with transparent color
    
    # Main shelf structure
    shelf_rect = pygame.Rect(0, 0, width, height)
    pygame.draw.rect(surface, color, shelf_rect)
    
    # Darker edge for depth
    dark_color = (color[0] * 0.7, color[1] * 0.7, color[2] * 0.7)
    edge_width = max(2, width // 10)
    edge_rect = pygame.Rect(width - edge_width, 0, edge_width, height)
    pygame.draw.rect(surface, dark_color, edge_rect)
    
    # Shelf dividers - horizontal lines
    divider_color = (color[0] * 0.8, color[1] * 0.8, color[2] * 0.8)
    num_shelves = 4
    shelf_spacing = height // (num_shelves + 1)
    
    for i in range(1, num_shelves + 1):
        y = i * shelf_spacing
        pygame.draw.line(surface, divider_color, (0, y), (width, y), 2)
    
    # Add books on the shelves
    book_colors = [
        (192, 57, 43),    # Red
        (41, 128, 185),   # Blue
        (39, 174, 96),    # Green
        (142, 68, 173),   # Purple
        (243, 156, 18)    # Yellow
    ]
    
    # Place books on each shelf
    for shelf in range(num_shelves + 1):
        shelf_y = shelf * shelf_spacing
        if shelf == 0:
            shelf_y = 2  # Adjust top shelf position
            
        book_height = shelf_spacing - 4
        book_width = width // 8
        book_spacing = book_width + 2
        
        # Place 3-5 books on each shelf, randomly colored
        for book in range(5):
            if book % 4 == 0:  # Skip some spots to create variation
                continue
                
            book_color = book_colors[book % len(book_colors)]
            book_x = book * book_spacing
            
            if book_x + book_width > width - edge_width:
                break
                
            book_rect = pygame.Rect(book_x, shelf_y + 2, book_width, book_height)
            pygame.draw.rect(surface, book_color, book_rect)
            
            # Add book spine detail
            spine_color = (book_color[0] * 0.8, book_color[1] * 0.8, book_color[2] * 0.8)
            pygame.draw.line(surface, spine_color, 
                            (book_x + book_width // 2, shelf_y + 2), 
                            (book_x + book_width // 2, shelf_y + book_height), 1)
    
    # Add outline
    pygame.draw.rect(surface, (0, 0, 0), shelf_rect, 2)
    
    return surface


def create_desk(
    width: int = 96, 
    height: int = 64, 
    color: Tuple[int, int, int] = (160, 120, 80)
) -> pygame.Surface:
    """
    Create a simple desk sprite with a cel-shaded look.
    
    Args:
        width: Width of the desk in pixels
        height: Height of the desk in pixels
        color: Base color of the desk (RGB)
        
    Returns:
        A pygame Surface with the desk sprite
    """
    # Create a surface with alpha channel
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))  # Fill with transparent color
    
    # Main desk surface
    desk_top_height = height // 3
    desk_top_rect = pygame.Rect(0, 0, width, desk_top_height)
    pygame.draw.rect(surface, color, desk_top_rect)
    
    # Desk front panel
    front_color = (color[0] * 0.8, color[1] * 0.8, color[2] * 0.8)
    front_rect = pygame.Rect(0, desk_top_height, width, height - desk_top_height)
    pygame.draw.rect(surface, front_color, front_rect)
    
    # Desk drawers
    drawer_width = width // 3
    drawer_height = (height - desk_top_height) // 2
    drawer_color = (color[0] * 0.9, color[1] * 0.9, color[2] * 0.9)
    
    # Left drawer
    left_drawer = pygame.Rect(width // 10, desk_top_height + drawer_height // 4, drawer_width, drawer_height)
    pygame.draw.rect(surface, drawer_color, left_drawer)
    
    # Right drawer
    right_drawer = pygame.Rect(width - drawer_width - width // 10, 
                              desk_top_height + drawer_height // 4, 
                              drawer_width, drawer_height)
    pygame.draw.rect(surface, drawer_color, right_drawer)
    
    # Drawer handles
    handle_color = (50, 50, 50)
    handle_width = drawer_width // 4
    handle_height = drawer_height // 5
    
    # Left drawer handle
    left_handle = pygame.Rect(
        left_drawer.centerx - handle_width // 2,
        left_drawer.centery - handle_height // 2,
        handle_width, handle_height
    )
    pygame.draw.rect(surface, handle_color, left_handle)
    
    # Right drawer handle
    right_handle = pygame.Rect(
        right_drawer.centerx - handle_width // 2,
        right_drawer.centery - handle_height // 2,
        handle_width, handle_height
    )
    pygame.draw.rect(surface, handle_color, right_handle)
    
    # Add desk items
    # Simple paper stack
    paper_rect = pygame.Rect(width // 4, height // 15, width // 5, height // 10)
    pygame.draw.rect(surface, (240, 240, 240), paper_rect)
    
    # Add outline
    pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(0, 0, width, height), 2)
    
    return surface


def create_floor_tile(
    size: int = 64,
    base_color: Tuple[int, int, int] = (180, 160, 140),
    variant: str = "wood"
) -> pygame.Surface:
    """
    Create a floor tile with a cel-shaded look.
    
    Args:
        size: Size of the tile (square)
        base_color: Base color of the tile
        variant: Type of floor ("wood", "stone", "carpet")
        
    Returns:
        A pygame Surface with the floor tile
    """
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Base fill
    surface.fill(base_color)
    
    if variant == "wood":
        # Create wood grain effect
        grain_color = (base_color[0] - 20, base_color[1] - 20, base_color[2] - 20)
        grain_spacing = size // 8
        
        for i in range(0, size, grain_spacing):
            thickness = 1 if i % 2 == 0 else 2
            pygame.draw.line(surface, grain_color, (i, 0), (i, size), thickness)
            
        # Add some shorter grain lines for variation
        for _ in range(5):
            x = pygame.draw.line(surface, grain_color, 
                                (grain_spacing * 2, size // 3), 
                                (grain_spacing * 6, size // 3), 1)
            y = pygame.draw.line(surface, grain_color, 
                                (grain_spacing * 1, size // 2), 
                                (grain_spacing * 4, size // 2), 1)
    
    elif variant == "stone":
        # Create stone texture effect
        grout_color = (base_color[0] - 40, base_color[1] - 40, base_color[2] - 40)
        stone_size = size // 4
        
        # Create a grid of stones with grout lines
        for x in range(0, size, stone_size):
            for y in range(0, size, stone_size):
                # Slightly randomize each stone's color
                stone_color = (
                    base_color[0] + pygame.math.Vector3(x, y, x+y).x % 20 - 10,
                    base_color[1] + pygame.math.Vector3(x, y, x+y).y % 20 - 10,
                    base_color[2] + pygame.math.Vector3(x, y, x+y).z % 20 - 10
                )
                
                # Draw the stone
                stone_rect = pygame.Rect(x + 1, y + 1, stone_size - 2, stone_size - 2)
                pygame.draw.rect(surface, stone_color, stone_rect)
                
        # Draw grout lines
        for x in range(0, size + 1, stone_size):
            pygame.draw.line(surface, grout_color, (x, 0), (x, size), 1)
        for y in range(0, size + 1, stone_size):
            pygame.draw.line(surface, grout_color, (0, y), (size, y), 1)
            
    elif variant == "carpet":
        # Create a carpet texture
        pattern_color = (
            min(255, base_color[0] + 20),
            min(255, base_color[1] + 20),
            min(255, base_color[2] + 20)
        )
        
        # Create a simple pattern
        dot_size = 3
        dot_spacing = size // 8
        
        for x in range(dot_spacing, size, dot_spacing):
            for y in range(dot_spacing, size, dot_spacing):
                if (x // dot_spacing + y // dot_spacing) % 2 == 0:
                    pygame.draw.rect(surface, pattern_color, 
                                    pygame.Rect(x - dot_size // 2, y - dot_size // 2, 
                                                dot_size, dot_size))
    
    # Add subtle border
    pygame.draw.rect(surface, (base_color[0] - 30, base_color[1] - 30, base_color[2] - 30), 
                    pygame.Rect(0, 0, size, size), 1)
    
    return surface


def create_wall_tile(
    size: int = 64,
    base_color: Tuple[int, int, int] = (220, 210, 200),
    variant: str = "plain"
) -> pygame.Surface:
    """
    Create a wall tile with a cel-shaded look.
    
    Args:
        size: Size of the tile (square)
        base_color: Base color of the wall
        variant: Type of wall ("plain", "brick", "wood_panel")
        
    Returns:
        A pygame Surface with the wall tile
    """
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Base fill
    surface.fill(base_color)
    
    if variant == "plain":
        # Add subtle vertical gradient for plain walls
        lighter_color = (
            min(255, int(base_color[0] * 1.1)),
            min(255, int(base_color[1] * 1.1)),
            min(255, int(base_color[2] * 1.1))
        )
        
        # Create gradient by drawing lines with decreasing alpha
        gradient_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        for y in range(size):
            alpha = 255 - int((y / size) * 150)  # Fade from top to bottom
            pygame.draw.line(gradient_surface, (*lighter_color, alpha), (0, y), (size, y))
            
        surface.blit(gradient_surface, (0, 0))
    
    elif variant == "brick":
        # Create brick pattern
        brick_color = base_color
        mortar_color = (base_color[0] - 50, base_color[1] - 50, base_color[2] - 50)
        
        brick_height = size // 6
        brick_width = size // 3
        
        # Draw brick rows with offset
        for y in range(0, size, brick_height):
            offset = brick_width // 2 if (y // brick_height) % 2 == 1 else 0
            
            # Draw the mortar line
            pygame.draw.rect(surface, mortar_color, pygame.Rect(0, y, size, 1))
            
            # Draw the bricks in this row
            for x in range(-offset, size, brick_width):
                brick_rect = pygame.Rect(x + 1, y + 1, brick_width - 2, brick_height - 2)
                
                # Only draw if brick is at least partially visible
                if brick_rect.right > 0 and brick_rect.left < size:
                    # Adjust the brick color slightly for variation
                    variation = (y + x) % 30 - 15
                    brick_shade = (
                        max(0, min(255, brick_color[0] + variation)),
                        max(0, min(255, brick_color[1] + variation)),
                        max(0, min(255, brick_color[2] + variation))
                    )
                    pygame.draw.rect(surface, brick_shade, brick_rect)
                    
                # Draw vertical mortar between bricks
                if x > -offset:
                    pygame.draw.rect(surface, mortar_color, pygame.Rect(x, y, 1, brick_height))
                    
    elif variant == "wood_panel":
        # Create wood panel effect
        panel_color = base_color
        groove_color = (max(0, panel_color[0] - 30), 
                        max(0, panel_color[1] - 30), 
                        max(0, panel_color[2] - 30))
        
        panel_width = size // 4
        
        # Draw vertical panels
        for x in range(0, size, panel_width):
            # Draw panel
            pygame.draw.rect(surface, panel_color, 
                           pygame.Rect(x, 0, panel_width, size))
            
            # Add some wood grain detail
            grain_color = (panel_color[0] - 15, panel_color[1] - 15, panel_color[2] - 15)
            for i in range(2, panel_width - 2, 2):
                if i % 4 == 0:
                    pygame.draw.line(surface, grain_color, 
                                    (x + i, 0), 
                                    (x + i, size), 
                                    1)
            
            # Draw groove between panels
            if x > 0:
                pygame.draw.rect(surface, groove_color, 
                               pygame.Rect(x - 1, 0, 2, size))
    
    # Add border
    pygame.draw.rect(surface, (base_color[0] - 40, base_color[1] - 40, base_color[2] - 40), 
                    pygame.Rect(0, 0, size, size), 1)
    
    return surface


def create_book(
    width: int = 32,
    height: int = 40,
    color: Tuple[int, int, int] = (180, 30, 30)
) -> pygame.Surface:
    """
    Create a simple book sprite with a cel-shaded look.
    
    Args:
        width: Width of the book in pixels
        height: Height of the book in pixels
        color: Base color of the book (RGB)
        
    Returns:
        A pygame Surface with the book sprite
    """
    # Create a surface with alpha channel
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))  # Fill with transparent color
    
    # Book body
    book_rect = pygame.Rect(0, 0, width, height)
    pygame.draw.rect(surface, color, book_rect)
    
    # Book spine
    spine_width = max(2, width // 8)
    spine_color = (color[0] * 0.7, color[1] * 0.7, color[2] * 0.7)
    spine_rect = pygame.Rect(0, 0, spine_width, height)
    pygame.draw.rect(surface, spine_color, spine_rect)
    
    # Book cover detail - horizontal line
    cover_line_color = (color[0] * 1.2, color[1] * 1.2, color[2] * 1.2)
    cover_line_y = height // 3
    pygame.draw.line(surface, cover_line_color, 
                   (spine_width + 2, cover_line_y), 
                   (width - 2, cover_line_y),
                   1)
    
    # Book title text simulation (just a few horizontal lines)
    text_color = (min(255, color[0] * 1.3), min(255, color[1] * 1.3), min(255, color[2] * 1.3))
    text_y = height // 2
    
    # Simulate a few lines of text
    for i in range(3):
        line_length = width - spine_width - 8 - (i * 5)  # Make lines different lengths
        pygame.draw.line(surface, text_color,
                       (spine_width + 4, text_y + i * 6),
                       (spine_width + 4 + line_length, text_y + i * 6),
                       2)
    
    # Add outline
    pygame.draw.rect(surface, (0, 0, 0), book_rect, 1)
    
    return surface


def save_asset(surface: pygame.Surface, filename: str, directory: str = "assets/images") -> bool:
    """
    Save a generated asset to a file.
    
    Args:
        surface: The pygame Surface to save
        filename: Name for the saved file
        directory: Directory to save the file in
        
    Returns:
        bool: True if the save was successful, False otherwise
    """
    # Make sure the directory exists
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError:
            return False
    
    # Save the image
    full_path = os.path.join(directory, filename)
    try:
        pygame.image.save(surface, full_path)
        return True
    except pygame.error:
        return False


def generate_library_assets() -> Dict[str, pygame.Surface]:
    """
    Generate a set of assets for the library scene.
    
    Returns:
        Dictionary mapping asset names to pygame Surfaces
    """
    assets = {}
    
    # Generate floor tiles
    assets["floor_wood"] = create_floor_tile(64, (180, 160, 140), "wood")
    assets["floor_stone"] = create_floor_tile(64, (160, 150, 140), "stone")
    assets["floor_carpet"] = create_floor_tile(64, (120, 80, 40), "carpet")
    
    # Generate wall tiles
    assets["wall_plain"] = create_wall_tile(64, (220, 210, 200), "plain")
    assets["wall_brick"] = create_wall_tile(64, (180, 100, 80), "brick")
    assets["wall_wood"] = create_wall_tile(64, (160, 120, 80), "wood_panel")
    
    # Generate furniture
    assets["bookshelf"] = create_bookshelf(64, 96)
    assets["desk"] = create_desk(96, 64)
    
    # Generate books
    book_colors = [
        (180, 30, 30),    # Red
        (30, 100, 180),   # Blue
        (30, 150, 50),    # Green
        (150, 50, 150),   # Purple
        (180, 150, 30)    # Yellow
    ]
    
    for i, color in enumerate(book_colors):
        assets[f"book_{i+1}"] = create_book(32, 40, color)
    
    return assets


def save_library_assets(directory: str = "assets/images") -> None:
    """
    Generate and save library assets to the specified directory.
    
    Args:
        directory: Directory to save the assets in
    """
    # Generate assets
    assets = generate_library_assets()
    
    # Save assets
    for name, surface in assets.items():
        save_asset(surface, f"{name}.png", directory)