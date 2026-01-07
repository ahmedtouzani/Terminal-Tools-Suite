#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main Launcher for Terminal Tools
A beautiful launcher to access all terminal utilities

Created by Ahmed Touzani (R3D) - Parallel Universe Team
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.layout import Layout
from rich.columns import Columns
from rich import box
from rich.prompt import Prompt, Confirm

# Set UTF-8 encoding for Windows
if sys.platform == "win32":
    import locale
    os.system('chcp 65001 >nul')

console = Console()

class ToolLauncher:
    def __init__(self):
        self.console = Console()
        self.tools_dir = Path(__file__).parent
        self.tools = {
            "1": {
                "name": "System Information",
                "description": "Display comprehensive system information with beautiful UI",
                "file": "system_info.py",
                "icon": "[PC]",
                "color": "blue"
            },
            "2": {
                "name": "File Manager",
                "description": "Interactive file manager with rich interface",
                "file": "file_manager.py",
                "icon": "[FM]",
                "color": "green"
            },
            "3": {
                "name": "Process Monitor",
                "description": "Monitor system processes with real-time updates",
                "file": "process_monitor.py",
                "icon": "[PM]",
                "color": "red"
            },
            "4": {
                "name": "Network Utilities",
                "description": "Network tools including speed test and port scanner",
                "file": "network_utils.py",
                "icon": "[NT]",
                "color": "cyan"
            },
            "5": {
                "name": "Install Dependencies",
                "description": "Install required Python packages",
                "file": None,
                "icon": "[IN]",
                "color": "yellow"
            },
            "6": {
                "name": "About",
                "description": "Information about these tools",
                "file": None,
                "icon": "[AB]",
                "color": "magenta"
            }
        }
    
    def create_main_table(self):
        """Create the main tools selection table"""
        table = Table(title="Terminal Tools Suite", show_header=True, header_style="bold blue")
        table.add_column("Choice", style="cyan", width=6)
        table.add_column("Tool", style="bold", width=20)
        table.add_column("Description", style="white", width=30)
        table.add_column("Status", style="green", width=10)
        
        for choice, tool in self.tools.items():
            if tool["file"]:
                file_path = self.tools_dir / tool["file"]
                status = "[OK]" if file_path.exists() else "[XX]"
                status_style = "green" if file_path.exists() else "red"
            else:
                status = "[IN]"
                status_style = "yellow"
            
            tool_name = f"[{tool['color']}]{tool['icon']} {tool['name']}[/{tool['color']}]"
            
            table.add_row(
                choice,
                tool_name,
                tool["description"],
                f"[{status_style}]{status}[/{status_style}]"
            )
        
        return table
    
    def create_info_panel(self):
        """Create information panel"""
        info_text = """
[bold cyan]Welcome to Terminal Tools Suite![/bold cyan]

This collection of terminal utilities provides beautiful, interactive interfaces for common system administration tasks.

[bold yellow]Features:[/bold yellow]
• Rich, colorful terminal interfaces
• Real-time monitoring capabilities
• Interactive controls and navigation
• Comprehensive system information
• Network utilities and diagnostics

[bold green]Requirements:[/bold green]
• Python 3.7+
• Rich library for terminal UI
• psutil for system information
        """
        
        return Panel(info_text.strip(), title="Information", border_style="blue")
    
    def install_dependencies(self):
        """Install required dependencies"""
        self.console.print("[bold green]Installing Dependencies[/bold green]\n")
        
        dependencies = [
            "rich",
            "psutil"
        ]
        
        for dep in dependencies:
            try:
                __import__(dep)
                self.console.print(f"[OK] {dep} is already installed")
            except ImportError:
                self.console.print(f"[IN] Installing {dep}...")
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
                    self.console.print(f"[OK] {dep} installed successfully")
                except subprocess.CalledProcessError:
                    self.console.print(f"[XX] Failed to install {dep}")
                    return False
        
        self.console.print("\n[bold green]All dependencies installed successfully![/bold green]")
        input("\nPress Enter to continue...")
        return True
    
    def show_about(self):
        """Show about information"""
        about_text = """
[bold blue]Terminal Tools Suite v1.0[/bold blue]

[bold cyan]Created by:[/bold cyan] Ahmed Touzani (R3D)
[bold cyan]Team:[/bold cyan] Parallel Universe
[bold cyan]Description:[/bold cyan] A collection of beautiful terminal utilities with rich UI

[bold yellow]Included Tools:[/bold yellow]
[PC] System Information - Comprehensive system details
[FM] File Manager - Interactive file browser
[PM] Process Monitor - Real-time process monitoring
[NT] Network Utilities - Network diagnostics and tools

[bold green]Technologies Used:[/bold green]
• Python 3.7+
• Rich - Terminal UI library
• psutil - System and process utilities
• Standard library modules

[bold magenta]License:[/bold magenta] Created by Ahmed Touzani (R3D) - Parallel Universe Team
[bold red]Support:[/bold red] Created with passion by Parallel Universe team
        """
        
        about_panel = Panel(about_text.strip(), title="About Terminal Tools Suite", border_style="blue")
        self.console.print(about_panel)
        input("\nPress Enter to continue...")
    
    def run_tool(self, tool_key):
        """Run a specific tool"""
        tool = self.tools.get(tool_key)
        if not tool:
            self.console.print("[red]Invalid tool selection![/red]")
            return
        
        if tool_key == "5":
            self.install_dependencies()
            return
        
        if tool_key == "6":
            self.show_about()
            return
        
        if not tool["file"]:
            self.console.print("[red]Tool file not specified![/red]")
            return
        
        tool_path = self.tools_dir / tool["file"]
        
        if not tool_path.exists():
            self.console.print(f"[red]Tool file not found: {tool_path}[/red]")
            return
        
        try:
            self.console.print(f"[bold green]Launching {tool['name']}...[/bold green]")
            self.console.print("[dim]Press Ctrl+C to return to launcher[/dim]\n")
            
            # Run the tool in a subprocess
            subprocess.run([sys.executable, str(tool_path)], check=True)
            
        except subprocess.CalledProcessError as e:
            self.console.print(f"[red]Error running tool: {e}[/red]")
        except KeyboardInterrupt:
            self.console.print(f"\n[yellow]Returning to launcher...[/yellow]")
        except Exception as e:
            self.console.print(f"[red]Unexpected error: {e}[/red]")
        
        input("\nPress Enter to continue...")
    
    def check_dependencies(self):
        """Check if all dependencies are installed"""
        missing_deps = []
        dependencies = ["rich", "psutil"]
        
        for dep in dependencies:
            try:
                __import__(dep)
            except ImportError:
                missing_deps.append(dep)
        
        if missing_deps:
            warning_text = f"[yellow][!] Missing dependencies: {', '.join(missing_deps)}[/yellow]\n"
            warning_text += "[dim]Please install dependencies using option 5 or run:[/dim]\n"
            warning_text += "[cyan]pip install rich psutil[/cyan]"
            
            warning_panel = Panel(warning_text, title="Dependencies Warning", border_style="yellow")
            self.console.print(warning_panel)
            return False
        
        return True
    
    def run(self):
        """Main launcher loop"""
        while True:
            # Clear screen
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # Display title
            self.console.print("[bold blue]Terminal Tools Suite[/bold blue]")
            self.console.print("[dim]Created by Ahmed Touzani (R3D) - Parallel Universe Team[/dim]")
            self.console.print("[dim]A suite of powerful terminal-based tools.[/dim]\n")
            
            # Display table
            table = self.create_main_table()
            self.console.print(table)
            
            # Check dependencies
            deps_ok = self.check_dependencies()
            
            # Footer
            footer_text = "Enter your choice (1-6) or 'q' to quit"
            if not deps_ok:
                footer_text += " | [!] Missing dependencies"
            
            self.console.print(f"\n[bold green]{footer_text}[/bold green]")
            
            # Get user input
            try:
                choice = self.console.input("\n[bold cyan]Your choice:[/bold cyan] ").strip().lower()
                
                if choice == 'q':
                    break
                elif choice in self.tools:
                    self.run_tool(choice)
                else:
                    self.console.print("[red]Invalid choice! Please enter 1-6 or 'q' to quit.[/red]")
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                break
            except EOFError:
                break
        
        self.console.print("\n[bold green]Thank you for using Terminal Tools Suite![/bold green]")
        self.console.print("[dim]Created with passion by Ahmed Touzani (R3D) - Parallel Universe Team[/dim]")
        self.console.print("[dim]Goodbye![/dim]")

def main():
    """Main function"""
    try:
        launcher = ToolLauncher()
        launcher.run()
    except Exception as e:
        console.print(f"[red]Fatal error: {e}[/red]")

if __name__ == "__main__":
    main()
