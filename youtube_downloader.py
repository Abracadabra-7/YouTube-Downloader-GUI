import tkinter as tk
from tkinter import filedialog
from pytube import YouTube, Playlist
import os

def download_video():
    url = url_entry.get()

    # Check if the URL is a playlist URL
    if "playlist" in url:
        try:
            # Create a YouTube playlist object
            playlist = Playlist(url)

            # Loop through all the videos in the playlist
            for video_url in playlist.video_urls:
                # Create a YouTube object for the current video
                yt = YouTube(video_url)

                # Get the selected video quality
                selected_quality = quality_choices.get()

                if selected_quality == "Audio Only":
                    # Get the audio stream
                    audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()

                    # Get the download directory from the user input
                    download_directory = directory_entry.get()

                    # Download the audio to the selected directory as an MP3 file
                    audio_stream.download(download_directory)
                    file_name = audio_stream.default_filename
                    base, ext = file_name.split('.')
                    new_file_name = f"{base}.mp3"
                    os.rename(os.path.join(download_directory, file_name), os.path.join(download_directory, new_file_name))

                    # Display a success message
                    status_label.config(text=f"Downloaded {yt.title} audio successfully!")
                else:
                    # Get the video stream with the selected quality
                    video_stream = None
                    if selected_quality == "Low":
                        video_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').asc().first()
                    elif selected_quality == "Medium":
                        video_stream = yt.streams.filter(progressive=True, file_extension='mp4', res='360p').order_by('resolution').asc().first()
                    elif selected_quality == "High":
                        video_stream = yt.streams.filter(progressive=True, file_extension='mp4', res='720p').order_by('resolution').asc().first()

                    # Get the download directory from the user input
                    download_directory = directory_entry.get()

                    # Download the video to the selected directory
                    video_stream.download(download_directory)

                    # Display a success message
                    status_label.config(text=f"Downloaded {yt.title} video successfully!")
        except Exception as e:
            # Display an error message
            status_label.config(text=f"Error downloading playlist: {str(e)}")
    else:
        try:
            # Create a YouTube object
            yt = YouTube(url)

            # Get the selected video quality
            selected_quality = quality_choices.get()

            if selected_quality == "Audio Only":
                # Get the audio stream
                audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()

                # Get the download directory from the user input
                download_directory = directory_entry.get()

                # Download the audio to the selected directory as an MP3 file
                audio_stream.download(download_directory)
                file_name = audio_stream.default_filename
                base, ext = file_name.split('.')
                new_file_name = f"{base}.mp3"
                os.rename(os.path.join(download_directory, file_name), os.path.join(download_directory, new_file_name))

                # Display a success message
                status_label.config(text="Downloaded audio successfully!")
            else:
                # Get the video stream with the selectedquality
                video_stream = None
                if selected_quality == "Low":
                    video_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').asc().first()
                elif selected_quality == "Medium":
                    video_stream = yt.streams.filter(progressive=True, file_extension='mp4', res='360p').order_by('resolution').asc().first()
                elif selected_quality == "High":
                    video_stream = yt.streams.filter(progressive=True, file_extension='mp4', res='720p').order_by('resolution').asc().first()

                # Get the download directory from the user input
                download_directory = directory_entry.get()

                # Download the video to the selected directory
                video_stream.download(download_directory)

                # Display a success message
                status_label.config(text="Video downloaded successfully!")
        except Exception as e:
            # Display an error message
            status_label.config(text=f"Error: {str(e)}")

def choose_directory():
    # Open a file browser to choose the download directory
    download_directory = filedialog.askdirectory()
    directory_entry.delete(0, tk.END)
    directory_entry.insert(0, download_directory)

# Create the main window
window = tk.Tk()
window.title("YouTube Downloader")

# Create the URL label and entry box
url_label = tk.Label(text="Enter the YouTube video or playlist URL:")
url_label.pack()
url_entry = tk.Entry(width=50)
url_entry.pack()

# Create the quality labeland dropdown box
quality_label = tk.Label(text="Select the video quality:")
quality_label.pack()
quality_choices = tk.StringVar(window)
quality_choices.set("High") # default value
quality_dropdown = tk.OptionMenu(window, quality_choices, "Low", "Medium", "High", "Audio Only")
quality_dropdown.pack()

# Create the directory label, entry box, and button
directory_label = tk.Label(text="Select the download directory:")
directory_label.pack()
directory_entry = tk.Entry(width=50)
directory_entry.pack()
directory_button = tk.Button(text="Choose", command=choose_directory)
directory_button.pack()

# Create the download button and status label
download_button = tk.Button(text="Download", command=download_video)
download_button.pack()
status_label = tk.Label(text="")
status_label.pack()

# Run the window loop
window.mainloop()
