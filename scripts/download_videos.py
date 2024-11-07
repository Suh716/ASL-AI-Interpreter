import os
import yt_dlp as youtube_dl
import json
import subprocess
import random

# Load video data from the JSON file
with open('../data/MSASL_train.json', 'r') as f:
    data = json.load(f)

# Shuffle data to try different videos each time
random.shuffle(data)

# Create a directory to store the snippets if it doesn’t exist
output_folder = '../videos'
os.makedirs(output_folder, exist_ok=True)

# Function to download a video using yt-dlp
def download_video(url, output_path):
    ydl_opts = {
        'outtmpl': output_path,  # Save file to the specified output path
        'quiet': False,
        'cookiefile': '../data/www.youtube.com_cookies',  # Path to your cookies file
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',  # Specify mp4 format
        'merge_output_format': 'mp4'  # Ensure the output format is mp4
    }
    
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            return True
        except Exception as e:
            print(f"Failed to download {url}: {e}")
            return False

# Function to trim a video using ffmpeg
def trim_video(input_path, output_path, start_time, end_time):
    try:
        command = [
            'ffmpeg', '-y',  # Overwrite output file if it exists
            '-i', input_path,
            '-ss', str(start_time),
            '-to', str(end_time),
            '-c:v', 'libx264',  # Re-encode video using H.264 codec
            '-c:a', 'aac',      # Re-encode audio using AAC codec
            '-strict', 'experimental',
            output_path
        ]
        subprocess.run(command, check=True)
        print(f"Trimmed video saved to {output_path}")
    except Exception as e:
        print(f"Failed to trim video: {e}")

# Download and process videos until we have exactly 100 successful downloads
successful_downloads = 0
used_labels = set()

for video in data:
    if successful_downloads >= 100:  # Stop after 100 successful downloads
        break

    url = video['url']
    video_id = video['file']
    label_name = video['clean_text'].replace(" ", "_").replace("/", "-")
    start_time = video['start_time']
    end_time = video['end_time']

    # Skip if this label has already been used
    if label_name in used_labels:
        continue

    # Temporary path for the full video
    temp_video_path = os.path.join(output_folder, f"{video_id}_full.mp4")
    # Final path for the trimmed video snippet
    output_path = os.path.join(output_folder, f"{label_name}.mp4")

    # Download the full video
    if download_video(url, temp_video_path):
        # Trim the video to the specified snippet
        trim_video(temp_video_path, output_path, start_time, end_time)
        successful_downloads += 1
        used_labels.add(label_name)
        # Remove the full video to save space
        os.remove(temp_video_path)

print(f"Downloaded and trimmed {successful_downloads} video snippets successfully.")
