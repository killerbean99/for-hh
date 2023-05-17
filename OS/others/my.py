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
            return int(command[word_len + whitespaces + 1])
    return -1  


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
FILE = r"C:\Users\Elara\Downloads\OS\MicrosoftTeams-image.png"

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


import pygame

# Initialize Pygame
pygame.init()

# Set up the window
width, height = 1120, 630
window_size = (width, height)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Seconds Display")

# Set up a clock to control the frame rate
clock = pygame.time.Clock()

# Start the timer at 0 seconds
start_time = pygame.time.get_ticks()

# Set the maximum time to 48 seconds
max_time = 48

square_size = 40
square_spacing = 10
blue = (0, 255, 255)
red = (255, 0, 0)

square_color = blue

colors = [blue] * len(processor)

font_size = 30

processor_set = set(processor)
processor_set = sorted(processor_set)

while -1 in disk:
    disk.remove(-1)

disk_set = set(disk)
disk_set = sorted(disk_set)
# processor_set.reverse()


# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    # Clear the screen
    screen.fill((255, 255, 255))
    
    # Get the elapsed time in seconds
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000.0
    
    

    amount_of_pc = len(processor_set)
    ax = (window_size[0] - (amount_of_pc * square_size + square_spacing*(amount_of_pc - 1)))/2 + (square_size - font_size)/2
    ay = height/2 - square_size/2 + (square_size - font_size)/2

    for i in range(amount_of_pc):
        square_color = (0, 0, 255)
        x = (i * (square_size + square_spacing)) + (window_size[0] - (amount_of_pc * square_size + square_spacing*(amount_of_pc - 1))) // 2
        y = (window_size[1] - square_size) // 2
        
        square_rect = pygame.Rect(x, y, square_size, square_size)
        if int(elapsed_time) in time:
            square_color = (255, 0, 255)
        rect_block = pygame.draw.rect(screen, square_color, square_rect)

    amount_of_disk = len(disk_set)

    for i in range(amount_of_disk):
        square_color = blue
        x = (i * (square_size + square_spacing)*2)
        y = 50
        
        new_rect = pygame.Rect(x, y, square_size*2, square_size*2)
        if int(elapsed_time) in time:
            square_color = red
        rect_block = pygame.draw.rect(screen, square_color, new_rect)
        
    for i, (pc, color) in enumerate(zip(processor_set, colors)):
        font = pygame.font.Font(None, font_size)
        s = int(elapsed_time)
        if s in time and pc == processor[time.index(s)]:
            color = red
        text = font.render(pc, True, color)
        rect = text.get_rect(x=ax + i * (square_size + square_spacing), y=ay)
        screen.blit(text, rect)

    
    i = 0
    for disk in disk_set:
        font = pygame.font.Font(None, font_size)
        text = font.render('Disk'+str(disk), True, (0, 255, 0))
        rect = text.get_rect(x = i * 100, y = 50)
        screen.blit(text, rect)
        i += 1

    # Check if the time has exceeded the maximum
    if elapsed_time > max_time:
        elapsed_time = max_time
    
    # Calculate the remaining seconds
    seconds = int(elapsed_time) % 60
    
    # Draw the seconds as text on the screen
    font = pygame.font.Font(None, 100)
    text = font.render(str(seconds), True, (0, 0, 0))
    text_rect = text.get_rect(bottom=screen.get_rect().bottom)
    screen.blit(text, text_rect)
    
    # Update the screen
    pygame.display.update()
    
    # Control the frame rate
    clock.tick(60)  # 60 FPS