"""Local TXT File Scanner (stub)"""
from rich.console import Console
from rich.prompt import Prompt

console = Console()

def scan_txt_file():
    """Сканирование локального txt файла (заглушка)"""
    console.print("\n[cyan]Local TXT Scanner[/cyan]")
    
    filepath = Prompt.ask("[green]Enter path to .txt file[/green]", default="data/songs.txt")
    
    console.print(f"\n[yellow]Scanning file: {filepath}[/yellow]")
    console.print("[yellow]Not implemented yet...[/yellow]")
    input("\nPress Enter to continue...")
