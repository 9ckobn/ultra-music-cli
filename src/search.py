"""Direct Search (stub)"""
from rich.console import Console
from rich.prompt import Prompt

console = Console()

def direct_search():
    """Прямой поиск (заглушка)"""
    console.print("\n[cyan]Direct Search[/cyan]")
    
    query = Prompt.ask("[green]Enter song name[/green]")
    
    console.print(f"\n[yellow]Searching for: {query}[/yellow]")
    console.print("[yellow]Not implemented yet...[/yellow]")
    input("\nPress Enter to continue...")
