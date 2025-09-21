# beets-lastfm-bridge

**Coded/implemented and translated with significant support/assistance from Claude AI assistant by Anthropic.**

A comprehensive genre tagging solution for beets music library management. This tool bridges the gap between beets and Last.fm to provide intelligent, hierarchical genre tagging when the built-in lastgenre plugin fails.

## Features

### Core Functionality
- **Hierarchical Genre Discovery**: Track → Album → Artist fallback system
- **Advanced Blacklist System**: Filter unwanted genres (contains/exact matching)
- **Genre Mapping**: Normalize inconsistent genre names
- **Separate FLAC Tags**: Split comma-separated genres into individual tags
- **Batch Processing**: Automated workflow for large collections
- **Debug Tools**: Analyze existing genres and identify unmapped entries

### Key Advantages
- **Reliable**: Works when beets' lastgenre plugin fails
- **Flexible**: Highly customizable blacklists and mappings
- **Intelligent**: Filters numeric genres (80s, 1990s) and quality descriptors
- **Comprehensive**: Complete workflow from discovery to file writing

### Limitations
- Requires manual Last.fm API key setup
- Python script dependencies (not a native beets plugin)
- Only works with already imported beets libraries
- FLAC-specific features for separate genre tags

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Get Last.fm API credentials** at https://www.last.fm/api/account/create

3. **Configure scripts** with your API key and music directory

4. **Run the complete workflow**:
   ```bash
   python scripts/genre_batch.py
   ```

## Installation

### Prerequisites
- Python 3.7+
- beets music library manager
- Active Last.fm API account

### Install beets
```bash
# Ubuntu/Debian
sudo apt install beets

# macOS
brew install beets

# Python pip
pip install beets
```

### Setup beets-lastfm-bridge
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/beets-lastfm-bridge.git
   cd beets-lastfm-bridge
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy configuration templates:
   ```bash
   cp config/genre_blacklist.json ~/.config/beets/
   cp config/genre_mapping.json ~/.config/beets/
   ```

4. Configure your Last.fm API credentials in the scripts (see Configuration section)

## Configuration

### Last.fm API Setup
1. Register at https://www.last.fm/api/account/create
2. Note your API Key and Secret
3. Edit each script in `scripts/` directory and replace:
   ```python
   API_KEY = "YOUR_API_KEY_HERE"
   ```

### Directory Configuration
Update the music directory path in relevant scripts:
```python
# Change this line to match your music library path
directory_path = "/path/to/your/music/library"
```

### Blacklist Configuration
Edit `~/.config/beets/genre_blacklist.json`:
```json
{
  "contains": ["female", "seen live", "awesome"],
  "exact": ["rock", "metal", "pop"]
}
```

### Genre Mapping Configuration
Edit `~/.config/beets/genre_mapping.json`:
```json
{
  "nu metal": "Nu Metal",
  "post-hardcore": "Post-Hardcore"
}
```

## Usage

### Individual Scripts

#### Find New Genres
Discovers genres for tracks without existing genre tags:
```bash
python scripts/genre_finder.py
```

#### Apply Genre Mappings
Normalizes existing genre names based on your mapping configuration:
```bash
python scripts/genre_mapper.py
```

#### Split Genre Tags
Converts comma-separated genres into separate FLAC tags:
```bash
python scripts/genre_splitter.py
```

#### Clean Existing Genres
Removes unwanted genres from your existing collection:
```bash
python scripts/genre_cleaner.py
```

#### Debug and Analysis
View all genres or find unmapped ones:
```bash
python scripts/debug_genre_list.py all    # Show all genres
python scripts/debug_genre_list.py new    # Show unmapped genres
```

#### Batch Processing
Run the complete workflow automatically:
```bash
python scripts/genre_batch.py
```

### Recommended Workflow

1. **Import music to beets**:
   ```bash
   beet import -s -A --noautotag /path/to/music
   ```

2. **Run batch processing**:
   ```bash
   python scripts/genre_batch.py
   ```

3. **Review and refine**:
   ```bash
   python scripts/debug_genre_list.py new
   # Edit genre_mapping.json with new mappings
   python scripts/genre_mapper.py
   ```

## File Structure

- `scripts/genre_finder.py` - Core genre discovery from Last.fm
- `scripts/genre_mapper.py` - Apply genre name mappings
- `scripts/genre_splitter.py` - Create separate FLAC genre tags
- `scripts/genre_cleaner.py` - Remove unwanted genres
- `scripts/genre_batch.py` - Automated workflow runner
- `scripts/debug_genre_list.py` - Analysis and debugging tool
- `config/genre_blacklist.json` - Blacklist configuration template
- `config/genre_mapping.json` - Genre mapping template
- `examples/` - Sample configurations and beets config

## Troubleshooting

### Common Issues

**"No matching items found" error**:
- Check that music is properly imported to beets
- Verify beets database path in scripts

**API rate limiting**:
- Last.fm may throttle requests for large collections
- The scripts include timeout handling

**No genres found**:
- Verify Last.fm API credentials
- Check internet connectivity
- Some artists may not have genre data on Last.fm

**Permission errors**:
- Ensure scripts have read/write access to music files
- Check beets database permissions

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/svetixoxo/beets-lastfm-bridge/blob/main/LICENSE) file for details.

## Acknowledgments

- Built as a workaround for beets lastgenre plugin issues
- Uses Last.fm API for genre data
- Inspired by the need for better music collection organization
