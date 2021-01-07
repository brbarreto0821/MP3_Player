from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import tkinter.ttk as ttk
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
        Music_Slider = ttk.Scale(window, from_=0, to=100, value=0, orient='horizontal', command=self.slider, length=360)
       
        # Button Positions
        Load.place(x=10, y=20); Play.place(x=200,y=80); Pause.place(x=250, y=80); Stop.place(x=150, y=80); 
        Shuffle.place(x=300, y=80); Volume.place(x=275, y=10); Song_Title.place(x=100, y=20); 
        Next.place(x=100, y=80); Previous.place(x=50, y=80); Status_Bar.pack(fill=X, side=BOTTOM, ipady=2);
        Music_Slider.place(x=10, y=150); 
        
        self.music_file = False
        self.volume_slider = Volume
        self.volume_slider.set(1)
        self.music_slider = Music_Slider
        self.song_title = Song_Title
        self.list_of_songs = []
        self.playing_state = False
        self.status_bar = Status_Bar
        
        # Fixes double skipping
        self.stopped = False
        self.next = False
        self.previous = False
        self.count = 0


# -------------------------------------------------------------    
# The methods below are used to prevent DRY for the code below
# -------------------------------------------------------------       
    
    # Appends the music files to the attribute list_of_songs
    def list_song(self):
        mypath = directory + '/Music'   # directory is global. It is on line #319
        for path, subdir, files in os.walk(mypath):
            for name in files:
                if re.search('.*\.mp3', name):
                    self.list_of_songs.append(os.path.join(path, name)) 
                    
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
        if "MP3_Player/Music" in self.music_file:
            self.music_file = self.music_file.replace("/", "\\")
            self.music_file = self.music_file.replace(directory + '\\Music', "")
            self.music_file = self.music_file.replace("\\", "")
            self.music_file = self.music_file.replace("/", "")
            self.music_file = self.music_file.replace(".mp3", "")
            self.song_title.insert(END, self.music_file)           
    
    # Updates the slider position
    def update_slider(self):
        slider_position = int(song_len)
        self.music_slider.config(to=slider_position, value=int(current_time))
    
    # This resets slider and status bar    
    def reset_slider(self):    
        self.status_bar.config(text="")
        self.music_slider.config(value=0)
        self.play()
        
        
#----------------------------------------------------------------
# The methods below are all the buttons and sliders for the app
#----------------------------------------------------------------

    # This loads the music file
    def load(self):
        if not self.music_file: 
            self.music_file = filedialog.askopenfilename(initialdir='Music/', filetypes=(("mp3 Files", "*.mp3"), )) 
            if self.music_file == "":
                pass
            else:
                mixer.music.load(self.music_file)
                self.clean_name()
                mixer.music.play()      
        
        else:
            new_music_file = False
            new_music_file = filedialog.askopenfilename(initialdir='Music/', filetypes=(("mp3 Files", "*.mp3"), ))
            if new_music_file:
                self.remove_title()
                self.reset_slider()
                self.music_file = new_music_file
                mixer.music.load(self.music_file)
                self.clean_name()
                mixer.music.play()
            else:
                pass

        self.song_length() 
        self.count += 1      # Double skip fix
        
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
        self.count = 0      
        # This resets slider and status bar
        self.status_bar.config(text="")
        self.music_slider.config(value=0)
        # This will stop the song
        mixer.music.stop()
        try:
            # This will remove the title of the song off the Listbox when the stop button is pushed
            song = self.music_file
            item = self.song_title.get(END).index(song)
            self.song_title.delete(item)
        except:
            pass
        self.music_file = False
        
        # Double skip fix
        self.stopped = True
        
        
    # Volume slider added
    def vol(self, event):
        v = Scale.get(self.volume_slider)
        mixer.music.set_volume(v)
    
    # Plays a random song from the Music directory
    def shuffle(self):
        self.reset_slider()
        self.remove_title()
        self.list_song()
        self.music_file = random.choice(self.list_of_songs)
        if self.music_file:
            mixer.music.load(self.music_file)
            self.clean_name()
            mixer.music.play()
            self.song_length()
            # Update slider to position
            #self.update_slider()
        
        # Double skip fix    
        self.count += 1
            
    # Plays the next song            
    def next_song(self):
        self.reset_slider()
        self.remove_title()
        if self.music_file:
            self.list_song()
            next_one = self.list_of_songs.index(f'{directory}/Music\\{self.music_file}.mp3')
            self.music_file = self.list_of_songs[next_one + 1]
            mixer.music.load(self.music_file)
            self.clean_name()
            mixer.music.play()
            self.song_length()
        else:
            return
        # double skip fix
        self.next = True
                
    # Plays the previous song
    def previous_song(self):
        self.reset_slider()
        self.remove_title()
        if self.music_file:
            self.list_song()
            next_one = self.list_of_songs.index(f'{directory}/Music\\{self.music_file}.mp3')
            self.music_file = self.list_of_songs[next_one - 1]
            mixer.music.load(self.music_file)
            self.clean_name()
            mixer.music.play()
            self.song_length()
        else:
            return
        # double skip fix
        self.previous = True
        
    # Adds a slider for the song that is currently playing    
    def slider(self, event):
        song = self.song_title.get(ACTIVE)
        song = f'{directory}/Music\\{self.music_file}.mp3'
        mixer.music.load(song)
        mixer.music.play(start=int(self.music_slider.get()))
        
    # Gets the length of the song for the slider and status bar
    # Also gives functionality to the music slider
    def song_length(self):
        # Fixes double skipping
        if self.stopped:
            self.stopped = False
            return
        
        if self.next:
            self.next = False
            return
        
        if self.previous:
            self.previous = False
            return
        
        if self.count > 1:
            self.count = 1
            return
            
        # This grabs the current time of the song
        global current_time
        current_time = mixer.music.get_pos() / 1000
        
        # Converts the code above to time format
        convert_current_time = time.strftime('%M:%S', time.gmtime(current_time))
        
        if self.music_file:
            self.list_song()
            song = self.list_of_songs.index(f'{directory}/Music\\{self.music_file}.mp3')
            song = self.list_of_songs[song]
            # This loads song length with mutagen
            song_mutagen = MP3(song)
            # This gets the song length
            global song_len
            song_len = song_mutagen.info.length
            # This converts the song_mutagen into time format
            convert_song_len = time.strftime('%M:%S', time.gmtime(song_len))
            
            # updates the status bar to show that the song is done   
            if int(self.music_slider.get()) == int(song_len):
                self.status_bar.config(text=f'Time Elapsed: {convert_song_len}  of  {convert_song_len}  ')
            
            # updates the status bar when moving the slider
            elif self.playing_state:
                # If paused, this pauses the song again after moving the slider
                mixer.music.pause()
                # This mutes volume when moving the slider while paused
                mixer.music.set_volume(0)
                # The slider has moved
                slider_position = int(song_len)
                self.music_slider.config(to=slider_position, value=int(self.music_slider.get()))
                # Converted time format
                convert_current_time = time.strftime('%M:%S', time.gmtime(int(self.music_slider.get())))

                # Outputs the time to the status bar
                self.status_bar.config(text=f'Time Elapsed: {convert_current_time}  of  {convert_song_len}  ')
            
                # Sets the time to the status bar when the slider is moved 
                new_time = int(self.music_slider.get())
                self.music_slider.config(value=new_time)
                            
            elif int(self.music_slider.get()) == int(current_time):
                # The slider has not moved
                self.update_slider()
                
            else:
                # Sets the volume back to its original state after hitting play
                v = Scale.get(self.volume_slider)
                mixer.music.set_volume(v)
                # The slider has moved
                slider_position = int(song_len)
                self.music_slider.config(to=slider_position, value=int(self.music_slider.get()))
                
                # Converted time format
                convert_current_time = time.strftime('%M:%S', time.gmtime(int(self.music_slider.get())))

                # Outputs the time to the status bar
                self.status_bar.config(text=f'Time Elapsed: {convert_current_time}  of  {convert_song_len}  ')
            
                # Moves the slider by one second
                add_time = int(self.music_slider.get()) + 1
                self.music_slider.config(value=add_time)
                
            # Updates time
            self.status_bar.after(1000, self.song_length)
 
       
# Window prompt that asks if you want to quit                    
def closing_window():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        mixer.music.stop()
        root.destroy()
# Ask for Music directory that contains music files and then saves it in Music.txt file
def files():
    os.chdir(os.path.dirname(__file__))
    global directory
    directory = list(os.getcwd())
    directory[0] = "C"
    directory = "".join(directory)
    return directory
    
# Starts the application
mixer.init()
root = Tk()
player = MusicPlayer(root)
files()
root.protocol("WM_DELETE_WINDOW", closing_window)
root.mainloop()