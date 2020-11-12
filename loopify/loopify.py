from pathlib import Path

import subprocess


in_file = Path("./in.mkv")

name = in_file.stem

if not in_file.is_file():
    print("No input!")
    exit(1)

silent_file = Path("./in_silent.mkv")
reversed_file = Path("./in_reversed.mkv")
out_file = Path("./out.mkv")

concat_file = Path("./concat.txt")

if silent_file.is_file():
    silent_file.unlink()

subprocess.run([
    "ffmpeg",
    "-i", str(in_file),
    "-vcodec", "copy",
    "-an",
    str(silent_file)
    ])

if not silent_file.is_file():
    print("Failed to create silent file!")
    exit(1)

if reversed_file.is_file():
    reversed_file.unlink()

subprocess.run([
    "ffmpeg",
    "-i", str(silent_file),
    "-vf", "reverse",
    str(reversed_file)
    ])

if not reversed_file.is_file():
    print("Failed to create reversed file!")
    exit(1)

with concat_file.open("w") as f:
    f.write("file '{}'\n".format(str(silent_file)))
    f.write("file '{}'\n".format(str(reversed_file)))

if out_file.is_file():
    out_file.unlink()

subprocess.run([
    "ffmpeg",
    "-f", "concat",
    "-safe", "0",
    "-i", "concat.txt",
    "-c", "copy",
    str(out_file)
    ])

if not out_file.is_file():
    print("Failed to create output file!")
    exit(1)

silent_file.unlink()
reversed_file.unlink()
concat_file.unlink()