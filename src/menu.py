"""Interactive Menu"""
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

class Menu:
    def __init__(self):
        self.running = True
    
    def show_main_menu(self):
        """Главное меню"""
        console.clear()
        console.print(Panel.fit(
            "[bold cyan]🎵 Music Downloader CLI[/bold cyan]",
            border_style="cyan"
        ))
        
        console.print("\n[yellow]What do you want to do?[/yellow]\n")
        console.print("1) Scan music from streaming service")
        console.print("2) Scan local .txt file with songs")
        console.print("3) Direct search")
        console.print("0) Exit\n")
    
    def show_streaming_menu(self):
        """Меню выбора стримингового сервиса"""
        console.print("\n[yellow]Choose streaming service:[/yellow]\n")
        console.print("1) Apple Music")
        console.print("2) Spotify")
        console.print("0) Back\n")
    
    def get_choice(self, max_option):
        """Получить выбор пользователя"""
        while True:
            choice = Prompt.ask("[green]Enter choice[/green]")
            if choice.isdigit() and 0 <= int(choice) <= max_option:
                return int(choice)
            console.print("[red]Invalid choice! Try again.[/red]")
