# Album Art Extractor

Python script that extracts album art from MP3 and FLAC files and saves it as a 100x100 .bmp file. Resulting album art files tested and working on my iPod Photo running Rockbox. **Script only tested on Linux so be careful.**

Works with both single files and music folders.

Requires pillow and Mutagen.

## Usage

Download extractor.py and requirements.txt.

In the command line, same directory as extractor.py and requirements.txt:
``````
pip install -r requirements.txt

python3 extractor.py <music_directory> [output_directory]
``````
Output directory is optional. If not specified, image will be in the same directory as the music file.

By default, the image file will be named after the music file's album. If the music file doesn't have an album tag, the image file will be named after the track title. If the track has neither, the image file will be "cover.bmp".
