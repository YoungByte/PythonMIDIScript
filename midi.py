import pygame.midi, os, time, playsound, array, random, speech_recognition as sr
from gtts import gTTS

keys_down = []
mp3s = []
keyselect = 0

def print_devices():
    for n in range(pygame.midi.get_count()):
        print (n, pygame.midi.get_device_info(n))

def speak(text):
    tts = gTTS(text=text, lang="en")
    filename = text.replace(" ", "_") + ".mp3"
    mp3s.append(filename)
    tts.save(filename)
    #playsound.playsound(filename)

speak("I've seen more talented sandwiches")
speak("You suck")
speak("Maybe try another instrument")
speak("Ling Ling wannabe")
speak("Please give up")
speak("Play the right notes")

def startPrompt():
    global keyselect
    while True:
        try:
            print("""0. C
1. C#
2. D
3. D#
4. E
5. F
6. F#
7. G
8. G#
9. A
10. A#
11. B""")
            keyselect = int(input('Pick the key you would like to play in. >>> '))
        except ValueError:
           print('That\'s not a number!')
        else:
            if 0 <= keyselect <= 11:
                break
            else:
                print('Out of range. Try again')

keyDict = {}
keyDict[0] = ["C", "D", "E", "F", "G", "A", "B"] #C
keyDict[1] = ["C", "C#", "D#", "F", "F#", "G#", "A#"] #C#
keyDict[2] = ["C#", "D", "E", "F#", "G", "A", "B"] #D
keyDict[3] = ["C", "D", "D#", "F", "G", "G#", "A#"] #D#
keyDict[4] = ["C#", "D#", "E", "F#", "G#", "A", "B"] #E
keyDict[5] = ["C", "D", "E", "F", "G", "A", "A#"] #F
keyDict[6] = ["C#", "D#", "F", "F#", "G#", "A#", "B"] #F#
keyDict[7] = ["C", "D", "E", "F#", "G", "A", "B"] #G
keyDict[8] = ["C", "C#", "D#", "F", "G", "G#", "A#"] #G#
keyDict[9] = ["C#", "D", "E", "F#", "G#", "A", "B"] #A
keyDict[10] = ["C", "D", "D#", "F", "G", "A", "A#"] #A#
keyDict[11] = ["C#", "D#", "E", "F#", "G#", "A#", "B"] #B

def readInput(input_device):
    while True:
        if input_device.poll():
            event = input_device.read(1)[0]
            print(event)
            data = event[0]
            timestamp = event[1]
            note_number = data[1]
            velocity = data[2]
            if velocity > 0 and note_number not in keys_down:
                keys_down.append(note_number)
            elif velocity == 0 and note_number in keys_down:
                key_index = keys_down.index(note_number)
                del keys_down[key_index]
                print(keys_down)
                print (number_to_note(note_number), velocity)
                if number_to_note(note_number) not in keyDict[keyselect]:
                    playsound.playsound(random.choice(mp3s))

def number_to_note(number):
    print("Converting {0}".format(number))
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    return notes[number % 12]

startPrompt()
pygame.midi.init()
print_devices()
my_input = pygame.midi.Input(1)
readInput(my_input)
