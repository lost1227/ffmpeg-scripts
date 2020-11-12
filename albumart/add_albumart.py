import glob, os
import subprocess

# Helpful: https://www.covermytunes.com/
# Potential future project: automatically pull covers based on metadata

indir = 'in'
outdir = 'out'
cover = 'cover'
extensions = ['.png', '.jpg']

mp3files = glob.glob(indir + '/*.mp3')

coverpath = ""

for extension in extensions:
    path = os.path.join(indir, cover + extension)
    if os.path.isfile(path):
        coverpath = path

for mp3path in mp3files:
    basepath = os.path.splitext(mp3path)[0]
    
    outpath = os.path.join(outdir, os.path.basename(basepath) + ".mp3")
    cmd = ['ffmpeg', 
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
            outpath]
    
    #print(cmd)
    subprocess.run(cmd)
    print('\n')