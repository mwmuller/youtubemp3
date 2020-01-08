import youtube_dl
import sys
import os.path
import os
ydl_opts = None
sys.path.append("/PythonMusic")
os.chdir(os.path.dirname(os.path.realpath(__file__)) + "/PythonMusic")
def define_opts(codec):
    global ydl_opts
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': codec,
            'preferredquality': '320',
        }],
        'nocheckcertificate': True,
    }

def DownloadFromFile():
    ModifiedLines = [] # Used to store which links did not download
    define_opts('mp3')
    name = ""
    with open('mp3.txt', "r") as mp3r:
        lines = mp3r.readlines()
        for line in lines:
            try:
                url = line.split(' - ')
                Rename = url[1].strip()
                url = url[0]
                print(Rename)
            except:
                url = line
            if len(url) < 5:
                break
            print("Downloading: %s" % url)
            try:
                goodurl = download_no_matter_what(url)
                name = "_-" 
                name += url.split('=')[1]
                name += ".mp3"
                Rename += ".mp3"
                os.rename(name, Rename)
            except:
                if os.path.isfile(name):
                    os.remove(name)
                    print("File name is already used. Deleting downloaded file")
                else:
                    print("URL: %s\nWas broken." % url)
                    ModifiedLines.append(line)
    with open('mp3.txt', "w") as mp3w:
        mp3w.writelines(ModifiedLines)

def download_no_matter_what(url):
    try:
        youtube_dl.YoutubeDL(ydl_opts).download([url])
        return True
    except OSError:
        download_no_matter_what(url)
        return True
    except KeyboardInterrupt:
        sys.exit()
    except:
        return False

def ManualEnter():
    end = False # continue the loop while false
    while end == False:
        mp34 = 0
        goodurl = False
        while mp34 == 0:
            mp34 = input("Would you like to download (1)mp3 or (2)mp4? ")
            if int(mp34) == 1:
                codec = 'mp3'
            elif int(mp34) == 2:
              codec = 'mp4'
            else:
                print("Invalid selection.")
                mp34 = 0
        while not goodurl:   
            URL = input("Enter the URL of the youtube audio you would like to download: ")
            define_opts(codec)
            try:
                goodurl = download_no_matter_what(URL)
            except:
                print("The URL provided is broken, you have no connection, or it was invalid.")
        endit = "" 
        while endit is not "y" and endit is not "n":
            endit = input("Download another? (Y/N)")
            if endit.lower() == "y":
                end = False
            elif endit.lower() == "n":
                end = True

if __name__ == "__main__":
    codec = 'mp3' # assume mp3 as initial value
    mp34 = 0 # selection
    endit = "g" # Random value
    goodurl = False # Assume bad URL
    while 1:
        fileuse = input("(1) Download from URLs in File\n(2) Manual Enter\n(3) End\n")
        if int(fileuse) == 1:
            choosefile = input("(1) MP3 File\n(2) MP4 File\n(3) End\n")
            if int(choosefile) == 1:
                DownloadFromFile()
        elif int(fileuse) == 2:
            ManualEnter()
        elif int(fileuse) == 3:
            exit()
    
            