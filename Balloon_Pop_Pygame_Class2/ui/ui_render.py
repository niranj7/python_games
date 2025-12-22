
import pygame

COLORS = [
    (255, 99, 71),
    (135, 206, 250),
    (255, 215, 0),
    (144, 238, 144),
    (221, 160, 221)
]

def draw_balloon(screen, balloon, font):
    color = COLORS[balloon.number % len(COLORS)]
    pygame.draw.circle(screen, color, (balloon.x, balloon.y), balloon.radius)
    text = font.render(str(balloon.number), True, (0, 0, 0))
    screen.blit(text, (balloon.x - 12, balloon.y - 20))

def draw_text(screen, font, text, pos):
    render = font.render(text, True, (0, 0, 0))
    screen.blit(render, pos)
