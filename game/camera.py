from .core import *

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

    def update(self, target_rect):
        self.x = target_rect.centerx - SCREEN_WIDTH // 2
        self.y = target_rect.centery - SCREEN_HEIGHT // 2
        self.x = clamp(self.x, 0, max(0, WORLD_WIDTH - SCREEN_WIDTH))
        self.y = clamp(self.y, 0, max(0, WORLD_HEIGHT - SCREEN_HEIGHT))

    def world_to_screen(self, x, y):
        return int(x - self.x), int(y - self.y)


