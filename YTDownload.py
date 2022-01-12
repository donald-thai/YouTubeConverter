from __future__ import unicode_literals
import yt_dlp
from tkinter import Tk, Canvas, Button, Frame, Label, PhotoImage, Toplevel, Entry, Text, END, \
    Scrollbar, filedialog
from PIL import Image, ImageTk, ImageSequence
import glob


class Gif:
    def __init__(self, parent, gif_loc):
        self.parent = parent
        self.canvas = Canvas(parent, width = 480, height = 270, bg = "white",
                             highlightthickness = 0)
        self.canvas.place(relwidth = 1)
        self.sequence = [ImageTk.PhotoImage(img)
                         for img in ImageSequence.Iterator(
                Image.open(
                    gif_loc))]
        self.image = self.canvas.create_image(0, 0, image = self.sequence[0], anchor = "nw")
        self.animate(1)

    def animate(self, counter):
        self.canvas.itemconfig(self.image, image = self.sequence[counter])
        self.parent.after(35, lambda: self.animate((counter + 1) % len(self.sequence)))


class Welcome:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("YT Downloader by Donald Thai")
        self.parent.geometry("600x600")
        self.parent.resizable(width = False, height = False)

        self.picture = PhotoImage(file = "Pictures/Cherry Blossom Railroad.png")
        self.outside_pic = Label(self.parent, image = self.picture)
        self.outside_pic.place(relwidth = 1, relheight = 1)

        self.center_frame = Frame(parent, bg = "white", bd = 0)
        self.center_frame.place(relx = .1, rely = .1, relwidth = .8, relheight = .8)
        self.inside_pic = Label(self.center_frame, image = self.picture)
        self.inside_pic.place(relwidth = 1, relheight = 1)

        self.gif_frame = Frame(self.center_frame, bd = 0)
        self.gif_frame.place(relwidth = 1, relheight = .55)
        self.gif = Gif(self.gif_frame, "Gifs/cat-loading.gif")  # Maybe add a gif cycler?
        self.gif_num = 0
        self.gif_cycle_button = Button(self.parent, text = "Next", command = self.NextGif)
        self.gif_cycle_button.place(rely = .1, relwidth = .1, relheight = .05)

        self.video_button = Button(self.center_frame, text = "Download a video",
                                   command = self.OpenVidDown)
        self.video_button.place(relx = .3, rely = .6, relwidth = .4, relheight = .1)
        self.playlist_button = Button(self.center_frame, text = "Download a playlist",
                                      command = self.OpenPLDown)
        self.playlist_button.place(relx = .3, rely = .75, relwidth = .4, relheight = .1)

    def OpenVidDown(self):
        self.parent.withdraw()
        DownVid(self.parent)  # Pass main because Welcome (self) is not a widget (not a window)

    def OpenPLDown(self):
        self.parent.withdraw()
        DownPL(self.parent)

    def NextGif(self):
        gifs = glob.glob("Gifs/*.gif")
        total_gifs = len(gifs)
        self.gif_num += 1
        if self.gif_num == total_gifs:
            self.gif_num = 0
            self.gif = Gif(self.gif_frame, gifs[self.gif_num])
        else:
            self.gif = Gif(self.gif_frame, gifs[self.gif_num])


class DownVid(Toplevel):
    def __init__(self, parent):
        self.parent = parent
        Toplevel.__init__(self, self.parent)
        self.url = ""
        self.directory = ""
        self.geometry("551x600")
        self.title("Video Downloader")
        # self.resizable(width=False, height=False)

        self.picture = PhotoImage(file = "Pictures/space dog.png")
        self.outside_pic = Label(self, image = self.picture)
        self.outside_pic.place(relwidth = 1, relheight = 1)

        self.center_frame = Frame(self, bd = 0)
        self.center_frame.place(relx = .1, rely = .1, relwidth = .8, relheight = .8)

        self.inside_pic = Label(self.center_frame, image = self.picture)
        self.inside_pic.place(relwidth = 1, relheight = 1)

        self.enter_url = Entry(self.center_frame, bd = 0)
        self.enter_url.place(relwidth = .85, relheight = .05)
        self.get_url = Button(self.center_frame, text = "Get Url", command = self.getUrl)
        self.get_url.place(relx = .87, relwidth = .13, relheight = .05)

        self.vid_info = Text(self.center_frame, wrap = "word")
        self.vid_info.place(rely = .1, relwidth = .975, relheight = .65)
        scrollbar = Scrollbar(self.center_frame, command = self.vid_info.yview)
        scrollbar.place(relx = .975, rely = .1, relwidth = .025, relheight = .65)
        self.vid_info["yscrollcommand"] = scrollbar.set

        self.dir_button = Button(self.center_frame, text = "Download to",
                                 command = self.getDirectory)
        self.dir_button.place(rely = .8, relwidth = .25, relheight = .05)
        self.display_dir = Text(self.center_frame)
        self.display_dir.place(relx = .3, rely = .8, relwidth = .7, relheight = .05)

        self.download_mp4_button = Button(self.center_frame, text = "Download as MP4",
                                          command = self.downloadMP4)
        self.download_mp4_button.place(rely = .875, relwidth = .25, relheight = .05)
        self.download_mp3_button = Button(self.center_frame, text = "Download as MP3",
                                          command = self.downloadMP3)
        self.download_mp3_button.place(rely = .95, relwidth = .25, relheight = .05)
        self.download_results = Text(self.center_frame)
        self.download_results.place(relx = .3, rely = .875, relwidth = .7, relheight = .125)

        self.back_button = Button(self, text = "Back", command = self.goBack)
        self.back_button.place(relwidth = .1, relheight = .05)

        self.protocol("WM_DELETE_WINDOW", self.closing)

    def getUrl(self):
        self.vid_info.delete(1.0, END)
        self.url = self.enter_url.get()
        if self.url == "":
            self.vid_info.insert(END, "Sorry. Please enter a link.")
        else:
            with yt_dlp.YoutubeDL() as ydl:
                data = ydl.extract_info(self.url, download = False)
                title = data["title"]
                uploader = data["uploader"]
                views = data["view_count"]
                duration = data["duration"]  # In seconds
                if duration % 60 < 10:
                    seconds = "0" + str(duration % 60)
                else:
                    seconds = str(duration % 60)
                description = data["description"]
                format_info = f"Title: {title} \n" \
                              f"Uploaded By: {uploader} \n" \
                              f"View Count: {views} \n" \
                              f"Length: {int(duration / 60)}:{seconds} \n\n" \
                              f"{description}"
                self.vid_info.insert(END, format_info)

    def getDirectory(self):
        self.directory = filedialog.askdirectory()
        self.display_dir.delete(1.0, END)
        self.display_dir.insert(END, self.directory)

    def downloadMP4(self):
        self.download_results.delete(1.0, END)
        if self.directory != "":
            ydl_options = {
                # Don't download AV1 format vids
                "format": "bestvideo[ext=mp4][vcodec!*=av01]+bestaudio",
                "outtmpl": self.directory + "/%(title)s.%(ext)s"
            }
            with yt_dlp.YoutubeDL(ydl_options) as ydl:
                try:
                    ydl.download([self.url])
                    self.download_results.insert(END, "MP4 Download Complete!")
                except:
                    self.download_results.insert(END, "MP4 Download Failed.")
        else:
            self.download_results.insert(END, "Please choose a download location!")

    def downloadMP3(self):
        self.download_results.delete(1.0, END)
        if self.directory != "":
            ydl_options = {
                "format": "bestaudio",
                "outtmpl": self.directory + "/%(title)s.%(ext)s",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3"
                }]
            }
            with yt_dlp.YoutubeDL(ydl_options) as ydl:
                try:
                    ydl.download([self.url])
                    self.download_results.insert(END, "MP3 Download Complete!")
                except:
                    self.download_results.insert(END, "MP3 Download Failed.")
        else:
            self.download_results.insert(END, "Please choose a download location!")

    def goBack(self):
        self.withdraw()
        self.parent.deiconify()

    def closing(self):
        self.parent.destroy()  # Closes the main screen since it was just hidden before. Ensures that the program doesn't continue to run even after exitting the window.


class DownPL(Toplevel):
    def __init__(self,
                 parent):  # If this is the second window, then you can add a root variable to tell it where the root is (if it is not the parent) and then destroy it that way
        self.parent = parent
        Toplevel.__init__(self, self.parent)
        self.url = ""
        self.directory = ""
        self.geometry("551x600")
        self.title("Playlist Downloader")
        # self.resizable(width=False, height=False)

        self.picture = PhotoImage(file = "Pictures/space dog.png")
        self.outside_pic = Label(self, image = self.picture)
        self.outside_pic.place(relwidth = 1, relheight = 1)

        self.center_frame = Frame(self, bd = 0)
        self.center_frame.place(relx = .1, rely = .1, relwidth = .8, relheight = .8)

        self.inside_pic = Label(self.center_frame, image = self.picture)
        self.inside_pic.place(relwidth = 1, relheight = 1)

        self.enter_url = Entry(self.center_frame, bd = 0)
        self.enter_url.place(relwidth = .85, relheight = .05)
        self.get_url = Button(self.center_frame, text = "Get Url", command = self.getUrl)
        self.get_url.place(relx = .87, relwidth = .13, relheight = .05)

        self.vid_info = Text(self.center_frame, wrap = "word")
        self.vid_info.place(rely = .1, relwidth = .975, relheight = .65)
        scrollbar = Scrollbar(self.center_frame, command = self.vid_info.yview)
        scrollbar.place(relx = .975, rely = .1, relwidth = .025, relheight = .65)
        self.vid_info["yscrollcommand"] = scrollbar.set

        self.dir_button = Button(self.center_frame, text = "Download to",
                                 command = self.getDirectory)
        self.dir_button.place(rely = .8, relwidth = .25, relheight = .05)
        self.display_dir = Text(self.center_frame)
        self.display_dir.place(relx = .3, rely = .8, relwidth = .7, relheight = .05)

        self.download_mp4_button = Button(self.center_frame, text = "Download as MP4",
                                          command = self.downloadMP4)
        self.download_mp4_button.place(rely = .875, relwidth = .25, relheight = .05)
        self.download_mp3_button = Button(self.center_frame, text = "Download as MP3",
                                          command = self.downloadMP3)
        self.download_mp3_button.place(rely = .95, relwidth = .25, relheight = .05)
        self.download_results = Text(self.center_frame)
        self.download_results.place(relx = .3, rely = .875, relwidth = .7, relheight = .125)

        self.back_button = Button(self, text = "Back", command = self.goBack)
        self.back_button.place(relwidth = .1, relheight = .05)

        self.protocol("WM_DELETE_WINDOW", self.closing)

    def getUrl(self):
        self.vid_info.delete(1.0, END)
        self.url = self.enter_url.get()
        if self.url == "":
            self.vid_info.insert(END, "Sorry. Please enter a link.")
        else:
            self.vid_info.insert(END, "VIDEOS IN PLAYLIST \n\n")
            with yt_dlp.YoutubeDL() as ydl:
                data = ydl.extract_info(self.url, download = False)
                for video in data["entries"]:
                    title = video["title"]
                    uploader = video["uploader"]
                    views = video["view_count"]
                    duration = video["duration"]  # In seconds
                    if duration % 60 < 10:
                        seconds = "0" + str(duration % 60)
                    else:
                        seconds = str(duration % 60)
                    format_info = f"Title: {title} \n" \
                                  f"Uploaded By: {uploader} \n" \
                                  f"Views: {views} \n" \
                                  f"Length: {int(duration / 60)}:{seconds} \n" \
                                  f"----------------------------------------------------- \n"
                    self.vid_info.insert(END, format_info)

    def getDirectory(self):
        self.directory = filedialog.askdirectory()
        self.display_dir.delete(1.0, END)
        self.display_dir.insert(END, self.directory)

    def downloadMP4(self):
        self.download_results.delete(1.0, END)
        if self.directory != "":
            ydl_options = {
                # Don't download AV1 format vids
                "format": "bestvideo[ext=mp4][vcodec!*=av01]+bestaudio",
                "ignoreerrors": True,
                "outtmpl": self.directory + "/%(playlist_title)s/%(title)s.%(ext)s"
            }
            with yt_dlp.YoutubeDL(ydl_options) as ydl:
                ydl.download([self.url])
                self.download_results.insert(END, "MP4 Download Complete!")
        else:
            self.download_results.insert(END, "Please choose a download location!")

    def downloadMP3(self):
        self.download_results.delete(1.0, END)
        if self.directory != "":
            ydl_options = {
                "format": "bestaudio",
                "ignoreerrors": True,
                "outtmpl": self.directory + "/%(playlist_title)s audio/%(title)s.%(ext)s",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3"
                }]
            }
            with yt_dlp.YoutubeDL(ydl_options) as ydl:
                ydl.download([self.url])
                self.download_results.insert(END, "MP3 Download Complete!")
        else:
            self.download_results.insert(END, "Please choose a download location!")

    def goBack(self):
        self.destroy()
        self.parent.deiconify()

    def closing(self):
        self.parent.destroy()


def main():
    # ctypes.windll.shcore.SetProcessDpiAwareness(1)
    main = Tk()
    Welcome(main)
    main.mainloop()


if __name__ == "__main__":
    main()
