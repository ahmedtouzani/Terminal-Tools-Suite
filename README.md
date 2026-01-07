# Terminal Tools Suite

A collection of beautiful terminal utilities with rich UI for system administration and monitoring.

**Created by Ahmed Touzani (R3D) - Parallel Universe Team**

## 🚀 Features

- **Rich Terminal Interface**: Beautiful, colorful, and intuitive terminal UI
- **Real-time Monitoring**: Live updates for system metrics
- **Interactive Controls**: Keyboard navigation and user-friendly commands
- **Comprehensive Tools**: All essential system utilities in one suite

## 🛠️ Included Tools

### 1. System Information (`system_info.py`)
- Display comprehensive system information
- CPU, memory, disk, and network details
- Live monitoring mode with real-time updates
- Beautiful formatted tables and progress bars

### 2. File Manager (`file_manager.py`)
- Interactive file browser with rich interface
- Navigate directories with keyboard controls
- File operations: create, rename, delete, copy, move
- File type icons and color coding
- Hidden files toggle

### 3. Process Monitor (`process_monitor.py`)
- Real-time process monitoring
- Sort by CPU, memory, name, or PID
- Kill processes safely
- System statistics dashboard
- Live monitoring mode

### 4. Network Utilities (`network_utils.py`)
- Network interface information
- Active connections viewer
- Port scanner
- Ping test utility
- Network speed test
- Live network monitoring

### 5. Main Launcher (`launcher.py`)
- Beautiful menu interface to access all tools
- Dependency checker and installer
- Tool status monitoring
- Interactive navigation

## 📦 Installation

### Prerequisites
- Python 3.7 or higher
- Windows, macOS, or Linux

### Install Dependencies
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install rich psutil
```

## 🎮 Usage

### Quick Start
Run the main launcher to access all tools:
```bash
python launcher.py
```

### Individual Tools
You can also run each tool individually:
```bash
python system_info.py      # System information
python file_manager.py      # File manager
python process_monitor.py   # Process monitor
python network_utils.py     # Network utilities
```

## 🎯 Controls

### System Information
- **1**: Display system information
- **2**: Live monitoring (30 seconds)
- **3**: Exit

### File Manager
- **↑/↓ or j/k**: Move selection
- **Enter**: Enter directory/Open file
- **Backspace**: Parent directory
- **g**: Go to directory
- **h**: Toggle hidden files
- **r**: Rename file/directory
- **d**: Delete file/directory
- **n**: New file/directory
- **c**: Copy file/directory
- **m**: Move file/directory
- **i**: File/directory info
- **q**: Quit

### Process Monitor
- **c**: Sort by CPU
- **m**: Sort by Memory
- **n**: Sort by Name
- **p**: Sort by PID
- **r**: Reverse sort order
- **f**: Filter by name
- **u**: Toggle user processes only
- **k**: Kill process
- **q**: Quit

### Network Utilities
- **1**: Network interfaces information
- **2**: Active connections
- **3**: Network I/O statistics
- **4**: Speed test
- **5**: Ping test
- **6**: Port scan
- **7**: Live monitoring (30 seconds)
- **8**: Exit

## 🎨 Features

### Rich UI Elements
- **Tables**: Beautiful formatted data tables
- **Progress Bars**: Visual progress indicators
- **Panels**: Organized information panels
- **Colors**: Intuitive color coding
- **Icons**: File type and status icons
- **Layouts**: Responsive terminal layouts

### Real-time Updates
- **Live Monitoring**: Real-time system metrics
- **Auto-refresh**: Automatic data updates
- **Interactive Controls**: Responsive keyboard navigation
- **Status Indicators**: Visual status feedback

## 🔧 System Requirements

- **Python**: 3.7+
- **Memory**: 512MB+ RAM
- **Storage**: 50MB free space
- **Terminal**: ANSI-compatible terminal emulator

## 📋 Dependencies

- **rich**: Terminal UI library for beautiful interfaces
- **psutil**: System and process utilities
- **Standard Library**: os, sys, subprocess, threading, etc.

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   pip install rich psutil
   ```

2. **Permission Errors**
   - Run as administrator for full system access
   - Some features may require elevated privileges

3. **Terminal Compatibility**
   - Ensure your terminal supports ANSI colors
   - Windows: Use Windows Terminal or PowerShell
   - macOS: Use Terminal.app or iTerm2
   - Linux: Most modern terminals work fine

4. **Performance Issues**
   - Close unnecessary applications
   - Reduce refresh rate in live monitoring
   - Limit the number of processes displayed

## 🤝 Contributing

Created with ❤️ by Ahmed Touzani (R3D) from the Parallel Universe team.

Feel free to modify, improve, or extend these tools. The code is designed to be:
- **Modular**: Easy to add new features
- **Readable**: Clear code structure and comments
- **Extensible**: Simple to add new tools

## 📄 License

Created by Ahmed Touzani (R3D) - Parallel Universe Team.
Open Source - Feel free to modify and distribute.

## 🙏 Acknowledgments

- **Rich**: For the amazing terminal UI library
- **psutil**: For comprehensive system utilities
- **Python Community**: For the excellent ecosystem

---

**Created with passion by Ahmed Touzani (R3D) - Parallel Universe Team 🚀**
