#!/usr/bin/env python3
"""
Deployment Script for AI Text Humanizer
Helps automate the deployment process to GitHub and Streamlit Cloud.
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_git_status():
    """Check if git is initialized and has changes."""
    if not Path(".git").exists():
        print("❌ Git repository not initialized")
        return False
    
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    return len(result.stdout.strip()) > 0

def main():
    """Main deployment function."""
    print("🚀 AI Text Humanizer Deployment Script")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("app.py").exists():
        print("❌ app.py not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Check if .env exists
    if not Path(".env").exists():
        print("⚠️  .env file not found. Please create it with your API key:")
        print("   UNDETECTABLE_API_KEY=your_api_key_here")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Initialize git if not already done
    if not Path(".git").exists():
        print("📁 Initializing Git repository...")
        if not run_command("git init", "Git initialization"):
            sys.exit(1)
    
    # Add all files
    if not run_command("git add .", "Adding files to git"):
        sys.exit(1)
    
    # Check if there are changes to commit
    if not check_git_status():
        print("ℹ️  No changes to commit")
    else:
        # Commit changes
        commit_message = input("Enter commit message (or press Enter for default): ").strip()
        if not commit_message:
            commit_message = "Update AI Text Humanizer"
        
        if not run_command(f'git commit -m "{commit_message}"', "Committing changes"):
            sys.exit(1)
    
    # Check if remote is configured
    result = subprocess.run("git remote -v", shell=True, capture_output=True, text=True)
    if "origin" not in result.stdout:
        print("🌐 Setting up GitHub remote...")
        username = input("Enter your GitHub username: ").strip()
        if not username:
            print("❌ GitHub username required")
            sys.exit(1)
        
        repo_name = input("Enter repository name (or press Enter for 'ai-text-humanizer'): ").strip()
        if not repo_name:
            repo_name = "ai-text-humanizer"
        
        remote_url = f"https://github.com/{username}/{repo_name}.git"
        if not run_command(f"git remote add origin {remote_url}", "Adding remote"):
            sys.exit(1)
    
    # Push to GitHub
    if not run_command("git push -u origin main", "Pushing to GitHub"):
        sys.exit(1)
    
    print("\n🎉 Deployment to GitHub completed!")
    print("\n📋 Next steps:")
    print("1. Go to https://share.streamlit.io")
    print("2. Sign in with your GitHub account")
    print("3. Click 'New app'")
    print("4. Select your repository")
    print("5. Set main file path to: app.py")
    print("6. Click 'Deploy'")
    print("7. In Settings → Secrets, add your API key:")
    print("   UNDETECTABLE_API_KEY = \"your_api_key_here\"")
    print("\n🔗 Your app will be available at:")
    print("   https://yourusername-ai-text-humanizer-app-xxxxx.streamlit.app")

if __name__ == "__main__":
    main() 