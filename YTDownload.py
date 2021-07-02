from pytube import YouTube,Playlist
from moviepy.editor import *
import re
from os import remove

def downMP3(link):
   video = YouTube(link)
   save_dir = video.streams.get_highest_resolution().download(output_path=dir)
   print(save_dir)
   title = os.path.splitext(save_dir)
   turn_to_audio = VideoFileClip(save_dir)
   audio_clip = turn_to_audio.audio
   audio_clip.write_audiofile(save_dir[0:len(save_dir) - 1] + "3")
   turn_to_audio.close()
   os.remove(save_dir)

dir = "C:/Users/donal/Videos"
option = input("Do you want to download a video (1) or a playlist (2). If you want MP3, 3 is for video and 4 is for playlist:  ")
if option == "1":
   link = input("Input YT Link: ")
   video = YouTube(link)
   video.streams.get_highest_resolution().download(output_path= dir)
   print("Download Completed")
elif option == "2":
   link = input("Input Playlist Link: ")
   playlist = Playlist(link)
   for video_link in playlist.video_urls:
      video = YouTube(video_link)
      video.streams.get_highest_resolution().download(output_path= dir)
      print("Download Completed")
elif option == "3":
   link = input("Input YT Link: ")
   downMP3(link)
elif option == "4":
   link = input("Input Playlist Link: ")
   playlist = Playlist(link)
   for url in playlist.video_urls:
      downMP3(url)