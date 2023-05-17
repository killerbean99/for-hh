def check_row(ix, x):
    fr, sd = None, None
    for i in range(9):
        for j in range(9):
            if x[i] == x[j] and i != j:
                fr, sd = min(i, j), max(i, j)
                break
    
    return ix, fr, sd

def check_col(ix, x):
    fr, sd = None, None
    
    for i in range(9):
        for j in range(9):
            if x[i][ix] == x[j][ix] and i != j:
                fr, sd = min(i, j), max(i, j)
                break
    
    return ix, fr, sd


def transform_row(ix, fr, sd):
    fr_ix = ix * 9 + fr
    sd_ix = ix * 9 + sd
    
    return fr_ix, sd_ix

def transform_col(ix, fr, sd):
    fr_ix = ix + 9 * fr
    sd_ix = ix + 9 * sd
    
    return fr_ix, sd_ix


def is_valid_sudoku(matrix):
    dupplicates = []

    for i in range(9):
        ix_r, fr_r, sd_r = check_row(i, matrix[i])
        ix_c, fr_c, sd_c = check_col(i, matrix)
        if fr_r != None:
            a, b = transform_row(ix_r, fr_r, sd_r)
            dupplicates.append(a), dupplicates.append(b)
        if fr_c != None:
            a, b = transform_col(ix_c, fr_c, sd_c)
            dupplicates.append(a), dupplicates.append(b)
    
    return dupplicates


def to_array(matrix):
    arr = []

    for i in range(9): 
        arr += matrix[i]
    
    return arr


matrix = [[6, 2, 2, 5, 3, 9, 1, 8, 7],
          [6, 1, 9, 7, 2, 8, 6, 3, 4],
          [8, 3, 7, 6, 1, 4, 2, 9, 5],
          [1, 4, 3, 8, 6, 5, 7, 2, 9],
          [9, 5, 8, 2, 4, 7, 3, 6, 1],
          [7, 6, 2, 3, 9, 1, 4, 5, 8],
          [3, 7, 1, 9, 5, -1, 8, 4, 2],
          [4, 9, 6, 1, 8, 2, 5, 7, 3],
          [2, 8, 5, 4, 7, 3, 9, 1, 12]]

arr = to_array(matrix)

dupplicates = is_valid_sudoku(matrix)


import pygame
from pygame import display as pgd
from pygame.locals import *

def create_button(text, font, x, y, width, height, color):
    button = pygame.Surface((width, height))
    button.fill(color)
    text_surface = font.render(text, True, dark_blue)
    text_rect = text_surface.get_rect(center=(width//2, height//2))
    button.blit(text_surface, text_rect)
    screen.blit(button, (x, y))

sunrise = (255, 204, 187)
ocean = (110, 181, 192)
dark_blue = (0, 108, 132)
silver = (226, 232, 228)
button_size = 60
margin = button_size//6
display_size = button_size * 9 + margin * 10

pygame.init()

screen = pgd.set_mode((display_size, display_size))
pgd.set_caption("Sudoku")
screen.fill(dark_blue)

font_size = button_size//2
font = pygame.font.SysFont(None, font_size)

# create button grid
for i, num in enumerate(arr):
    row, col = divmod(i, 9)
    x = col * (button_size + margin) + margin
    y = row * (button_size + margin) + margin
    color = silver if num <= 9 and num >= 0 and i not in dupplicates else sunrise
    create_button(str(num), font, x, y, button_size, button_size, color)

pgd.flip()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
