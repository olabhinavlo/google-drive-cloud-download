import os
from pathlib import Path

# ------------------------------
# CONFIG
# ------------------------------
def ensure_path(path):
    Path(path).mkdir(parents=True, exist_ok=True)

# ------------------------------
# DOWNLOAD FUNCTION
# ------------------------------
def torrent_to_drive(url, output_path):
    """
    Download torrent/magnet link to output_path using aria2c.
    """
    ensure_path(output_path)
    print(f"🌐 Downloading torrent: {url}")
    cmd = f'''
    aria2c "{url}" \
    -d "{output_path}" \
    -x 16 -s 16 -k 1M \
    --continue=true \
    --max-tries=0 \
    --retry-wait=3
    '''
    os.system(cmd)