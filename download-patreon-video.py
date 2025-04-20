import os
import subprocess
import re

def download_patreon_video(post_id):
    URL = f"https://www.patreon.com/posts/{post_id}"

    resolution_id = "bv+ba/b"
    
    # Specify output directory and filename
    output_path = "~/patreon/%(title)s.%(ext)s"
    
    download_command = ["yt-dlp", "--cookies", "cookies.txt", URL, "-f", resolution_id, "-o", output_path]
    subprocess.run(download_command)

if __name__ == "__main__":
    post_id = input("Enter post id: ")
    download_patreon_video(post_id)

