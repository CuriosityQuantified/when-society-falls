#!/usr/bin/env python3
"""
Main entry point for the When Society Falls game.

This script initializes and runs the game application.
"""
import os
import sys
import logging

from src.core.application import Application


def main():
    """Main entry point for the game."""
    try:
        # Create and run the application
        app = Application()
        app.run()
    except Exception as e:
        logging.error(f"Error running the game: {e}", exc_info=True)
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 