#!/usr/bin/env python3
"""
Process Monitor with Real-time Updates
Monitor system processes with beautiful UI and real-time updates

Created by Ahmed Touzani (R3D) - Parallel Universe Team
"""

import psutil
import time
import os
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich.align import Align
from rich.columns import Columns
from rich.progress import Progress, BarColumn, TextColumn
from rich import box

console = Console()

class ProcessMonitor:
    def __init__(self):
        self.console = Console()
        self.sort_by = 'cpu'  # cpu, memory, name, pid
        self.sort_reverse = True
        self.filter_name = ""
        self.show_only_user = False
        
    def get_processes(self, limit=20):
        """Get list of processes with their information"""
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'memory_info', 'status']):
            try:
                proc_info = proc.info
                
                # Apply filters
                if self.filter_name and self.filter_name.lower() not in proc_info['name'].lower():
                    continue
                    
                if self.show_only_user and proc_info['username']:
                    username = proc_info['username']
                    current_user = os.getlogin() if hasattr(os, 'getlogin') else ""
                    if current_user not in username:
                        continue
                
                # Format memory info
                memory_mb = 0
                if proc_info['memory_info']:
                    memory_mb = proc_info['memory_info'].rss / (1024 * 1024)
                
                processes.append({
                    'pid': proc_info['pid'],
                    'name': proc_info['name'],
                    'username': proc_info['username'] or 'N/A',
                    'cpu_percent': proc_info['cpu_percent'] or 0,
                    'memory_percent': proc_info['memory_percent'] or 0,
                    'memory_mb': memory_mb,
                    'status': proc_info['status'] or 'Unknown'
                })
                
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        # Sort processes
        reverse_map = {'cpu': 'cpu_percent', 'memory': 'memory_mb', 'name': 'name', 'pid': 'pid'}
        sort_key = reverse_map.get(self.sort_by, 'cpu_percent')
        
        processes.sort(key=lambda x: x[sort_key], reverse=self.sort_reverse)
        
        return processes[:limit]
    
    def get_system_stats(self):
        """Get overall system statistics"""
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'memory_used_gb': memory.used / (1024**3),
            'memory_total_gb': memory.total / (1024**3),
            'disk_percent': disk.percent,
            'disk_used_gb': disk.used / (1024**3),
            'disk_total_gb': disk.total / (1024**3),
            'process_count': len(psutil.pids()),
            'boot_time': datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def create_process_table(self, processes):
        """Create process table"""
        table = Table(title="🔍 Running Processes", show_header=True, header_style="bold blue", box=box.ROUNDED)
        table.add_column("PID", style="cyan", width=8)
        table.add_column("Name", style="green", min_width=15)
        table.add_column("User", style="yellow", width=15)
        table.add_column("CPU %", style="red", width=8)
        table.add_column("Memory %", style="magenta", width=10)
        table.add_column("Memory (MB)", style="blue", width=12)
        table.add_column("Status", style="white", width=10)
        
        for proc in processes:
            # Color coding for CPU and memory usage
            cpu_color = "green" if proc['cpu_percent'] < 10 else "yellow" if proc['cpu_percent'] < 50 else "red"
            mem_color = "green" if proc['memory_percent'] < 10 else "yellow" if proc['memory_percent'] < 50 else "red"
            
            # Status color
            status_color = {
                'running': 'green',
                'sleeping': 'blue',
                'disk sleep': 'yellow',
                'stopped': 'red',
                'zombie': 'red',
                'dead': 'red'
            }.get(proc['status'].lower(), 'white')
            
            table.add_row(
                str(proc['pid']),
                proc['name'][:20] + "..." if len(proc['name']) > 20 else proc['name'],
                proc['username'].split('\\')[-1] if '\\' in proc['username'] else proc['username'],
                f"[{cpu_color}]{proc['cpu_percent']:.1f}[/{cpu_color}]",
                f"[{mem_color}]{proc['memory_percent']:.1f}[/{mem_color}]",
                f"{proc['memory_mb']:.1f}",
                f"[{status_color}]{proc['status']}[/{status_color}]"
            )
        
        return table
    
    def create_stats_panel(self, stats):
        """Create system statistics panel"""
        # CPU progress bar
        cpu_color = "green" if stats['cpu_percent'] < 50 else "yellow" if stats['cpu_percent'] < 80 else "red"
        cpu_progress = f"[{cpu_color}]{'█' * int(stats['cpu_percent'] / 5)}{'░' * (20 - int(stats['cpu_percent'] / 5))}[/{cpu_color}]"
        
        # Memory progress bar
        mem_color = "green" if stats['memory_percent'] < 50 else "yellow" if stats['memory_percent'] < 80 else "red"
        mem_progress = f"[{mem_color}]{'█' * int(stats['memory_percent'] / 5)}{'░' * (20 - int(stats['memory_percent'] / 5))}[/{mem_color}]"
        
        # Disk progress bar
        disk_color = "green" if stats['disk_percent'] < 50 else "yellow" if stats['disk_percent'] < 80 else "red"
        disk_progress = f"[{disk_color}]{'█' * int(stats['disk_percent'] / 5)}{'░' * (20 - int(stats['disk_percent'] / 5))}[/{disk_color}]"
        
        stats_text = f"""
[bold cyan]System Statistics[/bold cyan]

🖥️  CPU:     {cpu_progress} {stats['cpu_percent']:.1f}%
🧠 Memory:  {mem_progress} {stats['memory_percent']:.1f}% ({stats['memory_used_gb']:.1f}/{stats['memory_total_gb']:.1f} GB)
💾 Disk:    {disk_progress} {stats['disk_percent']:.1f}% ({stats['disk_used_gb']:.1f}/{stats['disk_total_gb']:.1f} GB)

📊 Processes: {stats['process_count']}
⏰ Uptime:    {stats['boot_time']}
        """
        
        return Panel(stats_text.strip(), title="📈 System Overview", border_style="blue")
    
    def create_controls_panel(self):
        """Create controls help panel"""
        controls_text = """
[bold cyan]Controls:[/bold cyan]
• [green]c[/green] - Sort by CPU
• [green]m[/green] - Sort by Memory  
• [green]n[/green] - Sort by Name
• [green]p[/green] - Sort by PID
• [green]r[/green] - Reverse sort order
• [green]f[/green] - Filter by name
• [green]u[/green] - Toggle user processes only
• [green]k[/green] - Kill process
• [green]q[/green] - Quit
        """
        
        return Panel(controls_text.strip(), title="🎮 Controls", border_style="green")
    
    def kill_process(self):
        """Kill a process by PID"""
        try:
            pid = int(input("Enter PID to kill: "))
            proc = psutil.Process(pid)
            
            # Show process info
            self.console.print(f"[yellow]Process: {proc.name()} (PID: {pid})[/yellow]")
            
            if Confirm.ask("Are you sure you want to kill this process?"):
                proc.terminate()
                self.console.print(f"[green]Process {pid} terminated[/green]")
                time.sleep(1)
            else:
                self.console.print("[yellow]Operation cancelled[/yellow]")
                
        except ValueError:
            self.console.print("[red]Invalid PID[/red]")
        except psutil.NoSuchProcess:
            self.console.print(f"[red]Process {pid} not found[/red]")
        except psutil.AccessDenied:
            self.console.print(f"[red]Access denied to kill process {pid}[/red]")
        except Exception as e:
            self.console.print(f"[red]Error killing process: {e}[/red]")
    
    def filter_processes(self):
        """Filter processes by name"""
        self.filter_name = input("Enter filter (empty to clear): ").strip()
        if self.filter_name:
            self.console.print(f"[green]Filtering by: {self.filter_name}[/green]")
        else:
            self.console.print("[green]Filter cleared[/green]")
        time.sleep(1)
    
    def run_interactive(self):
        """Run interactive process monitor"""
        self.console.print("[bold green]🔍 Process Monitor[/bold green]")
        self.console.print("[dim]Press 'q' to quit, 'h' for controls[/dim]\n")
        time.sleep(1)
        
        while True:
            try:
                # Clear screen
                os.system('cls' if os.name == 'nt' else 'clear')
                
                # Get data
                processes = self.get_processes()
                stats = self.get_system_stats()
                
                # Create layout
                layout = Layout()
                layout.split_column(
                    Layout(Columns([
                        self.create_stats_panel(stats),
                        self.create_controls_panel()
                    ]), name="stats", size=16),
                    Layout(self.create_process_table(processes), name="processes", ratio=2)
                )
                
                self.console.print(layout)
                
                # Status bar
                sort_text = f"Sort: {self.sort_by} ({'↓' if self.sort_reverse else '↑'})"
                filter_text = f"Filter: {self.filter_name or 'None'}"
                user_text = f"User only: {'Yes' if self.show_only_user else 'No'}"
                
                status_text = f"📊 {sort_text} | 🔍 {filter_text} | 👤 {user_text}"
                
                status_panel = Panel(
                    Align.center(Text(status_text, style="bold green")),
                    border_style="green",
                    padding=(0, 1)
                )
                self.console.print(status_panel)
                
                # Get input
                choice = self.console.input("[bold cyan]Command:[/bold cyan] ").strip().lower()
                
                if choice == 'q':
                    break
                elif choice == 'c':
                    self.sort_by = 'cpu'
                    self.sort_reverse = True
                elif choice == 'm':
                    self.sort_by = 'memory'
                    self.sort_reverse = True
                elif choice == 'n':
                    self.sort_by = 'name'
                    self.sort_reverse = False
                elif choice == 'p':
                    self.sort_by = 'pid'
                    self.sort_reverse = False
                elif choice == 'r':
                    self.sort_reverse = not self.sort_reverse
                elif choice == 'f':
                    self.filter_processes()
                elif choice == 'u':
                    self.show_only_user = not self.show_only_user
                    self.console.print(f"[green]User processes only: {'On' if self.show_only_user else 'Off'}[/green]")
                    time.sleep(1)
                elif choice == 'k':
                    self.kill_process()
                else:
                    self.console.print(f"[red]Unknown command: {choice}[/red]")
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                break
            except EOFError:
                break
        
        self.console.print("\n[bold green]Goodbye![/bold green]")
    
    def run_live(self, duration=60):
        """Run live monitoring mode"""
        self.console.print(f"[bold green]🔍 Live Process Monitor[/bold green]")
        self.console.print(f"[dim]Monitoring for {duration} seconds. Press Ctrl+C to exit.[/dim]\n")
        
        start_time = time.time()
        
        def generate_layout():
            processes = self.get_processes(10)  # Show top 10 in live mode
            stats = self.get_system_stats()
            
            # Create compact layout for live mode
            process_table = Table(show_header=True, header_style="bold blue", box=box.MINIMAL)
            process_table.add_column("PID", style="cyan", width=6)
            process_table.add_column("Name", style="green", width=15)
            process_table.add_column("CPU%", style="red", width=6)
            process_table.add_column("MEM%", style="magenta", width=6)
            process_table.add_column("MEM(MB)", style="blue", width=8)
            
            for proc in processes:
                cpu_color = "green" if proc['cpu_percent'] < 10 else "yellow" if proc['cpu_percent'] < 50 else "red"
                mem_color = "green" if proc['memory_percent'] < 10 else "yellow" if proc['memory_percent'] < 50 else "red"
                
                process_table.add_row(
                    str(proc['pid']),
                    proc['name'][:12] + "..." if len(proc['name']) > 12 else proc['name'],
                    f"[{cpu_color}]{proc['cpu_percent']:.1f}[/{cpu_color}]",
                    f"[{mem_color}]{proc['memory_percent']:.1f}[/{mem_color}]",
                    f"{proc['memory_mb']:.0f}"
                )
            
            # System stats
            elapsed = int(time.time() - start_time)
            stats_text = f"CPU: {stats['cpu_percent']:.1f}% | MEM: {stats['memory_percent']:.1f}% | PROC: {stats['process_count']} | TIME: {elapsed}s"
            
            layout = Layout()
            layout.split_column(
                Layout(Panel(stats_text, title="System Stats", border_style="blue"), name="stats", size=3),
                Layout(process_table, name="processes")
            )
            
            return layout
        
        try:
            with Live(generate_layout(), refresh_per_second=2, console=console) as live:
                while time.time() - start_time < duration:
                    live.update(generate_layout())
                    time.sleep(0.5)
        except KeyboardInterrupt:
            console.print("\n[yellow]Live monitoring stopped by user.[/yellow]")

def main():
    """Main function"""
    console.print("[bold cyan]Process Monitor[/bold cyan]")
    console.print("[dim]Choose mode:[/dim]\n")
    console.print("1. Interactive mode")
    console.print("2. Live monitoring (60 seconds)")
    console.print("3. Exit\n")
    
    try:
        choice = input("Enter your choice (1-3): ").strip()
        
        monitor = ProcessMonitor()
        
        if choice == "1":
            monitor.run_interactive()
        elif choice == "2":
            monitor.run_live()
        elif choice == "3":
            console.print("[yellow]Goodbye![/yellow]")
        else:
            console.print("[red]Invalid choice![/red]")
    except KeyboardInterrupt:
        console.print("\n[yellow]Goodbye![/yellow]")

if __name__ == "__main__":
    main()
