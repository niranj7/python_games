
import pygame
import sys
from logic.game_logic import Balloon
from ui.ui_render import draw_balloon, draw_text

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Balloon Pop - Learn Numbers")

FONT = pygame.font.SysFont(None, 50)
SMALL = pygame.font.SysFont(None, 32)
clock = pygame.time.Clock()

balloons = [Balloon(WIDTH, HEIGHT) for _ in range(5)]
target = 5
score = 0
message = ""

running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for b in balloons:
                if b.is_clicked(event.pos):
                    if b.number == target:
                        score += 1
                        message = "Good Job!"
                        target = (target % 10) + 1
                        balloons.remove(b)
                        balloons.append(Balloon(WIDTH, HEIGHT))
                    else:
                        message = "Try Again"

    for b in balloons:
        b.move()
        draw_balloon(screen, b, FONT)
        if b.y < -50:
            balloons.remove(b)
            balloons.append(Balloon(WIDTH, HEIGHT))

    draw_text(screen, FONT, f"Pop Number: {target}", (20, 20))
    draw_text(screen, SMALL, f"Score: {score}", (20, 80))
    draw_text(screen, SMALL, message, (20, 120))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
