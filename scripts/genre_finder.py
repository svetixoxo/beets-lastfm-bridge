#!/usr/bin/env python3
"""
Genre Finder for beets-lastfm-bridge
Discovers genres from Last.fm with hierarchical Track → Album → Artist fallback
"""

import subprocess
import requests
import json
import sys
import os

# Configuration - Replace with your Last.fm API credentials
API_KEY = "YOUR_LASTFM_API_KEY_HERE"

def load_genre_mapping():
    """Loads genre mappings from configuration file"""
    mapping_file = os.path.expanduser("~/.config/beets/genre_mapping.json")
    
    if not os.path.exists(mapping_file):
        with open(mapping_file, 'w') as f:
            json.dump({}, f, indent=2)
        print(f"Empty genre mapping file created: {mapping_file}")
    
    with open(mapping_file, 'r') as f:
        return json.load(f)

def load_blacklist():
    """Loads blacklist from configuration file"""
    blacklist_file = os.path.expanduser("~/.config/beets/genre_blacklist.json")
    
    if not os.path.exists(blacklist_file):
        default_blacklist = {
            "contains": [],
            "exact": []
        }
        with open(blacklist_file, 'w') as f:
            json.dump(default_blacklist, f, indent=2)
        print(f"Empty blacklist file created: {blacklist_file}")
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

def filter_blacklisted_genres(genres, blacklist):
    """Removes genres that are blacklisted or contain numbers"""
    filtered_genres = []
    
    for genre in genres:
        genre_lower = genre.lower().strip()
        should_exclude = False
        
        # Check if genre is exactly in the exact list
        if genre_lower in blacklist["exact"]:
            should_exclude = True
        
        # Check if genre contains any term from the contains list
        if not should_exclude:
            for blacklisted_term in blacklist["contains"]:
                if blacklisted_term in genre_lower:
                    should_exclude = True
                    break
        
        # Check if genre contains numbers
        if not should_exclude and any(char.isdigit() for char in genre):
            should_exclude = True
        
        if not should_exclude:
            filtered_genres.append(genre)
    
    return filtered_genres

def apply_genre_mapping(genres, mapping):
    """Applies genre mapping to a list of genres"""
    mapped_genres = []
    for genre in genres:
        mapped_genre = mapping.get(genre.lower(), genre.title())
        mapped_genres.append(mapped_genre)
    return mapped_genres

def get_genres_from_lastfm(artist, track=None, album=None):
    """Gets genres from Last.fm with hierarchy: Track → Album → Artist"""
    url = "http://ws.audioscrobbler.com/2.0/"
    
    # 1. Try track-specific genres
    if track:
        params = {
            "method": "track.gettoptags",
            "artist": artist,
            "track": track,
            "api_key": API_KEY,
            "format": "json"
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if "toptags" in data and "tag" in data["toptags"] and len(data["toptags"]["tag"]) > 0:
                tags = data["toptags"]["tag"]
                if len(tags) >= 2:  # Only if at least 2 good track tags available
                    raw_genres = [tag["name"] for tag in tags[:3]]
                    
                    # Apply blacklist
                    blacklist = load_blacklist()
                    filtered_genres = filter_blacklisted_genres(raw_genres, blacklist)
                    
                    if len(filtered_genres) >= 2:  # Only if enough remain after filtering
                        mapping = load_genre_mapping()
                        mapped_genres = apply_genre_mapping(filtered_genres, mapping)
                        return ", ".join(mapped_genres), "track"
        except Exception:
            pass
    
    # 2. Fallback: Album-specific genres
    if album:
        params = {
            "method": "album.gettoptags",
            "artist": artist,
            "album": album,
            "api_key": API_KEY,
            "format": "json"
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if "toptags" in data and "tag" in data["toptags"] and len(data["toptags"]["tag"]) > 0:
                tags = data["toptags"]["tag"]
                raw_genres = [tag["name"] for tag in tags[:3]]
                
                # Apply blacklist
                blacklist = load_blacklist()
                filtered_genres = filter_blacklisted_genres(raw_genres, blacklist)
                
                if len(filtered_genres) >= 1:  # At least 1 genre after filtering
                    mapping = load_genre_mapping()
                    mapped_genres = apply_genre_mapping(filtered_genres, mapping)
                    return ", ".join(mapped_genres), "album"
        except Exception:
            pass
    
    # 3. Fallback: Artist genres
    params = {
        "method": "artist.gettoptags",
        "artist": artist,
        "api_key": API_KEY,
        "format": "json"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if "toptags" in data and "tag" in data["toptags"]:
            tags = data["toptags"]["tag"]
            raw_genres = [tag["name"] for tag in tags[:3]]
            
            # Apply blacklist
            blacklist = load_blacklist()
            filtered_genres = filter_blacklisted_genres(raw_genres, blacklist)
            
            if len(filtered_genres) >= 1:  # At least 1 genre after filtering
                mapping = load_genre_mapping()
                mapped_genres = apply_genre_mapping(filtered_genres, mapping)
                return ", ".join(mapped_genres), "artist"
        return None, None
    except Exception as e:
        print(f"Error for {artist}: {e}")
        return None, None

def get_tracks_without_genres():
    """Gets all tracks without genres from beets"""
    try:
        result = subprocess.run(
            ['beet', 'ls', '-f', '$albumartist§$album§$title§$id', 'genre:'],
            capture_output=True, text=True, check=True
        )
        tracks = []
        for line in result.stdout.strip().split('\n'):
            if line.strip() and '§' in line:
                parts = line.split('§')
                if len(parts) == 4:
                    albumartist, album, title, track_id = parts
                    tracks.append({
                        'artist': albumartist,
                        'album': album,
                        'title': title,
                        'id': track_id
                    })
        return tracks
    except subprocess.CalledProcessError:
        print("Error retrieving tracks from beets")
        return []

def set_genre_for_track(track_id, genres):
    """Sets genres for a track in beets"""
    try:
        subprocess.run(
            ['beet', 'modify', '-y', f'id:{track_id}', f'genre={genres}'],
            check=True, capture_output=True, timeout=30
        )
        return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return False

def main():
    if API_KEY == "YOUR_LASTFM_API_KEY_HERE":
        print("Error: Please configure your Last.fm API key in the script")
        print("Get your API key at: https://www.last.fm/api/account/create")
        return
    
    print("Searching for tracks without genres...")
    tracks = get_tracks_without_genres()
    
    if not tracks:
        print("No tracks without genres found")
        return
    
    print(f"Found: {len(tracks)} tracks")
    
    for i, track in enumerate(tracks, 1):
        print(f"[{i}/{len(tracks)}] {track['artist']} - {track['title']}")
        
        genres, source = get_genres_from_lastfm(
            track['artist'], 
            track['title'], 
            track['album']
        )
        
        if genres:
            if set_genre_for_track(track['id'], genres):
                print(f"  ✓ Genres set ({source}): {genres}")
            else:
                print(f"  ✗ Error setting genres")
        else:
            print(f"  - No genres found")
    
    print("\nWriting genres to files...")
    subprocess.run(['beet', 'write'], check=True)
    print("Done!")

if __name__ == "__main__":
    main()
