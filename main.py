from pytube import YouTube, Playlist
from django.utils.text import slugify
import os

################## EDIT THESE SETTINGS ###################################################################

# Root directory where all videos will go.
ROOT_DIR = 'C:\\users\\jake2\\youtube_videos'

# List of playlist URLs and option number of videos from each that you'd like to download.
PLAYLISTS = [
    {'url': 'https://youtube.com/playlist?list=PL4cUxeGkcC9hk02lFb6EkdXF2DYGl4Gg4', 'download_first': 3},
    {'url': 'https://youtube.com/playlist?list=PL4cUxeGkcC9gC88BEo9czgyS72A3doDeM'}
]

# List of singular video URLs
SINGLE_VIDEO_URLS = [
    'https://youtu.be/ZES3nJQYJok',
    'https://youtu.be/itRLRfuL_PQ'
]
#########################################################################################################


###################### SHOULDN'T HAVE TO EDIT THESE, BUT YOU CAN ########################################
PLAYLIST_DIR = os.path.join(ROOT_DIR, 'playlists')
SINGLE_VIDEO_DIR = os.path.join(ROOT_DIR, 'single_videos')
#########################################################################################################

if __name__ == '__main__':
    
    # Make sure every directory exists
    for directory in [ROOT_DIR, PLAYLIST_DIR, SINGLE_VIDEO_DIR]:
        if not os.path.exists(directory):
            os.mkdir(directory)

    # Download every single video if it isn't already downloaded
    for video_url in SINGLE_VIDEO_URLS:
        video_pointer = YouTube(video_url)
        filename = slugify(video_pointer.title) + '.mp4'
        
        if filename in os.listdir(SINGLE_VIDEO_DIR):
            print(f'The video {video_pointer.title} has already been downloaded and will be skipped.')
            continue

        video = video_pointer.streams.get_highest_resolution()
        print(f'Downloading {video.title}...')
        video.download(SINGLE_VIDEO_DIR, filename=filename)
        print('Done')

    # Download appropriate number of videos from each playlist
    for playlist in PLAYLISTS:

        playlist_obj = Playlist(playlist['url'])

        playlist_path = os.path.join(PLAYLIST_DIR, slugify(playlist_obj.title))
        if not os.path.exists(playlist_path):
            os.mkdir(playlist_path)

        download_limit = playlist.get('download_first')
        video_pointers = list(playlist_obj.videos)[:download_limit]

        for video_pointer in video_pointers:
            filename = slugify(video_pointer.title) + '.mp4'
            if filename in os.listdir(playlist_path):
                print(f'The video {video_pointer.title} has already been downloaded and will be skipped.')
                continue

            video = video_pointer.streams.get_highest_resolution()
            print(f'Downloading {video.title}...')
            video.download(playlist_path, filename=filename)
            print('Done.')

    print('Have a nice day, fuck face.')



