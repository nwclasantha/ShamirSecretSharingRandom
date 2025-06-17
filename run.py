#!/usr/bin/env python3
"""
Simple runner script for the Shamir Secret Sharing Random Password application.
"""

import subprocess
import sys
import os

def main():
    """Run the Shamir Secret Sharing application."""
    script_path = "ShamirSecretSharingRandomPassword.py"
    
    if not os.path.exists(script_path):
        print(f"Error: {script_path} not found in the current directory.")
        sys.exit(1)
    
    try:
        # Run the Python script
        subprocess.run([sys.executable, script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_path}: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nApplication interrupted by user.")
        sys.exit(0)

if __name__ == "__main__":
    main()