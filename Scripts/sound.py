import pygame
import threading
import time

pygame.mixer.init()

def play_sound(file: str) -> None:
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def play_dialog1():
    def play():
        play_sound("Audio/f1.mp3")

    threading.Thread(target=play, daemon=True).start()

def play_dialog2():
    def play():
        # pygame.mixer.stop()
        play_sound("Audio/f2.mp3")
        time.sleep(1)
        play_sound("Audio/f2_1.mp3")

    threading.Thread(target=play, daemon=True).start()



if __name__ == "__main__":
    play_sound("f1.mp3") # testing a part of the code