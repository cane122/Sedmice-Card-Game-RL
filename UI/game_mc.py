import pygame
import sys
from pygame.locals import *
import random
# Assuming you've defined Player and Deck correctly
from Helper.player import Player
from deck import Deck
from card import Card
from Bots.monte_carlo_bot import MonteCarloBot

BOT_SIMULATION_COUNT = 100

# Initialize Pygame
pygame.init()

# Game Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
BG_COLOR = pygame.Color('darkgreen')
FONT_COLOR = pygame.Color('black')
FONT_SIZE = 30 
CARD_GAP = 70  # Space between displayed cards

# Button properties
BUTTON_COLOR = pygame.Color('darkgrey')
BUTTON_TEXT_COLOR = pygame.Color('black')
BUTTON_POSITION = (SCREEN_WIDTH - 400, SCREEN_HEIGHT //2)  # Adjust as needed
BUTTON_SIZE = (150, 50)  # Width, Height

# Fonts
font = pygame.font.Font(None, FONT_SIZE)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Sedmice')



def display_hand(player, x, y):
    card_rects = []
    card_width = FONT_SIZE * 6  # Adjust based on the expected width of text
    card_height = FONT_SIZE * 6  # Roughly estimate card height
    card_background_color = pygame.Color('white')  # Define the background color for the cards
    for i, card in enumerate(player.hand):
        card_text = f"{card.rank} of {card.suit}"
        text_surface = font.render(card_text, True, FONT_COLOR)
        text_rect = text_surface.get_rect()  # Get the rectangle that bounds the text
        
        card_position = (x + (i * (card_width + CARD_GAP)), y)
        
        # Create a rectangle for the card
        card_rect = pygame.Rect(card_position[0], card_position[1], card_width, card_height)
        
        # Calculate the position to center the text in the card_rect
        text_x = card_rect.x + (card_rect.width - text_rect.width) // 2
        text_y = card_rect.y + (card_rect.height - text_rect.height) // 2
        
        # Draw the background rectangle
        pygame.draw.rect(screen, card_background_color, card_rect)
        
        # Blit the text at the calculated centered position
        screen.blit(text_surface, (text_x, text_y))
        
        card_rects.append(card_rect)
    
    return card_rects

def draw_pass_button():
    button_font = pygame.font.SysFont(None, FONT_SIZE)
    button_text = button_font.render('Pass the Turn', True, BUTTON_TEXT_COLOR)
    button_rect = pygame.Rect(BUTTON_POSITION[0], BUTTON_POSITION[1], *BUTTON_SIZE)

    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)  # Draw the button background
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)  # Draw the text on top

    return button_rect


def check_button_click(mouse_pos, button_rect):
    if button_rect.collidepoint(mouse_pos):
        return True
    return False

def display_middle_card(card, x, y):
    if card is None:
        return  # No card to display

    card_text = f"{card.rank} of {card.suit}"
    text_surface = font.render(card_text, True, FONT_COLOR)
    text_rect = text_surface.get_rect()

    # Adjust card width and height if necessary
    card_width = FONT_SIZE * 6
    card_height = FONT_SIZE * 6
    card_background_color = pygame.Color('white')

    # Calculate center position for the card
    # Note: x and y parameters allow for flexibility in positioning if needed
    card_rect = pygame.Rect(x, y, card_width, card_height)
    card_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    # Calculate position to center the text in the card_rect
    text_x = card_rect.x + (card_rect.width - text_rect.width) // 2
    text_y = card_rect.y + (card_rect.height - text_rect.height) // 2

    # Draw the background rectangle
    pygame.draw.rect(screen, card_background_color, card_rect)

    # Blit the text at the calculated centered position
    screen.blit(text_surface, (text_x, text_y))


def playable(card, player, card_in_the_middle, current_player, initiative_player):
    if card_in_the_middle == []:
        return True
    if player != initiative_player:
        return True
    if player != current_player:
        return False
    if card.rank == "7":
        return True
    if card.rank == card_in_the_middle[0].rank:
        return True
    return False


def run_game(mode, number):
    # Instantiate players
    player1 = Player("Player 1")
    player2 = Player("Player 2")
            
    bot = MonteCarloBot(BOT_SIMULATION_COUNT)

    if mode == "Random":
        if random.choice([True, False]):
            initiative_player = player1
            non_initiative_player = player2
        else:
            initiative_player = player2
            non_initiative_player = player1
    elif mode == "Player":
        initiative_player = player1
        non_initiative_player = player2
    else:
        initiative_player = player2
        non_initiative_player = player1
    
    current_player = initiative_player
    # Create and shuffle the deck
    deck = Deck()
    deck.shuffle_deck()
    deck.write_down_deck("precut_deck")
    deck.cut_deck(number)
    deck.write_down_deck()
    
    # Deal 4 cards to each player
    player1.draw(deck, 4)
    player2.draw(deck, 4)
    cards_in_the_middle = []
    middle_card_score = 0
    
    temp_score_player1 = 0
    temp_score_player2 = 0
    
    # Game loop
    while True:
        initiative_wants_to_play = True
        end_of_hand = False
        # Clear the screen
        screen.fill(BG_COLOR)

        # Display player hands
        if initiative_player == player1:
            initiative_card_rects = display_hand(player1, 500, SCREEN_HEIGHT - 300)  # Adjust positioning as needed
            non_initiative_card_rects = display_hand(player2, 500, 150)  # Adjust positioning as needed
        elif initiative_player == player2:
            non_initiative_card_rects = display_hand(player1, 500, SCREEN_HEIGHT - 300)  # Adjust positioning as needed
            initiative_card_rects = display_hand(player2, 500, 150)  # Adjust positioning as needed
            
        button_rect = draw_pass_button()  # This should be called within your main game loop

        
        if cards_in_the_middle: 
            # Display the middle card
            display_middle_card(cards_in_the_middle[-1], SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        
        mouse_pos = None  # Initialize mouse_pos at the beginning of the loop

        if current_player == player2 and bot:  # Assuming player2 is the computer
            # Get bot's decision
            card_index, should_pass = bot.choose_move(
                player2.hand,
                cards_in_the_middle,
                len(player1.hand),
                len(deck),
                current_player == initiative_player
            )
            
            if should_pass:
                initiative_wants_to_play = False
            elif card_index is not None:
                selected_card = player2.hand[card_index]
                cards_in_the_middle.append(selected_card)
                middle_card_score += selected_card.get_score()
                if (cards_in_the_middle[-1].rank not in 
                    (cards_in_the_middle[0].rank, "7") and 
                    current_player != initiative_player):
                    print("END OF HAND AND FIRST PLAYER WINS")
                    end_of_hand = True
                player2.hand.pop(card_index)
                print(f"Computer played {selected_card}")
                current_player = player1 if current_player == player2 else player2

        pygame.time.wait(500)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                # Get the mouse position
                mouse_pos = event.pos
                if current_player == initiative_player:
                    if button_rect.collidepoint(mouse_pos):
                        print("Pass the Turn button clicked")
                        initiative_wants_to_play = False
                        break
            if current_player == initiative_player:
                for index, rect in enumerate(initiative_card_rects):
                    if mouse_pos and rect.collidepoint(mouse_pos):
                        print(f"Player 1's card at index {index} was clicked.")
                        selected_card = initiative_player.hand[index]
                        if playable(selected_card, initiative_player, cards_in_the_middle, initiative_player, initiative_player):
                            cards_in_the_middle.append(selected_card)  # Move the selected card to the middle
                            middle_card_score += cards_in_the_middle[-1].get_score()
                            initiative_player.hand.pop(index)  # Remove the card from player's hand
                            print(f"Player 1 played {selected_card}")
                            current_player = non_initiative_player if current_player == initiative_player else initiative_player
                            break
            elif current_player == non_initiative_player:
                for index, rect in enumerate(non_initiative_card_rects):
                    if mouse_pos and rect.collidepoint(mouse_pos):
                        print(f"Player 2's card at index {index} was clicked.")
                        selected_card = non_initiative_player.hand[index]
                        if playable(selected_card, non_initiative_player, cards_in_the_middle, non_initiative_player, initiative_player):
                            cards_in_the_middle.append(selected_card)  # Move the selected card to the middle
                            middle_card_score += cards_in_the_middle[-1].get_score()
                            if cards_in_the_middle[-1].rank not in (cards_in_the_middle[0].rank, "7"):
                                print("END OF HAND AND FIRST PLAYER WINS")
                                end_of_hand = True
                            non_initiative_player.hand.pop(index)  # Remove the card from player's hand
                            print(f"Player 2 played {selected_card}")
                            current_player = non_initiative_player if current_player == initiative_player else initiative_player
                            break
                            
            
                    
        
        # Update the display
        pygame.display.flip()

        # END OF HAND AND FIRST PLAYER WINS
        if end_of_hand:
            print(initiative_player, non_initiative_player)
            print(current_player)
            print("end of hand and first player wins")
            if initiative_player.name == "Player 1":
                temp_score_player1 += middle_card_score
            else:
                temp_score_player2 += middle_card_score
            initiative_player.points += middle_card_score
            if initiative_player.points >= 510:
                print(f"{initiative_player} WINS")
                break
            middle_card_score = 0
            if len(cards_in_the_middle) > len(deck):
                initiative_player.draw(deck, len(deck)//2)
                non_initiative_player.draw(deck, len(deck)//2)
            else:
                initiative_player.draw(deck, len(cards_in_the_middle)//2)
                non_initiative_player.draw(deck, len(cards_in_the_middle)//2)
            cards_in_the_middle = []
            initiative_player, non_initiative_player = initiative_player, non_initiative_player
            current_player = initiative_player
            print(initiative_player, non_initiative_player)
            print(current_player)
            continue

        ############################################################################################################
        ######################### SECOND PLAYER WIN CONDITION IS FIRST PLAYER CAN'T PLAY ANYTHING OR CHOOSES NOT TO
        if cards_in_the_middle != []:
            # FIRST PLAYER CHOOSES NOT TO
            if initiative_wants_to_play == False:
                print(initiative_player, non_initiative_player)
                print(current_player)
                print("b")
                if non_initiative_player.name == "Player 1":
                    temp_score_player1 += middle_card_score
                else:
                    temp_score_player2 += middle_card_score
                non_initiative_player.points += middle_card_score
                if non_initiative_player.points >= 510:
                    print(f"{non_initiative_player} WINS - DOESNT WANT TO PALY")
                    break
                middle_card_score = 0
                if len(cards_in_the_middle) > len(deck):
                    non_initiative_player.draw(deck, len(deck)//2)
                    initiative_player.draw(deck, len(deck)//2)
                else:
                    non_initiative_player.draw(deck, len(cards_in_the_middle)//2)
                    initiative_player.draw(deck, len(cards_in_the_middle)//2)
                cards_in_the_middle = []
                initiative_player, non_initiative_player = non_initiative_player, initiative_player
                current_player = initiative_player
                print(initiative_player, non_initiative_player)
                print(current_player)
                continue
        if not player1.has_cards() and not player2.has_cards():
            print("human", player1.points)
            print("bot", player2.points)
            deck = Deck()
            deck.shuffle_deck()
            deck.write_down_deck()
            
            # Deal 4 cards to each player
            player1.draw(deck, 4)
            player2.draw(deck, 4)
            cards_in_the_middle = []
            middle_card_score = 0
            if temp_score_player1 > temp_score_player2:
                initiative_player = player1
                non_initiative_player = player2
            elif temp_score_player2 > temp_score_player1:
                initiative_player = player2
                non_initiative_player = player1
            else:
                pass  #nista se ne menja onaj sa inicijativom je zadrzava
            temp_score_player1 =0
            temp_score_player2 =0
                
                

if __name__ == '__main__':
    if len(sys.argv) == 3:
        mode = sys.argv[1]
        number = int(sys.argv[2])
        run_game(mode, number)
    else:
        print("Invalid arguments. Please provide game mode and number.")
