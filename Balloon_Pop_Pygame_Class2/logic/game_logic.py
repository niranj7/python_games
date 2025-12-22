
import random

class Balloon:
    def __init__(self, width, height):
        self.radius = 40
        self.x = random.randint(self.radius, width - self.radius)
        self.y = height + random.randint(50, 300)
        self.speed = random.randint(1, 3)
        self.number = random.randint(1, 10)

    def move(self):
        self.y -= self.speed

    def is_clicked(self, pos):
        dx = pos[0] - self.x
        dy = pos[1] - self.y
        return dx * dx + dy * dy <= self.radius * self.radius
