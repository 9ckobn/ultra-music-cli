#!/usr/bin/env python3
"""
Music Downloader CLI
"""

from src.menu import Menu
from src.apple_music import scan_apple_music
from src.spotify import scan_spotify
from src.scanner import scan_txt_file
from src.search import direct_search

def main():
    menu = Menu()
    
    while menu.running:
        menu.show_main_menu()
        choice = menu.get_choice(3)
        
        if choice == 1:
            # Streaming service
            menu.show_streaming_menu()
            streaming_choice = menu.get_choice(2)
            
            if streaming_choice == 1:
                scan_apple_music()
            elif streaming_choice == 2:
                scan_spotify()
            # 0 = back
        
        elif choice == 2:
            # Local TXT scan
            scan_txt_file()
        
        elif choice == 3:
            # Direct search
            direct_search()
        
        elif choice == 0:
            # Exit
            menu.running = False
            print("\nGoodbye! 👋")

if __name__ == '__main__':
    main()
