#!/usr/bin/env python3
"""
Genre Cleaner for beets-lastfm-bridge
Removes unwanted genres from existing collection based on blacklist
"""

import subprocess
import json
import os

def load_blacklist():
    """Loads blacklist from configuration file"""
    blacklist_file = os.path.expanduser("~/.config/beets/genre_blacklist.json")
    
    if not os.path.exists(blacklist_file):
        print(f"Blacklist file not found: {blacklist_file}")
        return {"contains": [], "exact": []}
    
    with open(blacklist_file, 'r') as f:
        data = json.load(f)
        
        # Backwards compatibility for old array structure
        if isinstance(data, list):
            return {"contains": [term.lower() for term in data], "exact": []}
        
        # New object structure
        return {
            "contains": [term.lower() for term in data.get("contains", [])],
            "exact": [term.lower() for term in data.get("exact", [])]
        }

def should_remove_genre(genre, blacklist):
    """Checks if a genre should be removed"""
    genre_lower = genre.lower().strip()
    
    # Check if genre is exactly in the exact list
    if genre_lower in blacklist["exact"]:
        return True
    
    # Check if genre contains any term from the contains list
    for blacklisted_term in blacklist["contains"]:
        if blacklisted_term in genre_lower:
            return True
    
    # Check if genre contains numbers
    if any(char.isdigit() for char in genre):
        return True
    
    return False

def clean_existing_genres():
    """Removes unwanted genres from existing collection"""
    blacklist = load_blacklist()
    
    if not blacklist["contains"] and not blacklist["exact"]:
        print("No blacklist entries found")
        return
    
    # Get all songs with genres
    try:
        result = subprocess.run(
            ['beet', 'ls', '-f', '$albumartist§$album§$title§$genre§$id'],
            capture_output=True, text=True, check=True
        )
        lines = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
    except subprocess.CalledProcessError:
        print("Error retrieving songs")
        return
    
    cleaned_count = 0
    total_songs = len(lines)
    
    print(f"Processing {total_songs} songs...")
    
    for i, line in enumerate(lines, 1):
        if '§' not in line:
            continue
            
        try:
            parts = line.split('§')
            if len(parts) != 5:
                continue
                
            albumartist, album, title, current_genres, song_id = parts
            
            if not current_genres.strip():
                continue
            
            # Split genres and filter
            genres = [g.strip() for g in current_genres.split(',')]
            filtered_genres = []
            removed_genres = []
            
            for genre in genres:
                if should_remove_genre(genre, blacklist):
                    removed_genres.append(genre)
                else:
                    filtered_genres.append(genre)
            
            # Only update if genres were removed
            if removed_genres:
                new_genre_string = ", ".join(filtered_genres) if filtered_genres else ""
                
                print(f"[{i}/{total_songs}] {albumartist} - {album} - {title}")
                print(f"  Removed: {', '.join(removed_genres)}")
                if filtered_genres:
                    print(f"  Kept: {', '.join(filtered_genres)}")
                else:
                    print(f"  All genres removed")
                
                subprocess.run(
                    ['beet', 'modify', '-y', f'id:{song_id}', f'genre={new_genre_string}'],
                    check=True, capture_output=True, timeout=30
                )
                cleaned_count += 1
            elif i % 500 == 0:
                print(f"[{i}/{total_songs}] Processed...")
                
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, ValueError):
            continue
    
    print(f"\nGenres cleaned for {cleaned_count} songs")
    
    # Write changes to files
    print("Writing changes to files...")
    subprocess.run(['beet', 'write'], check=True)
    print("Done!")

def main():
    print("Genre cleaning for existing collection")
    print("=" * 45)
    clean_existing_genres()

if __name__ == "__main__":
    main()
