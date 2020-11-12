from pathlib import Path
import shutil
import os
import subprocess

script_dir = Path(__file__).resolve().parent

os.chdir(script_dir)

in_dir = Path("./in")
out_dir = Path("./out")

if not in_dir.is_dir():
    print("No inputs!")
    if in_dir.exists():
        in_dir.unlink()
    in_dir.mkdir()
    exit
    
if out_dir.exists():
    shutil.rmtree(out_dir)
out_dir.mkdir()

in_files = in_dir.glob("*.mp3")


for in_file in in_files:
    out_file = out_dir / in_file.name
    
    subprocess.run([
        "ffmpeg",
        "-i", str(in_file),
        "-c", "copy",
        "-id3v2_version", "3",
        "-metadata:s:v", "title=cover",
        "-metadata:s:v", "comment=Cover (front)",
        str(out_file)
    ])