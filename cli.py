#!/usr/bin/env python3
"""Command-line interface for log-viewer-cli."""
import argparse
import sys
from src.viewer.engine import LogViewer
from src.parsers.syslog import SyslogParser
from src.parsers.json_parser import JsonParser
from src.parsers.apache import ApacheParser
from src.parsers.custom import CustomParser
from src.filters.text import TextFilter
from src.filters.regex import RegexFilter
from src.filters.level import LevelFilter
from src.filters.time import TimeFilter
from src.highlighters.log_level import LogLevelHighlighter
from src.highlighters.timestamp import TimestampHighlighter
from src.highlighters.patterns import PatternHighlighter


def create_parser(args):
    """Create appropriate log parser based on arguments."""
    if args.format == 'syslog':
        return SyslogParser()
    elif args.format == 'json':
        return JsonParser()
    elif args.format == 'apache':
        return ApacheParser()
    elif args.format and args.pattern:
        return CustomParser(pattern=args.pattern)
    return None


def create_filters(args):
    """Create filter chain from arguments."""
    filters = []

    if args.level:
        levels = [l.strip() for l in args.level.split(',')]
        filters.append(LevelFilter(levels))

    if args.filter:
        filters.append(TextFilter(args.filter))

    if args.regex:
        filters.append(RegexFilter(args.regex))

    if args.since or args.until:
        from datetime import datetime
        since = None
        until = None
        if args.since:
            try:
                since = datetime.fromisoformat(args.since)
            except ValueError:
                since = TimeFilter.from_query(args.since).since
        if args.until:
            try:
                until = datetime.fromisoformat(args.until)
            except ValueError:
                until = TimeFilter.from_query(args.until).until
        filters.append(TimeFilter(since=since, until=until))

    return filters


def create_highlighters(args):
    """Create list of highlighters."""
    highlighters = [LogLevelHighlighter(), TimestampHighlighter()]

    if args.no_color:
        return []

    return highlighters


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        prog='logview',
        description='Terminal log file viewer with filtering and highlighting'
    )

    parser.add_argument(
        'files',
        nargs='*',
        help='Log files to view'
    )
    parser.add_argument(
        '-f', '--follow',
        action='store_true',
        help='Follow log file (like tail -f)'
    )
    parser.add_argument(
        '-l', '--level',
        help='Filter by log level (ERROR,WARN,INFO,DEBUG)'
    )
    parser.add_argument(
        '--filter',
        help='Filter by text content'
    )
    parser.add_argument(
        '-r', '--regex',
        help='Filter by regex pattern'
    )
    parser.add_argument(
        '--since',
        help='Show entries since timestamp'
    )
    parser.add_argument(
        '--until',
        help='Show entries until timestamp'
    )
    parser.add_argument(
        '--format',
        choices=['syslog', 'json', 'apache', 'custom'],
        help='Log format'
    )
    parser.add_argument(
        '--pattern',
        help='Custom regex pattern for custom format'
    )
    parser.add_argument(
        '--theme',
        default='default',
        choices=['default', 'monokai', 'solarized', 'light'],
        help='Color theme'
    )
    parser.add_argument(
        '--no-color',
        action='store_true',
        help='Disable colors'
    )
    parser.add_argument(
        '--export',
        help='Export filtered results to file'
    )
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Show statistics'
    )
    parser.add_argument(
        '--list-themes',
        action='store_true',
        help='List available themes'
    )
    parser.add_argument(
        '-n', '--buffer-size',
        type=int,
        default=10000,
        help='Buffer size'
    )

    args = parser.parse_args()

    if args.list_themes:
        print("Available themes: default, monokai, solarized, light")
        return 0

    if not args.files:
        parser.print_help()
        return 1

    log_parser = create_parser(args)
    filters = create_filters(args)
    highlighters = create_highlighters(args)

    viewer = LogViewer(
        files=args.files,
        follow=args.follow,
        parser=log_parser,
        filters=filters,
        highlighters=highlighters,
        theme=args.theme,
        buffer_size=args.buffer_size
    )

    try:
        viewer.start()

        if args.export:
            viewer.export_filtered(args.export)
            print(f"Exported to {args.export}")

        if args.stats:
            stats = viewer.get_stats()
            print(f"\nStatistics:")
            print(f"  Total entries: {stats['total']}")
            print(f"  Files: {stats['files']}")
            print(f"  Bookmarks: {stats['bookmarks']}")
            if stats['levels']:
                print(f"  Levels:")
                for level, count in stats['levels'].items():
                    print(f"    {level}: {count}")

        return 0
    except KeyboardInterrupt:
        print("\nStopped.")
        return 130


if __name__ == '__main__':
    sys.exit(main())
