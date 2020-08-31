from tkinter import *
from tkinter import filedialog
from pygame import mixer
import os
import random
import codecs
import re

class MusicPlayer:
    # This creates the window with the buttons to load, play, pause, and stop music
    def __init__(self, window):
        # Creates window and buttons
        window.geometry('400x200'); window.title("Brian's Player"); window.resizable(0,0)
        Load = Button(window, text='Load', width=10, font=('Times', 10), command=self.load)
        Next = Button(window, text='⏭', width=5, font=('Times', 11), command=self.next_song)
        Previous = Button(window, text='⏮', width=5, font=('Times', 11), command=self.previous_song)
        Play = Button(window, text='►', width=5, font=('Times', 11), command=self.play)
        Pause = Button(window, text='⏸', width=5, font=('Times', 11), command=self.pause)
        Stop = Button(window, text='⏹', width=5, font=('Times', 11), command=self.stop)
        Shuffle = Button(window, text='🔀', width=5, font=('Times', 11), command=self.shuffle)
        Volume = Scale(window, from_=0, to=1, label='Volume', orient='horizontal', resolution=.01, command=self.vol)
        Song_Title = Listbox(window, bg="black", fg="white", width=25, height=1)
        
        # Button Positions
        Load.place(x=10, y=20); Play.place(x=200,y=80); Pause.place(x=250, y=80); Stop.place(x=150, y=80); 
        Shuffle.place(x=300, y=80); Volume.place(x=10, y=120); Song_Title.place(x=100, y=20); 
        Next.place(x=100, y=80); Previous.place(x=50, y=80)
        
        self.music_file = False
        Volume.set(1)
        self.volume_slider = Volume
        self.song_title = Song_Title
        self.list_of_songs = []
        self.playing_state = False
        
    # Appends the music files to the attribute list_of_songs
    def list_song(self):
        mypath = os.getcwd() + '/Music'
        for path, subdir, files in os.walk(mypath):
            for name in files:
                if re.search('.*\.mp3', name):
                    self.list_of_songs.append(os.path.join(path, name)) 

    # This method loads the music file
    def load(self):
        self.music_file = filedialog.askopenfilename(initialdir='Music/', filetypes=(("mp3 Files", "*.mp3"), ))
        if self.music_file:
            mixer.init()
            mixer.music.load(self.music_file)
            
            # strips the file path and file extionsion off the title of song
            self.music_file = self.music_file.replace("C:/Users/bbarr/Desktop/Computer_Exercises/Python/MP3_Player/Music/", "")
            self.music_file = self.music_file.replace(".mp3", "")
            self.song_title.insert(END, self.music_file)
            
            mixer.music.play()
    
    # This will play the music
    def play(self):
        if self.playing_state:
            mixer.music.unpause()
            self.playing_state = False        

    # Pauses the music
    def pause(self):
        if not self.playing_state:
            mixer.music.pause()
            self.playing_state = True
         
    # Stops the music from playing        
    def stop(self):
        mixer.music.stop()
        try:
            song = self.music_file
            item = self.song_title.get(END).index(song)
            self.song_title.delete(item)
        except:
            pass
        
    # Volume slider added
    def vol(self, event):
        v = Scale.get(self.volume_slider)
        mixer.music.set_volume(v)
    
    # Plays a random song from the Music directory
    def shuffle(self):
        # Removes current song on the Listbox
        if self.music_file:
            try:
                song = self.music_file
                item = self.song_title.get(END).index(song)
                self.song_title.delete(item)
            except:
                pass
        self.list_song()
        self.music_file = random.choice(self.list_of_songs)
        if self.music_file:
            mixer.init()
            mixer.music.load(self.music_file)
            
            # strips off the file path and file extension on the title of song
            self.music_file = self.music_file.replace("C:\\Users\\bbarr\\Desktop\\Computer_Exercises\\Python\\MP3_Player/Music\\", "")
            self.music_file = self.music_file.replace(".mp3", "")
            self.song_title.insert(END, self.music_file)
            
            mixer.music.play()
    
    # Plays the next song            
    def next_song(self):
        # Removes current song on the Listbox
        if self.music_file:
            try:
                song = self.music_file
                item = self.song_title.get(END).index(song)
                self.song_title.delete(item)
            except:
                pass
        if self.music_file:
            self.list_song()
            next_one = self.list_of_songs.index(f'C:\\Users\\bbarr\\Desktop\\Computer_Exercises\\Python\\MP3_Player/Music\\{self.music_file}.mp3')
            self.music_file = self.list_of_songs[next_one + 1]
            mixer.music.load(self.music_file)
            
            # strips off the file path and file extension on the title of song
            self.music_file = self.music_file.replace("C:\\Users\\bbarr\\Desktop\\Computer_Exercises\\Python\\MP3_Player/Music\\", "")
            self.music_file = self.music_file.replace(".mp3", "")
            self.song_title.insert(END, self.music_file)
            
            mixer.music.play()
    
    # Plays the previous song
    def previous_song(self):
        # Removes current song on the Listbox
        if self.music_file:
            try:
                song = self.music_file
                item = self.song_title.get(END).index(song)
                self.song_title.delete(item)
            except:
                pass
        if self.music_file:
            self.list_song()
            next_one = self.list_of_songs.index(f'C:\\Users\\bbarr\\Desktop\\Computer_Exercises\\Python\\MP3_Player/Music\\{self.music_file}.mp3')
            self.music_file = self.list_of_songs[next_one - 1]
            mixer.music.load(self.music_file)
            
            # strips off the file path and file extension on the title of song
            self.music_file = self.music_file.replace("C:\\Users\\bbarr\\Desktop\\Computer_Exercises\\Python\\MP3_Player/Music\\", "")
            self.music_file = self.music_file.replace(".mp3", "")
            self.song_title.insert(END, self.music_file)
            
            mixer.music.play()

# Window prompt that asks if you want to quit                    
def closing_window():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        mixer.init()
        mixer.music.stop()
        root.destroy()
                 
# Starts the application        
root = Tk()
player = MusicPlayer(root)
root.protocol("WM_DELETE_WINDOW", closing_window)
root.mainloop()
