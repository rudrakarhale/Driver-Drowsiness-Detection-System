import pygame
import os
import threading
import time

class AlarmSystem:
    def __init__(self, sound_file_path):
        """
        Initialize the audio system.
        :param sound_file_path: Relative or absolute path to the .wav or .mp3 file.
        """
        pygame.mixer.init()
        self.sound_file = sound_file_path
        self.is_playing = False
        
        # Verify file exists
        if not os.path.exists(self.sound_file):
            print(f"⚠️  WARNING: Alarm sound file not found at: {self.sound_file}")
            print("Please ensure 'alarm.wav' is in the assets folder.")

    def _play_loop(self):
        """Internal method to play sound in a loop."""
        try:
            if os.path.exists(self.sound_file):
                pygame.mixer.music.load(self.sound_file)
                # -1 means loop indefinitely
                pygame.mixer.music.play(-1) 
        except Exception as e:
            print(f"Audio Error: {e}")

    def start_alarm(self):
        """
        Triggers the alarm if it is not already playing.
        """
        if not self.is_playing:
            self.is_playing = True
            # Pygame music play is non-blocking by default, 
            # but wrapping logic keeps state management clean.
            self._play_loop()

    def stop_alarm(self):
        """
        Stops the alarm immediately.
        """
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False