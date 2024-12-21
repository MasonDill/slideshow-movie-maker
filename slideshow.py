import zipfile
import os
import shutil
import argparse
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from moviepy import *
from natsort import natsorted

def create_slideshow(input_dir, audio_path, output_path, image_duration=0.5, video_fps=30):
    if os.path.exists(input_dir):
        shutil.rmtree(input_dir)
    os.makedirs(input_dir)
    
    image_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
    image_files = natsorted(image_files)
    
    if not image_files:
        raise ValueError("No images found in " +str(input_dir))
    
    clips = [ImageClip(img, duration=1) for img in image_files]

    video = concatenate_videoclips(clips)
    audio = AudioFileClip(audio_path)
    video.audio = audio
    
    video.write_videofile(
        filename="output.mp4",
        fps=30
    )

    print(f"Slideshow video saved to: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a video slideshow from a .zip of images and a .mp4 file.")
    parser.add_argument("-p", "--zip_path", help="Path to the .zip file containing images.")
    parser.add_argument("-v", "--audio_path", help="Path to the audio file (mp4, mp3, flac).")
    parser.add_argument("-o", "--output_path", default="slideshow.mp4", help="Path to save the output video.")
    args = parser.parse_args()

    zip_path = args.zip_path
    video_path = args.audio_path
    output_path = args.output_path

    if not zip_path or not video_path:
        Tk().withdraw()
        if not zip_path:
            zip_path = askopenfilename(filetypes=[("ZIP files", "*.zip")], title="Select image album")
        if not video_path:
            audio_path = askopenfilename(filetypes=[("Audio files", "*.mp4 *.mp3 *.flac")])
    
    if not zip_path or not video_path:
        exit()
    create_slideshow(zip_path, video_path, output_path)
