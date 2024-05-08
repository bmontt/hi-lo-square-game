import pygame
import random

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600
CARD_WIDTH, CARD_HEIGHT = 100, 150
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hi-Lo Card Game")
font = pygame.font.Font(None, 36)
win_sound = pygame.mixer.Sound('hi_lo_square/packs/sounds/win_song.wav')
loss_sound = pygame.mixer.Sound('hi_lo_square/packs/sounds/loss_song.wav')

SUITS = ['hearts', 'diamonds', 'clubs', 'spades']
RANKS = ['02', '03', '04', '05', '06', '07', '08', '09', '10', 'J', 'Q', 'K', 'A']
CARDS = [(rank, suit) for suit in SUITS for rank in RANKS]
card_images = {}
for rank, suit in CARDS:
    image = pygame.image.load(f'hi_lo_square/packs/cards/card_{suit}_{rank}.png')
    card_images[(rank, suit)] = pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))
card_back_image = pygame.transform.scale(pygame.image.load('hi_lo_square/packs/cards/card_back.png'), (CARD_WIDTH, CARD_HEIGHT))

class HiLo:
    def __init__(self):
        self.deck = CARDS.copy()
        random.shuffle(self.deck)
        self.grid = [[(self.deck.pop(), 1, False) for _ in range(3)] for _ in range(3)]  # (top card, stack count, is flipped)
        self.selected_card = None
        self.message = ""
        self.flipped_piles = 0
        self.game_over = False

    def draw_grid(self):
        for i in range(3):
            for j in range(3):
                card, count, is_flipped = self.grid[i][j]
                pos_x = 100 + j * 110
                pos_y = 50 + i * 160
                if is_flipped:
                    for offset in range(count):
                        screen.blit(card_back_image, (pos_x + offset * 2, pos_y + offset * 2))  # Add offset for depth effect
                    count_surface = font.render(str(count), True, (0, 0, 0))  # Change text color here
                    count_rect = count_surface.get_rect(center=(pos_x + CARD_WIDTH // 2 + (count - 1) * 2, pos_y + CARD_HEIGHT // 2 + (count - 1) * 2))
                    count_surface.set_alpha(128)
                    screen.blit(count_surface, count_rect)
                else:
                    for offset in range(count):
                        screen.blit(card_images[card], (pos_x + offset * 2, pos_y + offset * 2))
                if (i, j) == self.selected_card:
                    pygame.draw.rect(screen, (255, 0, 0), (pos_x, pos_y, CARD_WIDTH, CARD_HEIGHT), 2)
        # Draw remaining deck
        screen.blit(card_back_image, (800, 450))
        deck_count_surface = font.render(str(len(self.deck)), True, (0, 0, 0))  # Change text color here
        deck_count_rect = deck_count_surface.get_rect(center=(800 + CARD_WIDTH // 2, 500 + CARD_HEIGHT // 2))
        deck_count_surface.set_alpha(128)
    def select_card(self, x, y):
        row, col = (y - 50) // 160, (x - 100) // 110
        if 0 <= row < 3 and 0 <= col < 3 and self.grid[row][col][0] and not self.grid[row][col][2]:
            self.selected_card = (row, col)
            card, count, is_flipped = self.grid[row][col]
            self.message = f"Selected {card[0]} of {card[1]}"

    def play_turn(self, guess):
        if self.game_over or not self.selected_card:
            self.message = "Select a card first."
            return

        x, y = self.selected_card
        chosen_card, count, is_flipped = self.grid[x][y]
        next_card = self.deck.pop() if self.deck else None

        if not next_card:
            self.check_end_conditions()
            return

        if is_flipped:
            self.message = "This pile has been flipped. Choose another pile."
            return

        def rank_to_int(rank):
            return {'02': 2, '03': 3, '04': 4, '05': 5, '06': 6, '07': 7, '08': 8, '09': 9, '10': 10,
                    'J': 11, 'Q': 12, 'K': 13, 'A': 14}[rank]

        chosen_rank = rank_to_int(chosen_card[0])
        next_rank = rank_to_int(next_card[0])

        if (guess == 'higher' and next_rank > chosen_rank) or (guess == 'lower' and next_rank < chosen_rank) or (guess == 'post' and next_rank == chosen_rank):
            self.message = f"Correct! Next card was {next_card[0]} of {next_card[1]}"
            self.grid[x][y] = (next_card, count + 1, is_flipped)
        else:
            self.message = f"Wrong! Next card was {next_card[0]} of {next_card[1]}."
            if not is_flipped:
                self.flipped_piles += 1
            self.grid[x][y] = (next_card, count + 1, True)

            self.check_end_conditions()

    def check_end_conditions(self):
        if self.flipped_piles >= 9:
            self.message = "Game over! All piles are flipped."
            self.show_loss_screen()
        elif not self.deck:
            self.message = "You win! Finished the deck."
            self.show_win_screen()

    def show_win_screen(self):
        pygame.mixer.Sound.play(win_sound)
        self.game_over = True
        # Display win screen
        screen.fill((0, 255, 0))
        win_text = font.render("Congratulations! You Win!", True, (0, 0, 0))
        win_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(win_text, win_rect)
        pygame.display.flip()
        pygame.time.delay(3000)

    def show_loss_screen(self):
        pygame.mixer.Sound.play(loss_sound)
        self.game_over = True
        # Display loss screen
        screen.fill((255, 0, 0))
        loss_text = font.render("Game Over. Better luck next time!", True, (255, 255, 255))
        loss_rect = loss_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(loss_text, loss_rect)
        pygame.display.flip()
        pygame.time.delay(3000)

    def reset_game(self):
        self.deck = CARDS.copy()
        random.shuffle(self.deck)
        self.grid = [[(self.deck.pop(), 1, False) for _ in range(3)] for _ in range(3)]
        self.selected_card = None
        self.flipped_piles = 0
        self.message = "Game reset!"

    def draw_message(self):
        message_surface = font.render(self.message, True, (255, 255, 255))
        screen.blit(message_surface, (20, SCREEN_HEIGHT - 50))

# Initialize game instance
game = HiLo()

# Main game loop
running = True
while running:
    screen.fill((0, 128, 0))
    game.draw_grid()
    game.draw_message()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            game.select_card(x, y)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                game.play_turn('higher')
            elif event.key == pygame.K_l:
                game.play_turn('lower')
            elif event.key == pygame.K_p:
                game.play_turn('post')
            elif event.key == pygame.K_r:
                game.reset_game()

pygame.quit()