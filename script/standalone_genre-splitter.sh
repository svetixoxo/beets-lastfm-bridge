#!/bin/bash

beet ls -f '$path' 'genre:,' | while IFS= read -r file; do
    if [[ -f "$file" ]]; then
        current=$(metaflac --show-tag=GENRE "$file" 2>/dev/null | cut -d= -f2)
        if [[ "$current" == *","* ]]; then
            echo "Converting: $(basename "$file")"
            metaflac --remove-tag=GENRE "$file"
            echo "$current" | tr ',' '\n' | while read -r genre; do
                genre=$(echo "$genre" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
                if [[ -n "$genre" ]]; then
                    metaflac --set-tag=GENRE="$genre" "$file"
                fi
            done
        fi
    fi
done
