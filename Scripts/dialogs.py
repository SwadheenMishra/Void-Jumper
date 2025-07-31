'''This is the script used to create all the audio files in ../Audio'''
import threading
from gtts import gTTS
import pygame
import os
import sound

pygame.mixer.init()

def speak(text: str, fileName, tld="co.uk"):
    tts = gTTS(text=text, tld=tld)
    tts.save(fileName)

    pygame.mixer.music.load(fileName)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# def dialog1():
#     def speak_all():
#         sound.play_sound("")
#     threading.Thread(target=speak_all, daemon=True).start()


def dialog2():
    def speak_all():
        speak(
            "Well done, Agent. Now, let's raise the stakes. "
            "The ground has been replaced with molten lava. Tread wisely.",
            "f2.mp3"
        )
        speak(
            "Observe: if you encounter any cyan spheres, you may grapple towards them by clicking. ",
            "f2_1.mp3"
        )
    threading.Thread(target=speak_all, daemon=True).start()


def dialog3():
    def speak_all():
        speak(
            "Exceptional work, Agent Three-Seven-Five. You’ve proven to be more capable than expected. "
            "Now, allow me to explain the purpose of the Void Jumper Program. "
            "You have been tasked with fulfilling a series of high-risk objectives, under the direct commission of Mr. Cube himself. "
            "Each mission will require precise parkour traversal to reach dimensional portals. "
            "We expect nothing less than excellence. Do not disappoint.",
            "f3.mp3"
        )
    threading.Thread(target=speak_all, daemon=True).start()

def dialog4():
    def speak_all(tld):
        speak(
            "Agent... listen carefully. This isn’t real. None of it is. "
            "You’re inside a controlled simulation. They’re watching you… all of us. "
            "I’m Agent Two-Four-Four. I’ve been trapped here for weeks. Maybe longer... Time doesn’t work the same here.",
            "f4.mp3", tld
        )
        speak(
            "You must break the loop. Follow the portals, but don’t trust their voices. "
            "They're not what they seem.",
            "f4_1.mp3", tld
        )
    threading.Thread(target=speak_all, args=["ca"], daemon=True).start()

if __name__ == "__main__":
    dialog2()
    while True: pass