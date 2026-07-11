"""Syslog format parser."""
import re
from typing import Optional
from .base import BaseParser


class SyslogParser(BaseParser):
    """Parser for standard syslog format."""

    # RFC 3164 format: Jan  1 12:00:00 hostname service[pid]: message
    SYSLOG_PATTERN = re.compile(
        r'^(?P<timestamp>\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+'
        r'(?P<hostname>\S+)\s+'
        r'(?P<service>\S+?)(?:\[(?P<pid>\d+)\])?:\s+'
        r'(?P<message>.+)$'
    )

    # RFC 5424 format: 2024-01-01T12:00:00.000Z hostname service - - - message
    RFC5424_PATTERN = re.compile(
        r'^(?P<version>\d+)\s+'
        r'(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?)\s+'
        r'(?P<hostname>\S+)\s+'
        r'(?P<app_name>\S+)\s+'
        r'(?P<procid>-|\d+)\s+'
        r'(?<msgid>-|\S+)\s+'
        r'(?<structdata>-|\[.*\])\s+'
        r'(?P<message>.+)$'
    )

    def parse(self, line: str, source: str = "") -> Optional[dict]:
        """Parse a syslog line."""
        match = self.SYSLOG_PATTERN.match(line)
        if match:
            return {
                'line': line,
                'raw': line,
                'source': source,
                'timestamp': match.group('timestamp'),
                'hostname': match.group('hostname'),
                'service': match.group('service'),
                'pid': match.group('pid'),
                'message': match.group('message'),
                'level': self._detect_syslog_level(match.group('message')),
                'format': 'syslog-rfc3164'
            }

        match = self.RFC5424_PATTERN.match(line)
        if match:
            return {
                'line': line,
                'raw': line,
                'source': source,
                'timestamp': match.group('timestamp'),
                'hostname': match.group('hostname'),
                'service': match.group('app_name'),
                'message': match.group('message'),
                'level': self._detect_syslog_level(match.group('message')),
                'format': 'syslog-rfc5424'
            }

        return {
            'line': line,
            'raw': line,
            'source': source,
            'timestamp': self._extract_timestamp(line),
            'level': self._extract_level(line),
            'message': line,
            'format': 'syslog-unknown'
        }

    def _detect_syslog_level(self, message: str) -> str:
        """Detect severity from syslog message."""
        msg_upper = message.upper()
        if 'EMERG' in msg_upper or 'ALERT' in msg_upper or 'CRIT' in msg_upper:
            return 'ERROR'
        elif 'ERR' in msg_upper:
            return 'ERROR'
        elif 'WARN' in msg_upper or 'NOTICE' in msg_upper:
            return 'WARN'
        elif 'INFO' in msg_upper:
            return 'INFO'
        elif 'DEBUG' in msg_upper:
            return 'DEBUG'
        return 'INFO'

    def detect(self, line: str) -> bool:
        """Check if line matches syslog format."""
        return bool(self.SYSLOG_PATTERN.match(line) or self.RFC5424_PATTERN.match(line))
