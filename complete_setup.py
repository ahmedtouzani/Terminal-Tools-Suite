#!/usr/bin/env python3
"""
Complete Git setup and push to GitHub
"""

import os
import subprocess
import sys

def run_git_command(command, cwd=None):
    """Run Git command"""
    git_path = r"C:\Program Files\Git\bin\git.exe"
    full_cmd = f'"{git_path}" {command}'
    
    try:
        result = subprocess.run(full_cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print("=== Terminal Tools Suite - GitHub Setup ===")
    
    # Initialize repository
    print("1. Initializing Git repository...")
    success, stdout, stderr = run_git_command("init", ".")
    if success:
        print("   [OK] Repository initialized")
    else:
        print(f"   [ERROR] {stderr}")
        return False
    
    # Configure user (if needed)
    print("2. Configuring Git user...")
    run_git_command('config user.name "Ahmed Touzani"', ".")
    run_git_command('config user.email "ahmed.touzani@example.com"', ".")
    print("   [OK] User configured")
    
    # Add all files
    print("3. Adding files...")
    success, stdout, stderr = run_git_command("add .", ".")
    if success:
        print("   [OK] Files added")
    else:
        print(f"   [ERROR] {stderr}")
        return False
    
    # Create initial commit
    print("4. Creating initial commit...")
    success, stdout, stderr = run_git_command('commit -m "Initial commit: Terminal Tools Suite v1.0 - Created by Ahmed Touzani (R3D) - Parallel Universe Team"', ".")
    if success:
        print("   [OK] Initial commit created")
    else:
        print(f"   [ERROR] {stderr}")
        return False
    
    # Add remote origin
    print("5. Adding remote origin...")
    success, stdout, stderr = run_git_command("remote add origin https://github.com/ahmedtouzani/Terminal-Tools-Suite.git", ".")
    if success:
        print("   [OK] Remote origin added")
    else:
        print(f"   [ERROR] {stderr}")
    
    # Push to GitHub
    print("6. Pushing to GitHub...")
    success, stdout, stderr = run_git_command("push -u origin main", ".")
    if success:
        print("   [SUCCESS] Code pushed to GitHub!")
        print("\n🎉 Repository is now live at:")
        print("   https://github.com/ahmedtouzani/Terminal-Tools-Suite")
    else:
        print(f"   [ERROR] {stderr}")
        print("\n⚠️  You may need to:")
        print("   1. Create a personal access token on GitHub")
        print("   2. Use: git push -u origin main")
        print("   3. Or push manually from Git GUI")
    
    return True

if __name__ == "__main__":
    main()
