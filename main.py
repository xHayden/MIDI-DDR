import sys, pygame
from pygame.locals import *
import os
import pygame.midi

size = width, height = 1920, 1080
notes = 88
spacing = width/10/notes

patternFromA = [0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1] # Black notes pattern

pygame.init()
screen = pygame.display.set_mode(size)
lowest_note = 21

def print_device_info():
    pygame.midi.init()
    _print_device_info()
    pygame.midi.quit()


def _print_device_info():
    for i in range(pygame.midi.get_count()):
        r = pygame.midi.get_device_info(i)
        (interf, name, input, output, opened) = r

        in_out = ""
        if input:
            in_out = "(input)"
        if output:
            in_out = "(output)"

        print(
            "%2i: interface :%s:, name :%s:, opened :%s:  %s"
            % (i, interf, name, opened, in_out)
        )


# pygame.mixer.music.load('midi_files/la_camp.mid')
# print(pygame.mixer.surfarray)
# pygame.mixer.music.play()

# class Note():
#     def __init__(self, color, x, y = 0, height = 50):
#         self.color = color
#         self.x = x
#         self.width = (width - (spacing * notes))/notes
#         self.y = y
#         self.height = height
#     def checkIfDestroyed(self):
#         if (self.y > height):
#             del self
#     def moveDown(self, amount = 0.5):
#         self.y += amount
#     def draw(self):
#         self.l = self.x;
#         self.t = self.y;
#         self.w = self.width;
#         self.h = self.height;
#         pygame.draw.rect(screen, self.color, pygame.Rect(self.l, self.t, self.w, self.h))

# class Note():
#     def __init__(self, color, number):
#         self.color = color
#         self.number = number + lowest_note
#         self.height = 100;
#         self.end = False;
#         self.y = 0;
#         self.black = patternFromA[((self.number - lowest_note) % 12)]
#         self.width = (width - (spacing * notes))/notes
#         self.scaleFactor = 2 if self.black else 1
#     def moveDown(self, amount=0.5):
#         if (not(self.end)):
#             self.y += amount;
#         self.height += amount;
#     def draw(self):
#         if (self.end):
#             noteLength = self.y
#         else:
#            noteLength = self.height
#         self.l = (self.width * (self.number - lowest_note) + (spacing * (self.number - lowest_note))) + (self.black * (1/4 * self.width))
#         self.t = self.height
#         self.w = self.width / self.scaleFactor
#         self.h = noteLength
#         pygame.draw.rect(screen, (0, 200, 200), pygame.Rect(self.l, self.t, self.w, self.h))

class PlayedNote():
    def __init__(self, number, color = (0, 0, 200)):
        self.color = color
        self.number = number
        self.height = 0
        self.end = False;
        self.y = 0;
        self.black = patternFromA[((self.number - lowest_note) % 12)]
        self.width = (width - (spacing * notes))/notes
        self.scaleFactor = 2 if self.black else 1
    def moveUp(self, amount=0.5):
        if (not(self.end)):
            self.y += amount;
        self.height += amount;
    def draw(self):
        self.moveUp();
        if (self.end):
            noteLength = self.y
        else:
           noteLength = self.height
        self.l = (self.width * (self.number - lowest_note) + (spacing * (self.number - lowest_note))) + (self.black * (1/4 * self.width))
        self.t = height-(self.height)
        self.w = self.width / self.scaleFactor
        self.h = noteLength
        pygame.draw.rect(screen, (0, 200, 200), pygame.Rect(self.l, self.t, self.w, self.h))

def main():
    notesArr = []
    played = []

    device_id = None; 
    color = (255,0,0)
    # for i in range(notes):
    #     note = Note(color, i);
    #     note.draw();
    #     notesArr.append(note)
    pygame.display.flip();
    pygame.init()
    pygame.fastevent.init()
    event_get = pygame.fastevent.get
    event_post = pygame.fastevent.post

    pygame.midi.init()

    _print_device_info()

    if device_id is None:
        input_id = pygame.midi.get_default_input_id()
    else:
        input_id = device_id

    print("using input_id :%s:" % input_id)
    i = pygame.midi.Input(input_id)
    
    while True: 
        screen.fill((0,0,0))
        for note in notesArr:
            note.moveDown();
            note.draw();

        events = event_get()

        for e in events:
            if e.type==QUIT:
                pygame.quit()
                sys.exit()
            if e.type in [pygame.midi.MIDIIN]:
                #print(e)
                pass


        if i.poll():
            midi_events = i.read(10)
            # convert them into pygame events.
            midi_evs = pygame.midi.midis2events(midi_events, i.device_id)

            for m_e in midi_evs:
                event_post(m_e)
                if (m_e.status == 144):
                    if (m_e.data1 >= lowest_note and m_e.data1 < lowest_note + notes):
                    # Pressed
                        played.append(PlayedNote(m_e.data1))
                    #print(played)
                if (m_e.status == 128):
                    #print(m_e.status)
                    # Released
                    try:
                        for note in played:
                            if (note.number == m_e.data1):
                                note.end = True;
                    except Exception as e:
                        print(e)
                        pass

            # Data 1: Note, status: 144 pressed, 128 released
        for notePlayed in played:
            notePlayed.draw();
        #pygame.draw.rect(screen, (0, 0, 100), pygame.Rect(0, 7 * (height/8), width, 10))
        pygame.display.update()
    del i

    pygame.midi.quit()
main()