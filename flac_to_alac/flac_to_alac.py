import argparse
from pathlib import Path
import subprocess
import shutil

script_dir = Path(__file__).resolve().parent

parser = argparse.ArgumentParser()

parser.add_argument('--in', default=str(script_dir / 'in'), dest='indir')
parser.add_argument('--out', default=str(script_dir / 'out'), dest='outdir')
parser.add_argument('--cover')
parser.add_argument('--number', action='store_true')
parser.add_argument('--album')

args = parser.parse_args()

indir = Path(args.indir)
outdir = Path(args.outdir)

coverpath = None
if args.cover:
    coverpath = Path(args.cover)
    if not coverpath.is_file():
        coverpath = None


if outdir.exists():
    shutil.rmtree(outdir)

outdir.mkdir()

infiles = list(indir.glob("*.flac"))

def get_ffmpeg_invocation(i, inpath, outpath, coverpath):
    metadata = []
    if args.number:
        metadata += [ '-metadata', f'track={i+1}']
    if args.album:
        metadata += [ '-metadata', f'album={args.album}' ]
    if coverpath is None:
        return [
            'ffmpeg',
            '-i', str(inpath),
            '-acodec', 'alac',
            '-vcodec', 'copy',
            '-disposition:v', 'attached_pic'
            ] + metadata + [
            str(outpath)
        ]
    else:
        return [
            'ffmpeg',
            '-i', str(inpath),
            '-i', str(coverpath),
            '-map', '0:a',
            '-map', '1:v',
            '-acodec', 'alac',
            '-vcodec', 'copy',
            '-disposition:v', 'attached_pic'
            ] + metadata + [
            str(outpath)
        ]

for i, inpath in enumerate(infiles):
    outpath = outdir / f"{inpath.stem}.m4a"
    completion = subprocess.run(get_ffmpeg_invocation(i, inpath, outpath, coverpath))
    if completion.returncode != 0:
        print("ffmpeg error")
        exit(1)
    print()