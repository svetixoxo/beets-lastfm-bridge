#!/usr/bin/env python3
"""
Genre Batch Processor for beets-lastfm-bridge
Runs all genre scripts in sequence for automated workflow
"""

import subprocess
import sys
import os

def run_script(script_name):
    """Runs a script and shows status"""
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    
    if not os.path.exists(script_path):
        print(f"Script not found: {script_path}")
        return False
    
    print(f"\n{'='*60}")
    print(f"Starting: {script_name}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(['python3', script_path], check=True)
        print(f"\n✓ {script_name} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error in {script_name} (Exit Code: {e.returncode})")
        return False
    except KeyboardInterrupt:
        print(f"\n⚠ {script_name} cancelled by user")
        return False

def main():
    print("Genre Batch Processing")
    print("=" * 30)
    print("Will run in sequence:")
    print("1. genre_finder.py")
    print("2. genre_mapper.py") 
    print("3. genre_splitter.py")
    print()
    
    # User confirmation
    response = input("Do you want to continue? (y/N): ").lower()
    if response not in ['y', 'yes']:
        print("Cancelled")
        return
    
    scripts = [
        'genre_finder.py',
        'genre_mapper.py',
        'genre_splitter.py'
    ]
    
    success_count = 0
    
    for i, script in enumerate(scripts, 1):
        print(f"\nStep {i}/3:")
        if run_script(script):
            success_count += 1
        else:
            print(f"\nError running {script}")
            response = input("Continue with next script? (y/N): ").lower()
            if response not in ['y', 'yes']:
                break
    
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Successful: {success_count}/{len(scripts)} scripts")
    
    if success_count == len(scripts):
        print("✓ All scripts completed successfully!")
    else:
        print("⚠ Not all scripts completed successfully")
        
    print("\nGenre processing completed")

if __name__ == "__main__":
    main()
