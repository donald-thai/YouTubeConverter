from pytube import YouTube

link = "https://www.youtube.com/watch?v=g5CRtp5blTQ"
yt = YouTube(link)
print(yt.title)