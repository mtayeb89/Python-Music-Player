import pygame
import os
import tkinter as tk
from tkinter import filedialog, ttk
from mutagen.mp3 import MP3
import time


class MusicPlayer:
    def __init__(self):
        # Initialize pygame mixer
        pygame.mixer.init()

        # Create the main window
        self.root = tk.Tk()
        self.root.title("Python Music Player")
        self.root.geometry("400x600")

        # Initialize variables
        self.current_track = ""
        self.paused = False
        self.playlist = []
        self.current_index = 0

        # Create GUI elements
        self.create_gui()

        # Start the GUI event loop
        self.root.mainloop()

    def create_gui(self):
        # Playlist frame
        playlist_frame = ttk.LabelFrame(self.root, text="Playlist")
        playlist_frame.pack(padx=10, pady=5, fill="both", expand=True)

        # Playlist listbox
        self.playlist_box = tk.Listbox(playlist_frame, selectmode=tk.SINGLE)
        self.playlist_box.pack(padx=10, pady=5, fill="both", expand=True)

        # Current track label
        self.track_label = ttk.Label(self.root, text="No Track Selected")
        self.track_label.pack(padx=10, pady=5)

        # Time slider
        self.time_slider = ttk.Scale(self.root, from_=0, to=100, orient="horizontal")
        self.time_slider.pack(padx=10, pady=5, fill="x")

        # Control buttons frame
        controls_frame = ttk.Frame(self.root)
        controls_frame.pack(padx=10, pady=5)

        # Control buttons
        ttk.Button(controls_frame, text="Add Song", command=self.add_song).pack(side="left", padx=5)
        ttk.Button(controls_frame, text="Previous", command=self.previous_track).pack(side="left", padx=5)
        self.play_button = ttk.Button(controls_frame, text="Play", command=self.play_pause)
        self.play_button.pack(side="left", padx=5)
        ttk.Button(controls_frame, text="Next", command=self.next_track).pack(side="left", padx=5)
        ttk.Button(controls_frame, text="Remove", command=self.remove_song).pack(side="left", padx=5)

        # Volume control
        volume_frame = ttk.LabelFrame(self.root, text="Volume")
        volume_frame.pack(padx=10, pady=5, fill="x")

        self.volume_slider = ttk.Scale(volume_frame, from_=0, to=100, orient="horizontal")
        self.volume_slider.set(70)  # Default volume
        self.volume_slider.pack(padx=10, pady=5, fill="x")
        self.volume_slider.bind("<Motion>", self.change_volume)

        # Start update timer
        self.root.after(1000, self.update_player)

    def add_song(self):
        # Open file dialog to select music files
        files = filedialog.askopenfilenames(
            title="Choose Music Files",
            filetypes=(("MP3 Files", "*.mp3"), ("All Files", "*.*"))
        )

        # Add selected files to playlist
        for file in files:
            self.playlist.append(file)
            self.playlist_box.insert(tk.END, os.path.basename(file))

    def remove_song(self):
        try:
            # Get selected song index
            selected_index = self.playlist_box.curselection()[0]

            # Remove from playlist and listbox
            self.playlist_box.delete(selected_index)
            self.playlist.pop(selected_index)

            # Stop playback if current song is removed
            if selected_index == self.current_index:
                pygame.mixer.music.stop()
                self.track_label.config(text="No Track Selected")
                self.current_index = 0
        except IndexError:
            pass

    def play_pause(self):
        if not self.playlist:
            return

        if self.paused:
            pygame.mixer.music.unpause()
            self.play_button.config(text="Pause")
            self.paused = False
        elif pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.play_button.config(text="Play")
            self.paused = True
        else:
            self.play_track()

    def play_track(self):
        # Load and play the current track
        track_path = self.playlist[self.current_index]
        pygame.mixer.music.load(track_path)
        pygame.mixer.music.play()

        # Update label and button
        self.track_label.config(text=os.path.basename(track_path))
        self.play_button.config(text="Pause")
        self.paused = False

        # Update time slider
        audio = MP3(track_path)
        self.time_slider.config(to=audio.info.length)

    def previous_track(self):
        if not self.playlist:
            return

        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play_track()

    def next_track(self):
        if not self.playlist:
            return

        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.play_track()

    def change_volume(self, event=None):
        volume = self.volume_slider.get() / 100
        pygame.mixer.music.set_volume(volume)

    def update_player(self):
        # Update time slider if music is playing
        if pygame.mixer.music.get_busy() and not self.paused:
            current_time = pygame.mixer.music.get_pos() / 1000
            self.time_slider.set(current_time)

            # Check if track has ended
            if current_time >= self.time_slider.cget("to"):
                self.next_track()

        # Schedule next update
        self.root.after(1000, self.update_player)


if __name__ == "__main__":
    player = MusicPlayer()