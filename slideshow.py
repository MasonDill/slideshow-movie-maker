import zipfile
import os
import shutil
import argparse
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from moviepy import *
from natsort import natsorted
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip, concatenate_audioclips

def create_slideshow(input_dir, audio_paths, output_path, image_duration=0.5, video_fps=30):
    if os.path.exists(input_dir):
        shutil.rmtree(input_dir)
    os.makedirs(input_dir)
    
    image_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
    image_files = natsorted(image_files)
    
    if not image_files:
        raise ValueError("No images found in " + str(input_dir))
    
    clips = [ImageClip(img, duration=1) for img in image_files]
    video = concatenate_videoclips(clips)
    
    # Handle multiple audio files
    audio_clips = [AudioFileClip(audio_path) for audio_path in audio_paths]
    final_audio = concatenate_audioclips(audio_clips)
    video.audio = final_audio
    
    video.write_videofile(
        filename=output_path,  # Fixed to use output_path instead of hardcoded value
        fps=video_fps
    )

    print(f"Slideshow video saved to: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a video slideshow from a .zip of images and audio files.")
    parser.add_argument("-p", "--zip_path", help="Path to the .zip file containing images.")
    parser.add_argument("-v", "--audio_paths", nargs='+', help="Paths to the audio files (mp4, mp3, flac).")
    parser.add_argument("-o", "--output_path", default="slideshow.mp4", help="Path to save the output video.")
    args = parser.parse_args()

    zip_path = args.zip_path
    audio_paths = args.audio_paths
    output_path = args.output_path

    if not zip_path or not audio_paths:
        Tk().withdraw()
        if not zip_path:
            zip_path = askopenfilename(filetypes=[("ZIP files", "*.zip")], title="Select image album")
        if not audio_paths:
            audio_paths = []
            while True:
                audio_path = askopenfilename(filetypes=[("Audio files", "*.mp4 *.mp3 *.flac")], 
                                          title="Select audio file (Cancel when done)")
                if not audio_path:
                    break
                audio_paths.append(audio_path)
    
    if not zip_path or not audio_paths:
        print("Both images and at least one audio file are required.")
        exit()
        
    create_slideshow(zip_path, audio_paths, output_path)
