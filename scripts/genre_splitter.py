#!/usr/bin/env python3
"""
Genre Splitter for beets-lastfm-bridge
Splits comma-separated genres into separate FLAC tags
"""

import subprocess
import os

def split_genres():
    """Splits comma-separated genres into separate FLAC tags"""
    
    # Find all FLAC files with comma-separated genres
    try:
        result = subprocess.run(
            ['beet', 'ls', '-f', '$path', 'genre:,'],
            capture_output=True, text=True, check=True
        )
        flac_files = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
    except subprocess.CalledProcessError:
        print("Error retrieving FLAC files")
        return
    
    if not flac_files:
        print("No files with comma-separated genres found")
        return
    
    total_files = len(flac_files)
    converted_files = 0
    
    print(f"Processing {total_files} files with comma-separated genres...")
    
    for i, file_path in enumerate(flac_files, 1):
        if not os.path.exists(file_path):
            continue
            
        try:
            # Read current genres
            result = subprocess.run(
                ['metaflac', '--show-tag=GENRE', file_path],
                capture_output=True, text=True, check=True
            )
            
            if not result.stdout.strip():
                continue
                
            # Take first GENRE tag (should be the comma-separated one)
            genre_line = result.stdout.strip().split('\n')[0]
            if '=' not in genre_line:
                continue
                
            current_genres = genre_line.split('=', 1)[1]
            
            # Only process if commas are present
            if ',' in current_genres:
                print(f"[{i}/{total_files}] Converting: {os.path.basename(file_path)}")
                
                # Remove all GENRE tags
                subprocess.run(
                    ['metaflac', '--remove-tag=GENRE', file_path],
                    check=True, capture_output=True
                )
                
                # Split genres and add individually
                genres = [g.strip() for g in current_genres.split(',')]
                for genre in genres:
                    if genre:  # Only non-empty genres
                        subprocess.run(
                            ['metaflac', f'--set-tag=GENRE={genre}', file_path],
                            check=True, capture_output=True
                        )
                
                print(f"  {current_genres} -> {len(genres)} separate tags")
                converted_files += 1
                
            elif i % 1000 == 0:
                print(f"[{i}/{total_files}] Processed...")
                
        except subprocess.CalledProcessError:
            continue
    
    print(f"\nResult:")
    print(f"- {converted_files} files converted")
    print(f"- Genres were split into separate tags")
    
    # Update beets database
    print("\nUpdating beets database...")
    subprocess.run(['beet', 'update'], check=True)
    print("Done!")

def main():
    print("Genre Splitter for FLAC files")
    print("=" * 35)
    split_genres()

if __name__ == "__main__":
    main()
