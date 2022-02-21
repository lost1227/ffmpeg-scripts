from pathlib import Path
import subprocess
import shutil

script_dir = Path(__file__).resolve().parent

indir = script_dir / 'in'
outdir = script_dir / 'out'

if outdir.exists():
    shutil.rmtree(outdir)

outdir.mkdir()

for inpath in indir.glob("*.flac"):
    outpath = outdir / f"{inpath.stem}.m4a"
    completion = subprocess.run(['ffmpeg', 
            '-i', inpath,
            '-acodec', 'alac',
            '-vcodec', 'copy',
            '-disposition:v', 'attached_pic',
            str(outpath)
            ])
    if completion.returncode != 0:
        print("ffmpeg error")
        exit(1)
    print()