from pytube import YouTube, Playlist
import os
from django.utils.text import slugify

# Edit these settings only
DOWNLOAD_PATH = 'C:/users/jake2/youtube'
PLAYLIST_FOLDER = 'playlists'
SINGLE_VIDEOS_FOLDER = 'single_videos'
SINGLE_VIDEO_URLS = [
    'https://youtu.be/OUK4qNvP0Dc'
]
PLAYLIST_URLS = [
    'https://youtube.com/playlist?list=PL4cUxeGkcC9gC88BEo9czgyS72A3doDeM'
]



if __name__ == '__main__':
    
    # Create full paths for single videos and playlists
    PLAYLIST_PATH = os.path.join(DOWNLOAD_PATH, PLAYLIST_FOLDER)
    SINGLE_VIDEOS_PATH = os.path.join(DOWNLOAD_PATH, SINGLE_VIDEOS_FOLDER)

    # Make sure all paths exist
    if not os.path.exists(DOWNLOAD_PATH):
        os.mkdir(DOWNLOAD_PATH)

    if not os.path.exists(PLAYLIST_PATH):
        os.mkdir(PLAYLIST_PATH)

    if not os.path.exists(SINGLE_VIDEOS_PATH):
        os.mkdir(SINGLE_VIDEOS_PATH)


    for video_url in SINGLE_VIDEO_URLS:

        yt = YouTube(video_url)

        filename = slugify(yt.title) + '.mp4'
        if filename in os.listdir(SINGLE_VIDEOS_PATH):
            print(f'The video {filename} has already been downloaded. Skipping to the next one.')
            continue

        video = yt.streams.get_highest_resolution()

        video.download(SINGLE_VIDEOS_PATH, filename=filename)


    for playlist_url in PLAYLIST_URLS:
        p = Playlist(playlist_url)
        owner = p.owner
        title = p.title
        
        full_playlist_path = os.path.join(PLAYLIST_PATH, slugify(f'{title} by {owner}'))

        if not os.path.exists(full_playlist_path):
            os.mkdir(full_playlist_path)

        for video in p.videos:

            filename = slugify(video.title) + '.mp4'

            if filename in os.listdir(full_playlist_path):
                print(f'The video {filename} already exists in the playlist folder for {title}.  Skipping this video.')
                continue

            video = video.streams.get_highest_resolution()

            print(f'Downloading video: {video.title}')
            video.download(full_playlist_path, filename=filename)
