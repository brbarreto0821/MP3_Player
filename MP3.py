from tkinter import *
from tkinter import filedialog
from pygame import mixer

class MusicPlayer:
    # This creates the window with the buttons to load, play, pause, and stop music
    def __init__(self, window):
        window.geometry('320x100'); window.title("Brian's Player"); window.resizable(0,0)
        Load = Button(window, text='Load', width=10, font=('Times', 10), command=self.load)
        Play = Button(window, text='Play', width=10, font=('Times', 10), command=self.play)
        Pause = Button(window, text='Pause', width=10, font=('Times', 10), command=self.pause)
        Stop = Button(window, text='Stop', width=10, font=('Times', 10), command=self.stop)
        Load.place(x=0, y=20); Play.place(x=110,y=20); Pause.place(x=220, y=20); Stop.place(x=110, y=60)
        self.music_file = False
        self.playing_state = False

    # This method loads the music file
    def load(self):
        self.music_file = filedialog.askopenfilename()
    
    # This will play the music
    def play(self):
        if self.music_file:
            mixer.init()
            mixer.music.load(self.music_file)
            mixer.music.play()