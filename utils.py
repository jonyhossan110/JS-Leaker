#!/usr/bin/env python3
"""
utils.py - Helper utilities for JS-Leaker

Provides:
- safe, cross-platform logging
- directory helpers
- regex-based secret detection helpers
- report generation helpers

"""

import logging
import sys
from pathlib import Path
from typing import List, Dict, Tuple
from datetime import datetime
import os
import re

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False

# Constants and tuning
TIMEOUT = 15
MAX_JS_COUNT = 500
MAX_FILE_SIZE_MB = 2  # Skip files >2MB
MAX_CONCURRENT = 8
MAX_SCRIPTS = 1000
MAX_CONTEXT_LINES = 6

# Common libraries to ignore (by filename or content hash)
IGNORED_LIBRARIES = {
    'filenames': {'jquery.min.js', 'jquery.js', 'bootstrap.min.js', 'bootstrap.js', 'swagger-ui-bundle.js', 'swagger-ui-standalone-preset.js'},
    'hashes': set()  # Will populate with known hashes if needed
}


def print_info(message: str):
    """Print info message with [INFO] prefix."""
    if HAS_COLORAMA:
        print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} {message}")
    else:
        print(f"[INFO] {message}")


def print_success(message: str):
    """Print success message with [SUCCESS] prefix."""
    if HAS_COLORAMA:
        print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} {message}")
    else:
        print(f"[SUCCESS] {message}")


def print_warning(message: str):
    """Print warning message with [WARNING] prefix."""
    if HAS_COLORAMA:
        print(f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} {message}")
    else:
        print(f"[WARNING] {message}")


def print_error(message: str):
    """Print error message with [ERROR] prefix."""
    if HAS_COLORAMA:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {message}")
    else:
        print(f"[ERROR] {message}")


def print_dashboard():
    """Print a professional colorized ASCII art dashboard for JS-Leaker."""
    if HAS_COLORAMA:
        # ASCII art with color codes
        dashboard = f"""
{Fore.CYAN}╔════════════════════════════════════════════════════════════════╗{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}                                                                  {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}  {Fore.CYAN}██╗███████╗{Style.RESET_ALL}{Fore.RED}██╗    ██╗███████╗ █████╗ ██╗  ██╗███████╗██████╗ {Style.RESET_ALL}  {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}  {Fore.CYAN}██║██╔════╝{Style.RESET_ALL}{Fore.RED}██║    ██║██╔════╝██╔══██╗██║ ██╔╝██╔════╝██╔══██╗{Style.RESET_ALL}  {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}  {Fore.CYAN}██║███████╗{Style.RESET_ALL}{Fore.RED}██║ █╗ ██║█████╗  ███████║█████╔╝ █████╗  ██████╔╝{Style.RESET_ALL}  {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}  {Fore.CYAN}██║╚════██║{Style.RESET_ALL}{Fore.RED}██║███╗██║██╔══╝  ██╔══██║██╔═██╗ ██╔══╝  ██╔══██╗{Style.RESET_ALL}  {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}  {Fore.CYAN}██║███████║{Style.RESET_ALL}{Fore.RED}╚███╔███╔╝███████╗██║  ██║██║  ██╗███████╗██║  ██║{Style.RESET_ALL}  {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}  {Fore.CYAN}╚═╝╚══════╝{Style.RESET_ALL}{Fore.RED} ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝{Style.RESET_ALL}  {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}                                                                  {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}          {Fore.YELLOW}JavaScript Secret Scanner & Extractor{Style.RESET_ALL}                 {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}║{Style.RESET_ALL}                                                                  {Fore.CYAN}║{Style.RESET_ALL}
{Fore.CYAN}╚════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.GREEN}┌──────────────────────────────────────────────────────────────┐{Style.RESET_ALL}
{Fore.GREEN}│{Style.RESET_ALL}  {Fore.CYAN}Created By:{Style.RESET_ALL} Md. Jony Hassain (HexaCyberLab)                {Fore.GREEN}│{Style.RESET_ALL}
{Fore.GREEN}│{Style.RESET_ALL}  {Fore.CYAN}LinkedIn:{Style.RESET_ALL}   https://www.linkedin.com/in/md-jony-hassain/  {Fore.GREEN}│{Style.RESET_ALL}
{Fore.GREEN}└──────────────────────────────────────────────────────────────┘{Style.RESET_ALL}
"""
    else:
        # Fallback plain ASCII art (no colors)
        dashboard = """
╔════════════════════════════════════════════════════════════════╗
║                                                                  ║
║  JS-Leaker - JavaScript Secret Scanner & Extractor             ║
║                                                                  ║
╚════════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────┐
│  Created By: Md. Jony Hassain (HexaCyberLab)                 │
│  LinkedIn:   https://www.linkedin.com/in/md-jony-hassain/    │
└──────────────────────────────────────────────────────────────┘
"""
    print(dashboard)


def log_print(message: str):
    """Print a message safely to console and logging.

    Ensures non-fatal behavior on Windows consoles with limited encodings.
    """
    try:
        if message is None:
            message = ''
        try:
            safe_msg = str(message)
        except Exception:
            safe_msg = repr(message)
        try:
            print(safe_msg)
        except UnicodeEncodeError:
            print(safe_msg.encode('ascii', 'ignore').decode('ascii', 'ignore'))
        try:
            logging.info(safe_msg)
        except Exception:
            pass
    except Exception:
        try:
            print('[LOG ERROR]')
        except Exception:
            pass


def setup_logging(logfile: str = 'js-leaker.log'):
    """Configure logging handlers for file + console.

    Uses UTF-8 file encoding and a console handler. If file handler creation
    fails, we continue with console-only logging.
    """
    handlers = []
    try:
        fh = logging.FileHandler(logfile, encoding='utf-8')
        fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        handlers.append(fh)
    except Exception:
        pass
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    handlers.append(ch)

    logging.basicConfig(level=logging.INFO, handlers=handlers)


def ensure_directories(*dirs: str):
    """Create directories if they don't exist. Ignores empty entries."""
    for directory in dirs:
        if not directory:
            continue
        Path(directory).mkdir(parents=True, exist_ok=True)


# SECRET PATTERNS: (name, regex, severity)
# Severity: HIGH, MEDIUM, LOW
SECRET_PATTERNS: List[Tuple[str, re.Pattern, str]] = [
    ('JWT Token', re.compile(r"\beyJ[\w-]+\.[\w-]+\.[\w-]+\b"), 'HIGH'),
    ('AWS Access Key ID', re.compile(r"\bAKIA[0-9A-Z]{16}\b"), 'HIGH'),
    ('AWS Secret Access Key', re.compile(r"\b[0-9a-zA-Z/+]{40}\b"), 'HIGH'),
    ('Firebase URL', re.compile(r"https?://[\w.-]+\.firebaseio\.com"), 'HIGH'),
    ('Google API Key', re.compile(r"\bAIza[0-9A-Za-z\-_]{35}\b"), 'HIGH'),
    ('Slack Token', re.compile(r"\bxox[baprs]-[0-9A-Za-z-]+\b"), 'HIGH'),
    ('Password in clear', re.compile(r"\bpass(word)?\s*[:=]\s*['\"]?[^\s'\"]{6,60}['\"]?\b", re.I), 'HIGH'),
    ('Private RSA Key', re.compile(r"-----BEGIN (RSA )?PRIVATE KEY-----"), 'HIGH'),
    ('OAuth Bearer', re.compile(r"\bBearer\s+[A-Za-z0-9\-_.]+=*\b"), 'MEDIUM'),
    ('Basic Auth Base64', re.compile(r"\bBasic\s+[A-Za-z0-9+/=]{20,}\b"), 'MEDIUM'),
    ('Generic API Key', re.compile(r"\bapi[_-]?key\s*[:=]\s*['\"]?[A-Za-z0-9-_]{16,64}['\"]?\b", re.I), 'MEDIUM'),
    ('OAuth Token', re.compile(r"\boauth_token\s*[:=]\s*['\"]?[A-Za-z0-9\-_.]{8,}['\"]?\b", re.I), 'MEDIUM'),
]


def detect_secrets_in_text(text: str) -> List[Dict]:
    """Scan given text for known secret patterns.

    Returns list of findings with keys: type, match, severity, context, line
    """
    findings = []
    if not text:
        return findings

    lines = text.splitlines()

    for name, pattern, severity in SECRET_PATTERNS:
        try:
            for m in pattern.finditer(text):
                match_text = m.group(0)
                # approximate line number
                start_pos = m.start()
                line_no = text.count('\n', 0, start_pos) + 1
                # context: few lines around the hit
                start_line = max(0, line_no - 1 - (MAX_CONTEXT_LINES // 2))
                end_line = min(len(lines), start_line + MAX_CONTEXT_LINES)
                context = '\n'.join(lines[start_line:end_line])
                findings.append({
                    'type': name,
                    'match': match_text,
                    'severity': severity,
                    'line': line_no,
                    'context': context
                })
        except re.error:
            continue

    # Deduplicate by match content
    seen = set()
    dedup = []
    for f in findings:
        key = (f['type'], f['match'])
        if key in seen:
            continue
        seen.add(key)
        dedup.append(f)

    return dedup


def should_skip_file(filepath: str) -> bool:
    """Check if file should be skipped: size >2MB, empty, or ignored library."""
    try:
        if not os.path.exists(filepath):
            return True
        size = os.path.getsize(filepath)
        if size > MAX_FILE_SIZE_MB * 1024 * 1024:
            return True
        if size == 0:
            return True
        filename = os.path.basename(filepath).lower()
        if filename in IGNORED_LIBRARIES['filenames']:
            return True
        # Could add hash check here if needed
        return False
    except Exception:
        return True


def save_text_file(path: str, content: str, max_bytes: int = 5 * 1024 * 1024):
    """Write content safely to path with UTF-8 encoding and size cap."""
    try:
        ensure_directories(Path(path).parent.as_posix())
        with open(path, 'w', encoding='utf-8', errors='replace') as fh:
            fh.write(content[:max_bytes])
        return True
    except Exception as e:
        print_error(f"Could not save file {path}: {e}")
        return False


def write_scan_report(detailed_results: List[Dict], output_path: str = 'output/scan_report.txt') -> None:
    """Write a readable scan report enumerating files and findings."""
    ensure_directories(os.path.dirname(output_path) or '.')
    lines = []
    lines.append('JS-Leaker Scan Report')
    lines.append('=' * 60)
    lines.append(f'Generated: {datetime.now().isoformat()}')
    lines.append('')

    total = 0
    for res in detailed_results:
        file = res.get('file')
        findings = res.get('findings', [])
        lines.append(f'FILE: {file} ({len(findings)} findings)')
        lines.append('-' * 60)
        for f in findings:
            total += 1
            lines.append(f"[{f.get('severity')}] {f.get('type')} - Line {f.get('line')}")
            lines.append(f"Match: {f.get('match')}")
            ctx = f.get('context', '')
            if ctx:
                lines.append('Context:')
                lines.extend(['  ' + ln for ln in ctx.splitlines()])
            lines.append('')
        lines.append('')

    lines.insert(3, f'Total Findings: {total}')

    try:
        Path(output_path).write_text('\n'.join(lines), encoding='utf-8')
        print_success(f'Report saved: {output_path}')
    except Exception as e:
        print_error(f'Could not write scan report: {e}')
