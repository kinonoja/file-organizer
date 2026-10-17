# File Organizer

A Python CLI that cleans up messy folders (like Downloads) by sorting files into categorized subfolders based on their file type.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)

---

## Features

- Sorts files into 8 categories: Images, Documents, Videos, Audio, Code, Archives, Text, Data
- `--dry-run` mode previews changes without touching files
- Handles filename collisions (never overwrites)
- Logs every action to `organizer.log`
- Fully typed, linted, and tested with pytest
- Clean CLI built with Click

---

## Installation

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/file-organizer.git
cd file-organizer

python3 -m venv --copies .venv
source .venv/bin/activate        # Linux/Mac/WSL
# Windows (PowerShell): .venv\Scripts\Activate.ps1
# Windows (CMD):        .venv\Scripts\activate.bat


pip install --upgrade pip
pip install -e ".[dev]"


organize --source ~/Downloads --dry-run -v

organize --dry-run       # preview
organize                 # for real


organize -s ~/Downloads --dry-run -v


Downloads/
├── resume.pdf
├── photo.jpg
├── script.py
├── song.mp3
├── notes.txt
└── unknown.xyz


Downloads/
├── Documents/    -> resume.pdf
├── Images/       -> photo.jpg
├── Code/         -> script.py
├── Audio/        -> song.mp3
├── Text/         -> notes.txt
└── Others/       -> unknown.xyz


# View the log
cat organizer.log

# Tail it live
tail -f organizer.log


Tech Stack
Python 3.10+

Click - CLI framework

pytest - testing

ruff - fast linter and formatter

mypy - static type checking