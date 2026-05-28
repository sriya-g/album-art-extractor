import os
import sys
import re
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from PIL import Image
import io
import argparse

def extract_album_art(music_file_path, output_dir, output_size=100):
    """
    Extracts album art from a music file, converts it to a 100x100 BMP,
    and saves it in the output directory.

    Args:
        music_file_path (str): The path to the music file.
        output_dir (str): The directory to save the BMP file.
    """
    try:
        if music_file_path.lower().endswith('.flac'):
            audio = FLAC(music_file_path)
            album_name = audio.get('album', [None])[0]
            pictures = audio.pictures
            if pictures:
                picture = pictures[0]
                image_data = picture.data
            else:
                image_data = None

        elif music_file_path.lower().endswith('.mp3'):
            audio = MP3(music_file_path, ID3=ID3)
            album_name = audio.get('TALB', [None])[0]
            if album_name:
                album_name = str(album_name)

            pictures = audio.tags.getall('APIC')
            if pictures:
                picture = pictures[0]
                image_data = picture.data
            else:
                image_data = None
        else:
            print(f"Unsupported file format for: {music_file_path}")
            return

        if not album_name:
            # Try track name instead
            album_name = audio.get("TIT2", [None])[0]
            if not album_name:
                # Default to cover
                album_name = "cover"

        if not image_data:
            print(f"No album art found for: {music_file_path}")
            return

        # Sanitize album name for filename
        sanitized_album_name = re.sub(r'[\\/:<>?*|]', '_', album_name)

        
        if len(output_dir) >= 255:
            raise ValueError(f"Output directory path is too long: {output_dir}")

        bmp_filename = os.path.join(output_dir, f"{sanitized_album_name}.bmp")

        if len(bmp_filename) >= 255:
            # Shorten the filename to fit within the 255 character limit
            max_len = 255 - len(output_dir) - len(os.path.sep) - len(".bmp")
            sanitized_album_name = sanitized_album_name[:max_len]
            bmp_filename = os.path.join(output_dir, f"{sanitized_album_name}.bmp")

        # Process image
        image = Image.open(io.BytesIO(image_data))
        resized_image = image.resize((output_size, output_size))
        resized_image.save(bmp_filename, 'BMP')
        print(f"Saved album art to: {bmp_filename}")

    except Exception as e:
        print(f"Error processing {music_file_path}: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Extract album art and convert to BMP.")
    parser.add_argument("input_path", help="The path to the music file or directory.")
    parser.add_argument("output_path", nargs="?", default=None, help="The directory to save the BMP file (optional).")
    parser.add_argument("-s", "--size", type=int, default=100, help="Size of the output BMP in pixels (e.g., 300 for 300x300).")
    
    args = parser.parse_args()

    input_path = args.input_path
    output_path = args.output_path
    size = args.size

    if output_path and not os.path.exists(output_path):
        os.makedirs(output_path)

    if os.path.isdir(input_path):
        for root, _, files in os.walk(input_path):
            for file in files:
                if file.lower().endswith(('.mp3', '.flac')):
                    music_file = os.path.join(root, file)
                    output_dir = output_path if output_path else root
                    extract_album_art(music_file, output_dir, size)
    elif os.path.isfile(input_path):
        output_dir = output_path if output_path else os.path.dirname(input_path)
        extract_album_art(input_path, output_dir, size)
    else:
        print(f"Input path not found: {input_path}")
        sys.exit(1)
