# Set id3v2.3 Cover Art Tags

## Description
This script sets the `title` and `comment` tags on the Cover Art streams.
This is useful because, while just adding an image stream is good enough for
VLC and iTunes to display the cover art, Groove demands that the image
image stream also have the proper metadata tags.

This script does not add album art, it just fixes the metadata tags on
mp3 files that already have album art.

## Inputs
- `in/*.mp3` Covered mp3 files

## Outputs
- `out/*.mp3` Covered mp3 files with correct metadata