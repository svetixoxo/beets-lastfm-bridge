# beets-lastfm-bridge

> **Important:** This project was created by someone with ~minimal~ almost no programming experience as a personal solution to a specific problem. The entire codebase was developed with significant assistance from Claude AI assistant by Anthropic. While **it works on my system**, I cannot guarantee it will work on yours or provide ~extensive~ any support for issues you might encounter.

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
# Arch Linux
sudo pacman -S beets

# Ubuntu/Debian
sudo apt install beets
```

### Setup beets-lastfm-bridge
1. Clone this repository:
   ```bash
   git clone https://github.com/svetixoxo/beets-lastfm-bridge.git
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

## Support and Limitations

### About This Project

This tool was created out of necessity when the built-in beets lastgenre plugin stopped working reliably. As someone ~with very limited~ without programming knowledge, I relied heavily on Claude AI to develop and troubleshoot this solution.

### About the Documentation

I haven't actually read through most of the [documentation files in this repository](https://github.com/svetixoxo/beets-lastfm-bridge/tree/main/docs) at all. Claude generated them based on our development conversation, and I trust that they're probably accurate and helpful, but I can't personally verify for their contents or completeness. Use them as a starting point, but don't be surprised if something doesn't quite match reality.

### What This Means for Users

- **"It Works on My System"**: This code has been tested on my specific setup (Arch Linux, Python 3.x, specific beets configuration). Your mileage may vary.
- **Limited Support**: I cannot provide extensive technical support or debugging assistance beyond what's documented here.
- **Community Contribution**: If you're an experienced developer and find issues or improvements, contributions are welcome, but I may not be able to review complex technical changes.
- **Use at Your Own Risk**: Please backup your music library before using these scripts.

### If You Encounter Issues

1. Check the troubleshooting section above
2. Verify your system meets the prerequisites
3. Try the examples and documentation files
4. Consider seeking help from more experienced Python/beets users
5. Remember that this is a personal tool that may not work for all setups

### Why Share This?

Despite my limited programming skills, this solution solved a real problem that others might face. Sometimes "good enough" code that works is better than no solution at all. If it helps even one person manage their music library better, it was worth sharing.

## Contributing

While contributions are welcome, please understand that:
- I may not be able to review complex technical changes
- I'm learning as I go and can't provide expert guidance
- Simple fixes and documentation improvements are most helpful
- Consider this more of a "working example" than a polished product

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/svetixoxo/beets-lastfm-bridge/blob/main/LICENSE) file for details.

## Acknowledgments

- Built as a workaround for beets lastgenre plugin issues
- Uses Last.fm API for genre data
- Inspired by the need for better music collection organization
- **Special thanks to Claude AI by Anthropic for making this project possible despite my ~limited~ non-existing programming experience**
