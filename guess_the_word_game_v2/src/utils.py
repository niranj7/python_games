import pygame, math

def draw_text(surface, text, x, y, font, color=(0,0,0)):
    txt = font.render(text, True, color)
    surface.blit(txt, (x,y))

def draw_button(surface, rect, text, font, bg=(200,200,200)):
    pygame.draw.rect(surface, bg, rect, border_radius=6)
    txt = font.render(text, True, (0,0,0))
    tx, ty = txt.get_size()
    sx = rect[0] + (rect[2]-tx)//2
    sy = rect[1] + (rect[3]-ty)//2
    surface.blit(txt, (sx, sy))

def draw_progress_bar(surface, x, y, w, h, progress, border_color=(0,0,0)):
    pygame.draw.rect(surface, (220,220,220), (x,y,w,h))
    inner_w = max(1, int(w * max(0,min(1,progress))))
    pygame.draw.rect(surface, (100,200,100), (x,y,inner_w,h))
    pygame.draw.rect(surface, border_color, (x,y,w,h), 2)