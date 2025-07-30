import pygame

pygame.mixer.init()

def play_sound(file: str) -> None:
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

play_sound("f1.mp3")