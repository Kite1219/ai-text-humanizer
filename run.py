#!/usr/bin/env python3
"""
AI Text Humanizer - Entry Point
Run this file to start the AI Text Humanization Tool.
"""

import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.main import main

if __name__ == "__main__":
    main() 