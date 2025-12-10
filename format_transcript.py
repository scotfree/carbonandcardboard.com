#!/usr/bin/env python3
"""
Transcript to HTML Converter

This script converts a plain text transcript into a formatted HTML file.
It automatically detects speakers (identified by timestamps in parentheses)
and assigns each speaker a unique color scheme.

Usage:
    python format_transcript.py <input_transcript.txt> <output.html>

Example:
    python format_transcript.py transcript_episode1.txt transcript_ep1.html
"""

import sys
import re
import os
from pathlib import Path


def parse_transcript(transcript_path):
    """
    Parse the transcript file and extract speaker sections.
    
    Returns:
        list: A list of dictionaries with 'speaker', 'timestamp', and 'text' keys
    """
    with open(transcript_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Pattern to match speaker names with timestamps: "Name (HH:MM)"
    speaker_pattern = re.compile(r'^(.+?)\s+\((\d+:\d+)\)\s*$')
    
    sections = []
    current_speaker = None
    current_timestamp = None
    current_text = []
    
    for line in lines:
        line = line.rstrip('\n')
        
        # Check if this line is a speaker header
        match = speaker_pattern.match(line)
        
        if match:
            # Save the previous section if it exists
            if current_speaker is not None:
                sections.append({
                    'speaker': current_speaker,
                    'timestamp': current_timestamp,
                    'text': '\n'.join(current_text).strip()
                })
            
            # Start a new section
            current_speaker = match.group(1)
            current_timestamp = match.group(2)
            current_text = []
        else:
            # Add to current speaker's text
            if current_speaker is not None:
                current_text.append(line)
    
    # Don't forget the last section
    if current_speaker is not None:
        sections.append({
            'speaker': current_speaker,
            'timestamp': current_timestamp,
            'text': '\n'.join(current_text).strip()
        })
    
    return sections


def get_speaker_mapping(sections):
    """
    Create a mapping of speaker names to color class numbers.
    
    Returns:
        dict: Mapping of speaker name to speaker class number
    """
    unique_speakers = []
    for section in sections:
        if section['speaker'] not in unique_speakers:
            unique_speakers.append(section['speaker'])
    
    # Create mapping: speaker name -> class number (1-8)
    speaker_mapping = {}
    for i, speaker in enumerate(unique_speakers):
        speaker_mapping[speaker] = (i % 8) + 1
    
    return speaker_mapping


def extract_episode_number(filename):
    """
    Extract the episode number from a filename.
    
    Tries patterns like:
    - transcript_ep1.html -> 1
    - transcript_episode1.txt -> 1
    - episode2_transcript.txt -> 2
    
    Returns:
        int or None: The episode number if found, None otherwise
    """
    basename = os.path.basename(filename)
    
    # Try various patterns
    patterns = [
        r'ep(\d+)',           # ep1, ep2, etc.
        r'episode(\d+)',      # episode1, episode2, etc.
        r'episode_(\d+)',     # episode_1, episode_2, etc.
    ]
    
    for pattern in patterns:
        match = re.search(pattern, basename, re.IGNORECASE)
        if match:
            return int(match.group(1))
    
    return None


def generate_html(sections, speaker_mapping, output_path, episode_num=None):
    """
    Generate the HTML file from parsed sections.
    """
    # Get the CSS filename (in the same directory as output)
    css_file = 'transcript_styles.css'
    
    # Build the episode title
    if episode_num is not None:
        episode_title = f"Episode {episode_num} Transcript"
    else:
        episode_title = "Transcript"
    
    # Start building HTML
    html_parts = [
        '<!DOCTYPE html>',
        '<html lang="en">',
        '<head>',
        '    <meta charset="UTF-8">',
        '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
        f'    <title>Carbon and Cardboard - {episode_title}</title>',
        f'    <link rel="stylesheet" href="{css_file}">',
        '    <style>',
        '        .brand-badge {',
        '            display: block;',
        '            margin: 20px auto;',
        '            width: 160px;',
        '            height: auto;',
        '        }',
        '        h1 {',
        '            margin-top: 10px;',
        '        }',
        '    </style>',
        '</head>',
        '<body>',
        '    <div class="transcript-container">',
        f'        <h1>Carbon and Cardboard - {episode_title}</h1>',
        '        <img src="../brand_badge.png" alt="Carbon and Cardboard" class="brand-badge">',
    ]
    
    # Add each speaker section
    for section in sections:
        speaker = section['speaker']
        timestamp = section['timestamp']
        text = section['text']
        speaker_class = f"speaker-{speaker_mapping[speaker]}"
        
        html_parts.append(f'        <div class="speaker-section {speaker_class}">')
        html_parts.append(f'            <div class="speaker-header">')
        html_parts.append(f'                {speaker} <span class="timestamp">({timestamp})</span>')
        html_parts.append(f'            </div>')
        
        # Split text into paragraphs (separated by blank lines)
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        html_parts.append(f'            <div class="speaker-text">')
        for paragraph in paragraphs:
            # Replace single newlines with spaces, preserve paragraph breaks
            paragraph = paragraph.replace('\n', ' ')
            html_parts.append(f'                <p>{paragraph}</p>')
        html_parts.append(f'            </div>')
        html_parts.append(f'        </div>')
    
    # Close HTML
    html_parts.extend([
        '    </div>',
        '</body>',
        '</html>'
    ])
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html_parts))


def main():
    """Main function to handle command-line arguments and coordinate the conversion."""
    
    if len(sys.argv) != 3:
        print("Usage: python format_transcript.py <input_transcript.txt> <output.html>")
        print("\nExample:")
        print("    python format_transcript.py transcript_episode1.txt transcript_ep1.html")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    
    print(f"Reading transcript from: {input_file}")
    
    # Parse the transcript
    sections = parse_transcript(input_file)
    print(f"Found {len(sections)} speaker sections")
    
    # Get speaker mapping
    speaker_mapping = get_speaker_mapping(sections)
    print(f"Identified {len(speaker_mapping)} unique speakers:")
    for speaker, class_num in speaker_mapping.items():
        print(f"  - {speaker} (color theme {class_num})")
    
    # Try to extract episode number from filenames
    episode_num = extract_episode_number(output_file) or extract_episode_number(input_file)
    if episode_num:
        print(f"Detected episode number: {episode_num}")
    
    # Generate HTML
    generate_html(sections, speaker_mapping, output_file, episode_num)
    print(f"\nHTML file generated: {output_file}")
    print(f"Make sure '{os.path.join(os.path.dirname(output_file) or '.', 'transcript_styles.css')}' is in the same directory!")


if __name__ == '__main__':
    main()

