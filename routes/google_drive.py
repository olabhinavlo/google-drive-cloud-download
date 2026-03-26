import os
import re
from pathlib import Path

# ------------------------------
# CONFIG
# ------------------------------
def ensure_path(path):
    Path(path).mkdir(parents=True, exist_ok=True)

# ------------------------------
# HELPERS
# ------------------------------
def get_file_id(url):
    """Extract Google Drive file ID from link"""
    patterns = [r'id=([a-zA-Z0-9_-]+)', r'/d/([a-zA-Z0-9_-]+)']
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    return None

# ------------------------------
# DOWNLOAD FUNCTION
# ------------------------------
def drive_download(url, output_path):
    ensure_path(output_path)
    fid = get_file_id(url)
    if not fid:
        print("❌ Invalid Google Drive link")
        return
    print(f"📁 Downloading Google Drive file: {fid}")
    os.system(f'gdown --id {fid} -O "{output_path}" --fuzzy')