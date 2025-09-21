# Troubleshooting Guide

## Common Issues

### Installation Problems

#### "beet: command not found"
**Cause:** beets is not installed or not in system PATH

**Solutions:**
```bash
# Check if beets is installed
which beet

# Install beets if missing
pip install beets
# or
sudo apt install beets  # Ubuntu/Debian
brew install beets      # macOS
```

#### "No module named 'requests'"
**Cause:** Python dependencies not installed

**Solution:**
```bash
pip install -r requirements.txt
```

#### "metaflac: command not found"
**Cause:** FLAC tools not installed (needed for genre splitting)

**Solutions:**
```bash
sudo apt install flac       # Ubuntu/Debian
brew install flac           # macOS
sudo pacman -S flac         # Arch Linux
```

### API and Network Issues

#### "Error: Please configure your Last.fm API key"
**Cause:** API key not set in scripts

**Solution:**
1. Get API key from https://www.last.fm/api/account/create
2. Edit `scripts/genre_finder.py`:
   ```python
   API_KEY = "your_actual_api_key_here"
   ```

#### "Error for Artist: Invalid API key"
**Cause:** API key is incorrect or inactive

**Solutions:**
1. Verify API key is correctly copied
2. Check Last.fm account status
3. Generate new API key if needed

#### "Error for Artist: HTTP timeout"
**Cause:** Network connectivity or Last.fm server issues

**Solutions:**
1. Check internet connection
2. Try again later (Last.fm may be temporarily down)
3. Use smaller batch sizes

### Beets Library Issues

#### "Error retrieving tracks from beets"
**Cause:** Music not imported to beets library

**Solutions:**
```bash
# Import music to beets
beet import /path/to/your/music

# Check if music is in library
beet ls | head -10

# Verify beets config
beet config
```

#### "No matching items found"
**Cause:** Query syntax issue or empty library

**Solutions:**
```bash
# Check library contents
beet stats

# Verify specific query
beet ls genre:

# Check for tracks without genres
beet ls -f '$artist - $title: "$genre"' | grep ': ""'
```

### Genre Processing Issues

#### No genres found for any artist
**Possible causes:**
- Blacklist too aggressive
- API connectivity issues
- Artists not in Last.fm database

**Debug steps:**
```bash
# Test with well-known artist
python scripts/debug_genre_list.py all

# Check blacklist configuration
cat ~/.config/beets/genre_blacklist.json

# Test API manually
curl "http://ws.audioscrobbler.com/2.0/?method=artist.gettoptags&artist=Metallica&api_key=YOUR_API_KEY&format=json"
```

#### All genres being filtered out
**Cause:** Overly aggressive blacklist

**Solution:**
1. Review blacklist settings
2. Start with minimal blacklist:
   ```json
   {
     "contains": ["seen live"],
     "exact": ["rock"]
   }
   ```
3. Gradually expand based on results

#### Genres not splitting into separate tags
**Cause:** Not FLAC files or no comma-separated genres

**Solutions:**
```bash
# Check file format
beet ls -f '$format' | head -10

# Verify comma-separated genres exist
beet ls -f '$genre' | grep ","

# Only works with FLAC files
file /path/to/music/file.flac
```

### File Permission Issues

#### "Permission denied" errors
**Cause:** Scripts don't have write access to music files

**Solutions:**
```bash
# Check file permissions
ls -la /path/to/music/

# Fix permissions if needed
chmod 664 /path/to/music/*.flac
chown user:group /path/to/music/*.flac
```

#### "Database is locked"
**Cause:** Multiple beets processes running

**Solutions:**
```bash
# Check for running beets processes
ps aux | grep beet

# Kill hanging processes
pkill -f beet

# Restart scripts
```

### Performance Issues

#### Scripts running very slowly
**Possible causes:**
- Large music collection
- Slow network connection
- API rate limiting

**Solutions:**
1. Process smaller batches:
   ```bash
   # Process one artist at a time
   beet ls -f '$albumartist' | head -10 | while read artist; do
       python scripts/genre_finder.py "$artist"
   done
   ```

2. Increase timeout values in scripts

3. Run during off-peak hours

#### Memory issues with large collections
**Solution:**
Process in smaller chunks or increase system memory for the process.

## Debug Techniques

### Verbose Logging
Add debug prints to scripts for more information:
```python
print(f"Processing: {artist} - {track}")
print(f"API response: {response.status_code}")
```

### Test Individual Components

#### Test Last.fm API
```bash
curl "http://ws.audioscrobbler.com/2.0/?method=artist.gettoptags&artist=Architects&api_key=YOUR_API_KEY&format=json"
```

#### Test beets queries
```bash
beet ls -f '$albumartist§$album§
