#!/usr/bin/env python3
"""
Push Terminal Tools Suite to GitHub
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
    print("Pushing Terminal Tools Suite to GitHub...")
    
    # Git path
    git_cmd = r"C:\Program Files\Git\bin\git.exe"
    
    # Set remote origin
    print("Setting remote origin...")
    success, stdout, stderr = run_command(f'"{git_cmd}" remote add origin https://github.com/ahmedtouzani/Terminal-Tools-Suite.git')
    if success:
        print("[OK] Remote origin set")
    else:
        print(f"[ERROR] Failed to set remote: {stderr}")
    
    # Rename branch to main
    print("Setting main branch...")
    success, stdout, stderr = run_command(f'"{git_cmd}" branch -M main')
    if success:
        print("[OK] Main branch set")
    else:
        print(f"[ERROR] Failed to set branch: {stderr}")
    
    # Push to GitHub
    print("Pushing to GitHub...")
    success, stdout, stderr = run_command(f'"{git_cmd}" push -u origin main')
    if success:
        print("[SUCCESS] Code pushed to GitHub!")
        print("Repository: https://github.com/ahmedtouzani/Terminal-Tools-Suite")
    else:
        print(f"[ERROR] Failed to push: {stderr}")
        print("You may need to authenticate with GitHub")

if __name__ == "__main__":
    main()
