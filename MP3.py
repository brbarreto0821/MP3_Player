from tkinter import *
from tkinter import filedialog
from pygame import mixer
import os
import random
import codecs

class MusicPlayer:
    # This creates the window with the buttons to load, play, pause, and stop music
    def __init__(self, window):
        window.geometry('325x200'); window.title("Brian's Player"); window.resizable(0,0)
        Load = Button(window, text='Load', width=10, font=('Times', 10), command=self.load)
        Play = Button(window, text='Play', width=10, font=('Times', 10), command=self.play)
        Pause = Button(window, text='Pause', width=10, font=('Times', 10), command=self.pause)
        Stop = Button(window, text='Stop', width=10, font=('Times', 10), command=self.stop)
        Shuffle = Button(window, text='Shuffle', width=10, font=('Times', 10), command=self.shuffle)
        Volume = Scale(window, label='Volume', orient='horizontal', command=self.vol)
        Load.place(x=10, y=20); Play.place(x=120,y=20); Pause.place(x=230, y=20); Stop.place(x=60, y=60); 
        Shuffle.place(x=175, y=60); Volume.place(x=10, y=120)
        self.music_file = False
        self.volume_slider = Volume
        self.list_of_songs = []
        self.playing_state = False

    # This method loads the music file
    def load(self):
        self.music_file = filedialog.askopenfilename()
        if self.music_file:
            mixer.init()
            mixer.music.load(self.music_file)
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
        
    # Volume slider added
    def vol(self, event):
        v = Scale.get(self.volume_slider)
        mixer.music.set_volume(v)
    
    # Plays a random song from the Music directory
    def shuffle(self):
        root = '.\Music'
        for path, subdirs, files in os.walk(root):
            for name in files:
                if name[0:] != '.mp3':
                    continue
                self.list_of_songs.append(os.path.join(path, name))
        random_song = random.choice(self.list_of_songs)
        mixer.music.play(random_song)
        
# Starts the application        
root = Tk()
player = MusicPlayer(root)
root.mainloop()