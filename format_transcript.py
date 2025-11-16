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


def generate_html(sections, speaker_mapping, output_path):
    """
    Generate the HTML file from parsed sections.
    """
    # Get the CSS filename (in the same directory as output)
    css_file = 'transcript_styles.css'
    
    # Start building HTML
    html_parts = [
        '<!DOCTYPE html>',
        '<html lang="en">',
        '<head>',
        '    <meta charset="UTF-8">',
        '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '    <title>Carbon and Cardboard - Episode 1 Transcript</title>',
        f'    <link rel="stylesheet" href="{css_file}">',
        '</head>',
        '<body>',
        '    <div class="transcript-container">',
        '        <h1>Carbon and Cardboard - Episode 1 Transcript</h1>',
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
    
    # Generate HTML
    generate_html(sections, speaker_mapping, output_file)
    print(f"\nHTML file generated: {output_file}")
    print(f"Make sure '{os.path.join(os.path.dirname(output_file) or '.', 'transcript_styles.css')}' is in the same directory!")


if __name__ == '__main__':
    main()

