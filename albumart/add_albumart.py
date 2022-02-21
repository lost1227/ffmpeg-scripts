from pathlib import Path
import subprocess
import shutil
import itertools

# Helpful: https://www.covermytunes.com/
# Potential future project: automatically pull covers based on metadata

script_dir = Path(__file__).resolve().parent

ffmpeg_options_map = {
    '.mp3': [
        "-id3v2_version", "3",
        "-metadata:s:v", "title=cover",
        "-metadata:s:v", "comment=Cover (front)"
    ],
    '.flac': [
        "-disposition:1", "attached_pic"
    ]
}

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

globs = [indir.glob(f"*{ext}") for ext in ffmpeg_options_map.keys()]

for inpath in itertools.chain.from_iterable(globs):
    outpath = outdir / inpath.name
    ffmpeg_opts = ffmpeg_options_map[inpath.suffix]
    completion = subprocess.run(['ffmpeg', 
            '-i', inpath,
            '-i', coverpath,
            '-map', '0:a',
            '-map', '1:v',
            '-map_metadata', '0'
            ] + ffmpeg_opts + [
            outpath
            ])
    if completion.returncode != 0:
        print("ffmpeg error")
        exit(1)
    print()