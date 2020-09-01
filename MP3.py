from tkinter import *
from tkinter import filedialog
from pygame import mixer
from mutagen.mp3 import MP3
import os
import random
import codecs
import re
import time


class MusicPlayer:
    # This creates the window with the buttons to load, play, pause, and stop music
    def __init__(self, window):
        # Creates window and buttons
        window.geometry('400x250'); window.title("Brian's Player"); window.resizable(0,0)
        Load = Button(window, text='Load', width=10, font=('Times', 10), command=self.load)
        Next = Button(window, text='⏭', width=5, font=('Times', 11), command=self.next_song)
        Previous = Button(window, text='⏮', width=5, font=('Times', 11), command=self.previous_song)
        Play = Button(window, text='►', width=5, font=('Times', 11), command=self.play)
        Pause = Button(window, text='⏸', width=5, font=('Times', 11), command=self.pause)
        Stop = Button(window, text='⏹', width=5, font=('Times', 11), command=self.stop)
        Shuffle = Button(window, text='🔀', width=5, font=('Times', 11), command=self.shuffle)
        Volume = Scale(window, from_=0, to=1, showvalue=0, label='Volume', orient='horizontal', resolution=.01, command=self.vol)
        Song_Title = Listbox(window, bg="black", fg="white", width=25, height=1)
        Status_Bar = Label(window, text='', bd=1, relief=GROOVE, anchor=E)
        Music_Slider = Scale(window, from_=0, to=100, showvalue=0, orient='horizontal', command=self.slider, length=360)
        Music_Slider_Label = Label(window, text="0")
        # Button Positions
        Load.place(x=10, y=20); Play.place(x=200,y=80); Pause.place(x=250, y=80); Stop.place(x=150, y=80); 
        Shuffle.place(x=300, y=80); Volume.place(x=275, y=10); Song_Title.place(x=100, y=20); 
        Next.place(x=100, y=80); Previous.place(x=50, y=80); Status_Bar.pack(fill=X, side=BOTTOM, ipady=2)
        Music_Slider.place(x=10, y=150); Music_Slider_Label.place(x=190, y=200)
        
        self.music_file = False
        self.volume_slider = Volume
        self.volume_slider.set(1)
        self.music_slider = Music_Slider
        self.music_slider_label = Music_Slider_Label
        self.song_title = Song_Title
        self.list_of_songs = []
        self.playing_state = False
        self.status_bar = Status_Bar
        
    # Appends the music files to the attribute list_of_songs
    def list_song(self):
        mypath = os.getcwd() + '/Music'
        for path, subdir, files in os.walk(mypath):
            for name in files:
                if re.search('.*\.mp3', name):
                    self.list_of_songs.append(os.path.join(path, name)) 

    # This method loads the music file
    def load(self):
        self.remove_title()
        self.music_file = filedialog.askopenfilename(initialdir='Music/', filetypes=(("mp3 Files", "*.mp3"), ))
        if self.music_file:
            mixer.init()
            mixer.music.load(self.music_file)
            self.clean_name()
            mixer.music.play()
            self.song_length()
            
            # Update slider
            self.update_slider()
            
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
        self.music_file = False
        self.status_bar.config(text="")
        
    # Volume slider added
    def vol(self, event):
        v = Scale.get(self.volume_slider)
        mixer.music.set_volume(v)
    
    # Plays a random song from the Music directory
    def shuffle(self):
        self.remove_title()
        self.list_song()
        self.music_file = random.choice(self.list_of_songs)
        if self.music_file:
            mixer.init()
            mixer.music.load(self.music_file)
            self.clean_name()
            mixer.music.play()
            self.song_length()
            
            # Update slider to position
            self.update_slider()
    
    # Plays the next song            
    def next_song(self):
        self.remove_title()
        if self.music_file:
            self.list_song()
            next_one = self.list_of_songs.index(f'C:\\Users\\bbarr\\Desktop\\Computer_Exercises\\Python\\MP3_Player/Music\\{self.music_file}.mp3')
            self.music_file = self.list_of_songs[next_one + 1]
            mixer.music.load(self.music_file)
            self.clean_name()
            mixer.music.play()
            self.song_length()
    
    # Plays the previous song
    def previous_song(self):
        self.remove_title()
        if self.music_file:
            self.list_song()
            next_one = self.list_of_songs.index(f'C:\\Users\\bbarr\\Desktop\\Computer_Exercises\\Python\\MP3_Player/Music\\{self.music_file}.mp3')
            self.music_file = self.list_of_songs[next_one - 1]
            mixer.music.load(self.music_file)
            self.clean_name()
            mixer.music.play()
            self.song_length()
     
    # Adds a slider for the song that is currently playing    
    def slider(self, event):
        self.music_slider_label.config(text=f'{self.music_slider.get()} of {int(song_len)}')      
        
    # Gets the length of the song
    def song_length(self):
        # This grabs the current time of the song
        current_time = mixer.music.get_pos() / 1000
        
        # Converts the code above to time format
        convert_current_time = time.strftime('%M:%S', time.gmtime(current_time))
        
        if self.music_file:
            self.list_song()
            song = self.list_of_songs.index(f'C:\\Users\\bbarr\\Desktop\\Computer_Exercises\\Python\\MP3_Player/Music\\{self.music_file}.mp3')
            song = self.list_of_songs[song]
            # This loads song length with mutagen
            song_mutagen = MP3(song)
            # This gets the song length
            global song_len
            song_len = song_mutagen.info.length
            # This converts the song_mutagen into time format
            convert_song_len = time.strftime('%M:%S', time.gmtime(song_len))
            # Outputs the time to the status bar
            self.status_bar.config(text=f'Time Elapsed: {convert_current_time}  of  {convert_song_len}  ')
            # Update slider position value to current song position
            self.music_slider.set(current_time)
            # Updates time
            self.status_bar.after(1000, self.song_length)
        
    # Removes the title off the Listbox        
    def remove_title(self):
        if self.music_file:
            try:
                song = self.music_file
                item = self.song_title.get(END).index(song)
                self.song_title.delete(item)
            except:
                pass
            
    # strips off the file path and file extension on the title of song      
    def clean_name(self):
        if "C:\\Users\\bbarr\\Desktop\\Computer_Exercises\\Python\\MP3_Player/Music\\" in self.music_file:
            self.music_file = self.music_file.replace("C:\\Users\\bbarr\\Desktop\\Computer_Exercises\\Python\\MP3_Player/Music\\", "")
            self.music_file = self.music_file.replace(".mp3", "")
            self.song_title.insert(END, self.music_file)
            
        if "C:/Users/bbarr/Desktop/Computer_Exercises/Python/MP3_Player/Music/" in self.music_file:
            self.music_file = self.music_file.replace("C:/Users/bbarr/Desktop/Computer_Exercises/Python/MP3_Player/Music/", "")
            self.music_file = self.music_file.replace(".mp3", "")
            self.song_title.insert(END, self.music_file)
    
    # Updates the slider position
    def update_slider(self):
        slider_position = int(song_len)
        self.music_slider.config(to=slider_position)
        self.music_slider.set(0)
         
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