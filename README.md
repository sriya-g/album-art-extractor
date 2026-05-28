# Album Art Extractor
Python script that extracts album art from MP3 and FLAC files and saves it as a 100x100 .bmp file. Resulting album art files tested and working on my iPod Photo running Rockbox. **Script only tested on Linux so be careful.**

Works with both single files and music folders.

Requires pillow and Mutagen.

## Setup
Download extractor.py and requirements.txt.

In the command line, same directory as requirements.txt:
``````
pip install -r requirements.txt
``````
## Usage
In the command line, same directory as extractor.py:
``````
python3 extractor.py <music_directory> [output_directory]
``````
Output directory is optional. If not specified, image will be in the same directory as the music file.

File name priority:
- Album name (default)
- Track name
- "cover.bmp"

## Flags
- -s [size] or --size [size] changes all output bmp files to be sizexsize instead of the default 100x100.
    - Rockbox may have issues displaying files larger than 600x600; **any size value greater than 600 will be set to 600.**
- -h or --help displays a list of all flags/arguments
