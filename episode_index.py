#!/usr/bin/env python3
"""
Episode Index Generator

This script reads episode data from episodes.json and generates:
1. episodes/index.html - Episode list page
2. index.html - Main home page

Usage:
    python episode_index.py
"""

import json
from pathlib import Path


# Shared CSS styles for episode tables and buttons
TABLE_STYLES = '''
        .brand-badge {
            position: absolute;
            top: 20px;
            left: 20px;
            width: 160px;
            height: auto;
        }
        .episode-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        .episode-table th,
        .episode-table td {
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid rgba(100, 255, 218, 0.2);
        }
        .episode-table th {
            color: #64ffda;
            font-size: 1.1em;
            border-bottom: 2px solid rgba(100, 255, 218, 0.4);
        }
        .episode-table tr:hover {
            background-color: rgba(100, 255, 218, 0.05);
        }
        .episode-name {
            color: #e0e0e0;
            font-weight: 500;
        }
        .episode-num {
            color: #64ffda;
            font-size: 1.2em;
            font-weight: bold;
            text-align: center;
            width: 50px;
        }
        .episode-summary {
            color: #a0a0a0;
            font-size: 0.9em;
            margin-top: 5px;
        }
        .link-btn {
            display: inline-block;
            padding: 8px 16px;
            margin: 2px 4px;
            border-radius: 4px;
            text-decoration: none;
            font-size: 0.9em;
            transition: all 0.2s ease;
        }
        .link-transcript {
            background-color: rgba(100, 255, 218, 0.15);
            color: #64ffda;
        }
        .link-transcript:hover {
            background-color: rgba(100, 255, 218, 0.3);
            text-decoration: none;
        }
        .link-spotify {
            background-color: rgba(30, 215, 96, 0.15);
            color: #1ed760;
        }
        .link-spotify:hover {
            background-color: rgba(30, 215, 96, 0.3);
            text-decoration: none;
        }
        .link-youtube {
            background-color: rgba(255, 0, 0, 0.15);
            color: #ff4444;
        }
        .link-youtube:hover {
            background-color: rgba(255, 0, 0, 0.3);
            text-decoration: none;
        }
        .link-bar {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 10px;
            margin: 25px 0;
            padding: 20px;
            background-color: rgba(0, 0, 0, 0.2);
            border-radius: 8px;
        }
        .link-bar .link-btn {
            padding: 12px 24px;
            font-size: 1em;
        }
        .description {
            color: #b8c5d6;
            font-size: 1.1em;
            line-height: 1.8;
            margin: 20px 0;
            text-align: center;
        }
'''


def load_episodes(json_path):
    """Load episode data from the JSON file."""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_episode_table(episodes, transcript_prefix=''):
    """Generate HTML for the episode table."""
    rows = []
    for episode in episodes:
        ep_num = episode['episode_number']
        title = episode['title']
        summary = episode.get('summary', '')
        spotify_url = episode.get('spotify_url', '#')
        youtube_url = episode.get('youtube_url', '#')
        transcript_file = f"{transcript_prefix}transcript_ep{ep_num}.html"
        
        rows.extend([
            '                <tr>',
            f'                    <td class="episode-num">{ep_num}</td>',
            '                    <td>',
            f'                        <div class="episode-name">{title}</div>',
            f'                        <div class="episode-summary">{summary}</div>',
            '                    </td>',
            '                    <td>',
            f'                        <a href="{transcript_file}" class="link-btn link-transcript">Transcript</a>',
            f'                        <a href="{spotify_url}" class="link-btn link-spotify" target="_blank">Spotify</a>',
            f'                        <a href="{youtube_url}" class="link-btn link-youtube" target="_blank">YouTube</a>',
            '                    </td>',
            '                </tr>',
        ])
    
    return '\n'.join([
        '        <table class="episode-table">',
        '            <thead>',
        '                <tr>',
        '                    <th>#</th>',
        '                    <th>Episode</th>',
        '                    <th>Links</th>',
        '                </tr>',
        '            </thead>',
        '            <tbody>',
        '\n'.join(rows),
        '            </tbody>',
        '        </table>',
    ])


def generate_episodes_index(episodes, output_path, css_file='transcript_styles.css'):
    """Generate the episodes/index.html file."""
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Carbon and Cardboard - Episode List</title>
    <link rel="stylesheet" href="{css_file}">
    <style>{TABLE_STYLES}
    </style>
</head>
<body>
    <img src="../brand_badge.png" alt="Carbon and Cardboard" class="brand-badge">
    <div class="transcript-container">
        <h1>Carbon and Cardboard - Episode List</h1>
{generate_episode_table(episodes)}
    </div>
</body>
</html>'''
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)


def generate_home_page(episodes, output_path, css_file='episodes/transcript_styles.css'):
    """Generate the main index.html home page."""
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Carbon and Cardboard</title>
    <link rel="stylesheet" href="{css_file}">
    <style>{TABLE_STYLES}
    </style>
</head>
<body>
    <img src="brand_badge.png" alt="Carbon and Cardboard" class="brand-badge">
    <div class="transcript-container">
        <h1>Carbon and Cardboard</h1>
        
        <p class="description">
            A podcast exploring board games as a way to talk about environment and the climate.
            We discuss game mechanics, educational design, and the ways that play can help engage with these complex topics.
            We use many games as lenses into this rich space, and started as part of the 
            <A HREF="https://climatebase.org/fellowship">Climatebase Fellowship</A>.
        </p>
        
        <div class="link-bar">
            <a href="https://open.spotify.com/show/2ypWbMcbH9GtGvrRLgxN0X?si=311b368b0c0d43d9" class="link-btn link-spotify" target="_blank">
                Spotify
            </a>
            <a href="https://www.youtube.com/@CarbonAndCardboard" class="link-btn link-youtube" target="_blank">
                YouTube
            </a>
            <a href="https://github.com/scotfree/carbonandcardboard.com/" class="link-btn link-transcript" target="_blank">
                GitHub
            </a>
        </div>
        
        <h2><a href="episodes/index.html">Episodes</a></h2>
{generate_episode_table(episodes, transcript_prefix='episodes/')}
    </div>
</body>
</html>'''
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)


def main():
    """Main function to generate the episode indexes."""
    
    script_dir = Path(__file__).parent
    episodes_dir = script_dir / 'episodes'
    json_path = episodes_dir / 'episodes.json'
    
    if not json_path.exists():
        print(f"Error: {json_path} not found.")
        return 1
    
    print(f"Reading episodes from: {json_path}")
    episodes = load_episodes(json_path)
    # Sort by episode number descending (most recent first)
    episodes.sort(key=lambda ep: ep['episode_number'], reverse=True)
    print(f"Found {len(episodes)} episode(s)")
    
    for ep in episodes:
        print(f"  - Episode {ep['episode_number']}: {ep['title']}")
    
    # Generate episodes/index.html
    episodes_index_path = episodes_dir / 'index.html'
    generate_episodes_index(episodes, episodes_index_path)
    print(f"\nEpisodes index generated: {episodes_index_path}")
    
    # Generate main index.html
    home_path = script_dir / 'index.html'
    generate_home_page(episodes, home_path)
    print(f"Home page generated: {home_path}")
    
    return 0


if __name__ == '__main__':
    exit(main())
