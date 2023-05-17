import pygame
import cv2
import tkinter as tk
from tkinter import filedialog
import os

# Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set the window dimensions
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 150

# Create the Pygame window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("cut video")

# Open the video file
video_capture = cv2.VideoCapture(r"C:\Users\Elara\Downloads\OS\video.mp4")

# Set the frame rate and count
frame_rate = video_capture.get(cv2.CAP_PROP_FPS)
frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

print(frame_rate, frame_count)

def do_cut():
    # Iterate through the frames and extract photos
    for i in range(frame_count):
        # Read the frame
        success, frame = video_capture.read()
        
        if not success:
            break
        
        file_path = os.path.join(new_folder_path, f'frame_{i}.png')
        print(file_path)
        cv2.imwrite(file_path, frame)

    # Release the video capture object
    video_capture.release()

def choose_folder():
    folder_path = filedialog.askdirectory()
    new_folder_name = "Vidoes Frames"
    global new_folder_path
    new_folder_path = os.path.join(folder_path, new_folder_name)
    os.mkdir(new_folder_path)
    do_cut()

def change_fps():
    fps_window = tk.Toplevel(root)
    fps_window.title("Change FPS")

    fps_label = tk.Label(fps_window, text="Enter FPS:")
    fps_label.pack()

    fps_entry = tk.Entry(fps_window)
    fps_entry.pack()

    def apply_fps():
        global fps
        fps = fps_entry.get()
        print(f"New FPS: {fps}")
        fps_window.destroy()

    apply_button = tk.Button(fps_window, text="Apply", command=apply_fps)
    apply_button.pack()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Fill the screen with white
    screen.fill(WHITE)
    
    # Create the "Choose Folder" button
    choose_folder_button = pygame.draw.rect(screen, BLACK, (50, 50, 200, 50))
    choose_folder_text = pygame.font.SysFont('calibri', 20).render("Choose Folder", True, WHITE)
    screen.blit(choose_folder_text, (70, 65))
    
    # Create the "Change FPS" button
    change_fps_button = pygame.draw.rect(screen, BLACK, (50, 110, 200, 50))
    change_fps_text = pygame.font.SysFont('calibri', 20).render("Change FPS", True, WHITE)
    screen.blit(change_fps_text, (70, 125))

    # Check if the "Choose Folder" button is clicked
    if pygame.mouse.get_pressed()[0] and choose_folder_button.collidepoint(pygame.mouse.get_pos()):
        choose_folder()
    
    # Check if the "Change FPS" button is clicked
    if pygame.mouse.get_pressed()[0] and change_fps_button.collidepoint(pygame.mouse.get_pos()):
        change_fps()
    
    # Update the screen
    pygame.display.update()

# Quit Pygame
pygame.quit()
