import pygame, sys, os, time
from word_manager import WordManager
from utils import draw_text, draw_button, draw_progress_bar

pygame.init()
WIDTH, HEIGHT = 900, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Guess the Word — Intermediate")

FONT = pygame.font.SysFont("DejaVuSans", 32)
BIG = pygame.font.SysFont("DejaVuSans", 48)
SMALL = pygame.font.SysFont("DejaVuSans", 24)

# Paths
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_JSON = os.path.join(ROOT, "data", "words.json")
IMAGES_FOLDER = os.path.join(ROOT, "assets", "images")

wm = WordManager(DATA_JSON, IMAGES_FOLDER)

# Game variables
score = 0
streak = 0
life = 3
time_limit = 5
round_start = None
round_over = False
game_over_screen = False

def load_round():
    global current_word, current_img, current_snippet, user_input, round_start, round_over
    current_word, current_img, current_snippet = wm.get_random()
    # load image safely
    try:
        img = pygame.image.load(current_img)
        img = pygame.transform.scale(img, (380, 300))
    except Exception:
        # placeholder surface
        img = pygame.Surface((380,300))
        img.fill((240,240,240))
    current_img_surf = img
    user_input = ""
    round_start = time.time()
    # new round is active, not over — ensure round_over is False
    round_over = False
    return current_img_surf

# Buttons
NEXT_BTN = (700, 500, 140, 50)
RESTART_BTN = (320, 360, 140, 50)
QUIT_BTN = (500, 360, 140, 50)

current_img_surf = load_round()
total_rounds_played = 0

clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(30) / 1000.0

    # If we're in game over state, draw a full black screen and skip normal UI
    if game_over_screen:
        SCREEN.fill((0, 0, 0))
    else:
        SCREEN.fill((255,255,255))

        # Draw image
        SCREEN.blit(current_img_surf, (40,150))
        draw_text(SCREEN, "Guess the Word", 40, 30, BIG)

        # Right panel info
        draw_text(SCREEN, f"Score: {score}", 500, 30, FONT)
        draw_text(SCREEN, f"Lives: {life}", 500, 70, FONT)
        draw_text(SCREEN, f"Streak: {streak}", 680, 30, FONT)
        draw_text(SCREEN, f"Hint: {current_snippet}", 460, 150, FONT)

        draw_text(SCREEN, f"Your Guess: {user_input}", 460, 220, BIG)

        # Timer & progress bar
        elapsed = time.time() - round_start
        remaining = max(0, time_limit - elapsed)
        draw_text(SCREEN, f"Time Left: {int(remaining)}s", 460, 280, FONT)
        draw_progress_bar(SCREEN, 460, 320, 360, 24, remaining / time_limit)

        # Next button
        draw_button(SCREEN, NEXT_BTN, "Next", FONT)

        # Check automatic timeout — when the timer hits zero: mark the round over,
        # decrement life and reset streak. If lives run out, show Game Over and stop
        # loading new rounds; otherwise pause briefly and load the next round.
        if remaining <= 0 and not round_over:
            round_over = True
            streak = 0
            life -= 1

            if life <= 0:
                # Activate game over screen (don't quit immediately, no new round)
                game_over_screen = True
            else:
                # small pause so the player can see the timeout, then load the next round
                pygame.time.delay(700)
                current_img_surf = load_round()
                total_rounds_played += 1

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos

            # If we're on the Game Over screen, only allow Restart / Quit clicks
            if game_over_screen:
                rx, ry, rw, rh = RESTART_BTN
                qx, qy, qw, qh = QUIT_BTN
                if rx <= mx <= rx+rw and ry <= my <= ry+rh:
                    # restart game: reset game state and load a fresh round
                    score = 0
                    streak = 0
                    life = 3
                    total_rounds_played = 0
                    current_img_surf = load_round()
                    round_over = False
                    game_over_screen = False
                elif qx <= mx <= qx+qw and qy <= my <= qy+qh:
                    running = False
                    break
                # ignore other clicks while in game over
                continue

            # Normal click handling
            x,y,w,h = NEXT_BTN
            if x <= mx <= x+w and y <= my <= y+h:
                # load next round
                current_img_surf = load_round()
                total_rounds_played += 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]
            elif event.key == pygame.K_RETURN:
                # submit guess
                if user_input.strip().lower() == current_word.lower():
                    # correct!
                    score += 10 + int((time_limit - (time.time()-round_start)))  # bonus for speed
                    streak += 1
                    round_over =True
                    # auto load next round after a brief pause
                    pygame.time.delay(700)
                    current_img_surf = load_round()
                    total_rounds_played += 1
                else:
                    # wrong
                    score = max(0, score-2)
                    streak = 0
                    user_input = ""
            else:
                ch = event.unicode
                if ch.isprintable() and len(ch) == 1:
                    user_input += ch

    # draw game over UI on top if the board is in that state
    if game_over_screen:
        # gray out / overlay could be added, for now just show center Game Over and options
        draw_text(SCREEN, "Game Over", 320, 300, BIG, color=(200,0,0))
        draw_button(SCREEN, RESTART_BTN, "Restart", FONT)
        draw_button(SCREEN, QUIT_BTN, "Quit", FONT)

    pygame.display.flip()

pygame.quit()
sys.exit()