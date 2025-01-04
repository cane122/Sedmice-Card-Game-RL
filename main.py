import pygame
import sys
import os
import subprocess
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Screen dimensions and colors
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600  # Adjust as needed
BG_COLOR = pygame.Color('darkgreen')
FONT_COLOR = pygame.Color('white')
MENU_FONT_SIZE = 40
TITLE_FONT_SIZE = 80

# Title settings
TITLE_TEXT = 'SEDMICE'
TITLE_COLOR = pygame.Color('lightblue')  # Title color
BORDER_COLOR = pygame.Color('black')  # Border color
TITLE_FONT_COLOR = pygame.Color('lightgray')  # Text color for the title
TITLE_FONT_SIZE = 150  # Increased font size
border_shift = 5  # Border thickness

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('SEDMICE Main Menu')

# Fonts
menu_font = pygame.font.Font(None, MENU_FONT_SIZE)
title_font = pygame.font.Font(None, TITLE_FONT_SIZE)

# Menu options
options = ['Start Game Free Play', 'Options', 'Exit']
option_rects = []

def draw_menu():
    screen.fill(BG_COLOR)

    # Adjusted title settings
    title_text = TITLE_TEXT
    title_color = TITLE_COLOR  # Title color
    border_color = BORDER_COLOR  # Border color
    title_font_size = TITLE_FONT_SIZE  # Increased font size
    title_font = pygame.font.Font(None, title_font_size)
    border_shift =  8 # Adjust border thickness if needed

   # Draw the bordered title
    # First, draw the border
    for dx in range(-border_shift, border_shift+1):
        for dy in range(-border_shift, border_shift+1):
            if dx or dy:  # Draw border components
                title_surface = title_font.render(title_text, True, border_color)
                title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2 + dx, SCREEN_HEIGHT // 4 + dy))
                screen.blit(title_surface, (title_rect.x - border_shift // 2, title_rect.y))

    # Then, draw the main title text in the intended color on top of the border
    title_surface = title_font.render(title_text, True, title_color)
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    screen.blit(title_surface, title_rect)
    
    # Draw the menu options
    for index, option in enumerate(options):
        option_surface = menu_font.render(option, True, FONT_COLOR)
        option_rect = option_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + index * 60))
        option_rects.append(option_rect)
        screen.blit(option_surface, option_rect)

    pygame.display.flip()

def main_menu():
    running = True
    while running:
        draw_menu()

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for index, rect in enumerate(option_rects):
                    if rect.collidepoint(mouse_pos):
                        if index == 0:
                            print("Starting Free Play...")
                            pygame.quit()  # Close the Pygame window
                            os.system('python setup.py')  # Calls setup.py which in turn starts the game
                            running = False
                            
                        elif index == 1:
                            print("Opening Options...")
                            # options_function()  # Placeholder, define this function for handling options
                        elif index == 2:
                            running = False
                            pygame.quit()
                            sys.exit()

if __name__ == '__main__':
    main_menu()
