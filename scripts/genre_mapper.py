#!/usr/bin/env python3
"""
Genre Mapper for beets-lastfm-bridge
Applies genre name mappings to existing genres in your collection
"""

import subprocess
import json
import os

def load_genre_mapping():
    """Loads genre mappings from configuration file"""
    mapping_file = os.path.expanduser("~/.config/beets/genre_mapping.json")
    
    if not os.path.exists(mapping_file):
        print(f"Mapping file not found: {mapping_file}")
        print("Creating empty mapping file - please edit and run again")
        with open(mapping_file, 'w') as f:
            json.dump({}, f, indent=2)
        return {}
    
    with open(mapping_file, 'r') as f:
        return json.load(f)

def update_existing_genres():
    """Updates all existing genres based on mapping file"""
    mapping = load_genre_mapping()
    
    if not mapping:
        print("No mappings found in file")
        return
    
    # Get all songs with genres in one call
    try:
        result = subprocess.run(
            ['beet', 'ls', '-f', '$albumartist§$album§$title§$genre§$id'],
            capture_output=True, text=True, check=True
        )
        lines = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
    except subprocess.CalledProcessError:
        print("Error retrieving songs")
        return
    
    updated_count = 0
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
            
            # Split genres and apply mapping
            genres = [g.strip() for g in current_genres.split(',')]
            mapped_genres = []
            changed = False
            
            for genre in genres:
                mapped_genre = mapping.get(genre.lower(), genre)
                mapped_genres.append(mapped_genre)
                if mapped_genre != genre:
                    changed = True
            
            # Only update if something changed
            if changed:
                new_genre_string = ", ".join(mapped_genres)
                
                print(f"[{i}/{total_songs}] {albumartist} - {album} - {title}")
                print(f"  {current_genres} -> {new_genre_string}")
                
                subprocess.run(
                    ['beet', 'modify', '-y', f'id:{song_id}', f'genre={new_genre_string}'],
                    check=True, capture_output=True, timeout=30
                )
                updated_count += 1
            elif i % 500 == 0:
                print(f"[{i}/{total_songs}] Processed...")
                
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, ValueError):
            continue
    
    print(f"\nGenres updated for {updated_count} songs")
    
    # Write changes to files
    print("Writing changes to files...")
    subprocess.run(['beet', 'write'], check=True)
    print("Done!")

def main():
    print("Updating existing genres based on mapping file...")
    update_existing_genres()

if __name__ == "__main__":
    main()
