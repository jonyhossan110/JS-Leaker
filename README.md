# JS-Leaker

**JavaScript Secret Scanner** - A professional cybersecurity tool for detecting exposed secrets in website JavaScript files.

Created by **HexaCyberLab**  
Author: **Md. Jony Hassain**  
LinkedIn: [https://www.linkedin.com/in/md-jony-hassain/](https://www.linkedin.com/in/md-jony-hassain/)

## 🚀 Features

- **Advanced JS Collection**: Static and dynamic JavaScript file discovery
- **Concurrent Processing**: Multi-threaded downloads and scanning for speed
- **Comprehensive Secret Detection**: JWT tokens, API keys, passwords, and more
- **Base64 Decoding**: Automatically decodes and scans Base64-encoded secrets
- **Severity Classification**: HIGH, MEDIUM, LOW risk categorization
- **Cross-Platform**: Works on Windows, Linux, and macOS
- **Clean CLI Interface**: Professional terminal UI with color support

## 📋 Requirements

- Python 3.9+
- Playwright browsers (for dynamic JS collection)

## 🛠️ Installation

### Windows/Linux/macOS

1. **Clone or download the repository**

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv jsleaker-env
   # On Windows:
   jsleaker-env\Scripts\activate
   # On Linux/macOS:
   source jsleaker-env/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers**:
   ```bash
   playwright install
   ```

## 🎯 Usage

### Basic Scan
```bash
python main.py -u https://example.com
```

### Advanced Usage
```bash
# Specify worker threads
python main.py -u https://example.com -t 8

# Custom output file
python main.py -u https://example.com -o custom_report.txt

# Full command with all options
python main.py -u https://target-site.com -t 6 -o reports/scan.txt
```

### Command Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `-u, --url` | Target URL to scan (required) | - |
| `-t, --threads` | Number of worker threads | 4 |
| `-o, --output-file` | Output file path | `output/scan_report.txt` |

## 📊 Output

The tool generates two types of reports:

1. **Detailed Report** (`output/scan_report.txt`): Complete findings with context
2. **Summary Report** (`output/report.txt`): Severity-based summary

### Sample Output
```
==================================
   JS-Leaker - Secret Scanner
==================================
Created by HexaCyberLab
Author: Md. Jony Hassain
LinkedIn: https://www.linkedin.com/in/md-jony-hassain/
==================================

[INFO] Target: https://example.com/
[INFO] Workers: 4
[INFO] Collecting JavaScript files...
[SUCCESS] Found 43 external JS, 42 inline JS
[INFO] Downloading external JavaScript files...
[INFO] Scanning 85 files for secrets...
[SUCCESS] Scan complete. Reports saved to output directory.
```

## 🔍 Detected Secrets

The tool scans for:

- **HIGH Severity**:
  - JWT Tokens
  - AWS Access Keys
  - Google API Keys
  - Private RSA Keys
  - Firebase URLs

- **MEDIUM Severity**:
  - OAuth Tokens
  - Generic API Keys
  - Basic Auth (Base64)

- **LOW Severity**:
  - Passwords in clear text

## 📁 Project Structure

```
JS-Leaker/
│
├── main.py              # CLI entry point with banner
├── collector.py         # JavaScript collection (static + dynamic)
├── scanner.py           # Secret scanning engine
├── downloader.py        # Concurrent file downloader
├── utils.py             # Utilities and logging functions
├── requirements.txt     # Python dependencies
├── README.md            # This file
├── LICENSE              # MIT License
├── .gitignore           # Git ignore rules
│
├── data/                # Collected JavaScript files
│   ├── external/        # Downloaded external JS
│   ├── inline/          # Extracted inline JS
│   └── hashes.json      # Content hash cache
│
└── output/              # Scan reports and summaries
```

## 🐧 Linux Compatibility

The tool is fully compatible with Linux:

```bash
# Install Python 3.9+ if needed
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Run the tool
python3 main.py -u https://target.com
```

## ⚠️ Ethical Usage

This tool is designed for **ethical cybersecurity purposes only**:

- Use only on websites you own or have explicit permission to test
- Respect robots.txt and terms of service
- Do not use for unauthorized security testing
- Report findings responsibly to website owners

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

**HexaCyberLab**  
**Md. Jony Hassain**  
[LinkedIn](https://www.linkedin.com/in/md-jony-hassain/)

---

*Built with ❤️ for the cybersecurity community*

