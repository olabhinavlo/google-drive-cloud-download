import os
import sys
from pathlib import Path
import re
import subprocess

# ------------------------------
# CONFIG
# ------------------------------
DOWNLOAD_PATH = "/content/drive/MyDrive/Downloads"
Path(DOWNLOAD_PATH).mkdir(parents=True, exist_ok=True)

# ------------------------------
# GOOGLE DRIVE
# ------------------------------
def is_drive(url):
    return "drive.google.com" in url

def get_drive_file_id(url):
    match = re.search(r'(?:id=|/d/)([a-zA-Z0-9_-]+)', url)
    return match.group(1) if match else None

def download_drive(url):
    fid = get_drive_file_id(url)
    if not fid:
        print("❌ Invalid Google Drive link")
        return
    print(f"📁 Downloading Google Drive file: {fid}")
    os.system(f'gdown --id {fid} -O "{DOWNLOAD_PATH}" --fuzzy')

# ------------------------------
# TORRENT
# ------------------------------
def is_torrent(url):
    return url.startswith("magnet:") or url.endswith(".torrent")

def download_torrent(url):
    print(f"🌐 Downloading torrent: {url}\n")
    cmd = [
        "aria2c",
        url,
        f"-d{DOWNLOAD_PATH}",
        "-x16", "-s16", "-k1M",
        "--continue=true",
        "--max-tries=0",
        "--retry-wait=3",
        "--summary-interval=1"
    ]
    # Stream aria2c output line by line
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    try:
        for line in process.stdout:
            print(line, end="")
        process.wait()
    except KeyboardInterrupt:
        process.terminate()
        print("\n❌ Torrent download interrupted by user")
    if process.returncode == 0:
        print("\n✅ Torrent download complete!")
    else:
        print(f"\n❌ Torrent failed with exit code {process.returncode}")

# ------------------------------
# DIRECT
# ------------------------------
def download_direct(url):
    print(f"🌐 Downloading direct link: {url}\n")
    cmd = [
        "aria2c",
        url,
        f"-d{DOWNLOAD_PATH}",
        "-x16", "-s16", "-k1M",
        "--continue=true",
        "--max-tries=0",
        "--retry-wait=3",
        "--summary-interval=1"
    ]
    subprocess.run(cmd)

# ------------------------------
# MAIN
# ------------------------------
def main():
    try:
        url = input("🔗 Enter download link: ").strip()
        if is_drive(url):
            download_drive(url)
        elif is_torrent(url):
            download_torrent(url)
        else:
            download_direct(url)
        print("\n✅ All done!")
    except KeyboardInterrupt:
        print("\n❌ Download interrupted by user")
        sys.exit(1)

# ------------------------------
# RUN
# ------------------------------
if __name__ == "__main__":
    # Mount Google Drive (force remount if already mounted)
    from google.colab import drive
    drive.mount('/content/drive', force_remount=True)
    main()