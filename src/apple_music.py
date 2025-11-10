"""Apple Music Library Scraper"""
import os
import json
import re
import requests
import time
import logging
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn
from rich.panel import Panel
from dotenv import load_dotenv
from urllib.parse import urljoin

load_dotenv()
console = Console()

Path('logs').mkdir(exist_ok=True)
logging.basicConfig(
    filename='logs/apple_music.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class AppleMusicScraper:
    
    def __init__(self):
        self.developer_token = os.getenv('APPLE_DEVELOPER_TOKEN')
        self.user_token = os.getenv('APPLE_MUSIC_USER_TOKEN')
        self.output_dir = Path(os.getenv('OUTPUT_DIR', 'output'))
        self.api_base = "https://amp-api.music.apple.com"
        self.session = requests.Session()
    
    @staticmethod
    def clean_song_title(title):
        if not title:
            return title
        
        title = re.sub(r'\s*\[.*?\]\s*', ' ', title)
        title = re.sub(r'\s*\(.*?\)\s*', ' ', title)
        title = re.sub(r'\s+', ' ', title).strip()
        
        return title
    
    def _fetch_page(self, url):
        headers = {
            'authorization': f'Bearer {self.developer_token}',
            'media-user-token': self.user_token,
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64)',
            'origin': 'https://music.apple.com',
            'referer': 'https://music.apple.com/'
        }
        
        try:
            response = self.session.get(url, headers=headers, timeout=20)
            
            if response.status_code == 200:
                return response.json()
            
            logging.error(f"HTTP {response.status_code}: {url}")
            
        except requests.exceptions.Timeout:
            logging.error(f"Timeout: {url}")
        except Exception as e:
            logging.error(f"Error: {str(e)}")
        
        return None
    
    def get_library_songs(self):
        if not self.developer_token or not self.user_token:
            console.print("[red]✗ Tokens not found in .env[/red]")
            self._show_help()
            return None
        
        console.print("[green]✓ Tokens loaded[/green]\n")
        logging.info("Starting library scan")
        
        all_songs = []
        url = f"{self.api_base}/v1/me/library/songs?limit=100"
        page = 0
        max_pages = 100
        
        progress = Progress(
            TextColumn("[cyan]Scanning library[/cyan]"),
            BarColumn(),
            TextColumn("{task.completed} songs"),
        )
        
        with progress:
            task = progress.add_task("", total=None)
            
            while url and page < max_pages:
                data = self._fetch_page(url)
                
                if not data:
                    logging.error(f"Failed to fetch page {page + 1}")
                    break
                
                songs = data.get('data', [])
                all_songs.extend(songs)
                progress.update(task, completed=len(all_songs))
                
                logging.info(f"Page {page + 1}: {len(songs)} songs (total: {len(all_songs)})")
                
                next_url = data.get('next')
                if next_url:
                    if next_url.startswith('/'):
                        url = urljoin(self.api_base, next_url)
                    else:
                        url = next_url
                else:
                    url = None
                
                page += 1
        
        self.session.close()
        logging.info(f"Scan completed: {len(all_songs)} songs total")
        
        return all_songs if all_songs else None
    
    def save_data(self, songs, clean_titles=True):
        if not songs:
            return
        
        self.output_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        txt_file = self.output_dir / f"apple_music_{timestamp}.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            for song in songs:
                attrs = song.get('attributes', {})
                artist = attrs.get('artistName', 'Unknown Artist')
                title = attrs.get('name', 'Unknown Title')
                
                if clean_titles:
                    title = self.clean_song_title(title)
                
                f.write(f"{artist} - {title}\n")
        
        json_file = self.output_dir / f"apple_music_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            export_data = {
                'export_date': datetime.now().isoformat(),
                'total_songs': len(songs),
                'songs': []
            }
            
            for song in songs:
                attrs = song.get('attributes', {})
                title = attrs.get('name', 'Unknown')
                
                song_data = {
                    'artist': attrs.get('artistName', 'Unknown'),
                    'title': title,
                    'title_clean': self.clean_song_title(title),
                    'album': attrs.get('albumName', ''),
                    'genre': attrs.get('genreNames', []),
                    'duration': attrs.get('durationInMillis', 0) // 1000,
                    'year': attrs.get('releaseDate', '').split('-')[0] if attrs.get('releaseDate') else ''
                }
                export_data['songs'].append(song_data)
            
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        console.print(f"\n[green]✓ TXT:[/green] {txt_file.name}")
        console.print(f"[green]✓ JSON:[/green] {json_file.name}")
        
        logging.info(f"Saved to {txt_file.name} and {json_file.name}")
    
    def _show_help(self):
        help_text = """[yellow]How to get tokens:[/yellow]

[cyan]1.[/cyan] Open [bold]https://music.apple.com[/bold] in browser
[cyan]2.[/cyan] Press [bold]F12[/bold] → [bold]Network[/bold] tab
[cyan]3.[/cyan] Refresh page ([bold]Ctrl+R[/bold])
[cyan]4.[/cyan] Find request to [bold]amp-api.music.apple.com[/bold]
[cyan]5.[/cyan] Click it → [bold]Headers[/bold] tab
[cyan]6.[/cyan] Copy from Request Headers:
   • [green]authorization: Bearer eyJ...[/green]
   • [green]media-user-token: Aqo...[/green]

[cyan]7.[/cyan] Add to [bold].env[/bold] file:
   [green]APPLE_DEVELOPER_TOKEN=eyJ...[/green]
   [green]APPLE_MUSIC_USER_TOKEN=Aqo...[/green]

[dim]Tokens valid for ~6 months[/dim]
"""
        console.print(Panel(help_text, title="🍎 Apple Music", border_style="cyan"))

def scan_apple_music():
    console.print(Panel.fit(
        "[bold cyan]🍎 Apple Music Library Scanner[/bold cyan]",
        border_style="cyan"
    ))
    console.print()
    
    start = time.time()
    
    scraper = AppleMusicScraper()
    songs = scraper.get_library_songs()
    
    if songs:
        elapsed = time.time() - start
        scraper.save_data(songs, clean_titles=True)
        console.print(f"\n[bold green]✓ Scanned {len(songs)} songs in {elapsed:.1f}s[/bold green]")
    else:
        console.print("[red]✗ Failed to scan library[/red]")
        console.print("[yellow]Check tokens in .env or see logs/apple_music.log[/yellow]")
    
    input("\nPress Enter...")
