import pytesseract as pst
from pytesseract import Output
from glob import glob as gg
import PIL.Image as pi


def check_time(command):
    if command[9] == ':':
        return int(command[8])
    else:
        return int(command[8:10])


def check_processor(command):
    for char in command:
        if char == 'P':
            P_ix = command.index(char)
            return command[P_ix:P_ix+2]


def check_disk(command):
    command_list = command.split()
    whitespaces = -1
    word_len = 0
    for word in command_list:
        word_len += len(word)
        whitespaces += 1
        if word == 'unit':
            return 'disk ' + command[word_len + whitespaces + 1]   


def check_action(command):
    command_list = command.split()
    for word in command_list:
        if word == 'to':
            return command_list[command_list.index(word) + 1] + ' is starts'
        elif word == 'complete.':
            return command_list[command_list.index(word) - 2] + ' is complete'
        elif word == 'terminates.':
            return 'terminates'
        elif word == 'out.':
            return 'is swapped out'
        elif word == 'back':
            return 'is swapped back'
        elif word == 'slice':
            return 'time slice expires'


MY_CONFIG = r"--psm 3 --oem 3 -l eng" # --psm 3, 6 
FILE = gg('./png/MicrosoftTeams-image.png')

text = pst.image_to_string(pi.open(FILE), config = MY_CONFIG)
test_list = text.split()
test_list = test_list[test_list.index('events:') + 1:]
str1 = ' '.join(test_list)
new_list = str1.split('. ')


for sentence in new_list:
    if sentence[-1] != '.':
        new_list[new_list.index(sentence)] += '.'


step = 0
steps = 12

command = []

time = []
processor = []
disk = []
action = []

while(step < steps):
    command.append(new_list[step])
    time.append(check_time(command[step]))
    processor.append(check_processor(command[step]))
    disk.append(check_disk(command[step]))
    action.append(check_action(command[step]))
    step += 1

step = 0
while(step < steps):
    if disk[step] != None:
        print(time[step], disk[step], processor[step], action[step])
    else:
        print(time[step], processor[step], action[step])
    step += 1
