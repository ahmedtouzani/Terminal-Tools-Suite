#!/usr/bin/env python3
"""
Interactive File Manager with Rich UI
A terminal-based file manager with beautiful interface and intuitive controls

Created by Ahmed Touzani (R3D) - Parallel Universe Team
"""

import os
import shutil
import stat
import time
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.text import Text
from rich.layout import Layout
from rich.columns import Columns
from rich.align import Align
from rich import box

console = Console()

class FileManager:
    def __init__(self):
        self.console = Console()
        self.current_path = Path.cwd()
        self.selected_index = 0
        self.show_hidden = False
        
    def get_directory_contents(self):
        """Get directory contents with file information"""
        try:
            items = []
            for item in sorted(self.current_path.iterdir(), key=lambda x: (x.is_file(), x.name.lower())):
                if not self.show_hidden and item.name.startswith('.'):
                    continue
                    
                try:
                    stat_info = item.stat()
                    size = stat_info.st_size
                    modified = datetime.fromtimestamp(stat_info.st_mtime)
                    
                    if item.is_dir():
                        size_str = "<DIR>"
                        icon = "📁"
                        color = "blue"
                    else:
                        size_str = self.format_size(size)
                        icon = self.get_file_icon(item.suffix)
                        color = self.get_file_color(item.suffix)
                    
                    items.append({
                        'name': item.name,
                        'path': item,
                        'is_dir': item.is_file() == False,
                        'size': size_str,
                        'modified': modified.strftime('%Y-%m-%d %H:%M'),
                        'icon': icon,
                        'color': color
                    })
                except (OSError, PermissionError):
                    continue
                    
            return items
        except PermissionError:
            return []
    
    def format_size(self, size_bytes):
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"
    
    def get_file_icon(self, extension):
        """Get icon based on file extension"""
        extension = extension.lower()
        icons = {
            '.py': '🐍',
            '.js': '📜',
            '.html': '🌐',
            '.css': '🎨',
            '.json': '📋',
            '.xml': '📄',
            '.txt': '📝',
            '.md': '📖',
            '.pdf': '📕',
            '.doc': '📘',
            '.docx': '📘',
            '.xls': '📗',
            '.xlsx': '📗',
            '.zip': '🗜️',
            '.tar': '📦',
            '.gz': '🗜️',
            '.jpg': '🖼️',
            '.jpeg': '🖼️',
            '.png': '🖼️',
            '.gif': '🖼️',
            '.mp3': '🎵',
            '.mp4': '🎬',
            '.avi': '🎬',
            '.exe': '⚙️',
            '.msi': '⚙️',
        }
        return icons.get(extension, '📄')
    
    def get_file_color(self, extension):
        """Get color based on file extension"""
        extension = extension.lower()
        colors = {
            '.py': 'green',
            '.js': 'yellow',
            '.html': 'blue',
            '.css': 'magenta',
            '.json': 'cyan',
            '.txt': 'white',
            '.md': 'green',
            '.pdf': 'red',
            '.zip': 'orange',
            '.jpg': 'magenta',
            '.png': 'magenta',
            '.mp3': 'purple',
            '.mp4': 'purple',
            '.exe': 'red',
        }
        return colors.get(extension, 'white')
    
    def create_file_table(self):
        """Create file listing table"""
        items = self.get_directory_contents()
        
        table = Table(title=f"📁 {self.current_path}", show_header=True, header_style="bold blue", box=box.ROUNDED)
        table.add_column("#", style="dim", width=3)
        table.add_column("Icon", style="bold", width=4)
        table.add_column("Name", style="bold", min_width=20)
        table.add_column("Size", style="cyan", width=10)
        table.add_column("Modified", style="yellow", width=16)
        
        for idx, item in enumerate(items):
            index_str = f"[green]{idx + 1}[/green]" if idx == self.selected_index else str(idx + 1)
            name_style = item['color'] if item['is_dir'] == False else 'bold blue'
            
            if idx == self.selected_index:
                name = f"[{name_style} on_black]{item['name']}[/{name_style} on_black]"
            else:
                name = f"[{name_style}]{item['name']}[/{name_style}]"
            
            table.add_row(
                index_str,
                item['icon'],
                name,
                item['size'],
                item['modified']
            )
        
        return table
    
    def create_help_panel(self):
        """Create help panel"""
        help_text = """
[bold cyan]Navigation:[/bold cyan]
• [green]↑/↓[/green] or [green]j/k[/green] - Move selection
• [green]Enter[/green] - Enter directory / Open file
• [green]Backspace[/green] - Parent directory
• [green]g[/green] - Go to directory
• [green]h[/green] - Toggle hidden files
• [green]r[/green] - Rename file/directory
• [green]d[/green] - Delete file/directory
• [green]n[/green] - New file/directory
• [green]c[/green] - Copy file/directory
• [green]m[/green] - Move file/directory
• [green]i[/green] - File/directory info
• [green]q[/green] - Quit
        """
        return Panel(help_text, title="Help", border_style="blue")
    
    def display_interface(self):
        """Display the main interface"""
        # Clear screen
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Create layout
        layout = Layout()
        layout.split_column(
            Layout(self.create_file_table(), name="files", ratio=3),
            Layout(self.create_help_panel(), name="help", size=20)
        )
        
        self.console.print(layout)
        
        # Status bar
        status_text = f"📁 {self.current_path} | 📊 {len(self.get_directory_contents())} items | "
        status_text += f"👁️ Hidden: {'On' if self.show_hidden else 'Off'}"
        
        status_panel = Panel(
            Align.center(Text(status_text, style="bold green")),
            border_style="green",
            padding=(0, 1)
        )
        self.console.print(status_panel)
    
    def navigate_to_directory(self, path_str):
        """Navigate to a specific directory"""
        try:
            new_path = Path(path_str).expanduser().resolve()
            if new_path.is_dir():
                self.current_path = new_path
                self.selected_index = 0
                return True
            else:
                self.console.print(f"[red]Error: '{path_str}' is not a directory[/red]")
                return False
        except Exception as e:
            self.console.print(f"[red]Error navigating to '{path_str}': {e}[/red]")
            return False
    
    def handle_enter(self):
        """Handle Enter key press"""
        items = self.get_directory_contents()
        if self.selected_index < len(items):
            item = items[self.selected_index]
            if item['is_dir']:
                self.current_path = item['path']
                self.selected_index = 0
            else:
                self.console.print(f"[yellow]Opening file: {item['path']}[/yellow]")
                try:
                    os.startfile(str(item['path']))  # Windows specific
                except:
                    self.console.print(f"[red]Could not open file: {item['path']}[/red]")
    
    def handle_parent_directory(self):
        """Go to parent directory"""
        parent = self.current_path.parent
        if parent != self.current_path:
            self.current_path = parent
            self.selected_index = 0
    
    def show_file_info(self):
        """Show detailed file information"""
        items = self.get_directory_contents()
        if self.selected_index < len(items):
            item = items[self.selected_index]
            path = item['path']
            
            try:
                stat_info = path.stat()
                
                info_table = Table(title=f"Information: {item['name']}", show_header=True, header_style="bold blue")
                info_table.add_column("Property", style="cyan")
                info_table.add_column("Value", style="green")
                
                info_table.add_row("Type", "Directory" if item['is_dir'] else "File")
                info_table.add_row("Size", item['size'])
                info_table.add_row("Modified", item['modified'])
                info_table.add_row("Created", datetime.fromtimestamp(stat_info.st_ctime).strftime('%Y-%m-%d %H:%M:%S'))
                info_table.add_row("Accessed", datetime.fromtimestamp(stat_info.st_atime).strftime('%Y-%m-%d %H:%M:%S'))
                info_table.add_row("Permissions", oct(stat_info.st_mode)[-3:])
                info_table.add_row("Full Path", str(path))
                
                self.console.print(info_table)
                input("\nPress Enter to continue...")
                
            except Exception as e:
                self.console.print(f"[red]Error getting file info: {e}[/red]")
                input("\nPress Enter to continue...")
    
    def create_new_item(self):
        """Create new file or directory"""
        choice = Prompt.ask("Create [F]ile or [D]irectory?", choices=["F", "D"], default="F")
        name = Prompt.ask("Enter name")
        
        if not name:
            self.console.print("[red]Name cannot be empty[/red]")
            return
        
        new_path = self.current_path / name
        
        try:
            if choice.upper() == "D":
                new_path.mkdir(exist_ok=False)
                self.console.print(f"[green]Directory '{name}' created successfully[/green]")
            else:
                new_path.touch(exist_ok=False)
                self.console.print(f"[green]File '{name}' created successfully[/green]")
        except FileExistsError:
            self.console.print(f"[red]'{name}' already exists[/red]")
        except Exception as e:
            self.console.print(f"[red]Error creating '{name}': {e}[/red]")
        
        time.sleep(1)
    
    def rename_item(self):
        """Rename selected item"""
        items = self.get_directory_contents()
        if self.selected_index < len(items):
            item = items[self.selected_index]
            old_name = item['name']
            
            new_name = Prompt.ask(f"Rename '{old_name}' to")
            if not new_name:
                return
            
            try:
                new_path = item['path'].parent / new_name
                item['path'].rename(new_path)
                self.console.print(f"[green]Renamed '{old_name}' to '{new_name}'[/green]")
            except Exception as e:
                self.console.print(f"[red]Error renaming: {e}[/red]")
            
            time.sleep(1)
    
    def delete_item(self):
        """Delete selected item"""
        items = self.get_directory_contents()
        if self.selected_index < len(items):
            item = items[self.selected_index]
            name = item['name']
            
            if Confirm.ask(f"Are you sure you want to delete '{name}'?"):
                try:
                    if item['is_dir']:
                        shutil.rmtree(item['path'])
                    else:
                        item['path'].unlink()
                    self.console.print(f"[green]Deleted '{name}'[/green]")
                    
                    # Adjust selection if necessary
                    if self.selected_index >= len(self.get_directory_contents()):
                        self.selected_index = max(0, self.selected_index - 1)
                        
                except Exception as e:
                    self.console.print(f"[red]Error deleting '{name}': {e}[/red]")
                
                time.sleep(1)
    
    def run(self):
        """Main run loop"""
        self.console.print("[bold green]🗂️  Interactive File Manager[/bold green]")
        self.console.print("[dim]Press 'q' to quit, 'h' for help[/dim]\n")
        time.sleep(2)
        
        while True:
            self.display_interface()
            
            try:
                choice = self.console.input("[bold cyan]Command:[/bold cyan] ").strip().lower()
                
                if choice == 'q':
                    break
                elif choice in ['j', '↓']:
                    items = self.get_directory_contents()
                    if self.selected_index < len(items) - 1:
                        self.selected_index += 1
                elif choice in ['k', '↑']:
                    if self.selected_index > 0:
                        self.selected_index -= 1
                elif choice == '':
                    self.handle_enter()
                elif choice == 'h':
                    self.show_hidden = not self.show_hidden
                elif choice == 'g':
                    path = Prompt.ask("Enter directory path", default=str(self.current_path))
                    self.navigate_to_directory(path)
                elif choice == 'i':
                    self.show_file_info()
                elif choice == 'n':
                    self.create_new_item()
                elif choice == 'r':
                    self.rename_item()
                elif choice == 'd':
                    self.delete_item()
                elif choice == 'backspace':
                    self.handle_parent_directory()
                else:
                    self.console.print(f"[red]Unknown command: {choice}[/red]")
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                break
            except EOFError:
                break
        
        self.console.print("\n[bold green]Goodbye![/bold green]")

def main():
    """Main function"""
    try:
        fm = FileManager()
        fm.run()
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

if __name__ == "__main__":
    main()
