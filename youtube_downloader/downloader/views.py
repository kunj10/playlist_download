from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, TemplateDoesNotExist
from pytube import YouTube

from .forms import PlaylistForm
from pytube import Playlist
import os

def download_video(video_url, output_path='downloads', filename='downloaded_video.mp4'):
    try:
        # Create a YouTube object
        yt = YouTube(video_url)

        # Get the highest resolution stream
        video_stream = yt.streams.get_highest_resolution()

        # Set the output path
        output_path = os.path.join(output_path, filename)

        # Download the video, overwriting if the file already exists
        video_stream.download(output_path)

        return True, f'Download completed: {output_path}'

    except Exception as e:
        return False, f'Error: {str(e)}'

def download_playlist(request):
    template_path = 'downloader1/download_playlist.html'
    try:
        template = loader.get_template(template_path)
    except TemplateDoesNotExist:
        return HttpResponse(f"Template not found: {template_path}")

    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            playlist_url = form.cleaned_data['playlist_url']
            playlist = Playlist(playlist_url)

            # Create a directory for the playlist
            output_path = os.path.join('downloads', playlist.title)
            os.makedirs(output_path, exist_ok=True)

            # Download each video in the playlist
            for video_url in playlist.video_urls:
                success, message = download_video(video_url, output_path=output_path)
                if not success:
                    return HttpResponse(message)

            return render(request, 'downloader1/download_completed.html', {'playlist_title': playlist.title})
    else:
        form = PlaylistForm()

    return render(request, 'downloader1/download_playlist.html', {'form': form})
