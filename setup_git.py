#!/usr/bin/env python3
"""
Setup Git repository for Terminal Tools Suite
"""

import os
import subprocess
import sys

def run_command(cmd, cwd=None):
    """Run command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print("Setting up Git repository for Terminal Tools Suite...")
    
    # Try different Git paths
    git_paths = [
        "git",
        r"C:\Program Files\Git\bin\git.exe",
        r"C:\Program Files (x86)\Git\bin\git.exe",
        r"C:\Users\touza\AppData\Local\Programs\Git\bin\git.exe"
    ]
    
    git_cmd = None
    for path in git_paths:
        success, _, _ = run_command(f'"{path}" --version')
        if success:
            git_cmd = path
            print(f"[OK] Found Git at: {path}")
            break
    
    if not git_cmd:
        print("[ERROR] Git not found. Please restart your terminal or add Git to PATH.")
        return False
    
    # Initialize repository
    print("Initializing Git repository...")
    success, stdout, stderr = run_command(f'"{git_cmd}" init')
    if success:
        print("[OK] Repository initialized")
    else:
        print(f"[ERROR] Failed to initialize: {stderr}")
        return False
    
    # Add all files
    print("Adding files to repository...")
    success, stdout, stderr = run_command(f'"{git_cmd}" add .')
    if success:
        print("[OK] Files added")
    else:
        print(f"[ERROR] Failed to add files: {stderr}")
        return False
    
    # Create initial commit
    print("Creating initial commit...")
    success, stdout, stderr = run_command(f'"{git_cmd}" commit -m "Initial commit: Terminal Tools Suite v1.0"')
    if success:
        print("[OK] Initial commit created")
    else:
        print(f"[ERROR] Failed to commit: {stderr}")
        return False
    
    print("\n[SUCCESS] Git repository setup complete!")
    print("\nNext steps:")
    print("1. Create a new repository on GitHub")
    print("2. Run these commands to push:")
    print(f'   "{git_cmd}" branch -M main')
    print(f'   "{git_cmd}" remote add origin https://github.com/yourusername/terminal-tools.git')
    print(f'   "{git_cmd}" push -u origin main')
    
    return True

if __name__ == "__main__":
    main()
