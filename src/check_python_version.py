#!/usr/bin/env python3
"""
Check if Python version is compatible with the project
"""

import sys

MIN_PYTHON = (3, 10)
RECOMMENDED_PYTHON = (3, 11)

def check_python_version():
    """Check if Python version meets requirements"""
    current = sys.version_info[:2]
    
    print(f"Current Python version: {sys.version}")
    print(f"Version tuple: {current}")
    
    if current < MIN_PYTHON:
        print(f"\n❌ ERROR: Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+ required!")
        print(f"   Your version: {current[0]}.{current[1]}")
        print(f"\n   Please upgrade Python:")
        print(f"   - Download from: https://www.python.org/downloads/")
        print(f"   - Or use pyenv: pyenv install 3.11")
        sys.exit(1)
    
    elif current < RECOMMENDED_PYTHON:
        print(f"\n⚠️  WARNING: Python {RECOMMENDED_PYTHON[0]}.{RECOMMENDED_PYTHON[1]} recommended")
        print(f"   Your version works but consider upgrading")
        print(f"   Current: {current[0]}.{current[1]}")
    
    else:
        print(f"\n✅ Python version OK!")
        print(f"   Version {current[0]}.{current[1]} is fully supported")
    
    return True

if __name__ == "__main__":
    check_python_version()
