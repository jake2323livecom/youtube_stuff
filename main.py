from pytube import YouTube, Playlist
from django.utils.text import slugify
import os

ROOT_DIR = 'C:\\users\\jake2\\youtube_videos'
PLAYLIST_URLS = [
    {'url': 'https://youtube.com/playlist?list=PL4cUxeGkcC9hk02lFb6EkdXF2DYGl4Gg4', 'download_first': 3},
    {'url': 'https://youtube.com/playlist?list=PL4cUxeGkcC9gC88BEo9czgyS72A3doDeM'}
]
SINGLE_VIDEO_URLS = [
    'https://youtu.be/ZES3nJQYJok',
    'https://youtu.be/itRLRfuL_PQ'
]


# Make sure all intended directories exist
PLAYLIST_DIR = os.path.join(ROOT_DIR, 'playlists')
SINGLE_VIDEO_DIR = os.path.join(ROOT_DIR, 'single_videos')

for directory in [ROOT_DIR, PLAYLIST_DIR, SINGLE_VIDEO_DIR]:
    if not os.path.exists(directory):
        os.mkdir(directory)

# Download every single video if it isn't already downloaded
for video_url in SINGLE_VIDEO_URLS:
    video_pointer = YouTube(video_url)
    filename = slugify(video_pointer.title) + '.mp4'
    
    if filename in os.listdir(SINGLE_VIDEO_DIR):
        print(f'The video {video_pointer.title} has already been downloaded and will be skipped.')
    else:
        video = video_pointer.streams.get_highest_resolution()
        print(f'Downloading {video.title}...')
        video.download(SINGLE_VIDEO_DIR, filename=filename)
        print('Done')

# Download appropriate number of videos from each playlist
for playlist in PLAYLIST_URLS:
    playlist_obj = Playlist(playlist['url'])
    playlist_path = os.path.join(PLAYLIST_DIR, slugify(playlist_obj.title))
    if not os.path.exists(playlist_path):
        os.mkdir(playlist_path)

    download_limit = playlist['download_first'] if playlist.get('download_first') else len(playlist_obj.videos)

    for index in range(download_limit):
        video_pointer = playlist_obj.videos[index]
        filename = slugify(video_pointer.title) + '.mp4'

        if filename in os.listdir(playlist_path):
            print(f'The video {video_pointer.title} has already been downloaded and will be skipped.')
            continue

        video = video_pointer.streams.get_highest_resolution()
        print(f'Downloading {video.title}...')
        video.download(playlist_path, filename=filename)
        print('Done.')

print('Have a nice day, fuck face.')



