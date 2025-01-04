import pygame
import subprocess
import sys

# Initialize Pygame
pygame.init()

# Screen settings
screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game Mode Selection")

# Colors and Fonts
GREEN = pygame.Color('darkgreen')
BLACK = (0, 0, 0)
font = pygame.font.SysFont("Arial", 24)

# Global state
input_text = '0'
selected_option = None
selected_bot_mode = None  # To track "Monte Carlo" or "Player" under "Bot"

# Define UI components
button_rect = pygame.Rect(screen_width // 2 - 50, screen_height - 60, 200, 60)
button_text = "Start Game"
input_rect = pygame.Rect(screen_width // 2 - 50, screen_height - 120, 100, 40)
input_color = pygame.Color('white')
input_active = False

class RadioButton:
    def __init__(self, x, y, text, group):
        self.rect = pygame.Rect(x, y, 200, 30)
        self.text = text
        self.selected = False
        self.group = group
        group.append(self)
    
    def draw(self, screen):
        # No outline, just the circle for selected
        pygame.draw.circle(screen, pygame.Color('black'), (self.rect.x + 180, self.rect.centery), 5)
        if self.selected:
            pygame.draw.circle(screen, pygame.Color('green'), (self.rect.x + 180, self.rect.centery), 7)
        text_surf = font.render(self.text, True, BLACK)
        screen.blit(text_surf, (self.rect.x + 5, self.rect.y + 5))
    
    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.selected = True
            return True
        return False

def draw_ui(screen, primary_radio_buttons, bot_suboptions, label_first, label_opponent):
    global input_text, input_color
    screen.fill(GREEN)

    # Draw the "Who plays first" label
    label_surf = font.render(label_first, True, BLACK)
    screen.blit(label_surf, (50, 20))

    # Draw the "Opponent" label
    label_surf = font.render(label_opponent, True, BLACK)
    screen.blit(label_surf, (screen_width - 250, 20))

    # Draw radio buttons for primary options (left side)
    for button in primary_radio_buttons:
        button.draw(screen)

    # Draw radio buttons for bot sub-options (right side)
    for button in bot_suboptions:
        button.draw(screen)

    # Draw the input field
    pygame.draw.rect(screen, input_color, input_rect)
    input_surf = font.render(input_text, True, BLACK)
    screen.blit(input_surf, (input_rect.x + 5, input_rect.y + 10))

    # Draw the "Start Game" button
    mouse_pos = pygame.mouse.get_pos()
    button_color = pygame.Color('grey') if not button_rect.collidepoint(mouse_pos) else pygame.Color('lightgrey')
    draw_button(screen, button_rect, button_text, button_color)

    pygame.display.flip()

def draw_button(screen, rect, text, color):
    pygame.draw.rect(screen, color, rect)
    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

def main():
    global input_text, selected_option, selected_bot_mode, input_color, input_active
    running = True

    # Define options
    primary_options = ["Random", "Player", "Bot"]
    bot_suboptions = ["Monte Carlo", "Player"]  # Sub-options under "Bot"

    # Create radio buttons for primary options (left side)
    primary_radio_buttons = []
    for idx, option in enumerate(primary_options):
        RadioButton(50, 60 + idx * 40, option, primary_radio_buttons)
    
    # Create radio buttons for bot sub-options (right side)
    bot_radio_buttons = []
    for idx, option in enumerate(bot_suboptions):
        RadioButton(screen_width - 250, 60 + idx * 40, option, bot_radio_buttons)

    label_first = "Who plays first"
    label_opponent = "Opponent"

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse_event(event.pos, primary_radio_buttons, bot_radio_buttons, input_rect, button_rect)
            elif event.type == pygame.KEYDOWN and input_active:
                handle_keyboard_event(event)

        draw_ui(screen, primary_radio_buttons, bot_radio_buttons, label_first, label_opponent)

    pygame.quit()
    sys.exit()

def handle_mouse_event(pos, primary_radio_buttons, bot_radio_buttons, input_rect, button_rect):
    global input_active, input_color, input_text, selected_option, selected_bot_mode
    if input_rect.collidepoint(pos):
        input_active = not input_active
        input_color = pygame.Color('lightskyblue2') if input_active else pygame.Color('white')
    elif button_rect.collidepoint(pos):
        print(f"Start Game with option: {selected_option}, bot mode: {selected_bot_mode}, number: {input_text}")
        pygame.quit()

        if selected_bot_mode == "Monte Carlo":
            subprocess.run(['python', 'game_mc.py',selected_option, input_text])
        elif selected_bot_mode == "Player":
            subprocess.run(['python', 'game.py', selected_option, input_text])
        else:
            subprocess.run(['python', 'game.py', selected_option, input_text])
        sys.exit()
    else:
        input_active = False
        input_color = pygame.Color('white')

    # Check primary options (left side)
    for button in primary_radio_buttons:
        if button.check_click(pos):
            for other_button in primary_radio_buttons:
                other_button.selected = False
            button.selected = True
            selected_option = button.text
            print(f"Selected option: {selected_option}")

    # Check bot sub-options (right side)
    for button in bot_radio_buttons:
        if button.check_click(pos):
            for other_button in bot_radio_buttons:
                other_button.selected = False
            button.selected = True
            selected_bot_mode = button.text
            print(f"Selected bot mode: {selected_bot_mode}")

def handle_keyboard_event(event):
    global input_text
    if event.key == pygame.K_BACKSPACE:
        input_text = input_text[:-1]
    elif len(input_text) < 2 or not input_text.isdigit():
        if event.unicode.isdigit():
            temp_text = input_text + event.unicode
            temp_number = int(temp_text) if temp_text.isdigit() else None
            if temp_number and 1 <= temp_number <= 32:
                input_text = temp_text

if __name__ == "__main__":
    main()
