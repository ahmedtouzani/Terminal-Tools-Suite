#!/usr/bin/env python3
"""
System Information Tool with Rich UI
Displays comprehensive system information with beautiful terminal interface

Created by Ahmed Touzani (R3D) - Parallel Universe Team
"""

import platform
import psutil
import os
import time
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich.align import Align
from rich.columns import Columns

console = Console()

class SystemInfoTool:
    def __init__(self):
        self.console = Console()
        
    def get_basic_info(self):
        """Get basic system information"""
        return {
            "System": platform.system(),
            "Node Name": platform.node(),
            "Release": platform.release(),
            "Version": platform.version(),
            "Machine": platform.machine(),
            "Processor": platform.processor(),
            "Python Version": platform.python_version(),
        }
    
    def get_cpu_info(self):
        """Get CPU information"""
        cpu_freq = psutil.cpu_freq()
        cpu_percent = psutil.cpu_percent(interval=1)
        
        return {
            "Physical Cores": psutil.cpu_count(logical=False),
            "Total Cores": psutil.cpu_count(logical=True),
            "Max Frequency": f"{cpu_freq.max:.2f}Mhz" if cpu_freq else "Unknown",
            "Min Frequency": f"{cpu_freq.min:.2f}Mhz" if cpu_freq else "Unknown",
            "Current Frequency": f"{cpu_freq.current:.2f}Mhz" if cpu_freq else "Unknown",
            "CPU Usage": f"{cpu_percent}%",
        }
    
    def get_memory_info(self):
        """Get memory information"""
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        return {
            "Total": f"{memory.total / (1024**3):.2f} GB",
            "Available": f"{memory.available / (1024**3):.2f} GB",
            "Used": f"{memory.used / (1024**3):.2f} GB",
            "Percentage": f"{memory.percent}%",
            "Swap Total": f"{swap.total / (1024**3):.2f} GB",
            "Swap Used": f"{swap.used / (1024**3):.2f} GB",
            "Swap Free": f"{swap.free / (1024**3):.2f} GB",
        }
    
    def get_disk_info(self):
        """Get disk information"""
        disk_partitions = psutil.disk_partitions()
        disk_info = []
        
        for partition in disk_partitions:
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
                disk_info.append({
                    "Device": partition.device,
                    "Mountpoint": partition.mountpoint,
                    "File System": partition.fstype,
                    "Total Size": f"{partition_usage.total / (1024**3):.2f} GB",
                    "Used": f"{partition_usage.used / (1024**3):.2f} GB",
                    "Free": f"{partition_usage.free / (1024**3):.2f} GB",
                    "Percentage": f"{partition_usage.percent}%",
                })
            except PermissionError:
                continue
        
        return disk_info
    
    def get_network_info(self):
        """Get network information"""
        net_io = psutil.net_io_counters()
        net_if_addrs = psutil.net_if_addrs()
        
        interfaces = []
        for interface_name, addresses in net_if_addrs.items():
            for addr in addresses:
                if addr.family.name in ['AF_INET', 'AF_INET6']:
                    interfaces.append(f"{interface_name}: {addr.address}")
        
        return {
            "Bytes Sent": f"{net_io.bytes_sent / (1024**2):.2f} MB",
            "Bytes Received": f"{net_io.bytes_recv / (1024**2):.2f} MB",
            "Packets Sent": f"{net_io.packets_sent:,}",
            "Packets Received": f"{net_io.packets_recv:,}",
            "Interfaces": "\n".join(interfaces[:5])  # Show first 5 interfaces
        }
    
    def create_table(self, title, data):
        """Create a rich table"""
        table = Table(title=title, show_header=True, header_style="bold magenta")
        table.add_column("Property", style="cyan", width=20)
        table.add_column("Value", style="green")
        
        for key, value in data.items():
            table.add_row(key, str(value))
        
        return table
    
    def create_disk_table(self, disk_data):
        """Create disk information table"""
        table = Table(title="Disk Information", show_header=True, header_style="bold magenta")
        table.add_column("Device", style="cyan")
        table.add_column("Mount", style="blue")
        table.add_column("FS Type", style="yellow")
        table.add_column("Total", style="green")
        table.add_column("Used", style="red")
        table.add_column("Free", style="green")
        table.add_column("Usage", style="magenta")
        
        for disk in disk_data:
            table.add_row(
                disk["Device"],
                disk["Mountpoint"],
                disk["File System"],
                disk["Total Size"],
                disk["Used"],
                disk["Free"],
                disk["Percentage"]
            )
        
        return table
    
    def display_system_info(self):
        """Display all system information"""
        # Show loading animation
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task("Gathering system information...", total=None)
            
            basic_info = self.get_basic_info()
            cpu_info = self.get_cpu_info()
            memory_info = self.get_memory_info()
            disk_info = self.get_disk_info()
            network_info = self.get_network_info()
            
            progress.update(task, description="Rendering interface...")
            time.sleep(0.5)
        
        # Create title
        title = Panel(
            Align.center(Text("🖥️  SYSTEM INFORMATION DASHBOARD 🖥️", style="bold blue")),
            border_style="blue",
            padding=(1, 2)
        )
        
        # Create tables
        basic_table = self.create_table("Basic Information", basic_info)
        cpu_table = self.create_table("CPU Information", cpu_info)
        memory_table = self.create_table("Memory Information", memory_info)
        disk_table = self.create_disk_table(disk_info)
        network_table = self.create_table("Network Information", network_info)
        
        # Display everything
        self.console.print(title)
        self.console.print("\n")
        
        # Create columns layout
        layout = Layout()
        layout.split_column(
            Layout(basic_table, name="basic", size=8),
            Layout(Columns([cpu_table, memory_table]), name="cpu_mem", size=12),
            Layout(disk_table, name="disk", size=8),
            Layout(network_table, name="network", size=10)
        )
        
        self.console.print(layout)
        
        # Footer
        footer = Panel(
            Align.center(
                Text(f"Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                     style="dim")
            ),
            border_style="dim",
            padding=(0, 2)
        )
        self.console.print(footer)
    
    def run_live_monitor(self, duration=30):
        """Run live system monitoring"""
        console.print("[bold green]Starting live system monitoring...[/bold green]")
        console.print(f"[dim]Monitoring for {duration} seconds. Press Ctrl+C to exit.[/dim]\n")
        
        start_time = time.time()
        
        def generate_layout():
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            
            cpu_color = "green" if cpu_percent < 50 else "yellow" if cpu_percent < 80 else "red"
            mem_color = "green" if memory.percent < 50 else "yellow" if memory.percent < 80 else "red"
            
            cpu_text = Text(f"CPU: {cpu_percent}%", style=f"bold {cpu_color}")
            mem_text = Text(f"Memory: {memory.percent}%", style=f"bold {mem_color}")
            
            elapsed = int(time.time() - start_time)
            time_text = Text(f"Time: {elapsed}s", style="dim")
            
            panel = Panel(
                Columns([cpu_text, mem_text, time_text], equal=True, expand=True),
                title="Live System Monitor",
                border_style="blue"
            )
            
            return panel
        
        try:
            with Live(generate_layout(), refresh_per_second=2, console=console) as live:
                while time.time() - start_time < duration:
                    live.update(generate_layout())
                    time.sleep(0.5)
        except KeyboardInterrupt:
            console.print("\n[yellow]Monitoring stopped by user.[/yellow]")

def main():
    """Main function"""
    tool = SystemInfoTool()
    
    console.print("[bold cyan]System Information Tool[/bold cyan]")
    console.print("[dim]Choose an option:[/dim]\n")
    console.print("1. Display system information")
    console.print("2. Live monitoring (30 seconds)")
    console.print("3. Exit\n")
    
    try:
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == "1":
            tool.display_system_info()
        elif choice == "2":
            tool.run_live_monitor()
        elif choice == "3":
            console.print("[yellow]Goodbye![/yellow]")
        else:
            console.print("[red]Invalid choice![/red]")
    except KeyboardInterrupt:
        console.print("\n[yellow]Goodbye![/yellow]")

if __name__ == "__main__":
    main()
