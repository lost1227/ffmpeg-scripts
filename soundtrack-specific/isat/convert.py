from pathlib import Path
import subprocess
import shutil

script_dir = Path(__file__).resolve().parent

illegal_chars = "<>:\"/\|?*"

class Track:
    def __init__(self, disc, track, title):
        self.disc = disc
        self.track = track
        self.title = title

tracks = [
    Track(1, 1, "In Stars and Time (Title Theme)"),
    Track(1, 2, "Prologue"),
    Track(1, 3, "Dormont"),
    Track(1, 4, "Dormont (Welcome To My Home, Stranger)"),
    Track(1, 5, "The Journey So Far"),
    Track(1, 6, "Let's Play Rock Paper Scissors!"),
    Track(1, 7, "Get Ready, Everyone! (Battle Theme)"),
    Track(1, 8, "Be Careful, Everyone! (Boss Theme)"),
    Track(1, 9, "Go Back (Death's Theme)"),
    Track(1, 10, "Game Over"),
    Track(1, 11, "How Can I Help You, Stardust? (Loop's Theme)"),
    Track(1, 12, "The House (Floor 1)"),
    Track(1, 13, "The House (Floor 2)"),
    Track(1, 14, "The House (Floor 3)"),
    Track(1, 15, "We're Here With You!"),
    Track(1, 16, "Is It Snack Time Yet..."),
    Track(1, 17, "Frozen in Time"),
    Track(1, 18, "Please Don't Be Sad"),
    Track(1, 19, "In the Presence of the King"),
    Track(1, 20, "Do You Remember (King's Theme)"),
    Track(1, 21, "Power of Friendship"),
    Track(1, 22, "It's Finally Over..."),
    Track(2, 23, "Isn't It Over?"),
    Track(2, 24, "Friend Quest"),
    Track(2, 25, "Friend Quest (Solo)"),
    Track(2, 26, "Let's Hang Out, Stardust!"),
    Track(2, 27, "Thinking Time"),
    Track(2, 28, "Do You Remember (Our Country)"),
    Track(2, 29, "An Island North of Vaugarde"),
    Track(2, 30, "The House (Trapped)"),
    Track(2, 31, "Do You Remember (We've Been Through This Before)"),
    Track(2, 32, "Game Over (Don't Leave Me Alone Here)"),
    Track(2, 33, "Power of Love"),
    Track(2, 34, "I WON'T LET YOU GO HOME"),
    Track(2, 35, "Tell Us Tell Us Tell Us"),
    Track(2, 36, "You Want To Stay With Them"),
    Track(2, 37, "It's Finally Over... (Reprise)"),
    Track(2, 38, "How Can You Help Me, Stardust?"),
    Track(2, 39, "It's Thanks To You"),
    Track(2, 40, "Long Journey"),
    Track(2, 41, "Credits")
]

tracks = {track.track: track for track in tracks}

num_tracks = max(tracks.keys())
num_discs = max(track.disc for track in tracks.values())

artist = "Studio Thumpy Puppy"
album = "In Stars And Time Soundtrack"
date = 2023

files = list((script_dir / "in").glob("**/*.wav"))
assert len(files) > 0

coverpath = script_dir / "cover.jpg"
assert coverpath.is_file()

outdir = script_dir / album

if outdir.exists():
    shutil.rmtree(outdir)

outdir.mkdir()

for inpath in files:
    try:
        trackno = int(inpath.name.split("-")[0])
        track = tracks[trackno]

        sanitized_title = track.title
        for char in illegal_chars:
            if char in sanitized_title:
                sanitized_title = sanitized_title.replace(char, "")

        outpath = outdir / f"{track.track:02d} - {sanitized_title}.m4a"

        cmd = [
            "ffmpeg",
            "-i", str(inpath),
            "-i", str(coverpath),
            "-acodec", "alac",
            "-vcodec", "copy",
            "-map", "0:a",
            "-map", "1:v",
            "-disposition:v", "attached_pic",
            "-metadata", f"title={track.title}",
            "-metadata", f"track={track.track}/{num_tracks}",
            "-metadata", f"album={album}",
            "-metadata", f"artist={artist}",
            "-metadata", f"date={date}",
            "-metadata", f"disc={track.disc}/{num_discs}",
            str(outpath)
        ]

        print(cmd)

        subprocess.run(cmd).check_returncode()
        print()
    except (IndexError, ValueError):
        print(f"Invalid input file: {inpath.name}")
        continue
