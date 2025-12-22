
import pygame
import sys
import math
import random
from collections import deque

pygame.init()

# constants wifth and height mentioned here
WIDTH, HEIGHT = 1000, 640
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pizza Fraction Match — Animated")
FPS = 60
CLOCK = pygame.time.Clock()

# coilur lay about the game 
WHITE = (255, 255, 255)
BLACK = (10, 10,10)
BUTTON_COLOR = (230, 230, 230)
BUTTON_BORDER = (40, 40, 40)
CORRECT_GREEN = (70, 190, 110)
WRONG_RED = (220, 90, 90)
OVERLAY_COLOR = (255, 100, 100, 130)  

# Fonts size set according to your edit
FONT = pygame.font.SysFont(None, 30)
BIGFONT = pygame.font.SysFont(None, 40)
SCORE_FONT = pygame.font.SysFont(None, 48)

# Loading pizza image 
try:
    pizza_raw = pygame.image.load("pizza3.png").convert_alpha()
except Exception as e:
    raise SystemExit("Could not load 'pizza.png'. Put pizza.png in the same folder.") from e

# scaling size 2
PIZZA_SIZE = 360
pizza_raw = pygame.transform.smoothscale(pizza_raw, (PIZZA_SIZE, PIZZA_SIZE))


# angle decision 
def polar(cx, cy, r, angle):
    return (cx + r * math.cos(angle), cy + r * math.sin(angle))


def draw_text(surf, text, pos, font=FONT, color=BLACK):
    surf.blit(font.render(text, True, color), pos)


# all kind of animations
class FloatText:
    """Floating score text animation"""
    def __init__(self, text, pos, color=(0, 0, 0)):
        self.text = text
        self.x, self.y = pos
        self.vy = -1.6
        self.alpha = 255
        self.color = color
        img = SCORE_FONT.render(self.text, True, self.color)
        self.img = img.convert_alpha()

    def update(self):
        self.y += self.vy
        self.alpha -= 4
        if self.alpha < 0:
            self.alpha = 0
        self.img.set_alpha(self.alpha)

    def draw(self, surf):
        surf.blit(self.img, (self.x - self.img.get_width() // 2, self.y - self.img.get_height() // 2))

    def alive(self):
        return self.alpha > 0


# animation hovering effect
class Button:
    def __init__(self, rect, text, action=None):
        self.base_rect = pygame.Rect(rect)
        self.text = text
        self.action = action
        self.hover = False
        self.hover_scale = 1.0

    def update(self, mouse_pos):
        self.hover = self.base_rect.collidepoint(mouse_pos)
        # spring animation
        target = 1.06 if self.hover else 1.0
        self.hover_scale += (target - self.hover_scale) * 0.2

    def draw(self, surf):
        # draw polygon 
        bw, bh = self.base_rect.size
        w = int(bw * self.hover_scale)
        h = int(bh * self.hover_scale)
        x = self.base_rect.centerx - w // 2
        y = self.base_rect.centery - h // 2
        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(surf, BUTTON_COLOR, rect, border_radius=10)
        pygame.draw.rect(surf, BUTTON_BORDER, rect, 2, border_radius=10)
        txt = FONT.render(self.text, True, BLACK)
        surf.blit(txt, (rect.x + (rect.w - txt.get_width()) // 2,
                        rect.y + (rect.h - txt.get_height()) // 2))

    def handle_event(self, evt):
        if evt.type == pygame.MOUSEBUTTONDOWN and evt.button == 1:
            if self.base_rect.collidepoint(evt.pos):
                if self.action:
                    self.action()


# drawn animation x,y coordinates in line inside cls3 
class PizzaSprite:
    def __init__(self, image, center):
        self.base_image = image
        self.center = list(center)  
        self.size = image.get_width()
        self.radius = self.size // 2 - 6

        # rotation8
        self.angle = 0.0
        self.rotation_speed = 12.0 / FPS  

        # slice-cut animation (A)
        self.cut_progress = 0.0  # 0..1 : progress of drawing all cuts
        self.cutting = False

        # pop animation for correct slices (C)
        self.pop_progress = 0.0
        self.popping = False

        # shake animation for wrong answer (D)
        self.shake_timer = 0
        self.shake_strength = 0

        # current fraction details
        self.den = 8
        self.num = 3
        self.highlight_indices = set()

    def start_round(self, num, den):
        self.num = num
        self.den = den
        # choose random indices to highlight (non-contiguous permitted)
        indices = list(range(den))
        random.shuffle(indices)
        self.highlight_indices = set(sorted(indices[:num]))
        # start cut animation
        self.cutting = True
        self.cut_progress = 0.0
        # stop any pop/shake
        self.popping = False
        self.pop_progress = 0.0

    def update(self):
        # rotation always (slow)
        self.angle = (self.angle + self.rotation_speed) % 360

        # cutting animation progress
        if self.cutting:
            self.cut_progress += 0.03  # adjust speed
            if self.cut_progress >= 1.0:
                self.cut_progress = 1.0
                self.cutting = False

        # pop animation
        if self.popping:
            self.pop_progress += 0.06
            if self.pop_progress >= 1.0:
                self.pop_progress = 0.0
                self.popping = False

        # shake
        if self.shake_timer > 0:
            self.shake_timer -= 1
            # decline strength
            self.shake_strength *= 0.92
            if self.shake_timer <= 0:
                self.shake_strength = 0

    def trigger_pop(self):
        self.popping = True
        self.pop_progress = 0.0

    def trigger_shake(self):
        self.shake_timer = 18
        self.shake_strength = 10.0

    def draw(self, surf):
        # compute rotated pizza
        rotated = pygame.transform.rotozoom(self.base_image, -self.angle, 1.0)
        rect = rotated.get_rect(center=self.center)

        # apply shake offset if any
        shake_offset = (0, 0)
        if self.shake_strength > 0:
            sx = math.sin(pygame.time.get_ticks() * 0.05) * self.shake_strength
            sy = math.cos(pygame.time.get_ticks() * 0.04) * (self.shake_strength * 0.4)
            shake_offset = (sx, sy)
            rect = rect.move(shake_offset)

        # draw pizza line
        surf.blit(rotated, rect)


        cx, cy = rect.center

    
        total_lines = self.den
        revealed = int(total_lines * self.cut_progress + 1e-6)
        partial = (total_lines * self.cut_progress) - revealed  
        ang_step = 2 * math.pi / self.den

        
        overlay_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    
        pop_scale = 1.0
        if self.popping:
            p = self.pop_progress
            pop_scale = 1.0 + 0.25 * math.sin(math.pi * p)  
        rot_offset = math.radians(self.angle)

        for i in range(self.den):
            # overlay only for indices that should be highlighted
            if i in self.highlight_indices:
                start_ang = -math.pi/2 + i * ang_step + rot_offset
                end_ang = start_ang + ang_step

                #poping
                r = (self.radius) * pop_scale
                # polygon points of slice
                points = [(cx, cy)]
                steps = max(6, int(r * ang_step / 8))
                for s in range(steps + 1):
                    a = start_ang + (end_ang - start_ang) * (s / steps)
                    points.append(polar(cx, cy, r, a))

                pygame.draw.polygon(overlay_surf, OVERLAY_COLOR, points)

        surf.blit(overlay_surf, (0, 0))

        for i in range(total_lines):
            start_ang = -math.pi/2 + i * ang_step + rot_offset
            x1, y1 = polar(cx, cy, self.radius + 6, start_ang)
            x2, y2 = cx, cy
            if i < revealed:
                pygame.draw.line(surf, BLACK, (cx, cy), (x1, y1), 3)
            elif i == revealed and self.cutting:
                px, py = polar(cx, cy, (self.radius + 6) * max(0.02, partial), start_ang)
                pygame.draw.line(surf, BLACK, (cx, cy), (px, py), 3)

    
        pygame.draw.circle(surf, BLACK, (cx, cy), int(self.radius)+6, 2)


# game main part
class Game:
    def __init__(self):
        self.pizza = PizzaSprite(pizza_raw, (WIDTH//3, HEIGHT//2))
        self.score = 0
        self.round = 0
        self.lives = 3
        self.message = ""
        self.message_timer = 0

        self.buttons = []   # Button objects (answers)
        self.correct_answer = None
        self.options = []
        self.float_texts = deque()  # list of FloatText

        self.create_round()
        # restart button
        self.restart_btn = Button((WIDTH - 170, 20, 140, 44), "Restart (R)", self.restart)

    def restart(self):
        self.score = 0
        self.round = 0
        self.lives = 3
        self.create_round()

    def create_round(self):
        self.round += 1
        denom_choices = [2, 3, 4, 6, 8]
        d = random.choice(denom_choices)
        n = random.randint(1, d - 1)
        self.correct_answer = f"{n}/{d}"
        self.pizza.start_round(n, d)

        # build choices (one correct + 3 distractors)
        opts = {self.correct_answer}
        while len(opts) < 4:
            dd = random.choice(denom_choices)
            nn = random.randint(1, dd-1)
            opts.add(f"{nn}/{dd}")
        self.options = list(opts)
        random.shuffle(self.options)

        # create buttons on right side
        bx = WIDTH//2 + 30
        by = HEIGHT//2 - 120
        bw, bh = 260, 62
        gap = 18
        self.buttons = []
        for i, opt in enumerate(self.options):
            btn = Button((bx, by + i*(bh + gap), bw, bh), opt, action=lambda o=opt: self.select_option(o))
            self.buttons.append(btn)

    def select_option(self, opt_text):
        # ignore input if a message is showing for a long time
        if self.message_timer > 0:
            return

        if opt_text == self.correct_answer:
            # correct: +10, pop animation, floating score text
            self.score += 10
            self.message = "Correct!"
            self.message_timer = 24  # short message cooldown
            self.pizza.trigger_pop()
            # spawn float text above pizza
            ft = FloatText("+10", (self.pizza.center[0], self.pizza.center[1] - self.pizza.radius - 18), CORRECT_GREEN)
            self.float_texts.append(ft)
            # after pop, new round after slight delay
            pygame.time.set_timer(pygame.USEREVENT + 1, 700, True)  
        else:
            self.lives -= 1
            self.message = f"Wrong! Correct: {self.correct_answer}"
            self.message_timer = 60
            self.pizza.trigger_shake()
            # float wrong text
            ft = FloatText("-1", (self.pizza.center[0], self.pizza.center[1] - self.pizza.radius - 18), WRONG_RED)
            self.float_texts.append(ft)
            if self.lives <= 0:
                self.message = f"Game Over! Final Score: {self.score}. Press R."
                self.message_timer = 300

    def update(self):
        # update pizza sprite animations
        self.pizza.update()

        # update float texts
        for ft in list(self.float_texts):
            ft.update()
            if not ft.alive():
                self.float_texts.popleft()

        # update message timer
        if self.message_timer > 0:
            self.message_timer -= 1
            if self.message_timer <= 0:
                self.message = ""


        mpos = pygame.mouse.get_pos()
        for b in self.buttons + [self.restart_btn]:
            b.update(mpos)

    def handle_event(self, evt):
        if evt.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_r:
                self.restart()
        if evt.type == pygame.MOUSEBUTTONDOWN and evt.button == 1:
            for b in self.buttons:
                b.handle_event(evt)
            self.restart_btn.handle_event(evt)
    
        if evt.type == pygame.USEREVENT + 1:
            
            if self.lives > 0:
                self.create_round()

    def draw(self, surf):
        surf.fill(WHITE)

        
        self.pizza.draw(surf)

    
        draw_text(surf, "Select the fraction that matches", (WIDTH//2 + 30, 60), BIGFONT)
        for b in self.buttons:
            b.draw(surf)

        # restart
        self.restart_btn.draw(surf)

        draw_text(surf, f"Score: {self.score}", (18, 18))
        draw_text(surf, f"Lives: {self.lives}", (18, 48))
        draw_text(surf, f"Round: {self.round}", (18, 78))

        # message center
        if self.message:
            txt = BIGFONT.render(self.message, True, BLACK)
            r = txt.get_rect(center=(WIDTH//2, HEIGHT - 48))
            # backdrop
            pygame.draw.rect(surf, (250,250,250), r.inflate(18, 14), border_radius=10)
            pygame.draw.rect(surf, BLACK, r.inflate(18,14), 2, border_radius=10)
            surf.blit(txt, r.topleft)

        # draw floating texts sytle
        for ft in self.float_texts:
            ft.draw(surf)


#main loop
def main():
    game = Game()
    running = True
    while running:
        for evt in pygame.event.get():
            game.handle_event(evt)

        game.update()
        game.draw(SCREEN)

        pygame.display.flip()
        CLOCK.tick(FPS)


if __name__ == "__main__":
    main()

