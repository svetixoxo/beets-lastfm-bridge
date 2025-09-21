#!/usr/bin/env python3
"""
Debug Genre List for beets-lastfm-bridge
Shows all genres or unmapped genres for analysis
"""

import subprocess
import json
import sys
import os

def load_genre_mapping():
    """Loads genre mappings from configuration file"""
    mapping_file = os.path.expanduser("~/.config/beets/genre_mapping.json")
    
    if not os.path.exists(mapping_file):
        return {}
    
    with open(mapping_file, 'r') as f:
        return json.load(f)

def get_all_genres():
    """Gets all genres from beets library"""
    try:
        result = subprocess.run(
            ['beet', 'ls', '-f', '$genre'],
            capture_output=True, text=True, check=True
        )
        
        all_genres = set()
        for line in result.stdout.strip().split('\n'):
            if line.strip() and line != '':
                # Split comma-separated genres
                genres = [g.strip() for g in line.split(',')]
                all_genres.update(genres)
        
        return sorted([g for g in all_genres if g])
    except subprocess.CalledProcessError:
        print("Error retrieving genres from beets")
        return []

def show_usage():
    """Shows script usage"""
    print("Usage: python3 debug_genre_list.py [FLAG]")
    print("")
    print("Available flags:")
    print("  all   - Show all genres in music collection")
    print("  new   - Show only genres not in mapping JSON")
    print("")
    print("Examples:")
    print("  python3 debug_genre_list.py all")
    print("  python3 debug_genre_list.py new")

def main():
    if len(sys.argv) != 2:
        show_usage()
        return
    
    flag = sys.argv[1].lower()
    
    if flag not in ['all', 'new']:
        print(f"Unknown flag: {flag}")
        print("")
        show_usage()
        return
    
    print("Collecting all genres from music collection...")
    all_genres = get_all_genres()
    
    if not all_genres:
        print("No genres found in music collection")
        return
    
    if flag == 'all':
        print(f"\nAll genres in music collection ({len(all_genres)}):")
        print("=" * 50)
        for i, genre in enumerate(all_genres, 1):
            print(f"{i:3d}. {genre}")
    
    elif flag == 'new':
        mapping = load_genre_mapping()
        mapped_genres = set(mapping.keys())
        
        # Find genres not in mapping file
        new_genres = [genre for genre in all_genres if genre.lower() not in mapped_genres]
        
        if new_genres:
            print(f"\nGenres not in mapping file ({len(new_genres)}):")
            print("=" * 50)
            for i, genre in enumerate(new_genres, 1):
                print(f"{i:3d}. {genre}")
        else:
            print("\nAll genres are already in mapping file")
            print("No new genres found")
    
    print(f"\nTotal: {len(all_genres)} different genres in collection")

if __name__ == "__main__":
    main()
