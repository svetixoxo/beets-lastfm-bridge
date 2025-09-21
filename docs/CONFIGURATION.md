# Configuration Guide

## Overview

beets-lastfm-bridge uses two main configuration files to control genre filtering and mapping:

- `~/.config/beets/genre_blacklist.json` - Controls which genres to exclude
- `~/.config/beets/genre_mapping.json` - Controls genre name normalization

## Blacklist Configuration

The blacklist file uses two filtering methods:

### Structure
```json
{
  "contains": ["term1", "term2"],
  "exact": ["genre1", "genre2"]
}
```

### Contains Filtering
Removes genres that **contain** any of these terms:
```json
"contains": [
  "female",
  "seen live", 
  "awesome",
  "vocal"
]
```

**Examples:**
- `"female"` removes "Female Vocal", "Female Frontend Metal"
- `"seen live"` removes "Seen Live in Concert"
- `"awesome"` removes "Awesome Metal", "Totally Awesome"

### Exact Filtering
Removes genres that **exactly match** these terms (case-insensitive):
```json
"exact": [
  "rock",
  "metal",
  "pop"
]
```

**Examples:**
- `"rock"` removes "Rock", "ROCK", "rock"
- But keeps "Hard Rock", "Progressive Rock"

### Automatic Filtering
Additionally, all genres containing **numbers** are automatically removed:
- "80s", "1990s", "2000s Rock" - all filtered out

## Genre Mapping Configuration

Maps inconsistent genre names to standardized versions:

### Structure
```json
{
  "old_name": "New Name",
  "another_old": "Standard Name"
}
```

### Examples
```json
{
  "nu metal": "Nu Metal",
  "nu-metal": "Nu Metal",
  "nü metal": "Nu Metal",
  "post hardcore": "Post-Hardcore",
  "post-hardcore": "Post-Hardcore",
  "death metal": "Death Metal",
  "thrash metal": "Thrash Metal"
}
```

### Case Handling
- Mapping keys should be **lowercase**
- Values can use any capitalization you prefer
- Lookup is case-insensitive

## API Configuration

### Last.fm Credentials
Each script needs your API key. Edit these files:

```python
# In scripts/genre_finder.py
API_KEY = "your_actual_api_key_here"
```

Required files to update:
- `scripts/genre_finder.py`

### Directory Paths
Scripts automatically use beets' configured music directory. If needed, verify your beets config:

```yaml
# ~/.config/beets/config.yaml
directory: /path/to/your/music
library: ~/.config/beets/musiclibrary.db
```

## Advanced Configuration

### Custom Blacklist Categories

You can create more specific blacklist categories:

```json
{
  "contains": [
    "vocal", "vocals", "singer",
    "radio", "edit", "version"
  ],
  "exact": [
    "rock", "metal", "pop"
  ]
}
```

### Genre Hierarchy Mapping

Create hierarchical mappings for better organization:

```json
{
  "nu metal": "Nu Metal",
  "rap metal": "Nu Metal",
  "alternative metal": "Alternative Metal",
  "alt metal": "Alternative Metal",
  "progressive metal": "Progressive Metal",
  "prog metal": "Progressive Metal",
  "symphonic metal": "Symphonic Metal",
  "gothic metal": "Gothic Metal",
  "black metal": "Extreme Metal",
  "death metal": "Extreme Metal",
  "grindcore": "Extreme Metal"
}
```

### Regional Variations

Handle different regional spellings:

```json
{
  "colour bass": "Color Bass",
  "programme music": "Program Music",
  "analogue": "Analog"
}
```

## Workflow-Specific Configuration

### For Large Collections
- Use more aggressive blacklisting
- Focus on broad genre categories
- Avoid too many specific mappings initially

### For Curated Collections  
- Use minimal blacklisting
- Create detailed mapping hierarchies
- Include style-specific variations

### For FLAC Collections
- Remember that genre splitting only works with FLAC
- Consider how separate tags will display in your player
- Plan for players that may concatenate tags

## Testing Configuration

### Preview Changes
```bash
# See what genres exist
python scripts/debug_genre_list.py all

# See what would be mapped
python scripts/debug_genre_list.py new
```

### Incremental Testing
1. Start with a small blacklist
2. Run genre_finder on a few artists
3. Review results with debug script
4. Expand blacklist and mappings
5. Apply to full collection

## Configuration Management

### Backup Configurations
```bash
# Backup your working configs
cp ~/.config/beets/genre_blacklist.json ~/genre_blacklist_backup.json
cp ~/.config/beets/genre_mapping.json ~/genre_mapping_backup.json
```

### Version Control
Consider keeping your configurations in version control:
```bash
git init ~/.config/beets
cd ~/.config/beets
git add genre_*.json
git commit -m "Initial genre configuration"
```

### Sharing Configurations
You can share configuration files between systems or with other users by copying the JSON files.

## Troubleshooting Configuration

### Common Issues

**Too many genres filtered out**
- Check if blacklist is too aggressive
- Review exact matches - they might be filtering valid subgenres

**Inconsistent genre names remain**
- Check mapping file for typos
- Remember mapping keys must be lowercase
- Verify JSON syntax is valid

**API errors**
- Confirm API key is correctly set in all scripts
- Test API key with a simple curl command

**No genres found**
- Check if blacklist is filtering everything
- Verify internet connection and Last.fm availability
