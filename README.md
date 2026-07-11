# log-viewer-cli

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)]()
[![PyPI Version](https://img.shields.io/badge/PyPI-v1.0.0-orange)](https://pypi.org/project/log-viewer-cli/)
[![Downloads](https://img.shields.io/badge/downloads-10K+-blue)]()

A powerful, fast, and feature-rich terminal-based log file viewer with real-time filtering, syntax highlighting, and advanced search capabilities.

## Features

- Real-time log streaming and monitoring
- Advanced filtering with regex support
- Syntax highlighting for log levels (ERROR, WARN, INFO, DEBUG)
- Multiple color themes (dark, light, solarized, monokai)
- Bookmark and annotate log entries
- Export filtered results to file
- Follow mode for tail -f functionality
- Multi-file log viewing
- Pattern-based auto-scrolling
- Keyboard shortcuts for navigation

## Architecture

```
log-viewer-cli/
├── src/
│   ├── viewer/          # Core log viewing engine
│   │   ├── __init__.py
│   │   ├── engine.py    # Main viewing engine
│   │   ├── buffer.py    # Log buffer management
│   │   └── display.py   # Terminal rendering
│   ├── parsers/         # Log format parsers
│   │   ├── __init__.py
│   │   ├── base.py      # Base parser interface
│   │   ├── syslog.py    # Syslog parser
│   │   ├── json.py      # JSON log parser
│   │   ├── apache.py    # Apache/Nginx log parser
│   │   └── custom.py    # Custom format parser
│   ├── filters/         # Filter system
│   │   ├── __init__.py
│   │   ├── base.py      # Base filter interface
│   │   ├── text.py      # Text-based filters
│   │   ├── regex.py     # Regex filters
│   │   ├── level.py     # Log level filters
│   │   └── time.py      # Time range filters
│   └── highlighters/    # Syntax highlighting
│       ├── __init__.py
│       ├── base.py      # Base highlighter
│       ├── log_level.py # Log level highlighting
│       ├── timestamp.py # Timestamp highlighting
│       └── patterns.py  # Pattern highlighting
├── cli.py               # CLI entry point
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── setup.py
├── .gitignore
└── README.md
```

## Installation

### From PyPI

```bash
pip install log-viewer-cli
```

### From Source

```bash
git clone https://github.com/janderik/log-viewer-cli.git
cd log-viewer-cli
pip install -e .
```

### Using Docker

```bash
docker pull janderik/log-viewer-cli:latest
docker run -v /var/log:/logs janderik/log-viewer-cli /logs/syslog
```

## Usage

### Basic Usage

```bash
# View a log file
logview /var/log/syslog

# Follow a log file (like tail -f)
logview -f /var/log/app.log

# View multiple log files
logview /var/log/app.log /var/log/error.log
```

### Filtering

```bash
# Filter by text
logview /var/log/app.log --filter "ERROR"

# Filter by regex
logview /var/log/app.log --regex "timeout|connection refused"

# Filter by log level
logview /var/log/app.log --level ERROR,WARN

# Filter by time range
logview /var/log/app.log --since "2024-01-01 10:00" --until "2024-01-01 11:00"

# Combine filters
logview /var/log/app.log --level ERROR --since "1 hour ago" --grep "database"
```

### Filter Syntax

```
# Basic text matching
ERROR
WARN

# Regex patterns
\d{4}-\d{2}-\d{2}
timeout|refused

# Level filters
level:ERROR
level:ERROR,WARN
!level:DEBUG

# Time filters
time:today
time:yesterday
time:2024-01-01
time:1h (last hour)
time:30m (last 30 minutes)

# Field filters (for JSON logs)
field:status:500
field:method:POST
!field:user:admin

# Compound filters
level:ERROR AND time:today
ERROR OR WARN
ERROR AND NOT time:yesterday
```

### Color Themes

```bash
# List available themes
logview --list-themes

# Use a specific theme
logview --theme monokai /var/log/app.log

# Custom theme
logview --theme custom --config ~/.config/logview/themes.yaml
```

### Export

```bash
# Export filtered results
logview /var/log/app.log --level ERROR --export errors.txt

# Export as JSON
logview /var/log/app.log --format json --export errors.json

# Export with context
logview /var/log/app.log --level ERROR --context 3 --export context.txt
```

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `↑/↓` | Scroll up/down |
| `PgUp/PgDn` | Page up/down |
| `Home/End` | Jump to start/end |
| `Space` | Pause/Resume follow |
| `/` | Open search |
| `n/N` | Next/Previous match |
| `b` | Bookmark current line |
| `e` | Export view |
| `t` | Cycle themes |
| `q` | Quit |

## Configuration

Create `~/.config/logview/config.yaml`:

```yaml
theme: monokai
follow: true
buffer_size: 10000
highlight:
  - pattern: "ERROR|CRITICAL"
    color: red
    bold: true
  - pattern: "WARNING|WARN"
    color: yellow
  - pattern: "SUCCESS|OK"
    color: green
filters:
  default_level: INFO
  exclude_patterns:
    - "healthcheck"
    - "ping"
keybindings:
  quit: q
  search: /
  bookmark: b
```

## Supported Log Formats

| Format | Parser | Example |
|--------|--------|---------|
| Syslog | syslog | `Jan 1 12:00:00 host service[pid]: message` |
| JSON | json | `{"timestamp":"...","level":"ERROR","message":"..."}` |
| Apache | apache | `127.0.0.1 - - [01/Jan/2024:12:00:00] "GET / HTTP/1.1" 200` |
| Nginx | nginx | Same as Apache combined format |
| Custom | custom | Configurable regex pattern |
| CSV | csv | Comma-separated values with headers |

## Performance

- Handles files up to 10GB efficiently
- Memory-mapped file reading for large files
- Streaming mode for real-time monitoring
- Lazy loading for backward navigation
- Indexed searching for fast pattern matching

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
git clone https://github.com/janderik/log-viewer-cli.git
cd log-viewer-cli
pip install -e ".[dev]"
pytest
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with Python's curses library for terminal UI
- Inspired by `lnav`, `less`, and `htop`
- Thanks to all contributors
