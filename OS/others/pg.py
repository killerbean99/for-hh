import pygame

# Initialize Pygame
pygame.init()

# Set up the window
window_size = (400, 300)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Seconds Display")

# Set up a clock to control the frame rate
clock = pygame.time.Clock()

# Start the timer at 0 seconds
start_time = pygame.time.get_ticks()

# Set the maximum time to 48 seconds
max_time = 48

square_size = 20
square_spacing = 10
square_color = (255, 0, 0)

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
    
    if int(elapsed_time) == 5:
        font = pygame.font.Font(None, 30)
        text = font.render("Time is now 5 seconds!", True, (0, 0, 0))
        text_rect = text.get_rect(bottom=screen.get_rect().bottom)
        screen.blit(text, text_rect)

    # Check if the time has exceeded the maximum
    if elapsed_time > max_time:
        elapsed_time = max_time
    
    # Calculate the remaining seconds
    seconds = int(elapsed_time) % 60
    
    # Draw the seconds as text on the screen
    font = pygame.font.Font(None, 100)
    text = font.render(str(seconds), True, (0, 0, 0))
    text_rect = text.get_rect(center=screen.get_rect().center)
    screen.blit(text, text_rect)
    
    # Update the screen
    pygame.display.update()
    
    # Control the frame rate
    clock.tick(60)  # 60 FPS
