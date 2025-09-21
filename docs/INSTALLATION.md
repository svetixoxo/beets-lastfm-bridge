# Installation Guide

## Prerequisites

### System Requirements
- Python 3.7 or higher
- beets music library manager
- metaflac (part of flac package)
- Active internet connection for Last.fm API

### Install beets

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install beets flac
```

#### Arch Linux
```bash
sudo pacman -S beets flac
```

## Install beets-lastfm-bridge

### 1. Clone Repository
```bash
git clone https://github.com/svetixoxo/beets-lastfm-bridge.git
cd beets-lastfm-bridge
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Copy Configuration Files
```bash
# Create beets config directory if it doesn't exist
mkdir -p ~/.config/beets

# Copy configuration templates
cp config/genre_blacklist.json ~/.config/beets/
cp config/genre_mapping.json ~/.config/beets/

# Optional: Copy example beets config
cp examples/beets_config.yaml ~/.config/beets/config.yaml
```

### 4. Configure Last.fm API

1. **Get API credentials**:
   - Go to https://www.last.fm/api/account/create
   - Fill in the form:
     - Application name: "beets-lastfm-bridge"
     - Description: "Personal music library genre tagging"
     - Callback URL: (leave empty)
     - Homepage: (leave empty)
   - Note your API Key

2. **Update scripts with your API key**:
   ```bash
   # Edit each script file
   nano scripts/genre_finder.py
   
   # Replace this line:
   API_KEY = "YOUR_LASTFM_API_KEY_HERE"
   # With your actual API key:
   API_KEY = "your_actual_api_key_here"
   ```

### 5. Configure Music Directory

If your music is not in the default location, update the beets config:

```yaml
# ~/.config/beets/config.yaml
directory: /path/to/your/music/library
library: ~/.config/beets/musiclibrary.db
```

## Verify Installation

### Test beets
```bash
beet version
```

### Test scripts
```bash
cd beets-lastfm-bridge
python scripts/debug_genre_list.py
```

If this shows usage information, the installation is successful.

## Initial Setup

### Import your music to beets
```bash
# Import without writing tags (recommended for large collections)
beet import -s -A --noautotag /path/to/your/music
```

### Run first genre discovery
```bash
cd beets-lastfm-bridge
python scripts/genre_finder.py
```

## Troubleshooting

### Common Issues

**"beet: command not found"**
- beets is not installed or not in PATH
- Install using your package manager or pip

**"No module named 'requests'"**
- Python dependencies not installed
- Run: `pip install -r requirements.txt`

**"Error retrieving tracks from beets"**
- Music not imported to beets library
- Run: `beet import /path/to/music`

**"Error: Please configure your Last.fm API key"**
- API key not set in scripts
- Edit each script file and add your API key

**Permission errors**
- Scripts don't have write access to music files
- Check file permissions: `ls -la /path/to/music`

### Getting Help

1. Check the [TROUBLESHOOTING.md](https://github.com/svetixoxo/beets-lastfm-bridge/blob/main/docs/TROUBLESHOOTING.md) file
2. Review your beets configuration
3. Ensure all dependencies are installed
4. Verify API key is correct and active
