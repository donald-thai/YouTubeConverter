from __future__ import unicode_literals
from pytube import YouTube,Playlist
import youtube_dl
from moviepy.editor import *

from os import remove
from tkinter import *
from PIL import Image, ImageTk, ImageSequence

# class Gif:
#    def __init__(self, parent):
#       self.parent = parent
#       self.canvas = Canvas(parent, width=480, height=270, bg="white", highlightthickness=0)
#       self.canvas.place(relwidth=1)
#       self.sequence = [ImageTk.PhotoImage(img)
#                        for img in ImageSequence.Iterator(
#             Image.open(
#                r'C:/Users/donal/Videos/HEYHEYHEY.gif'))]
#       self.image = self.canvas.create_image(0, 0, image=self.sequence[0], anchor="nw")
#       self.animate(1)
#
#    def animate(self, counter):
#       self.canvas.itemconfig(self.image, image=self.sequence[counter])
#       self.parent.after(35, lambda: self.animate((counter + 1) % len(self.sequence)))
#
#
# class Welcome:
#    def __init__(self,parent):
#       self.parent = parent
#       self.parent.title("YT Downloader by Donald Thai")
#       self.parent.geometry("600x600")
#       self.parent.resizable(width=False, height=False)
#
#       self.picture = PhotoImage(file = "Cherry Blossom Railroad.png")
#       self.outside_pic = Label(self.parent, image = self.picture)
#       self.outside_pic.place(relwidth=1, relheight=1)
#
#       self.center_frame = Frame(parent, bg="white", bd=0)
#       self.inside_pic = Label(self.center_frame, image = self.picture)
#       self.inside_pic.place(relwidth=1, relheight=1)
#       self.gif_frame = Frame(self.center_frame, bd=0)
#       self.gif_frame.place(relwidth=1, relheight=.55)
#       self.gif = Gif(self.gif_frame) #Maybe add a gif cycler?
#       self.center_frame.place(relx=.1 , rely =.1, relwidth= .8, relheight=.8)
#       self.video_button = Button(self.center_frame, text = "Download a video")
#       self.video_button.place(relx = .3, rely=.6, relwidth = .4, relheight = .1)
#       self.playlist_button = Button(self.center_frame, text="Download a playlist")
#       self.playlist_button.place(relx=.3, rely = .75, relwidth=.4, relheight=.1)
#
#
#
#
# main = Tk()
# opening_screen = Welcome(main)
# main.mainloop()









# def downMP3(link):
#    video = YouTube(link)
#    save_dir = video.streams.get_highest_resolution().download(output_path=dir)
#    print(save_dir)
#    title = os.path.splitext(save_dir)
#    turn_to_audio = VideoFileClip(save_dir)
#    audio_clip = turn_to_audio.audio
#    audio_clip.write_audiofile(save_dir[0:len(save_dir) - 1] + "3")
#    turn_to_audio.close()
#    os.remove(save_dir)

dir = "C:/Users/donal/Videos"
option = input("Do you want to download a video (1) or a playlist (2). If you want MP3, 3 is for video and 4 is for playlist:  ")
if option == "1":
   link = input("Input YT Link: ")
   ydl_opts = {
      "outtmpl": dir + "/%(title)s.%(ext)s"
   }
   with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      ydl.download([link])

elif option == "2":
   link = input("Input Playlist Link: ")
   ydl_opts = {
      "format": "bestvideo[ext=mp4][vcodec!*=av01]+bestaudio", #Do not download av1 format videos
      "outtmpl": dir + "/%(playlist_title)s/%(title)s.%(ext)s"
   }
   with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      ydl.download([link])


elif option == "3":
   link = input("Input YT Link: ")
   # downMP3(link)
   ydl_opts = {
      "format": "bestaudio",
      "outtmpl": dir + "/%(title)s.%(ext)s",
      "postprocessors": [{
         "key": "FFmpegExtractAudio",
         "preferredcodec": "mp3"
      }]
   }
   with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      ydl.download([link])




elif option == "4":
   link = input("Input Playlist Link: ")
   ydl_opts = {
      "format": "bestaudio",
      "outtmpl": dir + "/%(playlist_title)s audio/%(title)s.%(ext)s",
      "postprocessors": [{
         "key": "FFmpegExtractAudio",
         "preferredcodec": "mp3"
      }]
   }
   with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      ydl.download([link])


