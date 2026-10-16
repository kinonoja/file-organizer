#  File Organizer

A Python CLI that cleans up messy folders (like Downloads) by sorting files into categorized subfolders.

##  Features
- Sorts files into 8 categories: Images, Documents, Videos, Audio, Code, Archives, Text, Data
- `--dry-run` mode to preview changes safely
- Handles filename collisions (never overwrites)
- Logs every action to `organizer.log`
- Fully typed + tested (pytest)

##  Install
```bash
git clone https://github.com/YOUR_USERNAME/file-organizer.git
cd file-organizer
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"