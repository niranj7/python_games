
import pygame
import sys
from game_logic import generate_question, check_answer
from ui import Button, draw_text

pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multiplication Missing Number Game")
clock = pygame.time.Clock()

WHITE = (245, 245, 245)
BLACK = (20, 20, 20)
GREEN = (70, 180, 120)
RED = (220, 90, 90)
BLUE = (80, 140, 220)

font_big = pygame.font.SysFont(None, 64)
font = pygame.font.SysFont(None, 36)

score = 0
feedback = ""
feedback_color = BLACK

question, correct_answer = generate_question()

buttons = []
for i in range(1, 11):
    x = 80 + ((i-1) % 5) * 150
    y = 360 + ((i-1) // 5) * 80
    buttons.append(Button(x, y, 120, 60, str(i)))

running = True
while running:
    screen.fill(WHITE)

    draw_text(screen, f"Score: {score}", font, BLACK, 20, 20)
    draw_text(screen, question, font_big, BLACK, WIDTH//2 - 150, 150)
    draw_text(screen, feedback, font, feedback_color, WIDTH//2 - 80, 250)

    for b in buttons:
        b.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            for b in buttons:
                if b.is_clicked(event.pos):
                    if check_answer(int(b.text), correct_answer):
                        score += 10
                        feedback = "Correct!"
                        feedback_color = GREEN
                        question, correct_answer = generate_question()
                    else:
                        feedback = "Try Again!"
                        feedback_color = RED

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
