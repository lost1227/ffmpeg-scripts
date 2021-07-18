from pathlib import Path
import subprocess
import shutil

# Helpful: https://www.covermytunes.com/
# Potential future project: automatically pull covers based on metadata

script_dir = Path(__file__).resolve().parent

indir = script_dir / 'in'
outdir = script_dir / 'out'

cover = 'cover'
extensions = ['.png', '.jpg']

coverpath = None

for extension in extensions:
    path = indir / (cover + extension)
    if path.is_file():
        coverpath = path
        break

if coverpath is None or not coverpath.is_file():
    print("Could not locate cover")
    exit(1)
    
if outdir.exists():
    shutil.rmtree(outdir)

outdir.mkdir()

for mp3path in indir.glob("*.mp3"):
    outpath = outdir / mp3path.name
    completion = subprocess.run(['ffmpeg', 
            '-i', mp3path,
            '-i', coverpath,
            '-map', '0:a',
            '-map', '1:v',
            '-map_metadata', '0',
            '-acodec', 'copy',
            '-vcodec', 'copy',
            "-id3v2_version", "3",
            "-metadata:s:v", "title=cover",
            "-metadata:s:v", "comment=Cover (front)",
            outpath
            ])
    if completion.returncode != 0:
        print("ffmpeg error")
        exit(1)
    print()