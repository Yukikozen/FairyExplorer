import os
import math
import random
import json
import pygame

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700
WORLD_WIDTH = 4000
WORLD_HEIGHT = 3000
PLAYER_SPEED = 4.0
COMPANION_SPEED = 3.5
NPC_MIN_SPEED = 1.0
NPC_MAX_SPEED = 1.7
NPC_INTERACTION_DISTANCE = 115
FPS = 60
# One full in-game day lasts 6 real minutes.
GAME_DAY_LENGTH_MS = 6 * 60 * 1000
NPC_HOME_HOUR = 20
NPC_WAKE_HOUR = 6

GAME_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(GAME_DIR)
ASSET_DIR = os.path.join(PROJECT_DIR, "assets", "fairies")

def asset_path(filename):
    return os.path.join(ASSET_DIR, filename)

def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))

def distance(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)

def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = word if not current else current + " " + word
        if font.size(test)[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines

def load_image(filename, size=None):
    path = asset_path(filename)
    if not os.path.exists(path):
        return None
    try:
        image = pygame.image.load(path).convert_alpha()
        if size:
            image = pygame.transform.smoothscale(image, size)
        return image
    except pygame.error:
        return None

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

# # ================================================================
# # game/game.py
# # ================================================================

# import os
# import math
# import random
# import pygame


# # ================================================================
# # CONSTANTS
# # ================================================================

# SCREEN_WIDTH = 1100
# SCREEN_HEIGHT = 700

# WORLD_WIDTH = 4000
# WORLD_HEIGHT = 3000

# PLAYER_SPEED = 4.0
# COMPANION_SPEED = 3.5

# NPC_MIN_SPEED = 1.0
# NPC_MAX_SPEED = 1.7

# NPC_INTERACTION_DISTANCE = 115

# FPS = 60
# One full in-game day lasts 6 real minutes.
GAME_DAY_LENGTH_MS = 6 * 60 * 1000
NPC_HOME_HOUR = 20
NPC_WAKE_HOUR = 6


# # ================================================================
# # PATHS
# # ================================================================

# GAME_DIR = os.path.dirname(os.path.abspath(__file__))
# PROJECT_DIR = os.path.dirname(GAME_DIR)
# ASSET_DIR = os.path.join(PROJECT_DIR, "assets", "fairies")


# def asset_path(filename):
#     return os.path.join(ASSET_DIR, filename)


# # ================================================================
# # HELPERS
# # ================================================================

# def clamp(value, minimum, maximum):
#     return max(minimum, min(value, maximum))


# def distance(x1, y1, x2, y2):
#     return math.hypot(x2 - x1, y2 - y1)


# def wrap_text(text, font, max_width):
#     words = text.split()
#     lines = []
#     current = ""

#     for word in words:
#         test = word if not current else current + " " + word

#         if font.size(test)[0] <= max_width:
#             current = test
#         else:
#             if current:
#                 lines.append(current)
#             current = word

#     if current:
#         lines.append(current)

#     return lines


# def load_image(filename, size=None):
#     path = asset_path(filename)

#     if not os.path.exists(path):
#         return None

#     try:
#         image = pygame.image.load(path).convert_alpha()

#         if size:
#             image = pygame.transform.smoothscale(
#                 image,
#                 size
#             )

#         return image

#     except pygame.error:
#         return None


# # ================================================================
# # CAMERA
# # ================================================================

# class Camera:
#     def __init__(self):
#         self.x = 0
#         self.y = 0

#     def update(self, target_rect):
#         self.x = target_rect.centerx - SCREEN_WIDTH // 2
#         self.y = target_rect.centery - SCREEN_HEIGHT // 2

#         self.x = clamp(
#             self.x,
#             0,
#             max(0, WORLD_WIDTH - SCREEN_WIDTH)
#         )

#         self.y = clamp(
#             self.y,
#             0,
#             max(0, WORLD_HEIGHT - SCREEN_HEIGHT)
#         )

#     def world_to_screen(self, x, y):
#         return (
#             int(x - self.x),
#             int(y - self.y)
#         )


# # ================================================================
# # OBSTACLE
# # ================================================================

# class Obstacle:
#     def __init__(
#         self,
#         x,
#         y,
#         width,
#         height,
#         kind="tree"
#     ):
#         self.rect = pygame.Rect(
#             x,
#             y,
#             width,
#             height
#         )

#         self.kind = kind

#     def draw(self, screen, camera):
#         rect = self.rect.move(
#             -camera.x,
#             -camera.y
#         )

#         if (
#             rect.right < 0
#             or rect.left > SCREEN_WIDTH
#             or rect.bottom < 0
#             or rect.top > SCREEN_HEIGHT
#         ):
#             return

#         if self.kind == "tree":

#             trunk = pygame.Rect(
#                 rect.centerx - 10,
#                 rect.bottom - 40,
#                 20,
#                 40
#             )

#             pygame.draw.rect(
#                 screen,
#                 (125, 82, 48),
#                 trunk,
#                 border_radius=5
#             )

#             pygame.draw.circle(
#                 screen,
#                 (70, 150, 80),
#                 (rect.centerx, rect.top + 25),
#                 42
#             )

#             pygame.draw.circle(
#                 screen,
#                 (90, 175, 95),
#                 (
#                     rect.centerx - 25,
#                     rect.top + 38
#                 ),
#                 30
#             )

#             pygame.draw.circle(
#                 screen,
#                 (65, 140, 75),
#                 (
#                     rect.centerx + 25,
#                     rect.top + 40
#                 ),
#                 30
#             )

#         elif self.kind == "rock":

#             pygame.draw.ellipse(
#                 screen,
#                 (125, 130, 145),
#                 rect
#             )

#             pygame.draw.ellipse(
#                 screen,
#                 (155, 160, 175),
#                 rect.inflate(-10, -10)
#             )

#         elif self.kind == "house":

            # Pseudo-3D fairy house: layered walls, side wall, foundation,
            # deep roof, eaves and highlights create an isometric-style look
            # while keeping the game fully compatible with Pygame 2D.
#             body_colors = {
#                 "mushroom": (232, 185, 145),
#                 "flower": (246, 205, 158),
#                 "crystal": (185, 170, 225),
#                 "treehouse": (176, 132, 92),
#                 "pond": (170, 210, 198),
#                 "default": (220, 172, 132),
#             }
#             roof_colors = {
#                 "mushroom": (205, 82, 125),
#                 "flower": (238, 135, 78),
#                 "crystal": (105, 125, 205),
#                 "treehouse": (82, 140, 76),
#                 "pond": (75, 160, 155),
#                 "default": (170, 88, 120),
#             }

#             body = body_colors.get(self.style, body_colors["default"])
#             roof = roof_colors.get(self.style, roof_colors["default"])
#             side = tuple(max(0, c - 38) for c in body)
#             dark = tuple(max(0, c - 65) for c in body)
#             light = tuple(min(255, c + 28) for c in body)

#             depth = 24
#             lift = 16

            # Ground shadow makes the building feel elevated from the ground.
#             shadow = pygame.Rect(
#                 rect.left - 8, rect.bottom - 4,
#                 rect.width + 30, 24
#             )
#             pygame.draw.ellipse(screen, (105, 120, 105), shadow)

            # Raised stone foundation.
#             foundation = pygame.Rect(
#                 rect.left - 2, rect.bottom - 20,
#                 rect.width + 4, 20
#             )
#             pygame.draw.rect(screen, dark, foundation, border_radius=5)
#             pygame.draw.line(
#                 screen, light,
#                 (foundation.left + 5, foundation.top + 4),
#                 (foundation.right - 5, foundation.top + 4), 3
#             )

            # Right-side wall gives the house visible depth.
#             side_points = [
#                 (rect.right, rect.top + 10),
#                 (rect.right + depth, rect.top - lift + 10),
#                 (rect.right + depth, rect.bottom - 20 - lift),
#                 (rect.right, rect.bottom - 20),
#             ]
#             pygame.draw.polygon(screen, side, side_points)
#             pygame.draw.line(screen, dark, side_points[1], side_points[2], 3)

            # Front wall.
#             pygame.draw.rect(screen, body, rect, border_radius=10)
#             pygame.draw.rect(
#                 screen, light, rect.inflate(-8, -8), 3, border_radius=8
#             )

            # Vertical wall shading to strengthen the 3D form.
#             pygame.draw.rect(
#                 screen, tuple(max(0, c - 18) for c in body),
#                 (rect.right - 18, rect.top + 10, 18, rect.height - 30)
#             )

            # Deep roof/eave layer.
#             roof_left = rect.left - 22
#             roof_right = rect.right + depth + 12
#             roof_base_y = rect.top + 28
#             roof_peak_y = rect.top - 58

            # Roof thickness first.
#             roof_depth = [
#                 (roof_left, roof_base_y),
#                 (rect.centerx, roof_peak_y),
#                 (roof_right, roof_base_y),
#                 (roof_right, roof_base_y + 18),
#                 (rect.centerx, roof_peak_y + 18),
#                 (roof_left, roof_base_y + 18),
#             ]
#             pygame.draw.polygon(
#                 screen, tuple(max(0, c - 42) for c in roof), roof_depth
#             )

            # Main solid roof.
#             roof_points = [
#                 (roof_left, roof_base_y),
#                 (rect.centerx, roof_peak_y),
#                 (roof_right, roof_base_y),
#             ]
#             pygame.draw.polygon(screen, roof, roof_points)
#             pygame.draw.polygon(screen, light, roof_points, 3)

            # Roof highlight gives a lit top plane.
#             highlight = tuple(min(255, c + 25) for c in roof)
#             pygame.draw.line(
#                 screen, highlight,
#                 (rect.centerx, roof_peak_y + 5),
#                 (roof_left + 24, roof_base_y - 5), 5
#             )

#             if self.style == "mushroom":
                # Solid mushroom cap with raised spots.
#                 for sx, sy, sr in [
#                     (rect.left + 30, rect.top - 20, 10),
#                     (rect.centerx, rect.top - 42, 13),
#                     (rect.right - 30, rect.top - 18, 9),
#                 ]:
#                     pygame.draw.circle(screen, (255, 225, 230), (sx, sy), sr)
#                     pygame.draw.circle(screen, (235, 185, 195), (sx, sy), sr, 2)

#             elif self.style == "flower":
                # Raised flower ornament on the roof peak.
#                 cx, cy = rect.centerx, roof_peak_y + 12
#                 for angle in range(0, 360, 72):
#                     rad = math.radians(angle)
#                     px = cx + int(math.cos(rad) * 22)
#                     py = cy + int(math.sin(rad) * 12)
#                     pygame.draw.ellipse(screen, (255, 180, 205), (px - 14, py - 9, 28, 18))
#                 pygame.draw.circle(screen, (255, 220, 80), (cx, cy), 9)

#             elif self.style == "crystal":
                # Crystal towers rising from the roof.
#                 for cx, cy, w, h in [
#                     (rect.left + 42, roof_base_y - 5, 18, 48),
#                     (rect.centerx + 8, roof_peak_y + 4, 22, 60),
#                     (rect.right - 38, roof_base_y - 3, 16, 42),
#                 ]:
#                     pts = [(cx, cy - h), (cx + w // 2, cy), (cx, cy + 4), (cx - w // 2, cy)]
#                     pygame.draw.polygon(screen, (165, 205, 255), pts)
#                     pygame.draw.polygon(screen, (240, 245, 255), pts, 2)

#             elif self.style == "treehouse":
                # Wooden supports extend below the elevated cottage.
#                 for px in (rect.left + 25, rect.right - 25):
#                     pygame.draw.line(
#                         screen, (92, 62, 38),
#                         (px, rect.bottom - 8),
#                         (px + 8, rect.bottom + 22), 13
#                     )
#                 pygame.draw.circle(screen, (110, 170, 85), (rect.centerx, roof_peak_y + 22), 42)
#                 pygame.draw.circle(screen, (145, 195, 100), (rect.left + 35, roof_base_y), 25)
#                 pygame.draw.circle(screen, (90, 150, 75), (rect.right - 30, roof_base_y + 4), 28)

#             elif self.style == "pond":
                # Layered blue roof like a magical water dome.
#                 pygame.draw.ellipse(
#                     screen, (105, 195, 190),
#                     (rect.left + 18, roof_peak_y - 2, rect.width - 36, 38)
#                 )
#                 pygame.draw.arc(
#                     screen, (225, 255, 250),
#                     (rect.left + 25, roof_peak_y + 4, rect.width - 50, 25),
#                     math.pi, math.pi * 2, 3
#                 )

            # Windows with thick frames and side shading.
#             window_y = rect.top + 55
#             for wx in (rect.left + 36, rect.right - 36):
#                 frame = pygame.Rect(wx - 18, window_y - 18, 36, 36)
#                 pygame.draw.rect(screen, dark, frame, border_radius=8)
#                 glass = frame.inflate(-5, -5)
#                 pygame.draw.rect(screen, (145, 220, 238), glass, border_radius=6)
#                 pygame.draw.line(screen, (235, 255, 255), glass.topleft, glass.bottomright, 3)
#                 pygame.draw.line(screen, (105, 170, 195), (wx, glass.top), (wx, glass.bottom), 2)
#                 pygame.draw.line(screen, (105, 170, 195), (glass.left, window_y), (glass.right, window_y), 2)

            # Recessed front door.
#             door = pygame.Rect(rect.centerx - 20, rect.bottom - 66, 40, 66)
#             pygame.draw.rect(screen, dark, door.inflate(8, 8), border_radius=10)
#             pygame.draw.rect(
#                 screen, (105, 70, 58) if self.style != "crystal" else (82, 78, 125),
#                 door, border_radius=8
#             )
#             pygame.draw.line(
#                 screen, (155, 110, 88),
#                 (door.left + 5, door.top + 5),
#                 (door.left + 5, door.bottom - 8), 3
#             )
#             pygame.draw.circle(screen, (255, 215, 100), (door.right - 8, door.centery), 4)

            # Chimney with visible top and side face.
#             chimney = pygame.Rect(rect.right - 42, rect.top - 30, 22, 48)
#             pygame.draw.rect(screen, (145, 105, 95), chimney)
#             pygame.draw.polygon(screen, (115, 82, 75), [
#                 (chimney.right, chimney.top),
#                 (chimney.right + 8, chimney.top - 5),
#                 (chimney.right + 8, chimney.bottom - 5),
#                 (chimney.right, chimney.bottom),
#             ])
#             pygame.draw.rect(screen, (190, 145, 130), chimney.inflate(4, 4), 3)

            # Small garden stones and flowers kept inside the house footprint.
#             for dx in (-58, 58):
#                 gx = rect.centerx + dx
#                 pygame.draw.ellipse(screen, (125, 135, 125), (gx - 8, rect.bottom - 12, 16, 8))
#                 pygame.draw.circle(screen, (255, 175, 210), (gx, rect.bottom - 18), 5)

#         elif self.kind == "fence":

#             pygame.draw.rect(
#                 screen,
#                 (170, 120, 75),
#                 rect,
#                 border_radius=3
#             )

#             for x in range(
#                 rect.left + 10,
#                 rect.right,
#                 35
#             ):
#                 pygame.draw.rect(
#                     screen,
#                     (195, 145, 90),
#                     (
#                         x,
#                         rect.top - 8,
#                         10,
#                         rect.height + 16
#                     ),
#                     border_radius=3
#                 )


# # ================================================================
# # FLOWER
# # ================================================================

# class Flower:
#     def __init__(self, x, y, flower_id):
#         self.x = x
#         self.y = y
#         self.flower_id = flower_id
#         self.collected = False

#         self.phase = random.uniform(
#             0,
#             math.pi * 2
#         )

#     def update(self, dt):
#         self.phase += dt * 0.003

#     def draw(self, screen, camera):
#         if self.collected:
#             return

#         sx, sy = camera.world_to_screen(
#             self.x,
#             self.y
#         )

#         if (
#             sx < -20
#             or sx > SCREEN_WIDTH + 20
#             or sy < -20
#             or sy > SCREEN_HEIGHT + 20
#         ):
#             return

#         bob = math.sin(self.phase) * 2

#         pygame.draw.line(
#             screen,
#             (70, 155, 75),
#             (
#                 sx,
#                 sy + 8 + bob
#             ),
#             (
#                 sx,
#                 sy + 22 + bob
#             ),
#             3
#         )

#         colors = [
#             (255, 145, 190),
#             (245, 170, 220),
#             (185, 145, 255),
#             (255, 190, 120)
#         ]

#         color = colors[
#             self.flower_id % len(colors)
#         ]

#         for angle in range(0, 360, 90):

#             rad = math.radians(angle)

#             px = sx + int(
#                 math.cos(rad) * 7
#             )

#             py = sy + int(
#                 math.sin(rad) * 7 + bob
#             )

#             pygame.draw.circle(
#                 screen,
#                 color,
#                 (px, py),
#                 6
#             )

#         pygame.draw.circle(
#             screen,
#             (255, 220, 80),
#             (
#                 sx,
#                 sy + bob
#             ),
#             5
#         )


# # ================================================================
# # QUEST ITEM
# # ================================================================

# class QuestItem:
#     def __init__(
#         self,
#         x,
#         y,
#         item_type,
#         name
#     ):
#         self.x = x
#         self.y = y
#         self.item_type = item_type
#         self.name = name

#         self.collected = False

#         self.phase = random.uniform(
#             0,
#             math.pi * 2
#         )

#     def update(self, dt):
#         self.phase += dt * 0.004

#     def draw(self, screen, camera):
#         if self.collected:
#             return

#         sx, sy = camera.world_to_screen(
#             self.x,
#             self.y
#         )

#         if (
#             sx < -40
#             or sx > SCREEN_WIDTH + 40
#             or sy < -40
#             or sy > SCREEN_HEIGHT + 40
#         ):
#             return

#         bob = math.sin(self.phase) * 3

#         if self.item_type == "ribbon":

#             color = (255, 120, 170)

#             pygame.draw.line(
#                 screen,
#                 color,
#                 (
#                     sx - 8,
#                     sy - 5 + bob
#                 ),
#                 (
#                     sx + 8,
#                     sy + 5 + bob
#                 ),
#                 5
#             )

#             pygame.draw.circle(
#                 screen,
#                 color,
#                 (
#                     sx,
#                     sy + bob
#                 ),
#                 5
#             )

#         elif self.item_type == "seed":

#             color = (125, 190, 100)

#             pygame.draw.ellipse(
#                 screen,
#                 color,
#                 (
#                     sx - 8,
#                     sy - 12 + bob,
#                     16,
#                     24
#                 )
#             )

#             pygame.draw.line(
#                 screen,
#                 (80, 150, 75),
#                 (
#                     sx,
#                     sy + 4 + bob
#                 ),
#                 (
#                     sx + 8,
#                     sy - 5 + bob
#                 ),
#                 3
#             )

#         elif self.item_type == "crystal":

#             color = (150, 190, 255)

#             points = [
#                 (
#                     sx,
#                     sy - 15 + bob
#                 ),
#                 (
#                     sx + 11,
#                     sy + bob
#                 ),
#                 (
#                     sx,
#                     sy + 15 + bob
#                 ),
#                 (
#                     sx - 11,
#                     sy + bob
#                 )
#             ]

#             pygame.draw.polygon(
#                 screen,
#                 color,
#                 points
#             )

#             pygame.draw.polygon(
#                 screen,
#                 (225, 240, 255),
#                 points,
#                 2
#             )

#         elif self.item_type == "lost_star":

#             color = (255, 220, 80)

#             points = []

#             for i in range(10):

#                 angle = (
#                     -math.pi / 2
#                     + i * math.pi / 5
#                 )

#                 radius = (
#                     16
#                     if i % 2 == 0
#                     else 7
#                 )

#                 points.append(
#                     (
#                         sx
#                         + math.cos(angle)
#                         * radius,

#                         sy
#                         + bob
#                         + math.sin(angle)
#                         * radius
#                     )
#                 )

#             pygame.draw.polygon(
#                 screen,
#                 color,
#                 points
#             )


# # ================================================================
# # QUEST LOCATION
# # ================================================================

# class QuestLocation:
#     def __init__(
#         self,
#         location_id,
#         name,
#         x,
#         y,
#         radius=90
#     ):
#         self.location_id = location_id
#         self.name = name
#         self.x = x
#         self.y = y
#         self.radius = radius

#     def draw(self, screen, camera):
#         sx, sy = camera.world_to_screen(
#             self.x,
#             self.y
#         )

#         if (
#             sx < -150
#             or sx > SCREEN_WIDTH + 150
#             or sy < -150
#             or sy > SCREEN_HEIGHT + 150
#         ):
#             return

#         pygame.draw.circle(
#             screen,
#             (255, 230, 150),
#             (sx, sy),
#             self.radius,
#             2
#         )

#         pygame.draw.circle(
#             screen,
#             (255, 240, 180),
#             (sx, sy),
#             8
#         )


# # ================================================================
# # QUEST
# # ================================================================

# class Quest:
#     def __init__(
#         self,
#         quest_id,
#         title,
#         description,
#         objective_type,
#         required_amount,
#         reward_coins,
#         giver_name,
#         chain_id,
#         chain_order,
#         prerequisite=None,
#         target_ids=None,
#         item_type=None,
#         target_npc=None
#     ):
#         self.quest_id = quest_id
#         self.title = title
#         self.description = description

#         self.objective_type = objective_type
#         self.required_amount = required_amount

#         self.reward_coins = reward_coins
#         self.giver_name = giver_name

#         self.chain_id = chain_id
#         self.chain_order = chain_order

#         self.prerequisite = prerequisite

#         self.target_ids = target_ids or []
#         self.item_type = item_type
#         self.target_npc = target_npc

#         self.progress = 0

#         self.accepted = False
#         self.completed = False
#         self.reward_claimed = False

#         self.visited_targets = set()

#     def is_finished(self):
#         return self.progress >= self.required_amount

#     def add_progress(self, amount=1):
#         if not self.accepted:
#             return

#         if self.completed:
#             return

#         self.progress += amount

#         self.progress = min(
#             self.progress,
#             self.required_amount
#         )


# # ================================================================
# # FAIRY
# # ================================================================

# class Fairy:
#     def __init__(
#         self,
#         name,
#         image_filename,
#         x,
#         y
#     ):
#         self.name = name

#         self.x = float(x)
#         self.y = float(y)

#         self.image = load_image(
#             image_filename,
#             (64, 78)
#         )

#         self.rect = pygame.Rect(
#             int(x),
#             int(y),
#             44,
#             60
#         )

#     def sync_rect(self):
#         self.rect.topleft = (
#             int(self.x),
#             int(self.y)
#         )

#     def draw(self, screen, camera):
#         sx, sy = camera.world_to_screen(
#             self.x,
#             self.y
#         )

#         if self.image:

#             image_rect = self.image.get_rect(
#                 center=(
#                     sx + self.rect.width // 2,
#                     sy + self.rect.height // 2
#                 )
#             )

#             screen.blit(
#                 self.image,
#                 image_rect
#             )

#         else:

#             pygame.draw.circle(
#                 screen,
#                 (255, 220, 200),
#                 (
#                     sx + 22,
#                     sy + 17
#                 ),
#                 12
#             )

#             pygame.draw.circle(
#                 screen,
#                 (90, 180, 240),
#                 (
#                     sx + 11,
#                     sy + 27
#                 ),
#                 11
#             )

#             pygame.draw.circle(
#                 screen,
#                 (90, 180, 240),
#                 (
#                     sx + 33,
#                     sy + 27
#                 ),
#                 11
#             )

#             pygame.draw.ellipse(
#                 screen,
#                 (255, 180, 210),
#                 (
#                     sx + 10,
#                     sy + 28,
#                     25,
#                     30
#                 )
#             )


# # ================================================================
# # PARTY FAIRY
# # ================================================================

# class PartyFairy(Fairy):
#     def __init__(
#         self,
#         name,
#         image_filename,
#         x,
#         y
#     ):
#         super().__init__(
#             name,
#             image_filename,
#             x,
#             y
#         )

#         self.speed = COMPANION_SPEED


# # ================================================================
# # FAIRY NPC
# # ================================================================

# class FairyNPC(Fairy):
#     def __init__(
#         self,
#         name,
#         image_filename,
#         x,
#         y,
#         dialogue,
#         wander_radius=200
#     ):
#         super().__init__(
#             name,
#             image_filename,
#             x,
#             y
#         )

#         self.spawn_x = float(x)
#         self.spawn_y = float(y)

#         self.dialogue = dialogue
#         self.dialogue_index = 0

#         self.is_talking = False

#         self.wander_radius = max(700, wander_radius)
#         self.wander_min_distance = 180.0

#         self.target_x = self.x
#         self.target_y = self.y

#         self.speed = random.uniform(
#             NPC_MIN_SPEED,
#             NPC_MAX_SPEED
#         )

#         self.wait_timer = random.uniform(
#             0,
#             2
#         )

#         self.quest_ids = []

#         self.choose_new_destination()

#     def choose_new_destination(self):
#         angle = random.uniform(
#             0,
#             math.pi * 2
#         )

#         radius = random.uniform(
#             50,
#             self.wander_radius
#         )

#         self.target_x = clamp(
#             self.spawn_x
#             + math.cos(angle) * radius,
#             50,
#             WORLD_WIDTH - 100
#         )

#         self.target_y = clamp(
#             self.spawn_y
#             + math.sin(angle) * radius,
#             50,
#             WORLD_HEIGHT - 100
#         )

#     def can_move_to(
#         self,
#         new_x,
#         new_y,
#         obstacles
#     ):
#         test_rect = pygame.Rect(
#             int(new_x),
#             int(new_y),
#             self.rect.width,
#             self.rect.height
#         )

#         for obstacle in obstacles:

#             if test_rect.colliderect(
#                 obstacle.rect.inflate(8, 8)
#             ):
#                 return False

#         return True

#     def update(
#         self,
#         dt,
#         obstacles
#     ):
#         if self.is_talking:
#             return

#         self.wait_timer -= dt / 1000.0

#         if self.wait_timer > 0:
#             return

#         dx = self.target_x - self.x
#         dy = self.target_y - self.y

#         dist = math.hypot(
#             dx,
#             dy
#         )

#         if dist < 10:

#             self.wait_timer = random.uniform(
#                 1,
#                 3
#             )

#             self.choose_new_destination()

#             return

#         dx /= dist
#         dy /= dist

#         step = (
#             self.speed
#             * dt
#             / 16.67
#         )

#         new_x = self.x + dx * step
#         new_y = self.y + dy * step

#         if self.can_move_to(
#             new_x,
#             self.y,
#             obstacles
#         ):
#             self.x = new_x
#         else:
#             self.choose_new_destination()

#         if self.can_move_to(
#             self.x,
#             new_y,
#             obstacles
#         ):
#             self.y = new_y

#         self.sync_rect()

#     def draw(
#         self,
#         screen,
#         camera,
#         game
#     ):
#         super().draw(
#             screen,
#             camera
#         )

#         sx, sy = camera.world_to_screen(
#             self.x,
#             self.y
#         )

#         name_surface = game.small_font.render(
#             self.name,
#             True,
#             (255, 255, 255)
#         )

#         name_rect = name_surface.get_rect(
#             center=(
#                 sx + self.rect.width // 2,
#                 sy - 14
#             )
#         )

#         bg = name_rect.inflate(
#             10,
#             5
#         )

#         pygame.draw.rect(
#             screen,
#             (70, 55, 90),
#             bg,
#             border_radius=8
#         )

#         screen.blit(
#             name_surface,
#             name_rect
#         )

#         marker = game.get_npc_marker(self)

#         if marker:

#             marker_surface = game.title_font.render(
#                 marker,
#                 True,
#                 (255, 230, 100)
#             )

#             marker_rect = marker_surface.get_rect(
#                 center=(
#                     sx + self.rect.width // 2,
#                     sy - 48
#                 )
#             )

#             screen.blit(
#                 marker_surface,
#                 marker_rect
#             )


# # ================================================================
# # GAME
# # ================================================================

# class Game:
#     def __init__(self, screen):
#         self.screen = screen
#         self.running = True

#         self.state = "character_select"

#         self.player = None
#         self.companion = None

#         self.camera = Camera()

#         self.obstacles = []
#         self.flowers = []
#         self.quest_items = []
#         self.quest_locations = []
#         self.npcs = []
#         self.quests = []

#         self.coins = 0

#         self.selected_character = None

#         # --------------------------------------------------------
#         # Dialogue
#         # --------------------------------------------------------

#         self.dialogue_npc = None
#         self.dialogue_lines = []
#         self.dialogue_index = 0

#         # --------------------------------------------------------
#         # Quest offer
#         # --------------------------------------------------------

#         self.pending_quest = None
#         self.quest_offer_ready = False

#         # --------------------------------------------------------
#         # Quest tabs
#         #
#         # 0 = ACTIVE
#         # 1 = AVAILABLE
#         # 2 = COMPLETED
#         # 3 = LOCKED
#         # --------------------------------------------------------

#         self.quest_tab = 0

#         self.quest_tab_names = [
#             "ACTIVE",
#             "AVAILABLE",
#             "COMPLETED",
#             "LOCKED"
#         ]

#         self.quest_scroll = [
#             0,
#             0,
#             0,
#             0
#         ]

#         self.quest_content_height = [
#             0,
#             0,
#             0,
#             0
#         ]

#         # --------------------------------------------------------
#         # Notification
#         # --------------------------------------------------------

#         self.notification_text = ""
#         self.notification_timer = 0

#         # --------------------------------------------------------
#         # Fonts
#         # --------------------------------------------------------

#         self.title_font = pygame.font.SysFont(
#             "arial",
#             30,
#             bold=True
#         )

#         self.large_font = pygame.font.SysFont(
#             "arial",
#             24,
#             bold=True
#         )

#         self.font = pygame.font.SysFont(
#             "arial",
#             20
#         )

#         self.small_font = pygame.font.SysFont(
#             "arial",
#             16
#         )

#         self.tiny_font = pygame.font.SysFont(
#             "arial",
#             14
#         )

#         self.generate_world()
#         self.create_quests()

#     # ============================================================
#     # WORLD
#     # ============================================================

#     def generate_world(self):
#         random.seed(42)

#         # Trees.
#         for _ in range(100):

#             x = random.randint(
#                 100,
#                 WORLD_WIDTH - 150
#             )

#             y = random.randint(
#                 100,
#                 WORLD_HEIGHT - 150
#             )

#             self.obstacles.append(
#                 Obstacle(
#                     x,
#                     y,
#                     70,
#                     90,
#                     "tree"
#                 )
#             )

#         # Rocks.
#         for _ in range(35):

#             x = random.randint(
#                 100,
#                 WORLD_WIDTH - 150
#             )

#             y = random.randint(
#                 100,
#                 WORLD_HEIGHT - 120
#             )

#             self.obstacles.append(
#                 Obstacle(
#                     x,
#                     y,
#                     70,
#                     45,
#                     "rock"
#                 )
#             )

#         # Houses.
#         houses = [
#             (500, 500),
#             (1800, 700),
#             (2900, 500),
#             (900, 2200),
#             (3000, 2200)
#         ]

#         for x, y in houses:

#             self.obstacles.append(
#                 Obstacle(
#                     x,
#                     y,
#                     170,
#                     130,
#                     "house"
#                 )
#             )

#         # Fences.
#         fences = [
#             (350, 850, 300, 20),
#             (2100, 1200, 350, 20),
#             (1200, 1900, 300, 20),
#             (2800, 1700, 300, 20)
#         ]

#         for x, y, w, h in fences:

#             self.obstacles.append(
#                 Obstacle(
#                     x,
#                     y,
#                     w,
#                     h,
#                     "fence"
#                 )
#             )

#         # Flowers.
#         for i in range(180):

#             for _attempt in range(50):

#                 x = random.randint(
#                     80,
#                     WORLD_WIDTH - 80
#                 )

#                 y = random.randint(
#                     80,
#                     WORLD_HEIGHT - 80
#                 )

#                 rect = pygame.Rect(
#                     x - 8,
#                     y - 8,
#                     16,
#                     16
#                 )

#                 blocked = any(
#                     rect.colliderect(
#                         obstacle.rect.inflate(
#                             30,
#                             30
#                         )
#                     )
#                     for obstacle in self.obstacles
#                 )

#                 if not blocked:

#                     self.flowers.append(
#                         Flower(
#                             x,
#                             y,
#                             i
#                         )
#                     )

#                     break

#         # Quest locations.
#         self.quest_locations = [

#             QuestLocation(
#                 "flower_meadow",
#                 "Flower Meadow",
#                 1250,
#                 650,
#                 100
#             ),

#             QuestLocation(
#                 "ancient_grove",
#                 "Ancient Grove",
#                 1900,
#                 500,
#                 100
#             ),

#             QuestLocation(
#                 "fairy_lake",
#                 "Fairy Lake",
#                 3200,
#                 900,
#                 110
#             ),

#             QuestLocation(
#                 "crystal_cave",
#                 "Crystal Cave",
#                 3350,
#                 1900,
#                 110
#             ),

#             QuestLocation(
#                 "star_shrine",
#                 "Star Shrine",
#                 2200,
#                 2500,
#                 100
#             ),

#             QuestLocation(
#                 "garden",
#                 "Fairy Garden",
#                 900,
#                 2500,
#                 100
#             ),

#             QuestLocation(
#                 "forest_pond",
#                 "Forest Pond",
#                 2600,
#                 2700,
#                 100
#             )
#         ]

#         # Quest items.
#         self.quest_items = [

#             QuestItem(
#                 700,
#                 1300,
#                 "ribbon",
#                 "Pink Ribbon"
#             ),

#             QuestItem(
#                 950,
#                 1450,
#                 "ribbon",
#                 "Pink Ribbon"
#             ),

#             QuestItem(
#                 1200,
#                 1250,
#                 "ribbon",
#                 "Pink Ribbon"
#             ),

#             QuestItem(
#                 1500,
#                 2100,
#                 "seed",
#                 "Magical Seed"
#             ),

#             QuestItem(
#                 1700,
#                 2250,
#                 "seed",
#                 "Magical Seed"
#             ),

#             QuestItem(
#                 1900,
#                 2050,
#                 "seed",
#                 "Magical Seed"
#             ),

#             QuestItem(
#                 2050,
#                 2350,
#                 "seed",
#                 "Magical Seed"
#             ),

#             QuestItem(
#                 3300,
#                 1850,
#                 "crystal",
#                 "Fairy Crystal"
#             ),

#             QuestItem(
#                 3500,
#                 2050,
#                 "crystal",
#                 "Fairy Crystal"
#             ),

#             QuestItem(
#                 3200,
#                 2150,
#                 "crystal",
#                 "Fairy Crystal"
#             ),

#             QuestItem(
#                 3000,
#                 1950,
#                 "crystal",
#                 "Fairy Crystal"
#             ),

#             QuestItem(
#                 2200,
#                 2500,
#                 "lost_star",
#                 "Lost Star"
#             )
#         ]

#         # NPCs.
#         self.npcs = [

#             FairyNPC(
#                 "Lumi",
#                 "lumi.png",
#                 2300,
#                 1300,
#                 [
#                     "Hi there! I'm Lumi!",
#                     "I've been exploring this magical forest all morning.",
#                     "There are so many mysterious places around here.",
#                     "I could really use your help!"
#                 ],
#                 300
#             ),

#             FairyNPC(
#                 "Pipi",
#                 "mepple.png",
#                 800,
#                 800,
#                 [
#                     "Hello!",
#                     "I was carrying something very important earlier.",
#                     "But now I can't remember where I dropped it.",
#                     "Could you help me look around?"
#                 ],
#                 220
#             ),

#             FairyNPC(
#                 "Coco",
#                 "mipple.png",
#                 1500,
#                 1700,
#                 [
#                     "Welcome to the magical forest!",
#                     "I love growing magical plants.",
#                     "But my supply of magical seeds is running low."
#                 ],
#                 250
#             ),

#             FairyNPC(
#                 "Ruru",
#                 "lumi.png",
#                 3100,
#                 1100,
#                 [
#                     "Hi!",
#                     "There are mysterious crystals hidden in the forest.",
#                     "I wonder what secrets they contain..."
#                 ],
#                 260
#             ),

#             FairyNPC(
#                 "Nana",
#                 "lumi.png",
#                 1000,
#                 2500,
#                 [
#                     "Good morning!",
#                     "Have you explored the eastern forest yet?",
#                     "There is a peaceful pond hidden among the trees."
#                 ],
#                 240
#             )
#         ]

#     # ============================================================
#     # QUEST CREATION
#     # ============================================================

#     def create_quests(self):

#         self.quests = [

#             # ----------------------------------------------------
#             # LUMI CHAIN
#             # ----------------------------------------------------

#             Quest(
#                 "lumi_001",
#                 "Magical Flower Gathering",
#                 "Collect 5 magical flowers for Lumi.",
#                 "flower",
#                 5,
#                 50,
#                 "Lumi",
#                 "lumi_chain",
#                 1
#             ),

#             Quest(
#                 "lumi_002",
#                 "Explore the Fairy Forest",
#                 "Visit the Flower Meadow, Ancient Grove and Fairy Lake.",
#                 "location",
#                 3,
#                 75,
#                 "Lumi",
#                 "lumi_chain",
#                 2,
#                 prerequisite="lumi_001",
#                 target_ids=[
#                     "flower_meadow",
#                     "ancient_grove",
#                     "fairy_lake"
#                 ]
#             ),

#             Quest(
#                 "lumi_003",
#                 "Find the Lost Star",
#                 "Find the mysterious Lost Star.",
#                 "item",
#                 1,
#                 100,
#                 "Lumi",
#                 "lumi_chain",
#                 3,
#                 prerequisite="lumi_002",
#                 item_type="lost_star"
#             ),

#             # ----------------------------------------------------
#             # PIPI CHAIN
#             # ----------------------------------------------------

#             Quest(
#                 "pipi_001",
#                 "Find My Missing Ribbons",
#                 "Find 3 ribbons that Pipi lost around the forest.",
#                 "item",
#                 3,
#                 40,
#                 "Pipi",
#                 "pipi_chain",
#                 1,
#                 item_type="ribbon"
#             ),

#             Quest(
#                 "pipi_002",
#                 "A Ribbon for the Fairy Festival",
#                 "Tell Coco about Pipi's ribbon.",
#                 "talk",
#                 1,
#                 60,
#                 "Pipi",
#                 "pipi_chain",
#                 2,
#                 prerequisite="pipi_001",
#                 target_npc="Coco"
#             ),

#             # ----------------------------------------------------
#             # COCO CHAIN
#             # ----------------------------------------------------

#             Quest(
#                 "coco_001",
#                 "Gather Magical Seeds",
#                 "Collect 4 magical seeds.",
#                 "item",
#                 4,
#                 50,
#                 "Coco",
#                 "coco_chain",
#                 1,
#                 item_type="seed"
#             ),

#             Quest(
#                 "coco_002",
#                 "Restore the Fairy Garden",
#                 "Visit three important places to restore the fairy garden.",
#                 "location",
#                 3,
#                 80,
#                 "Coco",
#                 "coco_chain",
#                 2,
#                 prerequisite="coco_001",
#                 target_ids=[
#                     "garden",
#                     "fairy_lake",
#                     "ancient_grove"
#                 ]
#             ),

#             # ----------------------------------------------------
#             # RURU CHAIN
#             # ----------------------------------------------------

#             Quest(
#                 "ruru_001",
#                 "Crystal Hunt",
#                 "Collect 4 mysterious fairy crystals.",
#                 "item",
#                 4,
#                 70,
#                 "Ruru",
#                 "ruru_chain",
#                 1,
#                 item_type="crystal"
#             ),

#             Quest(
#                 "ruru_002",
#                 "The Crystal Mystery",
#                 "Investigate the Crystal Cave.",
#                 "location",
#                 1,
#                 100,
#                 "Ruru",
#                 "ruru_chain",
#                 2,
#                 prerequisite="ruru_001",
#                 target_ids=[
#                     "crystal_cave"
#                 ]
#             ),

#             # ----------------------------------------------------
#             # NANA CHAIN
#             # ----------------------------------------------------

#             Quest(
#                 "nana_001",
#                 "Visit the Forest Pond",
#                 "Find the peaceful Forest Pond.",
#                 "location",
#                 1,
#                 45,
#                 "Nana",
#                 "nana_chain",
#                 1,
#                 target_ids=[
#                     "forest_pond"
#                 ]
#             ),

#             Quest(
#                 "nana_002",
#                 "Tell Pipi About the Pond",
#                 "Tell Pipi what you discovered at the pond.",
#                 "talk",
#                 1,
#                 65,
#                 "Nana",
#                 "nana_chain",
#                 2,
#                 prerequisite="nana_001",
#                 target_npc="Pipi"
#             )
#         ]

#         for npc in self.npcs:

#             npc.quest_ids = [
#                 quest.quest_id
#                 for quest in self.quests
#                 if quest.giver_name == npc.name
#             ]

#     # ============================================================
#     # QUEST STATUS
#     # ============================================================

#     def get_quest_by_id(self, quest_id):

#         for quest in self.quests:

#             if quest.quest_id == quest_id:
#                 return quest

#         return None

#     def is_quest_unlocked(self, quest):

#         if quest.prerequisite is None:
#             return True

#         prerequisite = self.get_quest_by_id(
#             quest.prerequisite
#         )

#         if prerequisite is None:
#             return False

#         return prerequisite.completed

#     def get_quest_status(self, quest):

#         if quest.completed:
#             return "COMPLETED"

#         if quest.accepted:
#             return "ACTIVE"

#         if not self.is_quest_unlocked(quest):
#             return "LOCKED"

#         return "AVAILABLE"

#     def get_active_quests(self):

#         return [
#             quest
#             for quest in self.quests
#             if self.get_quest_status(quest)
#             == "ACTIVE"
#         ]

#     def get_available_quests(self):

#         return [
#             quest
#             for quest in self.quests
#             if self.get_quest_status(quest)
#             == "AVAILABLE"
#         ]

#     def get_completed_quests(self):

#         return [
#             quest
#             for quest in self.quests
#             if self.get_quest_status(quest)
#             == "COMPLETED"
#         ]

#     def get_locked_quests(self):

#         return [
#             quest
#             for quest in self.quests
#             if self.get_quest_status(quest)
#             == "LOCKED"
#         ]

#     # ============================================================
#     # NPC QUEST
#     # ============================================================

#     def get_npc_quest(self, npc):

#         npc_quests = [
#             quest
#             for quest in self.quests
#             if quest.giver_name == npc.name
#         ]

#         # Active quest first.
#         for quest in npc_quests:

#             if self.get_quest_status(quest) == "ACTIVE":
#                 return quest

#         # Then available quest.
#         for quest in npc_quests:

#             if self.get_quest_status(quest) == "AVAILABLE":
#                 return quest

#         return None

#     def get_npc_marker(self, npc):

#         quest = self.get_npc_quest(npc)

#         if quest is None:
#             return ""

#         status = self.get_quest_status(
#             quest
#         )

#         if status == "AVAILABLE":
#             return "!"

#         if status == "ACTIVE":

#             if quest.is_finished():
#                 return "?"

#             return "..."

#         return ""

#     # ============================================================
#     # CHARACTER SELECT
#     # ============================================================

#     def find_safe_spawn(self):

#         candidates = [
#             (700, 1000),
#             (750, 1100),
#             (650, 1050),
#             (800, 1050),
#             (600, 1000)
#         ]

#         for x, y in candidates:

#             rect = pygame.Rect(
#                 x,
#                 y,
#                 44,
#                 60
#             )

#             blocked = any(
#                 rect.colliderect(
#                     obstacle.rect.inflate(
#                         20,
#                         20
#                     )
#                 )
#                 for obstacle in self.obstacles
#             )

#             if not blocked:
#                 return x, y

#         return 700, 1000

#     def start_adventure(self, character):

#         self.selected_character = character

#         x, y = self.find_safe_spawn()

#         if character == "Mepple":

#             self.player = Fairy(
#                 "Mepple",
#                 "mepple.png",
#                 x,
#                 y
#             )

#             self.companion = PartyFairy(
#                 "Mipple",
#                 "mipple.png",
#                 x - 80,
#                 y
#             )

#         else:

#             self.player = Fairy(
#                 "Mipple",
#                 "mipple.png",
#                 x,
#                 y
#             )

#             self.companion = PartyFairy(
#                 "Mepple",
#                 "mepple.png",
#                 x - 80,
#                 y
#             )

#         self.camera.update(
#             self.player.rect
#         )

#         self.state = "playing"

#         self.show_notification(
#             f"{character} joined the adventure!"
#         )

#     # ============================================================
#     # EVENT HANDLING
#     # ============================================================

#     def handle_event(self, event):

#         global SCREEN_WIDTH, SCREEN_HEIGHT

#         if event.type == pygame.QUIT:

#             self.running = False
#             return

#         if event.type == pygame.VIDEORESIZE:

#             SCREEN_WIDTH = max(
#                 800,
#                 event.w
#             )

#             SCREEN_HEIGHT = max(
#                 600,
#                 event.h
#             )

#             self.screen = pygame.display.set_mode(
#                 (
#                     SCREEN_WIDTH,
#                     SCREEN_HEIGHT
#                 ),
#                 pygame.RESIZABLE
#             )

#             return

#         # ========================================================
#         # CHARACTER SELECT
#         # ========================================================

#         if self.state == "character_select":

#             if event.type == pygame.KEYDOWN:

#                 if event.key == pygame.K_1:
#                     self.start_adventure(
#                         "Mepple"
#                     )

#                 elif event.key == pygame.K_2:
#                     self.start_adventure(
#                         "Mipple"
#                     )

#             elif event.type == pygame.MOUSEBUTTONDOWN:

#                 if event.button == 1:

#                     mepple_rect = pygame.Rect(
#                         SCREEN_WIDTH // 2 - 300,
#                         260,
#                         240,
#                         280
#                     )

#                     mipple_rect = pygame.Rect(
#                         SCREEN_WIDTH // 2 + 60,
#                         260,
#                         240,
#                         280
#                     )

#                     if mepple_rect.collidepoint(
#                         event.pos
#                     ):
#                         self.start_adventure(
#                             "Mepple"
#                         )

#                     elif mipple_rect.collidepoint(
#                         event.pos
#                     ):
#                         self.start_adventure(
#                             "Mipple"
#                         )

#             return

#         # ========================================================
#         # QUEST LOG
#         # ========================================================

#         if self.state == "quest_log":

#             if event.type == pygame.KEYDOWN:

#                 # Close.
#                 if event.key in (
#                     pygame.K_q,
#                     pygame.K_ESCAPE
#                 ):
#                     self.state = "playing"
#                     return

#                 # Change tab.
#                 elif event.key == pygame.K_LEFT:

#                     self.change_quest_tab(-1)

#                 elif event.key == pygame.K_RIGHT:

#                     self.change_quest_tab(1)

#                 # Scroll current tab.
#                 elif event.key == pygame.K_UP:

#                     self.scroll_current_quest_tab(
#                         -70
#                     )

#                 elif event.key == pygame.K_DOWN:

#                     self.scroll_current_quest_tab(
#                         70
#                     )

#                 elif event.key == pygame.K_PAGEUP:

#                     self.scroll_current_quest_tab(
#                         -350
#                     )

#                 elif event.key == pygame.K_PAGEDOWN:

#                     self.scroll_current_quest_tab(
#                         350
#                     )

#                 elif event.key == pygame.K_HOME:

#                     self.quest_scroll[
#                         self.quest_tab
#                     ] = 0

#                 elif event.key == pygame.K_END:

#                     self.quest_scroll[
#                         self.quest_tab
#                     ] = 999999

#             elif event.type == pygame.MOUSEWHEEL:

#                 self.scroll_current_quest_tab(
#                     -event.y * 60
#                 )

#             elif event.type == pygame.MOUSEBUTTONDOWN:

#                 # Mouse wheel fallback.
#                 if event.button == 4:

#                     self.scroll_current_quest_tab(
#                         -60
#                     )

#                 elif event.button == 5:

#                     self.scroll_current_quest_tab(
#                         60
#                     )

#                 # Click tabs.
#                 elif event.button == 1:

#                     tab = self.get_clicked_quest_tab(
#                         event.pos
#                     )

#                     if tab is not None:
#                         self.quest_tab = tab

#             return

#         # ========================================================
#         # DIALOGUE
#         # ========================================================

#         if self.dialogue_npc is not None:

#             if event.type == pygame.KEYDOWN:

#                 if event.key == pygame.K_ESCAPE:

#                     if self.quest_offer_ready:

#                         self.pending_quest = None
#                         self.quest_offer_ready = False

#                     self.close_dialogue()

#                     return

#                 if event.key == pygame.K_e:

#                     if self.quest_offer_ready:

#                         self.accept_pending_quest()

#                     else:

#                         self.advance_dialogue()

#                     return

#             return

#         # ========================================================
#         # PLAYING
#         # ========================================================

#         if self.state == "playing":

#             if event.type == pygame.KEYDOWN:

#                 if event.key == pygame.K_ESCAPE:

#                     self.state = "pause"

#                 elif event.key == pygame.K_q:

#                     self.open_quest_log()

#                 elif event.key == pygame.K_e:

#                     self.interact()

#         # ========================================================
#         # PAUSE
#         # ========================================================

#         elif self.state == "pause":

#             if event.type == pygame.KEYDOWN:

#                 if event.key == pygame.K_ESCAPE:

#                     self.state = "playing"

#                 elif event.key == pygame.K_q:

#                     self.open_quest_log()

#     # ============================================================
#     # QUEST TAB
#     # ============================================================

#     def get_current_quest_list(self):

#         if self.quest_tab == 0:
#             return self.get_active_quests()

#         if self.quest_tab == 1:
#             return self.get_available_quests()

#         if self.quest_tab == 2:
#             return self.get_completed_quests()

#         return self.get_locked_quests()

#     def change_quest_tab(self, direction):

#         self.quest_tab += direction

#         self.quest_tab = int(
#             clamp(
#                 self.quest_tab,
#                 0,
#                 len(self.quest_tab_names) - 1
#             )
#         )

#         self.quest_scroll[
#             self.quest_tab
#         ] = int(
#             clamp(
#                 self.quest_scroll[
#                     self.quest_tab
#                 ],
#                 0,
#                 999999
#             )
#         )

#     def get_quest_log_view_rect(self):

#         header_height = 160
#         footer_height = 55

#         return pygame.Rect(
#             25,
#             header_height,
#             SCREEN_WIDTH - 65,
#             SCREEN_HEIGHT
#             - header_height
#             - footer_height
#         )

#     def get_clicked_quest_tab(self, pos):

#         tab_y = 105
#         tab_height = 50

#         left = 25
#         total_width = SCREEN_WIDTH - 65

#         tab_width = total_width // 4

#         if not (
#             tab_y
#             <= pos[1]
#             <= tab_y + tab_height
#         ):
#             return None

#         if not (
#             left
#             <= pos[0]
#             <= left + total_width
#         ):
#             return None

#         index = (
#             pos[0] - left
#         ) // tab_width

#         return int(
#             clamp(
#                 index,
#                 0,
#                 3
#             )
#         )

#     def get_current_quest_view_height(self):

#         return self.get_quest_log_view_rect().height

#     def scroll_current_quest_tab(self, amount):

#         tab = self.quest_tab

#         self.quest_scroll[tab] += amount

#         max_scroll = max(
#             0,
#             self.quest_content_height[tab]
#             - self.get_current_quest_view_height()
#         )

#         self.quest_scroll[tab] = int(
#             clamp(
#                 self.quest_scroll[tab],
#                 0,
#                 max_scroll
#             )
#         )

#     def open_quest_log(self):

#         self.state = "quest_log"

#         self.quest_scroll[
#             self.quest_tab
#         ] = int(
#             clamp(
#                 self.quest_scroll[
#                     self.quest_tab
#                 ],
#                 0,
#                 999999
#             )
#         )

#     # ============================================================
#     # PLAYER MOVEMENT
#     # ============================================================

#     def move_player(self, dx, dy):

#         if not self.player:
#             return

#         length = math.hypot(
#             dx,
#             dy
#         )

#         if length > 0:

#             dx /= length
#             dy /= length

#         speed = PLAYER_SPEED

#         # Horizontal.
#         new_x = (
#             self.player.x
#             + dx * speed
#         )

#         test_rect = pygame.Rect(
#             int(new_x),
#             int(self.player.y),
#             self.player.rect.width,
#             self.player.rect.height
#         )

#         blocked = any(
#             test_rect.colliderect(
#                 obstacle.rect
#             )
#             for obstacle in self.obstacles
#         )

#         if not blocked:

#             self.player.x = clamp(
#                 new_x,
#                 0,
#                 WORLD_WIDTH
#                 - self.player.rect.width
#             )

#         # Vertical.
#         new_y = (
#             self.player.y
#             + dy * speed
#         )

#         test_rect = pygame.Rect(
#             int(self.player.x),
#             int(new_y),
#             self.player.rect.width,
#             self.player.rect.height
#         )

#         blocked = any(
#             test_rect.colliderect(
#                 obstacle.rect
#             )
#             for obstacle in self.obstacles
#         )

#         if not blocked:

#             self.player.y = clamp(
#                 new_y,
#                 0,
#                 WORLD_HEIGHT
#                 - self.player.rect.height
#             )

#         self.player.sync_rect()

#     # ============================================================
#     # COMPANION
#     # ============================================================

#     def update_companion(self, dt):

#         if not self.player or not self.companion:
#             return

#         dx = (
#             self.player.x
#             - self.companion.x
#         )

#         dy = (
#             self.player.y
#             - self.companion.y
#         )

#         dist = math.hypot(
#             dx,
#             dy
#         )

#         if dist > 100:

#             dx /= dist
#             dy /= dist

#             step = (
#                 self.companion.speed
#                 * dt
#                 / 16.67
#             )

#             self.companion.x += dx * step
#             self.companion.y += dy * step

#             self.companion.x = clamp(
#                 self.companion.x,
#                 0,
#                 WORLD_WIDTH
#                 - self.companion.rect.width
#             )

#             self.companion.y = clamp(
#                 self.companion.y,
#                 0,
#                 WORLD_HEIGHT
#                 - self.companion.rect.height
#             )

#             self.companion.sync_rect()

#     # ============================================================
#     # NPC INTERACTION
#     # ============================================================

#     def get_nearby_npc(self):

#         if not self.player:
#             return None

#         best_npc = None
#         best_distance = NPC_INTERACTION_DISTANCE

#         for npc in self.npcs:

#             d = distance(
#                 self.player.x,
#                 self.player.y,
#                 npc.x,
#                 npc.y
#             )

#             if d < best_distance:

#                 best_distance = d
#                 best_npc = npc

#         return best_npc

#     def interact(self):

#         npc = self.get_nearby_npc()

#         if npc is None:
#             return

#         self.record_talk_objectives(
#             npc.name
#         )

#         quest = self.get_npc_quest(npc)

#         if quest:

#             status = self.get_quest_status(
#                 quest
#             )

#             # Active quest.
#             if status == "ACTIVE":

#                 if quest.is_finished():

#                     self.complete_quest(
#                         quest,
#                         npc
#                     )

#                 else:

#                     self.start_progress_dialogue(
#                         npc,
#                         quest
#                     )

#                 return

#             # Available quest.
#             if status == "AVAILABLE":

#                 self.start_quest_offer(
#                     npc,
#                     quest
#                 )

#                 return

#         self.start_normal_dialogue(
#             npc
#         )

#     # ============================================================
#     # DIALOGUE
#     # ============================================================

#     def start_normal_dialogue(self, npc):

#         self.dialogue_npc = npc
#         self.pending_quest = None
#         self.quest_offer_ready = False

#         self.dialogue_lines = list(
#             npc.dialogue
#         )

#         self.dialogue_index = 0

#         npc.is_talking = True

#     def start_quest_offer(self, npc, quest):

#         self.dialogue_npc = npc
#         self.pending_quest = quest
#         self.quest_offer_ready = False

#         self.dialogue_lines = [

#             "Hi! I have a quest for you.",

#             quest.title,

#             quest.description,

#             f"Reward: {quest.reward_coins} coins.",

#             "Would you like to accept this quest?"
#         ]

#         self.dialogue_index = 0

#         npc.is_talking = True

#     def start_progress_dialogue(
#         self,
#         npc,
#         quest
#     ):

#         self.dialogue_npc = npc
#         self.pending_quest = None
#         self.quest_offer_ready = False

#         if quest.is_finished():

#             self.dialogue_lines = [
#                 "You did it!",
#                 "Your quest is ready to turn in.",
#                 (
#                     f"{quest.progress}/"
#                     f"{quest.required_amount}"
#                 )
#             ]

#         else:

#             self.dialogue_lines = [
#                 "You're doing great!",
#                 quest.title,
#                 (
#                     f"Progress: "
#                     f"{quest.progress}/"
#                     f"{quest.required_amount}"
#                 )
#             ]

#         self.dialogue_index = 0

#         npc.is_talking = True

#     def advance_dialogue(self):

#         if self.dialogue_npc is None:
#             return

#         if (
#             self.pending_quest is not None
#             and self.dialogue_index
#             >= len(self.dialogue_lines) - 1
#         ):

#             self.quest_offer_ready = True
#             return

#         self.dialogue_index += 1

#         if (
#             self.dialogue_index
#             >= len(self.dialogue_lines)
#         ):
#             self.close_dialogue()

#     def close_dialogue(self):

#         if self.dialogue_npc:

#             self.dialogue_npc.is_talking = False

#         self.dialogue_npc = None
#         self.dialogue_lines = []
#         self.dialogue_index = 0

#         self.pending_quest = None
#         self.quest_offer_ready = False

#     # ============================================================
#     # ACCEPT QUEST
#     # ============================================================

#     def accept_pending_quest(self):

#         if self.pending_quest is None:
#             return

#         quest = self.pending_quest

#         if self.get_quest_status(
#             quest
#         ) != "AVAILABLE":

#             self.close_dialogue()
#             return

#         quest.accepted = True
#         quest.completed = False

#         self.show_notification(
#             f"Quest accepted: {quest.title}"
#         )

#         self.dialogue_lines = [
#             "Thank you!",
#             f"Quest accepted: {quest.title}",
#             "Good luck on your adventure!"
#         ]

#         self.dialogue_index = 0

#         self.pending_quest = None
#         self.quest_offer_ready = False

#     # ============================================================
#     # COMPLETE QUEST
#     # ============================================================

#     def complete_quest(
#         self,
#         quest,
#         npc
#     ):

#         if quest.completed:
#             return

#         quest.completed = True
#         quest.accepted = False

#         if not quest.reward_claimed:

#             self.coins += quest.reward_coins

#             quest.reward_claimed = True

#         self.show_notification(
#             f"Quest completed! "
#             f"+{quest.reward_coins} coins"
#         )

#         next_quests = [
#             q
#             for q in self.quests
#             if q.prerequisite
#             == quest.quest_id
#         ]

#         self.dialogue_npc = npc
#         npc.is_talking = True

#         self.pending_quest = None
#         self.quest_offer_ready = False

#         self.dialogue_lines = [
#             "You did it!",
#             quest.title,
#             (
#                 f"You received "
#                 f"{quest.reward_coins} coins!"
#             )
#         ]

#         if next_quests:

#             self.dialogue_lines.append(
#                 (
#                     "New quest unlocked: "
#                     f"{next_quests[0].title}"
#                 )
#             )

#         self.dialogue_index = 0

#     # ============================================================
#     # TALK OBJECTIVES
#     # ============================================================

#     def record_talk_objectives(
#         self,
#         npc_name
#     ):

#         for quest in self.get_active_quests():

#             if quest.objective_type != "talk":
#                 continue

#             if quest.target_npc != npc_name:
#                 continue

#             if quest.is_finished():
#                 continue

#             quest.add_progress(1)

#             self.show_notification(
#                 (
#                     f"{quest.title}: "
#                     f"{quest.progress}/"
#                     f"{quest.required_amount}"
#                 )
#             )

#     # ============================================================
#     # FLOWER COLLECTION
#     # ============================================================

#     def check_flower_collection(self):

#         if not self.player:
#             return

#         active_flower_quests = [
#             quest
#             for quest in self.get_active_quests()
#             if quest.objective_type == "flower"
#         ]

#         if not active_flower_quests:
#             return

#         for flower in self.flowers:

#             if flower.collected:
#                 continue

#             d = distance(
#                 self.player.x,
#                 self.player.y,
#                 flower.x,
#                 flower.y
#             )

#             if d <= 28:

#                 flower.collected = True

#                 for quest in active_flower_quests:

#                     if not quest.is_finished():
#                         quest.add_progress(1)

#                 self.show_notification(
#                     "Magical flower collected!"
#                 )

#                 break

#     # ============================================================
#     # QUEST ITEMS
#     # ============================================================

#     def check_quest_items(self):

#         if not self.player:
#             return

#         active_item_quests = [
#             quest
#             for quest in self.get_active_quests()
#             if quest.objective_type == "item"
#         ]

#         if not active_item_quests:
#             return

#         for item in self.quest_items:

#             if item.collected:
#                 continue

#             matching_quests = [
#                 quest
#                 for quest in active_item_quests
#                 if quest.item_type
#                 == item.item_type
#                 and not quest.is_finished()
#             ]

#             if not matching_quests:
#                 continue

#             d = distance(
#                 self.player.x,
#                 self.player.y,
#                 item.x,
#                 item.y
#             )

#             if d <= 35:

#                 item.collected = True

#                 for quest in matching_quests:

#                     quest.add_progress(1)

#                     self.show_notification(
#                         (
#                             f"{item.name} collected! "
#                             f"{quest.progress}/"
#                             f"{quest.required_amount}"
#                         )
#                     )

#                 break

#     # ============================================================
#     # LOCATION OBJECTIVES
#     # ============================================================

#     def check_quest_locations(self):

#         if not self.player:
#             return

#         active_location_quests = [
#             quest
#             for quest in self.get_active_quests()
#             if quest.objective_type == "location"
#         ]

#         if not active_location_quests:
#             return

#         for location in self.quest_locations:

#             d = distance(
#                 self.player.x,
#                 self.player.y,
#                 location.x,
#                 location.y
#             )

#             if d > location.radius:
#                 continue

#             for quest in active_location_quests:

#                 if location.location_id not in quest.target_ids:
#                     continue

#                 if location.location_id in quest.visited_targets:
#                     continue

#                 quest.visited_targets.add(
#                     location.location_id
#                 )

#                 quest.progress = min(
#                     len(quest.visited_targets),
#                     quest.required_amount
#                 )

#                 self.show_notification(
#                     f"Discovered: {location.name}"
#                 )

#     # ============================================================
#     # UPDATE
#     # ============================================================

#     def update(self, dt):

#         if self.state != "playing":

#             self.update_notification(dt)
#             return

#         if self.dialogue_npc is not None:

#             self.update_notification(dt)
#             return

#         keys = pygame.key.get_pressed()

#         dx = 0
#         dy = 0

#         if (
#             keys[pygame.K_a]
#             or keys[pygame.K_LEFT]
#         ):
#             dx -= 1

#         if (
#             keys[pygame.K_d]
#             or keys[pygame.K_RIGHT]
#         ):
#             dx += 1

#         if (
#             keys[pygame.K_w]
#             or keys[pygame.K_UP]
#         ):
#             dy -= 1

#         if (
#             keys[pygame.K_s]
#             or keys[pygame.K_DOWN]
#         ):
#             dy += 1

#         self.move_player(
#             dx,
#             dy
#         )

#         self.update_companion(dt)

#         for flower in self.flowers:
#             flower.update(dt)

#         for item in self.quest_items:
#             item.update(dt)

#         for npc in self.npcs:
#             npc.update(
#                 dt,
#                 self.obstacles
#             )

#         self.check_flower_collection()
#         self.check_quest_items()
#         self.check_quest_locations()

#         self.camera.update(
#             self.player.rect
#         )

#         self.update_notification(dt)

#     # ============================================================
#     # NOTIFICATION
#     # ============================================================

#     def show_notification(self, text):

#         self.notification_text = text
#         self.notification_timer = 3000

#         print(
#             f"[QUEST] {text}"
#         )

#     def update_notification(self, dt):

#         if self.notification_timer > 0:

#             self.notification_timer -= dt

#             if self.notification_timer <= 0:

#                 self.notification_timer = 0
#                 self.notification_text = ""

#     # ============================================================
#     # WORLD DRAW
#     # ============================================================

#     def draw_world(self):

#         self.screen.fill(
#             (150, 205, 135)
#         )

#         random_generator = random.Random(100)

#         for _ in range(500):

#             x = random_generator.randint(
#                 0,
#                 WORLD_WIDTH
#             )

#             y = random_generator.randint(
#                 0,
#                 WORLD_HEIGHT
#             )

#             sx, sy = self.camera.world_to_screen(
#                 x,
#                 y
#             )

#             if (
#                 -5 <= sx <= SCREEN_WIDTH + 5
#                 and -5 <= sy <= SCREEN_HEIGHT + 5
#             ):

#                 pygame.draw.line(
#                     self.screen,
#                     (125, 185, 110),
#                     (
#                         sx,
#                         sy
#                     ),
#                     (
#                         sx + 3,
#                         sy - 4
#                     ),
#                     1
#                 )

#         for location in self.quest_locations:

#             location.draw(
#                 self.screen,
#                 self.camera
#             )

#         for flower in self.flowers:

#             flower.draw(
#                 self.screen,
#                 self.camera
#             )

#         for item in self.quest_items:

#             item.draw(
#                 self.screen,
#                 self.camera
#             )

#         for obstacle in self.obstacles:

#             obstacle.draw(
#                 self.screen,
#                 self.camera
#             )

#         for npc in self.npcs:

#             npc.draw(
#                 self.screen,
#                 self.camera,
#                 self
#             )

#         if self.companion:

#             self.companion.draw(
#                 self.screen,
#                 self.camera
#             )

#         if self.player:

#             self.player.draw(
#                 self.screen,
#                 self.camera
#             )

#     # ============================================================
#     # HUD
#     # ============================================================

#     def draw_hud(self):

#         if not self.player:
#             return

#         panel = pygame.Rect(
#             15,
#             15,
#             270,
#             95
#         )

#         pygame.draw.rect(
#             self.screen,
#             (50, 40, 70),
#             panel,
#             border_radius=14
#         )

#         pygame.draw.rect(
#             self.screen,
#             (255, 255, 255),
#             panel,
#             2,
#             border_radius=14
#         )

#         name = self.large_font.render(
#             self.player.name,
#             True,
#             (255, 255, 255)
#         )

#         self.screen.blit(
#             name,
#             (
#                 30,
#                 27
#             )
#         )

#         coins = self.font.render(
#             f"★ {self.coins} coins",
#             True,
#             (255, 225, 90)
#         )

#         self.screen.blit(
#             coins,
#             (
#                 30,
#                 62
#             )
#         )

#         active_count = len(
#             self.get_active_quests()
#         )

#         quest_text = self.small_font.render(
#             f"Active quests: {active_count}",
#             True,
#             (235, 235, 255)
#         )

#         self.screen.blit(
#             quest_text,
#             (
#                 30,
#                 87
#             )
#         )

#         controls = self.small_font.render(
#             "WASD Move   E Interact   Q Quest Log   ESC Pause",
#             True,
#             (255, 255, 255)
#         )

#         controls_rect = controls.get_rect(
#             top=15,
#             right=SCREEN_WIDTH - 15
#         )

#         control_bg = controls_rect.inflate(
#             18,
#             10
#         )

#         pygame.draw.rect(
#             self.screen,
#             (55, 45, 75),
#             control_bg,
#             border_radius=10
#         )

#         self.screen.blit(
#             controls,
#             controls_rect
#         )

#         # Active quest preview.
#         active_quests = self.get_active_quests()

#         if active_quests:

#             panel_x = 15
#             panel_y = 125
#             panel_w = 340

#             preview_count = min(
#                 len(active_quests),
#                 3
#             )

#             panel_h = (
#                 45
#                 + preview_count * 48
#             )

#             quest_panel = pygame.Rect(
#                 panel_x,
#                 panel_y,
#                 panel_w,
#                 panel_h
#             )

#             pygame.draw.rect(
#                 self.screen,
#                 (55, 45, 75),
#                 quest_panel,
#                 border_radius=12
#             )

#             pygame.draw.rect(
#                 self.screen,
#                 (255, 255, 255),
#                 quest_panel,
#                 2,
#                 border_radius=12
#             )

#             title = self.font.render(
#                 "ACTIVE QUESTS",
#                 True,
#                 (255, 230, 130)
#             )

#             self.screen.blit(
#                 title,
#                 (
#                     panel_x + 15,
#                     panel_y + 10
#                 )
#             )

#             y = panel_y + 42

#             for quest in active_quests[:3]:

#                 quest_name = self.small_font.render(
#                     quest.title,
#                     True,
#                     (255, 255, 255)
#                 )

#                 self.screen.blit(
#                     quest_name,
#                     (
#                         panel_x + 15,
#                         y
#                     )
#                 )

#                 progress = self.small_font.render(
#                     (
#                         f"{quest.progress}/"
#                         f"{quest.required_amount}"
#                     ),
#                     True,
#                     (220, 220, 240)
#                 )

#                 self.screen.blit(
#                     progress,
#                     (
#                         panel_x + 250,
#                         y
#                     )
#                 )

#                 y += 48

#         npc = self.get_nearby_npc()

#         if npc:

#             prompt = self.font.render(
#                 f"E  Talk to {npc.name}",
#                 True,
#                 (255, 255, 255)
#             )

#             rect = prompt.get_rect(
#                 center=(
#                     SCREEN_WIDTH // 2,
#                     SCREEN_HEIGHT - 45
#                 )
#             )

#             bg = rect.inflate(
#                 30,
#                 15
#             )

#             pygame.draw.rect(
#                 self.screen,
#                 (65, 50, 85),
#                 bg,
#                 border_radius=12
#             )

#             pygame.draw.rect(
#                 self.screen,
#                 (255, 255, 255),
#                 bg,
#                 2,
#                 border_radius=12
#             )

#             self.screen.blit(
#                 prompt,
#                 rect
#             )

#         self.draw_notification()

#     # ============================================================
#     # NOTIFICATION DRAW
#     # ============================================================

#     def draw_notification(self):

#         if not self.notification_text:
#             return

#         surface = self.font.render(
#             self.notification_text,
#             True,
#             (255, 255, 255)
#         )

#         rect = surface.get_rect(
#             center=(
#                 SCREEN_WIDTH // 2,
#                 75
#             )
#         )

#         bg = rect.inflate(
#             40,
#             22
#         )

#         pygame.draw.rect(
#             self.screen,
#             (70, 55, 95),
#             bg,
#             border_radius=12
#         )

#         pygame.draw.rect(
#             self.screen,
#             (255, 225, 120),
#             bg,
#             2,
#             border_radius=12
#         )

#         self.screen.blit(
#             surface,
#             rect
#         )

#     # ============================================================
#     # DIALOGUE
#     # ============================================================

#     def draw_dialogue(self):

#         if self.dialogue_npc is None:
#             return

#         panel_h = 190

#         panel = pygame.Rect(
#             30,
#             SCREEN_HEIGHT - panel_h - 25,
#             SCREEN_WIDTH - 60,
#             panel_h
#         )

#         pygame.draw.rect(
#             self.screen,
#             (45, 35, 65),
#             panel,
#             border_radius=18
#         )

#         pygame.draw.rect(
#             self.screen,
#             (255, 255, 255),
#             panel,
#             3,
#             border_radius=18
#         )

#         speaker = self.title_font.render(
#             self.dialogue_npc.name,
#             True,
#             (255, 220, 130)
#         )

#         self.screen.blit(
#             speaker,
#             (
#                 panel.x + 25,
#                 panel.y + 18
#             )
#         )

#         if self.dialogue_lines:

#             line = self.dialogue_lines[
#                 min(
#                     self.dialogue_index,
#                     len(self.dialogue_lines) - 1
#                 )
#             ]

#             lines = wrap_text(
#                 line,
#                 self.font,
#                 panel.width - 50
#             )

#             y = panel.y + 65

#             for text_line in lines[:3]:

#                 surface = self.font.render(
#                     text_line,
#                     True,
#                     (255, 255, 255)
#                 )

#                 self.screen.blit(
#                     surface,
#                     (
#                         panel.x + 25,
#                         y
#                     )
#                 )

#                 y += 28

#         if self.quest_offer_ready:

#             prompt_text = (
#                 "E  Accept Quest     "
#                 "ESC  Decline"
#             )

#         else:

#             prompt_text = "E  Continue"

#         prompt = self.small_font.render(
#             prompt_text,
#             True,
#             (230, 220, 255)
#         )

#         prompt_rect = prompt.get_rect(
#             right=panel.right - 25,
#             bottom=panel.bottom - 20
#         )

#         self.screen.blit(
#             prompt,
#             prompt_rect
#         )

#     # ============================================================
#     # QUEST ENTRY
#     # ============================================================

#     def draw_quest_entry(
#         self,
#         quest,
#         x,
#         y,
#         width,
#         status
#     ):

#         if status == "ACTIVE":

#             bg = (65, 55, 90)
#             border = (160, 140, 255)

#         elif status == "AVAILABLE":

#             bg = (55, 80, 65)
#             border = (140, 220, 160)

#         elif status == "COMPLETED":

#             bg = (65, 65, 65)
#             border = (150, 150, 150)

#         else:

#             bg = (48, 48, 58)
#             border = (105, 105, 115)

#         rect = pygame.Rect(
#             x,
#             y,
#             width,
#             92
#         )

#         pygame.draw.rect(
#             self.screen,
#             bg,
#             rect,
#             border_radius=12
#         )

#         pygame.draw.rect(
#             self.screen,
#             border,
#             rect,
#             2,
#             border_radius=12
#         )

#         title = self.font.render(
#             quest.title,
#             True,
#             (255, 255, 255)
#         )

#         self.screen.blit(
#             title,
#             (
#                 rect.x + 15,
#                 rect.y + 10
#             )
#         )

#         giver = self.tiny_font.render(
#             (
#                 f"From {quest.giver_name}  •  "
#                 f"{quest.chain_id}"
#             ),
#             True,
#             (190, 185, 210)
#         )

#         self.screen.blit(
#             giver,
#             (
#                 rect.x + 15,
#                 rect.y + 37
#             )
#         )

#         if status == "LOCKED":

#             prerequisite = self.get_quest_by_id(
#                 quest.prerequisite
#             )

#             if prerequisite:

#                 status_text = (
#                     "Locked — complete "
#                     f"'{prerequisite.title}'"
#                 )

#             else:

#                 status_text = "Locked"

#         elif status == "COMPLETED":

#             status_text = "Completed"

#         elif status == "AVAILABLE":

#             status_text = (
#                 f"Available  •  "
#                 f"Reward: {quest.reward_coins} coins"
#             )

#         else:

#             status_text = (
#                 f"Progress: "
#                 f"{quest.progress}/"
#                 f"{quest.required_amount}  •  "
#                 f"Reward: {quest.reward_coins}"
#             )

#         status_surface = self.small_font.render(
#             status_text,
#             True,
#             (235, 235, 235)
#         )

#         self.screen.blit(
#             status_surface,
#             (
#                 rect.x + 15,
#                 rect.y + 62
#             )
#         )

#         return rect.height

#     # ============================================================
#     # QUEST LOG
#     # ============================================================

#     def draw_quest_log(self):

#         self.screen.fill(
#             (30, 25, 45)
#         )

#         # ========================================================
#         # HEADER
#         # ========================================================

#         header = pygame.Rect(
#             0,
#             0,
#             SCREEN_WIDTH,
#             95
#         )

#         pygame.draw.rect(
#             self.screen,
#             (55, 45, 75),
#             header
#         )

#         title = self.title_font.render(
#             "QUEST LOG",
#             True,
#             (255, 230, 140)
#         )

#         self.screen.blit(
#             title,
#             (
#                 30,
#                 20
#             )
#         )

#         subtitle = self.small_font.render(
#             "Manage your magical adventures",
#             True,
#             (210, 205, 225)
#         )

#         self.screen.blit(
#             subtitle,
#             (
#                 30,
#                 57
#             )
#         )

#         # ========================================================
#         # TABS
#         # ========================================================

#         tab_y = 105
#         tab_height = 50

#         tab_left = 25
#         tab_total_width = SCREEN_WIDTH - 65

#         tab_width = tab_total_width // 4

#         tab_data = [
#             (
#                 "ACTIVE",
#                 len(self.get_active_quests())
#             ),
#             (
#                 "AVAILABLE",
#                 len(self.get_available_quests())
#             ),
#             (
#                 "COMPLETED",
#                 len(self.get_completed_quests())
#             ),
#             (
#                 "LOCKED",
#                 len(self.get_locked_quests())
#             )
#         ]

#         for index, (name, count) in enumerate(
#             tab_data
#         ):

#             x = (
#                 tab_left
#                 + index * tab_width
#             )

#             rect = pygame.Rect(
#                 x,
#                 tab_y,
#                 tab_width - 4,
#                 tab_height
#             )

#             if index == self.quest_tab:

#                 bg = (115, 90, 150)
#                 border = (255, 225, 130)

#             else:

#                 bg = (55, 48, 70)
#                 border = (100, 90, 115)

#             pygame.draw.rect(
#                 self.screen,
#                 bg,
#                 rect,
#                 border_radius=10
#             )

#             pygame.draw.rect(
#                 self.screen,
#                 border,
#                 rect,
#                 2,
#                 border_radius=10
#             )

#             label = self.small_font.render(
#                 f"{name} ({count})",
#                 True,
#                 (255, 255, 255)
#             )

#             label_rect = label.get_rect(
#                 center=rect.center
#             )

#             self.screen.blit(
#                 label,
#                 label_rect
#             )

#         # ========================================================
#         # VIEWPORT
#         # ========================================================

#         viewport = self.get_quest_log_view_rect()

#         pygame.draw.rect(
#             self.screen,
#             (38, 33, 52),
#             viewport,
#             border_radius=10
#         )

#         pygame.draw.rect(
#             self.screen,
#             (100, 90, 120),
#             viewport,
#             2,
#             border_radius=10
#         )

#         # ========================================================
#         # CURRENT TAB QUESTS
#         # ========================================================

#         quests = self.get_current_quest_list()

#         status = self.quest_tab_names[
#             self.quest_tab
#         ]

#         sorted_quests = sorted(
#             quests,
#             key=lambda q: (
#                 q.giver_name,
#                 q.chain_id,
#                 q.chain_order
#             )
#         )

#         entry_height = 105
#         top_padding = 20
#         bottom_padding = 20

#         content_height = (
#             top_padding
#             + len(sorted_quests)
#             * entry_height
#             + bottom_padding
#         )

#         self.quest_content_height[
#             self.quest_tab
#         ] = content_height

#         max_scroll = max(
#             0,
#             content_height - viewport.height
#         )

#         self.quest_scroll[
#             self.quest_tab
#         ] = int(
#             clamp(
#                 self.quest_scroll[
#                     self.quest_tab
#                 ],
#                 0,
#                 max_scroll
#             )
#         )

#         old_clip = self.screen.get_clip()

#         self.screen.set_clip(
#             viewport
#         )

#         x = viewport.x + 15

#         y = (
#             viewport.y
#             + top_padding
#             - self.quest_scroll[
#                 self.quest_tab
#             ]
#         )

#         width = viewport.width - 45

#         if not sorted_quests:

#             messages = {
#                 0: (
#                     "You don't have any active quests yet."
#                 ),
#                 1: (
#                     "There are no quests available "
#                     "right now."
#                 ),
#                 2: (
#                     "You haven't completed any quests yet."
#                 ),
#                 3: (
#                     "No locked quests."
#                 )
#             }

#             empty = self.font.render(
#                 messages[self.quest_tab],
#                 True,
#                 (150, 145, 165)
#             )

#             empty_rect = empty.get_rect(
#                 center=viewport.center
#             )

#             self.screen.blit(
#                 empty,
#                 empty_rect
#             )

#         else:

#             for quest in sorted_quests:

#                 self.draw_quest_entry(
#                     quest,
#                     x,
#                     y,
#                     width,
#                     status
#                 )

#                 y += entry_height

#         self.screen.set_clip(
#             old_clip
#         )

#         # ========================================================
#         # SCROLLBAR
#         # ========================================================

#         scrollbar_x = SCREEN_WIDTH - 27
#         scrollbar_y = viewport.y + 5
#         scrollbar_height = viewport.height - 10

#         pygame.draw.rect(
#             self.screen,
#             (55, 50, 68),
#             (
#                 scrollbar_x,
#                 scrollbar_y,
#                 10,
#                 scrollbar_height
#             ),
#             border_radius=5
#         )

#         if content_height > viewport.height:

#             thumb_height = max(
#                 40,
#                 int(
#                     scrollbar_height
#                     * viewport.height
#                     / content_height
#                 )
#             )

#             scroll_range = (
#                 scrollbar_height
#                 - thumb_height
#             )

#             thumb_y = (
#                 scrollbar_y
#                 + int(
#                     scroll_range
#                     * self.quest_scroll[
#                         self.quest_tab
#                     ]
#                     / max_scroll
#                 )
#             )

#             pygame.draw.rect(
#                 self.screen,
#                 (180, 155, 225),
#                 (
#                     scrollbar_x,
#                     thumb_y,
#                     10,
#                     thumb_height
#                 ),
#                 border_radius=5
#             )

#         else:

#             pygame.draw.rect(
#                 self.screen,
#                 (120, 110, 140),
#                 (
#                     scrollbar_x,
#                     scrollbar_y,
#                     10,
#                     scrollbar_height
#                 ),
#                 border_radius=5
#             )

#         # ========================================================
#         # FOOTER
#         # ========================================================

#         footer = pygame.Rect(
#             0,
#             SCREEN_HEIGHT - 55,
#             SCREEN_WIDTH,
#             55
#         )

#         pygame.draw.rect(
#             self.screen,
#             (55, 45, 75),
#             footer
#         )

#         footer_text = self.small_font.render(
#             (
#                 "← → Change Tab    "
#                 "↑ ↓ Scroll    "
#                 "Mouse Wheel    "
#                 "Home / End    "
#                 "Q / ESC Close"
#             ),
#             True,
#             (235, 235, 245)
#         )

#         footer_rect = footer_text.get_rect(
#             center=footer.center
#         )

#         self.screen.blit(
#             footer_text,
#             footer_rect
#         )

#     # ============================================================
#     # PAUSE
#     # ============================================================

#     def draw_pause(self):

#         overlay = pygame.Surface(
#             (
#                 SCREEN_WIDTH,
#                 SCREEN_HEIGHT
#             ),
#             pygame.SRCALPHA
#         )

#         overlay.fill(
#             (0, 0, 0, 150)
#         )

#         self.screen.blit(
#             overlay,
#             (0, 0)
#         )

#         title = self.title_font.render(
#             "PAUSED",
#             True,
#             (255, 255, 255)
#         )

#         title_rect = title.get_rect(
#             center=(
#                 SCREEN_WIDTH // 2,
#                 230
#             )
#         )

#         self.screen.blit(
#             title,
#             title_rect
#         )

#         instructions = [
#             "ESC  Resume",
#             "Q    Quest Log"
#         ]

#         y = 300

#         for text in instructions:

#             surface = self.font.render(
#                 text,
#                 True,
#                 (235, 235, 245)
#             )

#             rect = surface.get_rect(
#                 center=(
#                     SCREEN_WIDTH // 2,
#                     y
#                 )
#             )

#             self.screen.blit(
#                 surface,
#                 rect
#             )

#             y += 45

#     # ============================================================
#     # CHARACTER SELECT
#     # ============================================================

#     def draw_character_select(self):

#         self.screen.fill(
#             (120, 90, 150)
#         )

#         title = self.title_font.render(
#             "Choose Your Fairy",
#             True,
#             (255, 255, 255)
#         )

#         title_rect = title.get_rect(
#             center=(
#                 SCREEN_WIDTH // 2,
#                 110
#             )
#         )

#         self.screen.blit(
#             title,
#             title_rect
#         )

#         subtitle = self.font.render(
#             (
#                 "Choose Mepple or Mipple "
#                 "to begin your adventure"
#             ),
#             True,
#             (235, 225, 255)
#         )

#         subtitle_rect = subtitle.get_rect(
#             center=(
#                 SCREEN_WIDTH // 2,
#                 150
#             )
#         )

#         self.screen.blit(
#             subtitle,
#             subtitle_rect
#         )

#         cards = [

#             (
#                 "Mepple",
#                 "mepple.png",
#                 pygame.Rect(
#                     SCREEN_WIDTH // 2 - 300,
#                     260,
#                     240,
#                     280
#                 ),
#                 "1"
#             ),

#             (
#                 "Mipple",
#                 "mipple.png",
#                 pygame.Rect(
#                     SCREEN_WIDTH // 2 + 60,
#                     260,
#                     240,
#                     280
#                 ),
#                 "2"
#             )
#         ]

#         mouse_pos = pygame.mouse.get_pos()

#         for name, filename, rect, key in cards:

#             hovered = rect.collidepoint(
#                 mouse_pos
#             )

#             color = (
#                 (100, 80, 135)
#                 if hovered
#                 else (75, 60, 105)
#             )

#             pygame.draw.rect(
#                 self.screen,
#                 color,
#                 rect,
#                 border_radius=20
#             )

#             pygame.draw.rect(
#                 self.screen,
#                 (255, 255, 255),
#                 rect,
#                 3,
#                 border_radius=20
#             )

#             image = load_image(
#                 filename,
#                 (100, 120)
#             )

#             if image:

#                 image_rect = image.get_rect(
#                     center=(
#                         rect.centerx,
#                         rect.y + 100
#                     )
#                 )

#                 self.screen.blit(
#                     image,
#                     image_rect
#                 )

#             name_surface = self.large_font.render(
#                 name,
#                 True,
#                 (255, 255, 255)
#             )

#             name_rect = name_surface.get_rect(
#                 center=(
#                     rect.centerx,
#                     rect.y + 195
#                 )
#             )

#             self.screen.blit(
#                 name_surface,
#                 name_rect
#             )

#             key_surface = self.font.render(
#                 f"Press {key}",
#                 True,
#                 (255, 225, 130)
#             )

#             key_rect = key_surface.get_rect(
#                 center=(
#                     rect.centerx,
#                     rect.y + 235
#                 )
#             )

#             self.screen.blit(
#                 key_surface,
#                 key_rect
#             )

#         hint = self.small_font.render(
#             "Click a character or press 1 / 2",
#             True,
#             (235, 225, 255)
#         )

#         hint_rect = hint.get_rect(
#             center=(
#                 SCREEN_WIDTH // 2,
#                 600
#             )
#         )

#         self.screen.blit(
#             hint,
#             hint_rect
#         )

#     # ============================================================
#     # MAIN DRAW
#     # ============================================================

#     def draw(self):

#         if self.state == "character_select":

#             self.draw_character_select()
#             return

#         if self.state == "quest_log":

#             self.draw_quest_log()
#             return

#         self.draw_world()
#         self.draw_hud()

#         if self.dialogue_npc is not None:

#             self.draw_dialogue()

#         if self.state == "pause":

#             self.draw_pause()


# ================================================================
# game/game.py
# ================================================================

# import os
# import math
# import random
# import json
# import pygame


# ================================================================
# CONSTANTS
# ================================================================

# SCREEN_WIDTH = 1100
# SCREEN_HEIGHT = 700

# WORLD_WIDTH = 4000
# WORLD_HEIGHT = 3000

# PLAYER_SPEED = 4.0
# COMPANION_SPEED = 3.5

# NPC_MIN_SPEED = 1.0
# NPC_MAX_SPEED = 1.7

# NPC_INTERACTION_DISTANCE = 115

# FPS = 60
# One full in-game day lasts 6 real minutes.
GAME_DAY_LENGTH_MS = 6 * 60 * 1000
NPC_HOME_HOUR = 20
NPC_WAKE_HOUR = 6


# ================================================================
# PATHS
# ================================================================

# GAME_DIR = os.path.dirname(os.path.abspath(__file__))
# PROJECT_DIR = os.path.dirname(GAME_DIR)
# ASSET_DIR = os.path.join(PROJECT_DIR, "assets", "fairies")


# def asset_path(filename):
#     return os.path.join(ASSET_DIR, filename)


# ================================================================
# HELPERS
# ================================================================

# def clamp(value, minimum, maximum):
#     return max(minimum, min(value, maximum))


# def distance(x1, y1, x2, y2):
#     return math.hypot(x2 - x1, y2 - y1)


# def wrap_text(text, font, max_width):
#     words = text.split()

#     lines = []
#     current = ""

#     for word in words:

#         test = (
#             word
#             if not current
#             else current + " " + word
#         )

#         if font.size(test)[0] <= max_width:

#             current = test

#         else:

#             if current:
#                 lines.append(current)

#             current = word

#     if current:
#         lines.append(current)

#     return lines


# def load_image(filename, size=None):

#     path = asset_path(filename)

#     if not os.path.exists(path):
#         return None

#     try:

#         image = pygame.image.load(
#             path
#         ).convert_alpha()

#         if size:

#             image = pygame.transform.smoothscale(
#                 image,
#                 size
#             )

#         return image

#     except pygame.error:

#         return None


# ================================================================
# CAMERA
# ================================================================

# class Camera:

#     def __init__(self):

#         self.x = 0
#         self.y = 0

#     def update(self, target_rect):

#         self.x = (
#             target_rect.centerx
#             - SCREEN_WIDTH // 2
#         )

#         self.y = (
#             target_rect.centery
#             - SCREEN_HEIGHT // 2
#         )

#         self.x = clamp(
#             self.x,
#             0,
#             max(
#                 0,
#                 WORLD_WIDTH - SCREEN_WIDTH
#             )
#         )

#         self.y = clamp(
#             self.y,
#             0,
#             max(
#                 0,
#                 WORLD_HEIGHT - SCREEN_HEIGHT
#             )
#         )

#     def world_to_screen(self, x, y):

#         return (
#             int(x - self.x),
#             int(y - self.y)
#         )


# ================================================================
# OBSTACLE
# ================================================================

class Obstacle:

    def __init__(
        self,
        x,
        y,
        width,
        height,
        kind="tree",
        style="default"
    ):

        self.rect = pygame.Rect(
            x,
            y,
            width,
            height
        )

        self.kind = kind
        self.style = style
        # For fairy houses, this identifies the NPC who lives here.
        # It is intentionally stored on the house itself so the visible
        # owner label always follows the correct house after repositioning.
        self.owner = None

    def draw(self, screen, camera):

        rect = self.rect.move(
            -camera.x,
            -camera.y
        )

        if (
            rect.right < 0
            or rect.left > SCREEN_WIDTH
            or rect.bottom < 0
            or rect.top > SCREEN_HEIGHT
        ):
            return

        if self.kind == "tree":

            # --------------------------------------------------------
            # 3D FAIRY TREE
            # --------------------------------------------------------
            # The tree is still drawn with Pygame primitives, but uses
            # layered silhouettes, side shading, highlights, branches,
            # a ground shadow and depth offsets so it reads as a solid
            # 3D object instead of a flat 2D icon.

            # Ground shadow / contact shadow.
            shadow = pygame.Rect(
                rect.left - 8,
                rect.bottom - 13,
                rect.width + 16,
                25
            )
            pygame.draw.ellipse(
                screen,
                (62, 86, 65),
                shadow
            )
            pygame.draw.ellipse(
                screen,
                (48, 72, 52),
                shadow.inflate(-18, -8)
            )

            # Main trunk: dark rear side first.
            trunk_w = 34
            trunk_h = 78
            trunk = pygame.Rect(
                rect.centerx - trunk_w // 2,
                rect.bottom - trunk_h,
                trunk_w,
                trunk_h
            )

            pygame.draw.polygon(
                screen,
                (82, 52, 35),
                [
                    (trunk.left - 4, trunk.bottom),
                    (trunk.left + 1, trunk.top + 9),
                    (trunk.left + 7, trunk.top),
                    (trunk.right + 5, trunk.top + 7),
                    (trunk.right + 8, trunk.bottom),
                ]
            )

            # Warm front face.
            pygame.draw.rect(
                screen,
                (139, 88, 48),
                trunk,
                border_radius=6
            )

            # Bright side plane creates a rounded trunk highlight.
            pygame.draw.polygon(
                screen,
                (180, 116, 63),
                [
                    (trunk.left + 5, trunk.top + 4),
                    (trunk.left + 12, trunk.top + 1),
                    (trunk.left + 11, trunk.bottom - 4),
                    (trunk.left + 4, trunk.bottom),
                ]
            )

            # Dark bark plane on the opposite side.
            pygame.draw.polygon(
                screen,
                (101, 61, 38),
                [
                    (trunk.right - 7, trunk.top + 5),
                    (trunk.right, trunk.top + 9),
                    (trunk.right, trunk.bottom),
                    (trunk.right - 9, trunk.bottom - 3),
                ]
            )

            # Roots spread over the ground, reinforcing the 3D contact.
            pygame.draw.polygon(
                screen,
                (113, 69, 40),
                [
                    (trunk.left + 3, trunk.bottom - 14),
                    (trunk.left - 19, trunk.bottom - 4),
                    (trunk.left - 24, trunk.bottom + 4),
                    (trunk.centerx - 2, trunk.bottom - 2),
                ]
            )
            pygame.draw.polygon(
                screen,
                (95, 57, 36),
                [
                    (trunk.right - 3, trunk.bottom - 14),
                    (trunk.right + 18, trunk.bottom - 3),
                    (trunk.right + 23, trunk.bottom + 5),
                    (trunk.centerx + 3, trunk.bottom - 2),
                ]
            )

            # Branches behind the canopy.
            branch_color = (102, 63, 39)
            branch_hi = (157, 96, 49)

            pygame.draw.polygon(
                screen,
                branch_color,
                [
                    (trunk.centerx - 2, trunk.top + 24),
                    (trunk.left - 22, trunk.top + 2),
                    (trunk.left - 30, trunk.top + 6),
                    (trunk.centerx - 7, trunk.top + 34),
                ]
            )
            pygame.draw.polygon(
                screen,
                branch_color,
                [
                    (trunk.centerx + 3, trunk.top + 27),
                    (trunk.right + 24, trunk.top + 1),
                    (trunk.right + 31, trunk.top + 7),
                    (trunk.centerx + 9, trunk.top + 37),
                ]
            )
            pygame.draw.line(
                screen, branch_hi,
                (trunk.centerx - 2, trunk.top + 24),
                (trunk.left - 20, trunk.top + 5),
                4
            )

            # Canopy rear shadow: large dark volume.
            canopy_shadow = pygame.Rect(
                rect.left - 24,
                rect.top - 30,
                rect.width + 48,
                104
            )
            pygame.draw.ellipse(
                screen,
                (47, 104, 57),
                canopy_shadow.move(7, 11)
            )

            # Main canopy volume.
            canopy = pygame.Rect(
                rect.left - 22,
                rect.top - 34,
                rect.width + 44,
                104
            )
            pygame.draw.ellipse(
                screen,
                (69, 145, 76),
                canopy
            )

            # Lower darker foliage gives the canopy a rounded underside.
            lower = pygame.Rect(
                rect.left - 12,
                rect.top + 10,
                rect.width + 24,
                62
            )
            pygame.draw.ellipse(
                screen,
                (53, 119, 62),
                lower
            )

            # Individual overlapping foliage masses create depth.
            foliage_layers = [
                (rect.left - 2, rect.top + 10, 48, 50, (82, 163, 84)),
                (rect.left + 17, rect.top - 18, 58, 56, (108, 188, 101)),
                (rect.centerx - 29, rect.top - 29, 62, 60, (101, 181, 94)),
                (rect.right - 61, rect.top - 14, 59, 56, (79, 158, 81)),
                (rect.right - 43, rect.top + 12, 50, 49, (62, 137, 70)),
            ]

            for fx, fy, fw, fh, color in foliage_layers:
                pygame.draw.ellipse(
                    screen,
                    color,
                    pygame.Rect(fx, fy, fw, fh)
                )

            # Soft top highlight: a large curved patch rather than a flat
            # circle, making the canopy appear rounded toward the light.
            highlight = pygame.Rect(
                rect.left + 18,
                rect.top - 5,
                64,
                25
            )
            pygame.draw.ellipse(
                screen,
                (139, 207, 120),
                highlight
            )
            pygame.draw.ellipse(
                screen,
                (169, 222, 137),
                highlight.inflate(-15, -10)
            )

            # A few small darker leaf clusters add depth at the front.
            for fx, fy, r in [
                (rect.left + 16, rect.top + 43, 10),
                (rect.centerx + 2, rect.top + 51, 12),
                (rect.right - 14, rect.top + 42, 9),
            ]:
                pygame.draw.circle(screen, (48, 111, 58), (fx, fy), r)

            # Tiny leaf highlights.
            for fx, fy in [
                (rect.left + 31, rect.top + 19),
                (rect.centerx - 5, rect.top + 7),
                (rect.right - 30, rect.top + 16),
            ]:
                pygame.draw.ellipse(
                    screen,
                    (186, 225, 143),
                    pygame.Rect(fx, fy, 9, 5)
                )

        elif self.kind == "rock":

            pygame.draw.ellipse(screen, (105, 110, 125), rect)
            top = rect.inflate(-10, -8)
            top.move_ip(-2, -5)
            pygame.draw.ellipse(screen, (158, 164, 178), top)
            pygame.draw.ellipse(screen, (190, 195, 207), top.inflate(-14, -10))
            pygame.draw.line(screen, (220, 224, 232),
                             (top.left + 8, top.centery - 4),
                             (top.centerx, top.top + 4), 3)

        elif self.kind == "house":

            # Every house has its own silhouette, construction and entrance.
            style = self.style
            pygame.draw.ellipse(
                screen, (82, 100, 88),
                (rect.left - 20, rect.bottom - 3, rect.width + 65, 28)
            )

            if style == "mushroom":
                # Round mushroom cottage.
                wall = pygame.Rect(rect.left + 35, rect.top + 38, rect.width - 70, rect.height - 48)
                pygame.draw.rect(screen, (204, 139, 105), wall.move(8, 9), border_radius=28)
                pygame.draw.rect(screen, (246, 197, 157), wall, border_radius=28)
                cap = pygame.Rect(rect.left - 18, rect.top - 25, rect.width + 36, 92)
                pygame.draw.ellipse(screen, (158, 54, 91), cap.move(7, 13))
                pygame.draw.ellipse(screen, (218, 69, 122), cap)
                pygame.draw.arc(screen, (250, 137, 170), cap.inflate(-8, -8), math.pi*.08, math.pi*.92, 5)
                for sx, sy, sr in [(rect.left+28,rect.top+8,12),(rect.centerx-5,rect.top-9,16),(rect.right-28,rect.top+9,11)]:
                    pygame.draw.circle(screen, (255,232,235), (sx,sy), sr)
                    pygame.draw.circle(screen, (239,183,198), (sx,sy), sr, 2)
                porch = pygame.Rect(rect.centerx-43, wall.bottom-17, 86, 18)
                pygame.draw.rect(screen, (133,88,67), porch, border_radius=7)
                door = pygame.Rect(rect.centerx-22, wall.bottom-61, 44, 61)
                pygame.draw.ellipse(screen, (104,67,55), door)
                pygame.draw.circle(screen, (255,214,103), (door.right-9,door.centery), 4)
                for wx in (wall.left+22, wall.right-22):
                    pygame.draw.circle(screen, (117,78,67), (wx,wall.top+47), 17)
                    pygame.draw.circle(screen, (154,226,237), (wx,wall.top+47), 12)

            elif style == "flower":
                # Flower-shaped cottage with six giant petals.
                base = [(rect.left+50,rect.bottom-10),(rect.left+36,rect.top+65),(rect.left+58,rect.top+37),
                        (rect.centerx,rect.top+52),(rect.right-58,rect.top+37),(rect.right-36,rect.top+65),(rect.right-50,rect.bottom-10)]
                pygame.draw.polygon(screen, (177,111,91), [(x+8,y+9) for x,y in base])
                pygame.draw.polygon(screen, (249,205,151), base)
                cx,cy = rect.centerx,rect.top+27
                petals=[(245,117,169),(255,145,188),(239,112,180)]
                for i,angle in enumerate(range(0,360,60)):
                    rad=math.radians(angle); px=cx+int(math.cos(rad)*49); py=cy+int(math.sin(rad)*28)
                    petal=pygame.Rect(px-38,py-20,76,40)
                    pygame.draw.ellipse(screen,(185,78,130),petal.move(5,7))
                    pygame.draw.ellipse(screen,petals[i%3],petal)
                pygame.draw.circle(screen,(255,214,77),(cx,cy),25)
                pygame.draw.circle(screen,(255,238,126),(cx-5,cy-5),12)
                door=pygame.Rect(cx-22,rect.bottom-69,44,69)
                pygame.draw.ellipse(screen,(137,79,105),door)
                pygame.draw.ellipse(screen,(190,111,139),door.inflate(-7,-6))
                pygame.draw.ellipse(screen,(87,158,91),(rect.left+5,rect.bottom-48,55,25))
                pygame.draw.ellipse(screen,(105,177,95),(rect.right-60,rect.bottom-48,55,25))

            elif style == "crystal":
                # Tall crystal palace with three independent towers.
                body=[(rect.left+45,rect.bottom-15),(rect.left+45,rect.top+54),(rect.centerx,rect.top+15),
                      (rect.right-45,rect.top+54),(rect.right-45,rect.bottom-15)]
                pygame.draw.polygon(screen,(105,101,164),[(x+8,y+10) for x,y in body])
                pygame.draw.polygon(screen,(187,177,231),body)
                for cx,base_y,w,h in [(rect.left+32,rect.top+55,34,100),(rect.centerx,rect.top+8,46,145),(rect.right-32,rect.top+55,34,100)]:
                    pts=[(cx,base_y-h),(cx+w//2,base_y-24),(cx+w//3,base_y),(cx-w//3,base_y),(cx-w//2,base_y-24)]
                    pygame.draw.polygon(screen,(78,106,180),[(x+6,y+8) for x,y in pts])
                    pygame.draw.polygon(screen,(112,163,231),pts)
                    pygame.draw.line(screen,(225,247,255),pts[0],pts[2],3)
                crystal=[(rect.centerx,rect.top-33),(rect.centerx+13,rect.top-9),(rect.centerx,rect.top+14),(rect.centerx-13,rect.top-9)]
                pygame.draw.polygon(screen,(104,204,247),crystal)
                pygame.draw.polygon(screen,(235,255,255),crystal,2)
                door=pygame.Rect(rect.centerx-25,rect.bottom-79,50,79)
                pygame.draw.ellipse(screen,(63,65,117),door)
                pygame.draw.ellipse(screen,(121,142,214),door.inflate(-8,-7))
                for wx in (rect.left+70,rect.right-70):
                    pts=[(wx,rect.top+63),(wx+15,rect.top+82),(wx,rect.top+101),(wx-15,rect.top+82)]
                    pygame.draw.polygon(screen,(118,218,245),pts)
                    pygame.draw.polygon(screen,(238,255,255),pts,2)

            elif style == "treehouse":
                # Elevated wooden cabin built into a giant tree.
                tx=rect.centerx
                pygame.draw.polygon(screen,(87,57,36),[(tx-27,rect.bottom+15),(tx-17,rect.top+35),(tx+17,rect.top+35),(tx+32,rect.bottom+15)])
                pygame.draw.polygon(screen,(132,86,48),[(tx-13,rect.bottom+10),(tx-8,rect.top+43),(tx+11,rect.top+43),(tx+18,rect.bottom+10)])
                pygame.draw.line(screen,(95,61,37),(tx,rect.top+65),(rect.left-15,rect.top+20),14)
                pygame.draw.line(screen,(95,61,37),(tx+2,rect.top+62),(rect.right+15,rect.top+14),12)
                cabin=pygame.Rect(rect.left+25,rect.top+45,rect.width-50,76)
                pygame.draw.rect(screen,(91,57,38),cabin.move(8,10),border_radius=8)
                pygame.draw.rect(screen,(181,128,76),cabin,border_radius=8)
                for yy in range(cabin.top+10,cabin.bottom,16):
                    pygame.draw.line(screen,(130,85,51),(cabin.left+5,yy),(cabin.right-5,yy),3)
                leaves=[(rect.left+30,rect.top+28,38,(71,133,71)),(rect.centerx-35,rect.top+8,47,(94,161,76)),
                        (rect.centerx+30,rect.top+18,43,(79,145,69)),(rect.right-25,rect.top+38,34,(62,122,65))]
                for cx,cy,r,col in leaves: pygame.draw.circle(screen,col,(cx,cy),r)
                pygame.draw.line(screen,(151,103,61),(rect.centerx-27,cabin.bottom),(rect.centerx-27,rect.bottom+4),5)
                pygame.draw.line(screen,(151,103,61),(rect.centerx+27,cabin.bottom),(rect.centerx+27,rect.bottom+4),5)
                for yy in range(cabin.bottom+5,rect.bottom,14):
                    pygame.draw.line(screen,(181,130,76),(rect.centerx-27,yy),(rect.centerx+27,yy),4)
                for wx in (cabin.left+25,cabin.right-25):
                    pygame.draw.circle(screen,(92,61,43),(wx,cabin.centery),15)
                    pygame.draw.circle(screen,(154,220,229),(wx,cabin.centery),10)

            elif style == "pond":
                # Water dwelling sitting on a little magical pond.
                pond=pygame.Rect(rect.left-18,rect.bottom-15,rect.width+36,46)
                pygame.draw.ellipse(screen,(45,126,160),pond)
                pygame.draw.ellipse(screen,(83,187,205),pond.inflate(-8,-8))
                pygame.draw.arc(screen,(208,250,250),pond.inflate(-12,-12),math.pi,math.pi*2,4)
                body=pygame.Rect(rect.left+25,rect.top+48,rect.width-50,80)
                pygame.draw.ellipse(screen,(53,125,145),body.move(7,10))
                pygame.draw.ellipse(screen,(148,209,201),body)
                dome=pygame.Rect(rect.left+7,rect.top-16,rect.width-14,105)
                pygame.draw.ellipse(screen,(40,128,165),dome.move(6,9))
                pygame.draw.ellipse(screen,(78,181,201),dome)
                pygame.draw.arc(screen,(221,255,255),dome.inflate(-16,-16),math.pi*.08,math.pi*.92,5)
                door=pygame.Rect(rect.centerx-23,rect.bottom-62,46,62)
                pygame.draw.ellipse(screen,(36,103,132),door)
                pygame.draw.ellipse(screen,(91,194,211),door.inflate(-7,-5))
                for wx in (rect.left+40,rect.right-40):
                    pygame.draw.circle(screen,(43,120,150),(wx,rect.top+70),17)
                    pygame.draw.circle(screen,(167,239,241),(wx,rect.top+70),11)
                for px,py in [(rect.left+2,rect.bottom+12),(rect.right-4,rect.bottom+18)]:
                    pygame.draw.ellipse(screen,(76,158,96),(px-18,py-8,36,16))

            else:
                wall=pygame.Rect(rect.left+20,rect.top+35,rect.width-40,rect.height-45)
                pygame.draw.rect(screen,(225,180,140),wall,border_radius=12)
                pygame.draw.polygon(screen,(180,90,125),[(rect.left,rect.top+45),(rect.centerx,rect.top-35),(rect.right,rect.top+45)])
                pygame.draw.rect(screen,(105,70,58),(rect.centerx-20,wall.bottom-60,40,60),border_radius=8)

            for dx in (-62,62):
                gx=rect.centerx+dx
                pygame.draw.ellipse(screen,(126,137,128),(gx-8,rect.bottom-5,16,8))

            # --------------------------------------------------------
            # FAIRY HOUSE OWNER LABEL
            # --------------------------------------------------------
            # Keep this label attached to the actual house object. This
            # makes it impossible for the displayed owner to get separated
            # from a house if its world position changes.
            if self.owner:
                label = f"{self.owner}'s House"
                font = pygame.font.SysFont("arial", 16, bold=True)
                label_surface = font.render(label, True, (255, 255, 255))
                label_rect = label_surface.get_rect(
                    center=(rect.centerx, rect.top - 42)
                )
                bg = label_rect.inflate(18, 8)
                pygame.draw.rect(
                    screen, (67, 49, 84), bg, border_radius=9
                )
                pygame.draw.rect(
                    screen, (255, 224, 137), bg, 2, border_radius=9
                )
                screen.blit(label_surface, label_rect)

        elif self.kind == "fence":

            # Chunky isometric-style fence: rear shadow, thick rails,
            # highlighted front faces and dark side faces give each post
            # actual depth instead of a flat rectangle.
            shadow = pygame.Rect(rect.left - 2, rect.bottom - 2, rect.width + 8, 12)
            pygame.draw.ellipse(screen, (58, 78, 58), shadow)

            rail_back = pygame.Rect(rect.left, rect.top + 5, rect.width, max(8, rect.height - 4))
            pygame.draw.rect(screen, (108, 70, 42), rail_back, border_radius=5)
            pygame.draw.rect(screen, (184, 127, 70), rect.inflate(0, -4), border_radius=4)
            pygame.draw.line(screen, (232, 178, 103), (rect.left + 3, rect.top + 2), (rect.right - 3, rect.top + 2), 3)

            for x in range(rect.left + 10, rect.right, 35):
                post = pygame.Rect(x, rect.top - 14, 14, rect.height + 28)
                pygame.draw.rect(screen, (91, 57, 37), post.move(5, 4), border_radius=4)
                pygame.draw.rect(screen, (180, 119, 66), post, border_radius=4)
                pygame.draw.polygon(screen, (119, 75, 43), [(post.right-5, post.top+2), (post.right+5, post.top+7), (post.right+5, post.bottom-4), (post.right-5, post.bottom)])
                pygame.draw.line(screen, (235, 181, 104), (post.left+3, post.top+4), (post.left+3, post.bottom-5), 3)
                pygame.draw.polygon(screen, (201, 144, 81), [(post.left-2, post.top), (post.centerx, post.top-6), (post.right+2, post.top), (post.centerx, post.top+6)])


# ================================================================
# FLOWER
# ================================================================

class Flower:

    def __init__(
        self,
        x,
        y,
        flower_id
    ):

        self.x = x
        self.y = y
        self.flower_id = flower_id

        self.collected = False

        self.phase = random.uniform(
            0,
            math.pi * 2
        )

    def update(self, dt):

        self.phase += dt * 0.003

    def draw(self, screen, camera):

        if self.collected:
            return

        sx, sy = camera.world_to_screen(
            self.x,
            self.y
        )

        if (
            sx < -20
            or sx > SCREEN_WIDTH + 20
            or sy < -20
            or sy > SCREEN_HEIGHT + 20
        ):
            return

        bob = math.sin(
            self.phase
        ) * 2

        pygame.draw.line(
            screen,
            (70, 155, 75),
            (
                sx,
                sy + 8 + bob
            ),
            (
                sx,
                sy + 22 + bob
            ),
            3
        )

        colors = [
            (255, 145, 190),
            (245, 170, 220),
            (185, 145, 255),
            (255, 190, 120)
        ]

        color = colors[
            self.flower_id
            % len(colors)
        ]

        for angle in range(
            0,
            360,
            90
        ):

            rad = math.radians(
                angle
            )

            px = sx + int(
                math.cos(rad) * 7
            )

            py = sy + int(
                math.sin(rad) * 7
                + bob
            )

            pygame.draw.circle(
                screen,
                color,
                (px, py),
                6
            )

        pygame.draw.circle(
            screen,
            (255, 220, 80),
            (
                sx,
                sy + bob
            ),
            5
        )


# ================================================================
# QUEST ITEM
# ================================================================

class QuestItem:

    def __init__(
        self,
        x,
        y,
        item_type,
        name
    ):

        self.x = x
        self.y = y

        self.item_type = item_type
        self.name = name

        self.collected = False

        self.phase = random.uniform(
            0,
            math.pi * 2
        )

    def update(self, dt):

        self.phase += dt * 0.004

    def draw(self, screen, camera):

        if self.collected:
            return

        sx, sy = camera.world_to_screen(
            self.x,
            self.y
        )

        if (
            sx < -40
            or sx > SCREEN_WIDTH + 40
            or sy < -40
            or sy > SCREEN_HEIGHT + 40
        ):
            return

        bob = math.sin(
            self.phase
        ) * 3

        if self.item_type == "ribbon":

            color = (255, 120, 170)

            pygame.draw.line(
                screen,
                color,
                (
                    sx - 8,
                    sy - 5 + bob
                ),
                (
                    sx + 8,
                    sy + 5 + bob
                ),
                5
            )

            pygame.draw.circle(
                screen,
                color,
                (
                    sx,
                    sy + bob
                ),
                5
            )

        elif self.item_type == "seed":

            color = (125, 190, 100)

            pygame.draw.ellipse(
                screen,
                color,
                (
                    sx - 8,
                    sy - 12 + bob,
                    16,
                    24
                )
            )

        elif self.item_type == "crystal":

            color = (150, 190, 255)

            points = [
                (
                    sx,
                    sy - 15 + bob
                ),
                (
                    sx + 11,
                    sy + bob
                ),
                (
                    sx,
                    sy + 15 + bob
                ),
                (
                    sx - 11,
                    sy + bob
                )
            ]

            pygame.draw.polygon(
                screen,
                color,
                points
            )

            pygame.draw.polygon(
                screen,
                (225, 240, 255),
                points,
                2
            )

        elif self.item_type == "lost_star":

            color = (255, 220, 80)

            points = []

            for i in range(10):

                angle = (
                    -math.pi / 2
                    + i * math.pi / 5
                )

                radius = (
                    16
                    if i % 2 == 0
                    else 7
                )

                points.append(
                    (
                        sx
                        + math.cos(angle)
                        * radius,

                        sy
                        + bob
                        + math.sin(angle)
                        * radius
                    )
                )

            pygame.draw.polygon(
                screen,
                color,
                points
            )


# ================================================================
# QUEST LOCATION
# ================================================================

class QuestLocation:

    def __init__(
        self,
        location_id,
        name,
        x,
        y,
        radius=90
    ):

        self.location_id = location_id
        self.name = name

        self.x = x
        self.y = y

        self.radius = radius

    def draw(self, screen, camera):

        sx, sy = camera.world_to_screen(
            self.x,
            self.y
        )

        if (
            sx < -150
            or sx > SCREEN_WIDTH + 150
            or sy < -150
            or sy > SCREEN_HEIGHT + 150
        ):
            return

        pygame.draw.circle(
            screen,
            (255, 230, 150),
            (
                sx,
                sy
            ),
            self.radius,
            2
        )

        pygame.draw.circle(
            screen,
            (255, 240, 180),
            (
                sx,
                sy
            ),
            8
        )


# ================================================================
# QUEST
# ================================================================

class Quest:

    def __init__(
        self,
        quest_id,
        title,
        description,
        objective_type,
        required_amount,
        reward_coins,
        giver_name,
        chain_id,
        chain_order,
        prerequisite=None,
        target_ids=None,
        item_type=None,
        target_npc=None
    ):

        self.quest_id = quest_id
        self.title = title
        self.description = description

        self.objective_type = objective_type
        self.required_amount = required_amount

        self.reward_coins = reward_coins
        self.giver_name = giver_name

        self.chain_id = chain_id
        self.chain_order = chain_order

        self.prerequisite = prerequisite

        self.target_ids = target_ids or []
        self.item_type = item_type
        self.target_npc = target_npc

        self.progress = 0

        self.accepted = False
        self.completed = False
        self.reward_claimed = False

        self.visited_targets = set()

    def is_finished(self):

        return (
            self.progress
            >= self.required_amount
        )

    def add_progress(
        self,
        amount=1
    ):

        if not self.accepted:
            return

        if self.completed:
            return

        self.progress += amount

        self.progress = min(
            self.progress,
            self.required_amount
        )


# ================================================================
# FAIRY
# ================================================================

class Fairy:

    def __init__(
        self,
        name,
        image_filename,
        x,
        y
    ):

        self.name = name

        self.x = float(x)
        self.y = float(y)

        self.image = load_image(
            image_filename,
            (64, 78)
        )

        self.rect = pygame.Rect(
            int(x),
            int(y),
            44,
            60
        )

    def sync_rect(self):

        self.rect.topleft = (
            int(self.x),
            int(self.y)
        )

    def draw(
        self,
        screen,
        camera
    ):

        sx, sy = camera.world_to_screen(
            self.x,
            self.y
        )

        if self.image:

            image_rect = self.image.get_rect(
                center=(
                    sx
                    + self.rect.width // 2,

                    sy
                    + self.rect.height // 2
                )
            )

            screen.blit(
                self.image,
                image_rect
            )

        else:

            pygame.draw.circle(
                screen,
                (255, 220, 200),
                (
                    sx + 22,
                    sy + 17
                ),
                12
            )

            pygame.draw.circle(
                screen,
                (90, 180, 240),
                (
                    sx + 11,
                    sy + 27
                ),
                11
            )

            pygame.draw.circle(
                screen,
                (90, 180, 240),
                (
                    sx + 33,
                    sy + 27
                ),
                11
            )

            pygame.draw.ellipse(
                screen,
                (255, 180, 210),
                (
                    sx + 10,
                    sy + 28,
                    25,
                    30
                )
            )


# ================================================================
# PARTY FAIRY
# ================================================================

class PartyFairy(Fairy):

    def __init__(
        self,
        name,
        image_filename,
        x,
        y
    ):

        super().__init__(
            name,
            image_filename,
            x,
            y
        )

        self.speed = COMPANION_SPEED


# ================================================================
# FAIRY NPC
# ================================================================

class FairyNPC(Fairy):

    def __init__(self, name, image_filename, x, y, dialogue, wander_radius=200):
        super().__init__(name, image_filename, x, y)
        self.spawn_x = float(x)
        self.spawn_y = float(y)
        self.dialogue = dialogue
        self.dialogue_index = 0
        self.is_talking = False
        self.wander_radius = max(700, wander_radius)
        self.wander_min_distance = 180.0
        self.target_x = self.x
        self.target_y = self.y
        self.speed = random.uniform(1.6, 2.4)
        self.wait_timer = random.uniform(0.2, 1.0)
        self.stuck_timer = 0.0
        self.quest_ids = []
        self.house = None
        self.is_home = False
        self.home_reached = False
        self.home_target_x = self.x
        self.home_target_y = self.y

        # Non-romantic friendship relationship with the player.
        self.friendship = 0
        self.friendship_max = 100

        self.choose_new_destination()

    def add_friendship(self, amount):
        old_level = self.get_friendship_level()
        self.friendship = int(clamp(self.friendship + amount, 0, self.friendship_max))
        return old_level, self.get_friendship_level()

    def get_friendship_level(self):
        if self.friendship >= 80:
            return "Best Friends"
        if self.friendship >= 60:
            return "Close Friends"
        if self.friendship >= 40:
            return "Good Friends"
        if self.friendship >= 20:
            return "Friends"
        return "Acquaintances"

    def _fairy_rect(self, x, y):
        # Match the visible 64x78 sprite, with a small safety margin.
        return pygame.Rect(int(x) - 8, int(y) - 6, 60, 74)

    def _obstacle_visual_rect(self, obstacle):
        r = obstacle.rect
        if obstacle.kind == "tree":
            # Actual tree artwork extends about 7 px outside the 70x90 base.
            return pygame.Rect(r.left - 10, r.top - 20, r.width + 20, r.height + 28)
        if obstacle.kind == "fence":
            return r.inflate(16, 20)
        if obstacle.kind == "house":
            return r.inflate(24, 24)
        if obstacle.kind == "rock":
            return r.inflate(12, 12)
        return r.inflate(12, 12)

    def can_move_to(self, new_x, new_y, obstacles):
        test = self._fairy_rect(new_x, new_y)
        for obstacle in obstacles:
            if test.colliderect(self._obstacle_visual_rect(obstacle)):
                return False
        return True

    def choose_new_destination(self, obstacles=None):
        # Prefer nearby destinations so NPCs visibly wander instead of
        # repeatedly trying to cross the whole obstacle field.
        bases = [(self.x, self.y)]
        if obstacles is not None:
            for base_x, base_y in bases:
                for radius in range(150, int(self.wander_radius) + 1, 50):
                    for _ in range(18):
                        angle = random.uniform(0, math.tau)
                        tx = clamp(base_x + math.cos(angle) * radius, 80, WORLD_WIDTH - 100)
                        ty = clamp(base_y + math.sin(angle) * radius, 80, WORLD_HEIGHT - 100)
                        if self.can_move_to(tx, ty, obstacles):
                            self.target_x, self.target_y = tx, ty
                            return
        else:
            angle = random.uniform(0, math.tau)
            radius = random.uniform(60, self.wander_radius)
            self.target_x = clamp(self.spawn_x + math.cos(angle) * radius, 80, WORLD_WIDTH - 100)
            self.target_y = clamp(self.spawn_y + math.sin(angle) * radius, 80, WORLD_HEIGHT - 100)

        # Last resort: a short random step from the current position.
        for radius in (25, 35, 45):
            for angle_deg in range(0, 360, 30):
                angle = math.radians(angle_deg)
                tx = clamp(self.x + math.cos(angle) * radius, 80, WORLD_WIDTH - 100)
                ty = clamp(self.y + math.sin(angle) * radius, 80, WORLD_HEIGHT - 100)
                if obstacles is None or self.can_move_to(tx, ty, obstacles):
                    self.target_x, self.target_y = tx, ty
                    return
        self.target_x, self.target_y = self.x, self.y

    def set_home(self, house):
        self.house = house
        if house is not None:
            # Stand just outside the front of the house, rather than inside
            # the house collision rectangle.
            self.home_target_x = float(house.rect.centerx - self.rect.width // 2)
            self.home_target_y = float(house.rect.bottom + 18)

    def update_home_state(self, game_time_hour, obstacles):
        night = game_time_hour >= NPC_HOME_HOUR or game_time_hour < NPC_WAKE_HOUR
        if night and not self.is_home:
            self.is_home = True
            self.home_reached = False
            if self.house is not None:
                self.home_target_x = float(self.house.rect.centerx - self.rect.width // 2)
                self.home_target_y = float(self.house.rect.bottom + 18)
        elif not night and self.is_home:
            self.is_home = False
            self.home_reached = False
            self.choose_new_destination(obstacles)

    def _move_toward(self, tx, ty, dt, obstacles):
        dx = tx - self.x
        dy = ty - self.y
        dist = math.hypot(dx, dy)
        if dist < 12:
            return True
        dx /= dist
        dy /= dist
        step = min(2.8, max(1.0, self.speed * dt / 16.67))
        directions = [(dx, dy), (dx, 0), (0, dy), (-dy, dx), (dy, -dx)]
        desired_angle = math.atan2(dy, dx)
        for offset in (-0.45, 0.45, -0.9, 0.9, -1.35, 1.35, math.pi):
            directions.append((math.cos(desired_angle + offset), math.sin(desired_angle + offset)))
        for mx, my in directions:
            length = math.hypot(mx, my)
            if length == 0:
                continue
            mx, my = mx / length, my / length
            nx, ny = self.x + mx * step, self.y + my * step
            if self.can_move_to(nx, ny, obstacles):
                self.x, self.y = nx, ny
                self.stuck_timer = 0.0
                return False
        self.stuck_timer += dt / 1000.0
        return False

    def update(self, dt, obstacles, game_time_hour=None):
        if self.is_talking:
            return

        if game_time_hour is not None:
            self.update_home_state(game_time_hour, obstacles)

        seconds = max(0.001, dt / 1000.0)

        # At night, every NPC goes to their assigned house and stays there.
        if self.is_home:
            if self.house is None:
                self.is_home = False
            else:
                arrived = self._move_toward(self.home_target_x, self.home_target_y, dt, obstacles)
                if arrived:
                    self.home_reached = True
                    self.x = self.home_target_x
                    self.y = self.home_target_y
                self.sync_rect()
                return

        self.wait_timer -= seconds
        if self.wait_timer > 0:
            return

        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = math.hypot(dx, dy)
        if dist < 10:
            self.wait_timer = random.uniform(0.15, 0.7)
            self.stuck_timer = 0.0
            self.choose_new_destination(obstacles)
            self.sync_rect()
            return

        arrived = self._move_toward(self.target_x, self.target_y, dt, obstacles)
        if arrived:
            self.wait_timer = random.uniform(0.15, 0.7)
            self.choose_new_destination(obstacles)
        elif self.stuck_timer > 0.35:
            self.choose_new_destination(obstacles)
            self.stuck_timer = 0.0
            self.wait_timer = 0.0

        self.sync_rect()

    def draw(self, screen, camera, game):
        super().draw(screen, camera)
        sx, sy = camera.world_to_screen(self.x, self.y)
        name_surface = game.small_font.render(self.name, True, (255, 255, 255))
        name_rect = name_surface.get_rect(center=(sx + self.rect.width // 2, sy - 14))
        pygame.draw.rect(screen, (70, 55, 90), name_rect.inflate(10, 5), border_radius=8)
        screen.blit(name_surface, name_rect)
        marker = game.get_npc_marker(self)
        if marker:
            marker_surface = game.title_font.render(marker, True, (255, 230, 100))
            marker_rect = marker_surface.get_rect(center=(sx + self.rect.width // 2, sy - 48))
            screen.blit(marker_surface, marker_rect)

        if self.is_home:
            home_text = "HOME" if self.home_reached else "GOING HOME"
            home_surface = game.tiny_font.render(home_text, True, (190, 230, 255))
            home_rect = home_surface.get_rect(center=(sx + self.rect.width // 2, sy + 10))
            bg = home_rect.inflate(10, 4)
            pygame.draw.rect(screen, (45, 65, 95), bg, border_radius=7)
            screen.blit(home_surface, home_rect)


# ================================================================
# GAME
# ================================================================

# ================================================================
# SAVE MANAGER
# ================================================================

class SaveManager:
    def __init__(self):
        self.path = os.path.join(PROJECT_DIR, "data", "savegame.json")

    def has_save(self):
        return os.path.isfile(self.path)

    def save(self, data):
        try:
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            temp = self.path + ".tmp"
            with open(temp, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            os.replace(temp, self.path)
            return True
        except (OSError, TypeError, ValueError) as exc:
            print(f"[SAVE] Failed: {exc}")
            return False

    def load(self):
        if not self.has_save():
            return None
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"[SAVE] Load failed: {exc}")
            return None


class Game:

    def __init__(self, screen):

        self.screen = screen

        self.running = True
        self.save_manager = SaveManager()

        # --------------------------------------------------------
        # IMPORTANT:
        # Game now starts at MAIN MENU.
        # --------------------------------------------------------

        self.state = "main_menu"

        self.player = None
        self.companion = None

        self.camera = Camera()

        self.obstacles = []
        self.flowers = []
        self.quest_items = []
        self.quest_locations = []
        self.npcs = []
        self.quests = []

        self.coins = 0

        # In-game clock: starts at 08:00 and loops through a full day.
        self.game_time_ms = (8 * 60 / 24) * GAME_DAY_LENGTH_MS
        self.selected_character = None

        # --------------------------------------------------------
        # Main menu
        # --------------------------------------------------------

        self.main_menu_selected = 0

        self.main_menu_options = []
        self.refresh_main_menu_options()

        self.menu_sparkles = []

        for _ in range(80):

            self.menu_sparkles.append(
                {
                    "x": random.randint(
                        0,
                        SCREEN_WIDTH
                    ),
                    "y": random.randint(
                        0,
                        SCREEN_HEIGHT
                    ),
                    "speed": random.uniform(
                        0.2,
                        0.8
                    ),
                    "size": random.randint(
                        1,
                        4
                    ),
                    "phase": random.uniform(
                        0,
                        math.pi * 2
                    )
                }
            )

        self.menu_time = 0

        # Animation phase used by the quest navigator target pulse.
        self.phase = 0.0

        # --------------------------------------------------------
        # Dialogue
        # --------------------------------------------------------

        self.dialogue_npc = None
        self.dialogue_lines = []
        self.dialogue_index = 0

        # --------------------------------------------------------
        # Quest offer
        # --------------------------------------------------------

        self.pending_quest = None
        self.quest_offer_ready = False

        # --------------------------------------------------------
        # Quest tabs
        # --------------------------------------------------------

        self.quest_tab = 0

        self.quest_tab_names = [
            "ACTIVE",
            "AVAILABLE",
            "COMPLETED",
            "LOCKED"
        ]

        self.quest_scroll = [
            0,
            0,
            0,
            0
        ]

        self.quest_content_height = [
            0,
            0,
            0,
            0
        ]

        # --------------------------------------------------------
        # Quest navigator
        # --------------------------------------------------------

        self.navigator_enabled = False
        self.navigator_quest_index = 0
        self.navigator_quest_id = None

        # Quest details screen.
        self.selected_quest = None

        # Relationship menu.
        self.relationship_scroll = 0

        # --------------------------------------------------------
        # Notification
        # --------------------------------------------------------

        self.notification_text = ""
        self.notification_timer = 0

        # --------------------------------------------------------
        # Fonts
        # --------------------------------------------------------

        self.title_font = pygame.font.SysFont(
            "arial",
            30,
            bold=True
        )

        self.large_font = pygame.font.SysFont(
            "arial",
            24,
            bold=True
        )

        self.font = pygame.font.SysFont(
            "arial",
            20
        )

        self.small_font = pygame.font.SysFont(
            "arial",
            16
        )

        self.tiny_font = pygame.font.SysFont(
            "arial",
            14
        )

        self.generate_world()
        self.create_quests()

    # ============================================================
    # WORLD
    # ============================================================

    def generate_world(self):

        random.seed(42)

        # Fixed fence areas are reserved before generating trees so trees
        # never grow through the fences.
        fence_layout = [
            (350, 850, 300, 20),
            (2100, 1200, 350, 20),
            (1200, 1900, 300, 20),
            (2800, 1700, 300, 20),
        ]
        fence_rects = [pygame.Rect(x, y, w, h) for x, y, w, h in fence_layout]

        # Generate trees with generous 3D clearance.  The rendered canopy
        # extends well beyond the 70x90 collision footprint, so spacing is
        # based on an enlarged reservation rectangle rather than just the
        # trunk collision box.
        placed_tree_reservations = []
        for _ in range(75):
            placed = False

            for _attempt in range(180):
                x = random.randint(130, WORLD_WIDTH - 190)
                y = random.randint(150, WORLD_HEIGHT - 200)

                # The collision box is the trunk/base. The reservation is
                # intentionally much larger because the 3D canopy, branches
                # and ground shadow extend beyond the trunk.
                tree_rect = pygame.Rect(x, y, 78, 104)
                reserved = tree_rect.inflate(175, 165)

                # Keep the visible 3D canopy away from fences.
                if any(reserved.colliderect(fr.inflate(55, 55)) for fr in fence_rects):
                    continue

                # Keep neighboring trees separated so their canopies and
                # ground shadows do not visually merge.
                if any(reserved.colliderect(other) for other in placed_tree_reservations):
                    continue

                # Keep trees away from the player starting area.
                if reserved.colliderect(pygame.Rect(150, 150, 260, 220)):
                    continue

                self.obstacles.append(Obstacle(x, y, 78, 104, "tree"))
                placed_tree_reservations.append(reserved)
                placed = True
                break

            if not placed:
                continue

        # Five distinct fairy homes placed around the world.
        # Each house uses the same collision footprint but a different
        # visual style so the world feels like a real fairy village.
        houses = [
            (500, 500, "mushroom"),
            (1800, 700, "flower"),
            (2900, 500, "crystal"),
            (900, 2200, "treehouse"),
            (3000, 2200, "pond"),
        ]

        # Place houses only in clear areas.  The visible house artwork is
        # larger than its collision rectangle, so we reserve extra space
        # around every house to keep nearby trees from visually overlapping it.
        placed_houses = []

        house_owners = {
            "mushroom": "Lumi",
            "flower": "Pipi",
            "crystal": "Coco",
            "treehouse": "Ruru",
            "pond": "Nana",
        }

        for original_x, original_y, style in houses:
            house_w = 170
            house_h = 130
            chosen = None

            # Try the requested position first, then search outward in a
            # deterministic spiral/grid pattern for a clear location.
            candidates = [(original_x, original_y)]
            for radius in range(100, 701, 100):
                for ox, oy in (
                    (radius, 0), (-radius, 0),
                    (0, radius), (0, -radius),
                    (radius, radius), (-radius, radius),
                    (radius, -radius), (-radius, -radius),
                ):
                    candidates.append((original_x + ox, original_y + oy))

            for cx, cy in candidates:
                if cx < 100 or cy < 100:
                    continue
                if cx + house_w > WORLD_WIDTH - 100:
                    continue
                if cy + house_h > WORLD_HEIGHT - 100:
                    continue

                test_rect = pygame.Rect(cx, cy, house_w, house_h)

                # Extra clearance is intentional because some roofs,
                # branches and decorations extend beyond self.rect.
                reserved = test_rect.inflate(95, 85)

                blocked = False
                for obstacle in self.obstacles:
                    if reserved.colliderect(obstacle.rect):
                        blocked = True
                        break

                if not blocked:
                    for other in placed_houses:
                        if reserved.colliderect(other.inflate(95, 85)):
                            blocked = True
                            break

                if not blocked:
                    chosen = (cx, cy)
                    break

            if chosen is None:
                # Extremely unlikely fallback: use the requested position.
                chosen = (original_x, original_y)

            hx, hy = chosen
            house = Obstacle(
                hx,
                hy,
                house_w,
                house_h,
                "house",
                style
            )
            house.owner = house_owners.get(style, "Fairy")
            self.obstacles.append(house)
            placed_houses.append(house.rect.copy())

        # Pebbles/rocks are placed only where they do not overlap trees,
        # houses, fences, or other rocks. This prevents rocks from appearing
        # inside tree trunks or under buildings.
        for _ in range(35):
            for _attempt in range(60):
                x = random.randint(100, WORLD_WIDTH - 150)
                y = random.randint(100, WORLD_HEIGHT - 120)
                rock_rect = pygame.Rect(x, y, 70, 45)

                # Check all existing obstacles AND the reserved fence
                # rectangles. Fences are added to self.obstacles later, so
                # they must be checked explicitly here as well. The extra
                # clearance keeps the pebble artwork from touching fence posts.
                blocked = any(
                    rock_rect.inflate(24, 24).colliderect(obstacle.rect)
                    for obstacle in self.obstacles
                )

                if not blocked:
                    blocked = any(
                        rock_rect.inflate(24, 24).colliderect(fence_rect.inflate(18, 18))
                        for fence_rect in fence_rects
                    )

                if not blocked:
                    self.obstacles.append(
                        Obstacle(x, y, 70, 45, "rock")
                    )
                    break

        # Add the reserved fences after tree/house/rock placement.  Their
        # positions were already reserved during tree generation, and houses
        # also check against the actual obstacle list when placed.
        for x, y, w, h in fence_layout:
            self.obstacles.append(
                Obstacle(x, y, w, h, "fence")
            )

        for i in range(180):

            for _attempt in range(50):

                x = random.randint(
                    80,
                    WORLD_WIDTH - 80
                )

                y = random.randint(
                    80,
                    WORLD_HEIGHT - 80
                )

                rect = pygame.Rect(
                    x - 8,
                    y - 8,
                    16,
                    16
                )

                blocked = any(
                    rect.colliderect(
                        obstacle.rect.inflate(
                            30,
                            30
                        )
                    )
                    for obstacle in self.obstacles
                )

                if not blocked:

                    self.flowers.append(
                        Flower(
                            x,
                            y,
                            i
                        )
                    )

                    break

        self.quest_locations = [

            QuestLocation(
                "flower_meadow",
                "Flower Meadow",
                1250,
                650,
                100
            ),

            QuestLocation(
                "ancient_grove",
                "Ancient Grove",
                1900,
                500,
                100
            ),

            QuestLocation(
                "fairy_lake",
                "Fairy Lake",
                3200,
                900,
                110
            ),

            QuestLocation(
                "crystal_cave",
                "Crystal Cave",
                3350,
                1900,
                110
            ),

            QuestLocation(
                "star_shrine",
                "Star Shrine",
                2200,
                2500,
                100
            ),

            QuestLocation(
                "garden",
                "Fairy Garden",
                900,
                2500,
                100
            ),

            QuestLocation(
                "forest_pond",
                "Forest Pond",
                2600,
                2700,
                100
            )
        ]

        self.quest_items = [

            QuestItem(
                700,
                1300,
                "ribbon",
                "Pink Ribbon"
            ),

            QuestItem(
                950,
                1450,
                "ribbon",
                "Pink Ribbon"
            ),

            QuestItem(
                1200,
                1250,
                "ribbon",
                "Pink Ribbon"
            ),

            QuestItem(
                1500,
                2100,
                "seed",
                "Magical Seed"
            ),

            QuestItem(
                1700,
                2250,
                "seed",
                "Magical Seed"
            ),

            QuestItem(
                1900,
                2050,
                "seed",
                "Magical Seed"
            ),

            QuestItem(
                2050,
                2350,
                "seed",
                "Magical Seed"
            ),

            QuestItem(
                3300,
                1850,
                "crystal",
                "Fairy Crystal"
            ),

            QuestItem(
                3500,
                2050,
                "crystal",
                "Fairy Crystal"
            ),

            QuestItem(
                3200,
                2150,
                "crystal",
                "Fairy Crystal"
            ),

            QuestItem(
                3000,
                1950,
                "crystal",
                "Fairy Crystal"
            ),

            QuestItem(
                2200,
                2500,
                "lost_star",
                "Lost Star"
            )
        ]

        self.npcs = [

            FairyNPC(
                "Lumi",
                "lumi.png",
                2300,
                1300,
                [
                    "Hi there! I'm Lumi!",
                    "I've been exploring this magical forest all morning.",
                    "There are so many mysterious places around here.",
                    "I could really use your help!"
                ],
                300
            ),

            FairyNPC(
                "Pipi",
                "mepple.png",
                800,
                800,
                [
                    "Hello!",
                    "I was carrying something very important earlier.",
                    "But now I can't remember where I dropped it.",
                    "Could you help me look around?"
                ],
                220
            ),

            FairyNPC(
                "Coco",
                "mipple.png",
                1500,
                1700,
                [
                    "Welcome to the magical forest!",
                    "I love growing magical plants.",
                    "But my supply of magical seeds is running low."
                ],
                250
            ),

            FairyNPC(
                "Ruru",
                "lumi.png",
                3100,
                1100,
                [
                    "Hi!",
                    "There are mysterious crystals hidden in the forest.",
                    "I wonder what secrets they contain..."
                ],
                260
            ),

            FairyNPC(
                "Nana",
                "lumi.png",
                1000,
                2500,
                [
                    "Good morning!",
                    "Have you explored the eastern forest yet?",
                    "There is a peaceful pond hidden among the trees."
                ],
                240
            )
        ]

        # Ensure every fairy starts completely outside the visual footprint
        # of trees, fences and houses. If a fixed NPC spawn is too close,
        # move it to the nearest safe point around its original location.
        for npc in self.npcs:
            if not npc.can_move_to(npc.x, npc.y, self.obstacles):
                found = False
                for radius in (50, 80, 110, 140, 180, 220):
                    for angle_deg in range(0, 360, 15):
                        angle = math.radians(angle_deg)
                        nx = clamp(npc.spawn_x + math.cos(angle) * radius, 100, WORLD_WIDTH - 130)
                        ny = clamp(npc.spawn_y + math.sin(angle) * radius, 100, WORLD_HEIGHT - 130)
                        if npc.can_move_to(nx, ny, self.obstacles):
                            npc.x = nx
                            npc.y = ny
                            npc.sync_rect()
                            npc.spawn_x = nx
                            npc.spawn_y = ny
                            npc.choose_new_destination(self.obstacles)
                            found = True
                            break
                    if found:
                        break

    # ============================================================
    # QUEST CREATION
    # ============================================================

    def create_quests(self):

        self.quests = [

            Quest(
                "lumi_001",
                "Magical Flower Gathering",
                "Collect 5 magical flowers for Lumi.",
                "flower",
                5,
                50,
                "Lumi",
                "lumi_chain",
                1
            ),

            Quest(
                "lumi_002",
                "Explore the Fairy Forest",
                "Visit the Flower Meadow, Ancient Grove and Fairy Lake.",
                "location",
                3,
                75,
                "Lumi",
                "lumi_chain",
                2,
                prerequisite="lumi_001",
                target_ids=[
                    "flower_meadow",
                    "ancient_grove",
                    "fairy_lake"
                ]
            ),

            Quest(
                "lumi_003",
                "Find the Lost Star",
                "Find the mysterious Lost Star.",
                "item",
                1,
                100,
                "Lumi",
                "lumi_chain",
                3,
                prerequisite="lumi_002",
                item_type="lost_star"
            ),

            Quest(
                "pipi_001",
                "Find My Missing Ribbons",
                "Find 3 ribbons that Pipi lost around the forest.",
                "item",
                3,
                40,
                "Pipi",
                "pipi_chain",
                1,
                item_type="ribbon"
            ),

            Quest(
                "pipi_002",
                "A Ribbon for the Fairy Festival",
                "Tell Coco about Pipi's ribbon.",
                "talk",
                1,
                60,
                "Pipi",
                "pipi_chain",
                2,
                prerequisite="pipi_001",
                target_npc="Coco"
            ),

            Quest(
                "coco_001",
                "Gather Magical Seeds",
                "Collect 4 magical seeds.",
                "item",
                4,
                50,
                "Coco",
                "coco_chain",
                1,
                item_type="seed"
            ),

            Quest(
                "coco_002",
                "Restore the Fairy Garden",
                "Visit three important places to restore the fairy garden.",
                "location",
                3,
                80,
                "Coco",
                "coco_chain",
                2,
                prerequisite="coco_001",
                target_ids=[
                    "garden",
                    "fairy_lake",
                    "ancient_grove"
                ]
            ),

            Quest(
                "ruru_001",
                "Crystal Hunt",
                "Collect 4 mysterious fairy crystals.",
                "item",
                4,
                70,
                "Ruru",
                "ruru_chain",
                1,
                item_type="crystal"
            ),

            Quest(
                "ruru_002",
                "The Crystal Mystery",
                "Investigate the Crystal Cave.",
                "location",
                1,
                100,
                "Ruru",
                "ruru_chain",
                2,
                prerequisite="ruru_001",
                target_ids=[
                    "crystal_cave"
                ]
            ),

            Quest(
                "nana_001",
                "Visit the Forest Pond",
                "Find the peaceful Forest Pond.",
                "location",
                1,
                45,
                "Nana",
                "nana_chain",
                1,
                target_ids=[
                    "forest_pond"
                ]
            ),

            Quest(
                "nana_002",
                "Tell Pipi About the Pond",
                "Tell Pipi what you discovered at the pond.",
                "talk",
                1,
                65,
                "Nana",
                "nana_chain",
                2,
                prerequisite="nana_001",
                target_npc="Pipi"
            )
        ]

        for npc in self.npcs:

            npc.quest_ids = [
                quest.quest_id
                for quest in self.quests
                if quest.giver_name == npc.name
            ]

    # ============================================================
    # QUEST STATUS
    # ============================================================

    def get_quest_by_id(
        self,
        quest_id
    ):

        for quest in self.quests:

            if quest.quest_id == quest_id:
                return quest

        return None

    def is_quest_unlocked(
        self,
        quest
    ):

        if quest.prerequisite is None:
            return True

        prerequisite = self.get_quest_by_id(
            quest.prerequisite
        )

        if prerequisite is None:
            return False

        return prerequisite.completed

    def get_quest_status(
        self,
        quest
    ):

        if quest.completed:
            return "COMPLETED"

        if quest.accepted:
            return "ACTIVE"

        if not self.is_quest_unlocked(
            quest
        ):
            return "LOCKED"

        return "AVAILABLE"

    def get_active_quests(self):

        return [
            quest
            for quest in self.quests
            if self.get_quest_status(quest)
            == "ACTIVE"
        ]

    def get_available_quests(self):

        return [
            quest
            for quest in self.quests
            if self.get_quest_status(quest)
            == "AVAILABLE"
        ]

    def get_completed_quests(self):

        return [
            quest
            for quest in self.quests
            if self.get_quest_status(quest)
            == "COMPLETED"
        ]

    def get_locked_quests(self):

        return [
            quest
            for quest in self.quests
            if self.get_quest_status(quest)
            == "LOCKED"
        ]

    # ============================================================
    # NPC QUEST
    # ============================================================

    def get_npc_quest(
        self,
        npc
    ):

        npc_quests = [
            quest
            for quest in self.quests
            if quest.giver_name == npc.name
        ]

        for quest in npc_quests:

            if self.get_quest_status(
                quest
            ) == "ACTIVE":

                return quest

        for quest in npc_quests:

            if self.get_quest_status(
                quest
            ) == "AVAILABLE":

                return quest

        return None

    def get_npc_marker(
        self,
        npc
    ):

        quest = self.get_npc_quest(
            npc
        )

        if quest is None:
            return ""

        status = self.get_quest_status(
            quest
        )

        if status == "AVAILABLE":
            return "!"

        if status == "ACTIVE":

            if quest.is_finished():
                return "?"

            return "..."

        return ""

    # ============================================================
    # QUEST NAVIGATOR
    # ============================================================

    def get_navigator_quest(self):

        active_quests = self.get_active_quests()

        if not active_quests:
            return None

        if self.navigator_quest_id is not None:
            for quest in active_quests:
                if quest.quest_id == self.navigator_quest_id:
                    return quest

        self.navigator_quest_index = int(
            clamp(
                self.navigator_quest_index,
                0,
                len(active_quests) - 1
            )
        )

        return active_quests[
            self.navigator_quest_index
        ]

    def get_navigator_npc(self):

        quest = self.get_navigator_quest()

        if quest is None:
            return None

        target_name = quest.giver_name

        if (
            quest.objective_type == "talk"
            and quest.target_npc
        ):
            target_name = quest.target_npc

        for npc in self.npcs:
            if npc.name == target_name:
                return npc

        return None

    def get_navigator_npc_for_quest(self, quest):
        if quest is None:
            return None

        # IMPORTANT:
        # For a TALK quest, the objective NPC is the destination while
        # the objective is still incomplete. Once the player has talked
        # to that NPC and the objective reaches the required progress,
        # navigation must switch back to the quest giver.
        target_name = quest.giver_name

        if (
            not quest.is_finished()
            and quest.objective_type == "talk"
            and quest.target_npc
        ):
            target_name = quest.target_npc

        for npc in self.npcs:
            if npc.name == target_name:
                return npc

        return None

    def get_navigator_target(self, quest):
        """
        Return the current world target for a quest.

        While an objective is unfinished, navigate to the next relevant
        flower/item/location. Once the objective is finished, automatically
        switch the target back to the quest NPC.

        Returns:
            (target_object, target_type, display_name)
        """
        if quest is None:
            return None, None, None

        # Once the objective is complete, return to the quest NPC.
        if quest.is_finished():
            npc = self.get_navigator_npc_for_quest(quest)
            if npc:
                return npc, "npc", npc.name
            return None, None, None

        # Flower quests: find the nearest uncollected magical flower.
        if quest.objective_type == "flower":
            candidates = [
                flower
                for flower in self.flowers
                if not flower.collected
            ]

            if candidates and self.player:
                target = min(
                    candidates,
                    key=lambda flower: distance(
                        self.player.x,
                        self.player.y,
                        flower.x,
                        flower.y
                    )
                )
                return target, "flower", "Magical Flower"

            if candidates:
                return candidates[0], "flower", "Magical Flower"

        # Item quests: find the nearest remaining item of the required type.
        if quest.objective_type == "item":
            candidates = [
                item
                for item in self.quest_items
                if (
                    not item.collected
                    and item.item_type == quest.item_type
                )
            ]

            if candidates and self.player:
                target = min(
                    candidates,
                    key=lambda item: distance(
                        self.player.x,
                        self.player.y,
                        item.x,
                        item.y
                    )
                )
                return target, "item", target.name

            if candidates:
                return candidates[0], "item", candidates[0].name

        # Location quests: navigate to the next location not yet visited.
        if quest.objective_type == "location":
            candidates = [
                location
                for location in self.quest_locations
                if (
                    location.location_id in quest.target_ids
                    and location.location_id
                    not in quest.visited_targets
                )
            ]

            if candidates and self.player:
                target = min(
                    candidates,
                    key=lambda location: distance(
                        self.player.x,
                        self.player.y,
                        location.x,
                        location.y
                    )
                )
                return target, "location", target.name

            if candidates:
                return candidates[0], "location", candidates[0].name

        # TALK objectives should always navigate directly to the NPC.
        if quest.objective_type == "talk":
            npc = self.get_navigator_npc_for_quest(quest)
            if npc:
                return npc, "npc", npc.name

        # Fallback to the quest giver if no objective target can be found.
        npc = self.get_navigator_npc_for_quest(quest)
        if npc:
            return npc, "npc", npc.name

        return None, None, None

    def toggle_navigator(self):

        active_quests = self.get_active_quests()

        if not active_quests:

            self.navigator_enabled = False
            self.show_notification(
                "No active quest to navigate."
            )
            return

        if not self.navigator_enabled:

            self.navigator_quest_index = 0
            self.navigator_quest_id = active_quests[0].quest_id
            self.navigator_enabled = True

            quest = self.get_navigator_quest()
            npc = self.get_navigator_npc()

            if npc and quest:
                self.show_notification(
                    f"Navigator: {npc.name} - {quest.title}"
                )
            return

        # Press N again to cycle through active quests.
        self.navigator_quest_index = (
            self.navigator_quest_index + 1
        ) % len(active_quests)
        self.navigator_quest_id = active_quests[
            self.navigator_quest_index
        ].quest_id

        quest = self.get_navigator_quest()
        npc = self.get_navigator_npc()

        if npc and quest:
            self.show_notification(
                f"Navigator: {npc.name} - {quest.title}"
            )

    def draw_navigator(self):

        if not self.navigator_enabled:
            return

        if not self.player:
            return

        active_quests = self.get_active_quests()

        if not active_quests:
            self.navigator_enabled = False
            return

        if self.navigator_quest_index >= len(active_quests):
            self.navigator_quest_index = 0

        quest = self.get_navigator_quest()
        target, target_type, target_name = self.get_navigator_target(quest)

        if quest is None or target is None:
            return

        target_x = target.x
        target_y = target.y

        # NPCs and fairies use their sprite center; world objects use their
        # own coordinates.
        if hasattr(target, "rect"):
            target_x += target.rect.width / 2
            target_y += target.rect.height / 2

        player_x = self.player.x + self.player.rect.width / 2
        player_y = self.player.y + self.player.rect.height / 2

        dx = target_x - player_x
        dy = target_y - player_y
        target_distance = math.hypot(dx, dy)

        banner = pygame.Rect(
            SCREEN_WIDTH // 2 - 210,
            120,
            420,
            72
        )

        pygame.draw.rect(
            self.screen,
            (55, 45, 75),
            banner,
            border_radius=16
        )

        pygame.draw.rect(
            self.screen,
            (255, 225, 130),
            banner,
            2,
            border_radius=16
        )

        if target_type == "npc":
            header = f"RETURN TO {target_name}" if quest.is_finished() else f"NAVIGATE TO {target_name}"
        elif target_type == "flower":
            header = "NAVIGATE TO MAGICAL FLOWER"
        elif target_type == "item":
            header = f"NAVIGATE TO {target_name.upper()}"
        else:
            header = f"NAVIGATE TO {target_name.upper()}"

        title = self.font.render(
            header,
            True,
            (255, 235, 150)
        )
        self.screen.blit(
            title,
            title.get_rect(
                center=(banner.centerx, banner.y + 22)
            )
        )

        progress_text = (
            f"{int(target_distance)}m   •   "
            f"{quest.progress}/{quest.required_amount}   •   "
            f"{quest.title}"
        )
        distance_text = self.small_font.render(
            progress_text,
            True,
            (240, 235, 250)
        )
        self.screen.blit(
            distance_text,
            distance_text.get_rect(
                center=(banner.centerx, banner.y + 49)
            )
        )

        angle = math.atan2(dy, dx)
        center = (SCREEN_WIDTH // 2, 205)
        arrow_length = 30
        arrow_width = 15

        tip = (
            center[0] + int(math.cos(angle) * arrow_length),
            center[1] + int(math.sin(angle) * arrow_length)
        )
        left = (
            center[0] + int(math.cos(angle + 2.45) * arrow_width),
            center[1] + int(math.sin(angle + 2.45) * arrow_width)
        )
        right = (
            center[0] + int(math.cos(angle - 2.45) * arrow_width),
            center[1] + int(math.sin(angle - 2.45) * arrow_width)
        )

        pygame.draw.polygon(
            self.screen,
            (255, 225, 100),
            [tip, left, right]
        )
        pygame.draw.circle(
            self.screen,
            (255, 255, 255),
            center,
            4
        )

        # Highlight the current target when it is visible.
        sx, sy = self.camera.world_to_screen(
            target_x,
            target_y
        )

        if (
            -80 <= sx <= SCREEN_WIDTH + 80
            and -80 <= sy <= SCREEN_HEIGHT + 80
        ):
            pulse = int(
                5 + abs(math.sin(self.phase * 2)) * 8
            )

            pygame.draw.circle(
                self.screen,
                (255, 225, 100),
                (int(sx), int(sy)),
                25 + pulse,
                3
            )

            target_text = self.small_font.render(
                f"TARGET: {target_name}",
                True,
                (255, 240, 170)
            )
            target_rect = target_text.get_rect(
                center=(int(sx), int(sy) - 42)
            )
            target_bg = target_rect.inflate(18, 10)

            pygame.draw.rect(
                self.screen,
                (55, 45, 75),
                target_bg,
                border_radius=8
            )
            self.screen.blit(
                target_text,
                target_rect
            )

    # ============================================================
    # CHARACTER SELECT
    # ============================================================

    def find_safe_spawn(self):

        candidates = [
            (700, 1000),
            (750, 1100),
            (650, 1050),
            (800, 1050),
            (600, 1000)
        ]

        for x, y in candidates:

            rect = pygame.Rect(
                x,
                y,
                44,
                60
            )

            blocked = any(
                rect.colliderect(
                    obstacle.rect.inflate(
                        20,
                        20
                    )
                )
                for obstacle in self.obstacles
            )

            if not blocked:
                return x, y

        return 700, 1000

    # ============================================================
    # SAVE / LOAD
    # ============================================================

    def refresh_main_menu_options(self):
        if self.save_manager.has_save():
            self.main_menu_options = ["CONTINUE", "START ADVENTURE", "QUIT GAME"]
        else:
            self.main_menu_options = ["START ADVENTURE", "QUIT GAME"]
        self.main_menu_selected = int(clamp(self.main_menu_selected, 0, len(self.main_menu_options) - 1))

    def build_save_data(self):
        if self.player is None or self.selected_character is None:
            return None
        return {
            "version": 1,
            "selected_character": self.selected_character,
            "coins": self.coins,
            "game_time_ms": self.game_time_ms,
            "player": {"x": self.player.x, "y": self.player.y},
            "companion": ({"x": self.companion.x, "y": self.companion.y} if self.companion else None),
            "flowers": [bool(f.collected) for f in self.flowers],
            "quest_items": [bool(i.collected) for i in self.quest_items],
            "npcs": [{"name": n.name, "x": n.x, "y": n.y, "friendship": n.friendship} for n in self.npcs],
            "quests": [{"quest_id": q.quest_id, "progress": q.progress, "accepted": q.accepted, "completed": q.completed, "reward_claimed": q.reward_claimed, "visited_targets": list(q.visited_targets)} for q in self.quests],
            "navigator": {"enabled": self.navigator_enabled, "quest_id": self.navigator_quest_id}
        }

    def save_game(self, silent=False):
        data = self.build_save_data()
        if data is None:
            if not silent:
                self.show_notification("There is no active adventure to save.")
            return False
        if self.save_manager.save(data):
            self.refresh_main_menu_options()
            if not silent:
                self.show_notification("Game saved successfully!")
            print("[SAVE] Game saved successfully.")
            return True
        if not silent:
            self.show_notification("Unable to save the game.")
        return False

    def load_game(self):
        data = self.save_manager.load()
        if not data:
            self.show_notification("No save game found.")
            return False
        try:
            self.obstacles = []
            self.flowers = []
            self.quest_items = []
            self.quest_locations = []
            self.npcs = []
            self.quests = []
            self.generate_world()
            self.create_quests()

            character = data.get("selected_character", "Mepple")
            pdata = data.get("player", {})
            px, py = float(pdata.get("x", 500)), float(pdata.get("y", 1000))
            if character == "Mipple":
                self.player = Fairy("Mipple", "mipple.png", px, py)
                companion_name, companion_image = "Mepple", "mepple.png"
            else:
                self.player = Fairy("Mepple", "mepple.png", px, py)
                companion_name, companion_image = "Mipple", "mipple.png"
            cdata = data.get("companion") or {}
            self.companion = PartyFairy(companion_name, companion_image, float(cdata.get("x", px - 80)), float(cdata.get("y", py)))
            self.selected_character = character
            self.coins = int(data.get("coins", 0))
            self.game_time_ms = float(data.get("game_time_ms", (8 * 60 / 24) * GAME_DAY_LENGTH_MS)) % GAME_DAY_LENGTH_MS

            for i, value in enumerate(data.get("flowers", [])):
                if i < len(self.flowers): self.flowers[i].collected = bool(value)
            for i, value in enumerate(data.get("quest_items", [])):
                if i < len(self.quest_items): self.quest_items[i].collected = bool(value)

            npc_by_name = {n.name: n for n in self.npcs}
            for saved in data.get("npcs", []):
                npc = npc_by_name.get(saved.get("name"))
                if npc:
                    npc.x = float(saved.get("x", npc.x)); npc.y = float(saved.get("y", npc.y)); npc.sync_rect(); npc.target_x = npc.x; npc.target_y = npc.y
                    npc.friendship = int(clamp(saved.get("friendship", 0), 0, npc.friendship_max))

            quest_by_id = {q.quest_id: q for q in self.quests}
            for saved in data.get("quests", []):
                q = quest_by_id.get(saved.get("quest_id"))
                if not q: continue
                q.progress = min(int(saved.get("progress", 0)), q.required_amount)
                q.accepted = bool(saved.get("accepted", False)); q.completed = bool(saved.get("completed", False)); q.reward_claimed = bool(saved.get("reward_claimed", False)); q.visited_targets = set(saved.get("visited_targets", []))

            nav = data.get("navigator", {})
            self.navigator_enabled = bool(nav.get("enabled", False)); self.navigator_quest_id = nav.get("quest_id"); self.navigator_quest_index = 0
            if self.navigator_quest_id:
                for index, q in enumerate(self.get_active_quests()):
                    if q.quest_id == self.navigator_quest_id:
                        self.navigator_quest_index = index; break
                else:
                    self.navigator_enabled = False; self.navigator_quest_id = None

            self.pending_quest = None; self.quest_offer_ready = False; self.dialogue_npc = None; self.dialogue_lines = []; self.dialogue_index = 0; self.selected_quest = None
            self.state = "playing"
            self.camera.update(self.player.rect)
            self.show_notification("Game loaded successfully!")
            print("[SAVE] Game loaded successfully.")
            return True
        except (TypeError, ValueError, KeyError) as exc:
            print(f"[SAVE] Invalid save data: {exc}")
            self.show_notification("The save game could not be loaded.")
            return False

    def start_new_adventure(self, character):
        # START ADVENTURE is a completely fresh game. Do not reuse any
        # runtime progress from the previous adventure, and remove the
        # previous save so CONTINUE cannot load the old adventure.
        self.obstacles = []
        self.flowers = []
        self.quest_items = []
        self.quest_locations = []
        self.npcs = []
        self.quests = []

        self.coins = 0
        self.game_time_ms = (8 * 60 / 24) * GAME_DAY_LENGTH_MS
        self.selected_character = None

        self.navigator_enabled = False
        self.navigator_quest_id = None
        self.navigator_quest_index = 0
        self.selected_quest = None

        self.dialogue_npc = None
        self.dialogue_lines = []
        self.dialogue_index = 0
        self.pending_quest = None
        self.quest_offer_ready = False

        # Reset quest tabs/scroll position.
        self.quest_tab = 0
        self.quest_scroll = [0, 0, 0, 0]

        # Build a brand-new world and brand-new NPC objects. Their
        # friendship values therefore start at 0 again.
        self.generate_world()
        self.create_quests()

        # This game uses one save slot. Starting a new adventure replaces
        # the old save slot so CONTINUE can never restore the previous run.
        try:
            if self.save_manager.has_save():
                os.remove(self.save_manager.path)
                print("[SAVE] Old save removed for new adventure.")
        except OSError as exc:
            print(f"[SAVE] Could not remove old save: {exc}")

        self.start_adventure(character)

    def start_adventure(
        self,
        character
    ):

        self.selected_character = character
        self.navigator_enabled = False
        self.navigator_quest_id = None
        self.navigator_quest_index = 0
        self.selected_quest = None

        x, y = self.find_safe_spawn()

        if character == "Mepple":

            self.player = Fairy(
                "Mepple",
                "mepple.png",
                x,
                y
            )

            self.companion = PartyFairy(
                "Mipple",
                "mipple.png",
                x - 80,
                y
            )

        else:

            self.player = Fairy(
                "Mipple",
                "mipple.png",
                x,
                y
            )

            self.companion = PartyFairy(
                "Mepple",
                "mepple.png",
                x - 80,
                y
            )

        self.camera.update(
            self.player.rect
        )

        self.state = "playing"

        self.show_notification(
            f"{character} joined the adventure!"
        )

    # ============================================================
    # EVENT HANDLING
    # ============================================================

    def handle_event(
        self,
        event
    ):

        global SCREEN_WIDTH
        global SCREEN_HEIGHT

        if event.type == pygame.QUIT:

            self.running = False
            return

        if event.type == pygame.VIDEORESIZE:

            SCREEN_WIDTH = max(
                800,
                event.w
            )

            SCREEN_HEIGHT = max(
                600,
                event.h
            )

            self.screen = pygame.display.set_mode(
                (
                    SCREEN_WIDTH,
                    SCREEN_HEIGHT
                ),
                pygame.RESIZABLE
            )

            return

        # ========================================================
        # MAIN MENU
        # ========================================================

        if self.state == "main_menu":

            self.handle_main_menu_event(
                event
            )

            return

        # ========================================================
        # CHARACTER SELECT
        # ========================================================

        if self.state == "character_select":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    self.state = "main_menu"

                elif event.key == pygame.K_1:

                    self.start_new_adventure(
                        "Mepple"
                    )

                elif event.key == pygame.K_2:

                    self.start_new_adventure(
                        "Mipple"
                    )

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    mepple_rect = pygame.Rect(
                        SCREEN_WIDTH // 2 - 300,
                        260,
                        240,
                        280
                    )

                    mipple_rect = pygame.Rect(
                        SCREEN_WIDTH // 2 + 60,
                        260,
                        240,
                        280
                    )

                    if mepple_rect.collidepoint(
                        event.pos
                    ):

                        self.start_adventure(
                            "Mepple"
                        )

                    elif mipple_rect.collidepoint(
                        event.pos
                    ):

                        self.start_adventure(
                            "Mipple"
                        )

            return

        # ========================================================
        # RELATIONSHIPS
        # ========================================================

        if self.state == "relationships":

            if event.type == pygame.KEYDOWN:

                if event.key in (pygame.K_r, pygame.K_ESCAPE):
                    self.state = "playing"
                    return

                elif event.key == pygame.K_UP:
                    self.relationship_scroll = max(0, self.relationship_scroll - 70)
                    return

                elif event.key == pygame.K_DOWN:
                    self.relationship_scroll += 70
                    return

                elif event.key == pygame.K_HOME:
                    self.relationship_scroll = 0
                    return

                elif event.key == pygame.K_END:
                    self.relationship_scroll = 999999
                    return

            elif event.type == pygame.MOUSEWHEEL:
                self.relationship_scroll = max(0, self.relationship_scroll - event.y * 60)
                return

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.get_relationship_back_rect().collidepoint(event.pos):
                    self.state = "playing"
                    return

            return

        # ========================================================
        # QUEST LOG
        # ========================================================

        if self.state == "quest_log":

            if event.type == pygame.KEYDOWN:

                if event.key in (
                    pygame.K_q,
                    pygame.K_ESCAPE
                ):

                    self.state = "playing"
                    return

                elif event.key == pygame.K_LEFT:

                    self.change_quest_tab(-1)

                elif event.key == pygame.K_RIGHT:

                    self.change_quest_tab(1)

                elif event.key == pygame.K_UP:

                    self.scroll_current_quest_tab(
                        -70
                    )

                elif event.key == pygame.K_DOWN:

                    self.scroll_current_quest_tab(
                        70
                    )

                elif event.key == pygame.K_PAGEUP:

                    self.scroll_current_quest_tab(
                        -350
                    )

                elif event.key == pygame.K_PAGEDOWN:

                    self.scroll_current_quest_tab(
                        350
                    )

                elif event.key == pygame.K_HOME:

                    self.quest_scroll[
                        self.quest_tab
                    ] = 0

                elif event.key == pygame.K_END:

                    self.quest_scroll[
                        self.quest_tab
                    ] = 999999

            elif event.type == pygame.MOUSEWHEEL:

                self.scroll_current_quest_tab(
                    -event.y * 60
                )

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 4:

                    self.scroll_current_quest_tab(
                        -60
                    )

                elif event.button == 5:

                    self.scroll_current_quest_tab(
                        60
                    )

                elif event.button == 1:

                    tab = self.get_clicked_quest_tab(
                        event.pos
                    )

                    if tab is not None:

                        self.quest_tab = tab
                        return

                    quest = self.get_clicked_quest(
                        event.pos
                    )

                    if quest is not None:
                        self.selected_quest = quest
                        self.state = "quest_details"

            return

        # ========================================================
        # QUEST DETAILS
        # ========================================================

        if self.state == "quest_details":

            if event.type == pygame.KEYDOWN:

                if event.key in (
                    pygame.K_ESCAPE,
                    pygame.K_q
                ):
                    self.selected_quest = None
                    self.state = "quest_log"
                    return

                if event.key == pygame.K_n:
                    self.navigate_selected_quest()
                    return

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:
                    navigate_rect = self.get_quest_navigate_button_rect()

                    if navigate_rect.collidepoint(event.pos):
                        self.navigate_selected_quest()
                        return

                    back_rect = self.get_quest_details_back_rect()
                    if back_rect.collidepoint(event.pos):
                        self.selected_quest = None
                        self.state = "quest_log"
                        return

            return

        # ========================================================
        # DIALOGUE
        # ========================================================

        if self.dialogue_npc is not None:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    self.pending_quest = None
                    self.quest_offer_ready = False

                    self.close_dialogue()

                    return

                if event.key == pygame.K_e:

                    if self.quest_offer_ready:

                        self.accept_pending_quest()

                    else:

                        self.advance_dialogue()

                    return

            return

        # ========================================================
        # PLAYING
        # ========================================================

        if self.state == "playing":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    self.state = "pause"

                elif event.key == pygame.K_q:

                    self.open_quest_log()

                elif event.key == pygame.K_r:

                    self.open_relationships()

                elif event.key == pygame.K_n:

                    self.toggle_navigator()

                elif event.key == pygame.K_e:

                    self.interact()

        # ========================================================
        # PAUSE
        # ========================================================

        elif self.state == "pause":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    self.state = "playing"
                elif event.key == pygame.K_s:
                    self.save_game()
                elif event.key == pygame.K_r:
                    self.open_relationships()
                elif event.key == pygame.K_m:
                    self.save_game()
                    self.state = "main_menu"
                    self.refresh_main_menu_options()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.get_pause_resume_rect().collidepoint(event.pos):
                    self.state = "playing"
                elif self.get_pause_save_rect().collidepoint(event.pos):
                    self.save_game()
                elif self.get_pause_relationships_rect().collidepoint(event.pos):
                    self.open_relationships(from_pause=True)
                elif self.get_pause_menu_rect().collidepoint(event.pos):
                    self.save_game()
                    self.state = "main_menu"
                    self.refresh_main_menu_options()

    # ============================================================
    # MAIN MENU EVENTS
    # ============================================================

    def handle_main_menu_event(
        self,
        event
    ):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:

                self.main_menu_selected -= 1

                if self.main_menu_selected < 0:

                    self.main_menu_selected = (
                        len(
                            self.main_menu_options
                        ) - 1
                    )

            elif event.key == pygame.K_DOWN:

                self.main_menu_selected += 1

                if (
                    self.main_menu_selected
                    >= len(
                        self.main_menu_options
                    )
                ):

                    self.main_menu_selected = 0

            elif event.key in (
                pygame.K_RETURN,
                pygame.K_SPACE
            ):

                self.activate_main_menu_option()

            elif event.key == pygame.K_ESCAPE:

                self.running = False

        elif event.type == pygame.MOUSEMOTION:

            self.update_main_menu_hover(
                event.pos
            )

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                self.update_main_menu_hover(
                    event.pos
                )

                self.activate_main_menu_option()

    def get_main_menu_button_rect(
        self,
        index
    ):

        width = 420
        height = 65

        x = (
            SCREEN_WIDTH // 2
            - width // 2
        )

        y = 390 + index * 78

        return pygame.Rect(
            x,
            y,
            width,
            height
        )

    def update_main_menu_hover(
        self,
        mouse_pos
    ):

        for index in range(
            len(self.main_menu_options)
        ):

            rect = self.get_main_menu_button_rect(
                index
            )

            if rect.collidepoint(
                mouse_pos
            ):

                self.main_menu_selected = index
                return

    def activate_main_menu_option(self):

        selected = (
            self.main_menu_selected
        )

        option = self.main_menu_options[selected]

        if option == "CONTINUE":
            self.load_game()
        elif option == "START ADVENTURE":
            self.state = "character_select"
        elif option == "QUIT GAME":
            self.running = False

    # ============================================================
    # QUEST TAB
    # ============================================================

    def get_current_quest_list(self):

        if self.quest_tab == 0:
            return self.get_active_quests()

        if self.quest_tab == 1:
            return self.get_available_quests()

        if self.quest_tab == 2:
            return self.get_completed_quests()

        return self.get_locked_quests()

    def change_quest_tab(
        self,
        direction
    ):

        self.quest_tab += direction

        self.quest_tab = int(
            clamp(
                self.quest_tab,
                0,
                len(
                    self.quest_tab_names
                ) - 1
            )
        )

    def get_quest_log_view_rect(self):

        header_height = 160
        footer_height = 55

        return pygame.Rect(
            25,
            header_height,
            SCREEN_WIDTH - 65,
            SCREEN_HEIGHT
            - header_height
            - footer_height
        )

    def get_clicked_quest_tab(
        self,
        pos
    ):

        tab_y = 105
        tab_height = 50

        left = 25

        total_width = (
            SCREEN_WIDTH - 65
        )

        tab_width = (
            total_width // 4
        )

        if not (
            tab_y
            <= pos[1]
            <= tab_y + tab_height
        ):

            return None

        if not (
            left
            <= pos[0]
            <= left + total_width
        ):

            return None

        index = (
            pos[0] - left
        ) // tab_width

        return int(
            clamp(
                index,
                0,
                3
            )
        )

    def get_clicked_quest(
        self,
        pos
    ):
        """Return the quest entry clicked in the current quest tab."""
        viewport = self.get_quest_log_view_rect()

        if not viewport.collidepoint(pos):
            return None

        quests = self.get_current_quest_list()
        sorted_quests = sorted(
            quests,
            key=lambda q: (
                q.giver_name,
                q.chain_id,
                q.chain_order
            )
        )

        entry_height = 105
        top_padding = 20
        y = (
            viewport.y
            + top_padding
            - self.quest_scroll[self.quest_tab]
        )

        for quest in sorted_quests:
            rect = pygame.Rect(
                viewport.x + 15,
                y,
                viewport.width - 45,
                92
            )

            if rect.collidepoint(pos):
                return quest

            y += entry_height

        return None

    def get_quest_navigator_index(
        self,
        quest
    ):
        active_quests = self.get_active_quests()

        for index, active_quest in enumerate(active_quests):
            if active_quest.quest_id == quest.quest_id:
                return index

        return None

    def navigate_selected_quest(self):
        """Start navigation directly from the selected quest details."""
        quest = self.selected_quest

        if quest is None:
            return
        if self.get_quest_status(quest) != "ACTIVE":
            self.show_notification(
                "Only active quests can be navigated."
            )
            return

        index = self.get_quest_navigator_index(quest)

        if index is None:
            self.show_notification(
                "This quest is no longer active."
            )
            return

        self.navigator_quest_index = index
        self.navigator_quest_id = quest.quest_id
        self.navigator_enabled = True
        self.selected_quest = None
        self.state = "playing"

        target, target_type, target_name = self.get_navigator_target(quest)
        if target_name:
            self.show_notification(
                f"Navigating to {target_name} — {quest.title}"
            )

    def get_quest_navigate_button_rect(self):
        return pygame.Rect(
            SCREEN_WIDTH // 2 - 170,
            SCREEN_HEIGHT - 145,
            340,
            58
        )

    def get_quest_details_back_rect(self):
        return pygame.Rect(
            30,
            SCREEN_HEIGHT - 75,
            150,
            45
        )

    def draw_quest_details(self):
        quest = self.selected_quest

        if quest is None:
            self.state = "quest_log"
            return

        self.screen.fill((30, 25, 45))

        panel = pygame.Rect(
            45,
            45,
            SCREEN_WIDTH - 90,
            SCREEN_HEIGHT - 90
        )

        pygame.draw.rect(
            self.screen,
            (48, 40, 65),
            panel,
            border_radius=18
        )
        pygame.draw.rect(
            self.screen,
            (150, 125, 190),
            panel,
            2,
            border_radius=18
        )

        title = self.title_font.render(
            quest.title,
            True,
            (255, 230, 140)
        )
        self.screen.blit(title, (75, 75))

        status = self.get_quest_status(quest)
        status_text = self.font.render(
            f"{status}  •  From {quest.giver_name}",
            True,
            (220, 215, 235)
        )
        self.screen.blit(status_text, (75, 120))

        # Description.
        desc_y = 175
        words = quest.description.split()
        line = ""
        lines = []
        for word in words:
            test = (line + " " + word).strip()
            if self.font.size(test)[0] > SCREEN_WIDTH - 180:
                lines.append(line)
                line = word
            else:
                line = test
        if line:
            lines.append(line)

        for line in lines:
            surf = self.font.render(
                line,
                True,
                (240, 235, 245)
            )
            self.screen.blit(surf, (75, desc_y))
            desc_y += 34

        objective = self.font.render(
            f"Objective: {quest.progress}/{quest.required_amount}",
            True,
            (255, 220, 150)
        )
        self.screen.blit(objective, (75, desc_y + 25))

        reward = self.font.render(
            f"Reward: {quest.reward_coins} coins",
            True,
            (255, 220, 150)
        )
        self.screen.blit(reward, (75, desc_y + 65))

        target_npc = self.get_navigator_npc_for_quest(quest)
        target_name = target_npc.name if target_npc else quest.giver_name

        current_target, current_target_type, current_target_name = self.get_navigator_target(quest)

        if current_target_name:
            target_label = f"Current Navigator Target: {current_target_name}"
        else:
            target_label = f"Quest NPC: {target_name}"

        target = self.small_font.render(
            target_label,
            True,
            (205, 195, 225)
        )
        self.screen.blit(target, (75, desc_y + 105))

        if status == "ACTIVE":
            button = self.get_quest_navigate_button_rect()
            pygame.draw.rect(
                self.screen,
                (115, 90, 150),
                button,
                border_radius=12
            )
            pygame.draw.rect(
                self.screen,
                (255, 225, 130),
                button,
                2,
                border_radius=12
            )
            if current_target_name:
                if current_target_type == "npc" and quest.is_finished():
                    button_label = f"RETURN TO {current_target_name}"
                else:
                    button_label = f"NAVIGATE TO {current_target_name}"
            else:
                button_label = f"NAVIGATE TO {target_name}"

            label = self.font.render(
                button_label,
                True,
                (255, 255, 255)
            )
            self.screen.blit(label, label.get_rect(center=button.center))
        else:
            hint = self.small_font.render(
                "Accept this quest first to enable navigation.",
                True,
                (170, 165, 185)
            )
            self.screen.blit(
                hint,
                hint.get_rect(
                    center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 115)
                )
            )

        back = self.get_quest_details_back_rect()
        pygame.draw.rect(
            self.screen,
            (65, 55, 80),
            back,
            border_radius=10
        )
        back_text = self.small_font.render(
            "← BACK TO QUEST LOG",
            True,
            (240, 235, 245)
        )
        self.screen.blit(back_text, back_text.get_rect(center=back.center))

        hint = self.small_font.render(
            "Click Navigate, or press N",
            True,
            (180, 175, 195)
        )
        self.screen.blit(
            hint,
            hint.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 55)
            )
        )

    def get_current_quest_view_height(
        self
    ):

        return (
            self.get_quest_log_view_rect()
        ).height

    def scroll_current_quest_tab(
        self,
        amount
    ):

        tab = self.quest_tab

        self.quest_scroll[tab] += amount

        max_scroll = max(
            0,
            self.quest_content_height[tab]
            - self.get_current_quest_view_height()
        )

        self.quest_scroll[tab] = int(
            clamp(
                self.quest_scroll[tab],
                0,
                max_scroll
            )
        )

    def open_quest_log(self):

        # Quest Log is available only during active gameplay.
        if self.state != "playing":
            return

        self.state = "quest_log"

    # ============================================================
    # PLAYER MOVEMENT
    # ============================================================

    def move_player(
        self,
        dx,
        dy
    ):

        if not self.player:
            return

        length = math.hypot(
            dx,
            dy
        )

        if length > 0:

            dx /= length
            dy /= length

        speed = PLAYER_SPEED

        new_x = (
            self.player.x
            + dx * speed
        )

        test_rect = pygame.Rect(
            int(new_x),
            int(self.player.y),
            self.player.rect.width,
            self.player.rect.height
        )

        blocked = any(
            test_rect.colliderect(
                obstacle.rect
            )
            for obstacle in self.obstacles
        )

        if not blocked:

            self.player.x = clamp(
                new_x,
                0,
                WORLD_WIDTH
                - self.player.rect.width
            )

        new_y = (
            self.player.y
            + dy * speed
        )

        test_rect = pygame.Rect(
            int(self.player.x),
            int(new_y),
            self.player.rect.width,
            self.player.rect.height
        )

        blocked = any(
            test_rect.colliderect(
                obstacle.rect
            )
            for obstacle in self.obstacles
        )

        if not blocked:

            self.player.y = clamp(
                new_y,
                0,
                WORLD_HEIGHT
                - self.player.rect.height
            )

        self.player.sync_rect()

    # ============================================================
    # COMPANION
    # ============================================================

    def update_companion(
        self,
        dt
    ):

        if not self.player:
            return

        if not self.companion:
            return

        dx = (
            self.player.x
            - self.companion.x
        )

        dy = (
            self.player.y
            - self.companion.y
        )

        dist = math.hypot(
            dx,
            dy
        )

        if dist > 100:

            dx /= dist
            dy /= dist

            step = (
                self.companion.speed
                * dt
                / 16.67
            )

            self.companion.x += (
                dx * step
            )

            self.companion.y += (
                dy * step
            )

            self.companion.x = clamp(
                self.companion.x,
                0,
                WORLD_WIDTH
                - self.companion.rect.width
            )

            self.companion.y = clamp(
                self.companion.y,
                0,
                WORLD_HEIGHT
                - self.companion.rect.height
            )

            self.companion.sync_rect()

    # ============================================================
    # NPC INTERACTION
    # ============================================================

    def get_nearby_npc(self):

        if not self.player:
            return None

        best_npc = None

        best_distance = (
            NPC_INTERACTION_DISTANCE
        )

        for npc in self.npcs:

            d = distance(
                self.player.x,
                self.player.y,
                npc.x,
                npc.y
            )

            if d < best_distance:

                best_distance = d
                best_npc = npc

        return best_npc

    def add_npc_friendship(self, npc, amount, reason=None):
        old_level, new_level = npc.add_friendship(amount)
        if reason:
            self.show_notification(f"{npc.name} friendship +{amount} ({npc.friendship}/100)")
        if new_level != old_level:
            self.show_notification(f"{npc.name}: {new_level}!")

    def get_npc_friendship_text(self, npc):
        return f"{npc.get_friendship_level()}  {npc.friendship}/100"

    def interact(self):

        npc = self.get_nearby_npc()

        if npc is None:
            return

        self.record_talk_objectives(
            npc.name
        )

        self.add_npc_friendship(npc, 2, reason="talk")

        quest = self.get_npc_quest(
            npc
        )

        if quest:

            status = self.get_quest_status(
                quest
            )

            if status == "ACTIVE":

                if quest.is_finished():

                    self.complete_quest(
                        quest,
                        npc
                    )

                else:

                    self.start_progress_dialogue(
                        npc,
                        quest
                    )

                return

            if status == "AVAILABLE":

                self.start_quest_offer(
                    npc,
                    quest
                )

                return

        self.start_normal_dialogue(
            npc
        )

    # ============================================================
    # DIALOGUE
    # ============================================================

    def start_normal_dialogue(
        self,
        npc
    ):

        self.dialogue_npc = npc

        self.pending_quest = None
        self.quest_offer_ready = False

        self.dialogue_lines = list(
            npc.dialogue
        )

        self.dialogue_index = 0

        npc.is_talking = True

    def start_quest_offer(
        self,
        npc,
        quest
    ):

        self.dialogue_npc = npc

        self.pending_quest = quest
        self.quest_offer_ready = False

        self.dialogue_lines = [

            "Hi! I have a quest for you.",

            quest.title,

            quest.description,

            f"Reward: {quest.reward_coins} coins.",

            "Would you like to accept this quest?"
        ]

        self.dialogue_index = 0

        npc.is_talking = True

    def start_progress_dialogue(
        self,
        npc,
        quest
    ):

        self.dialogue_npc = npc

        self.pending_quest = None
        self.quest_offer_ready = False

        if quest.is_finished():

            self.dialogue_lines = [
                "You did it!",
                "Your quest is ready to turn in.",
                (
                    f"{quest.progress}/"
                    f"{quest.required_amount}"
                )
            ]

        else:

            self.dialogue_lines = [
                "You're doing great!",
                quest.title,
                (
                    f"Progress: "
                    f"{quest.progress}/"
                    f"{quest.required_amount}"
                )
            ]

        self.dialogue_index = 0

        npc.is_talking = True

    def advance_dialogue(self):

        if self.dialogue_npc is None:
            return

        if (
            self.pending_quest is not None
            and self.dialogue_index
            >= len(
                self.dialogue_lines
            ) - 1
        ):

            self.quest_offer_ready = True
            return

        self.dialogue_index += 1

        if (
            self.dialogue_index
            >= len(
                self.dialogue_lines
            )
        ):

            self.close_dialogue()

    def close_dialogue(self):

        if self.dialogue_npc:

            self.dialogue_npc.is_talking = False

        self.dialogue_npc = None

        self.dialogue_lines = []
        self.dialogue_index = 0

        self.pending_quest = None
        self.quest_offer_ready = False

    # ============================================================
    # ACCEPT QUEST
    # ============================================================

    def accept_pending_quest(self):

        if self.pending_quest is None:
            return

        quest = self.pending_quest

        if self.get_quest_status(
            quest
        ) != "AVAILABLE":

            self.close_dialogue()
            return

        quest.accepted = True
        quest.completed = False

        self.show_notification(
            f"Quest accepted: {quest.title}"
        )

        self.dialogue_lines = [
            "Thank you!",
            (
                f"Quest accepted: "
                f"{quest.title}"
            ),
            "Good luck on your adventure!"
        ]

        self.dialogue_index = 0

        self.pending_quest = None
        self.quest_offer_ready = False

    # ============================================================
    # COMPLETE QUEST
    # ============================================================

    def complete_quest(
        self,
        quest,
        npc
    ):

        if quest.completed:
            return

        quest.completed = True
        quest.accepted = False

        self.add_npc_friendship(npc, 15, reason="quest")

        if not quest.reward_claimed:

            self.coins += (
                quest.reward_coins
            )

            quest.reward_claimed = True

        self.show_notification(
            (
                f"Quest completed! "
                f"+{quest.reward_coins} coins"
            )
        )

        next_quests = [
            q
            for q in self.quests
            if q.prerequisite
            == quest.quest_id
        ]

        self.dialogue_npc = npc

        npc.is_talking = True

        self.pending_quest = None
        self.quest_offer_ready = False

        self.dialogue_lines = [
            "You did it!",
            quest.title,
            (
                f"You received "
                f"{quest.reward_coins} coins!"
            )
        ]

        if next_quests:

            self.dialogue_lines.append(
                (
                    "New quest unlocked: "
                    f"{next_quests[0].title}"
                )
            )

        self.dialogue_index = 0

    # ============================================================
    # TALK OBJECTIVES
    # ============================================================

    def record_talk_objectives(
        self,
        npc_name
    ):

        for quest in self.get_active_quests():

            if quest.objective_type != "talk":
                continue

            if quest.target_npc != npc_name:
                continue

            if quest.is_finished():
                continue

            quest.add_progress(1)

            self.show_notification(
                (
                    f"{quest.title}: "
                    f"{quest.progress}/"
                    f"{quest.required_amount}"
                )
            )

    # ============================================================
    # FLOWERS
    # ============================================================

    def check_flower_collection(self):

        if not self.player:
            return

        active_flower_quests = [
            quest
            for quest in self.get_active_quests()
            if quest.objective_type == "flower"
        ]

        if not active_flower_quests:
            return

        for flower in self.flowers:

            if flower.collected:
                continue

            d = distance(
                self.player.x,
                self.player.y,
                flower.x,
                flower.y
            )

            if d <= 28:

                flower.collected = True

                for quest in active_flower_quests:

                    if not quest.is_finished():

                        quest.add_progress(1)

                self.show_notification(
                    "Magical flower collected!"
                )

                break

    # ============================================================
    # QUEST ITEMS
    # ============================================================

    def check_quest_items(self):

        if not self.player:
            return

        active_item_quests = [
            quest
            for quest in self.get_active_quests()
            if quest.objective_type == "item"
        ]

        if not active_item_quests:
            return

        for item in self.quest_items:

            if item.collected:
                continue

            matching_quests = [
                quest
                for quest in active_item_quests
                if quest.item_type
                == item.item_type
                and not quest.is_finished()
            ]

            if not matching_quests:
                continue

            d = distance(
                self.player.x,
                self.player.y,
                item.x,
                item.y
            )

            # Use a generous pickup radius so quest items placed beside
            # rocks, trees, buildings, or other collision obstacles can
            # still be collected.  The navigator can bring the player as
            # close as the obstacle allows, so a small 35px radius could
            # otherwise make some items impossible to reach.
            if d <= 70:

                item.collected = True

                for quest in matching_quests:

                    quest.add_progress(1)

                    self.show_notification(
                        (
                            f"{item.name} collected! "
                            f"{quest.progress}/"
                            f"{quest.required_amount}"
                        )
                    )

                break

    # ============================================================
    # LOCATIONS
    # ============================================================

    def check_quest_locations(self):

        if not self.player:
            return

        active_location_quests = [
            quest
            for quest in self.get_active_quests()
            if quest.objective_type == "location"
        ]

        if not active_location_quests:
            return

        for location in self.quest_locations:

            d = distance(
                self.player.x,
                self.player.y,
                location.x,
                location.y
            )

            if d > location.radius:
                continue

            for quest in active_location_quests:

                if (
                    location.location_id
                    not in quest.target_ids
                ):
                    continue

                if (
                    location.location_id
                    in quest.visited_targets
                ):
                    continue

                quest.visited_targets.add(
                    location.location_id
                )

                quest.progress = min(
                    len(
                        quest.visited_targets
                    ),
                    quest.required_amount
                )

                self.show_notification(
                    (
                        f"Discovered: "
                        f"{location.name}"
                    )
                )

    # ============================================================
    # UPDATE
    # ============================================================

    def update(
        self,
        dt
    ):

        self.menu_time += dt
        self.phase += dt * 0.003

        if self.state == "main_menu":

            self.update_menu_sparkles(
                dt
            )

            return

        if self.state != "playing":

            self.update_notification(
                dt
            )

            return

        if self.dialogue_npc is not None:

            self.update_notification(
                dt
            )

            return

        keys = pygame.key.get_pressed()

        dx = 0
        dy = 0

        if (
            keys[pygame.K_a]
            or keys[pygame.K_LEFT]
        ):

            dx -= 1

        if (
            keys[pygame.K_d]
            or keys[pygame.K_RIGHT]
        ):

            dx += 1

        if (
            keys[pygame.K_w]
            or keys[pygame.K_UP]
        ):

            dy -= 1

        if (
            keys[pygame.K_s]
            or keys[pygame.K_DOWN]
        ):

            dy += 1

        self.move_player(
            dx,
            dy
        )

        self.update_companion(
            dt
        )

        for flower in self.flowers:

            flower.update(dt)

        for item in self.quest_items:

            item.update(dt)

        self.game_time_ms = (self.game_time_ms + dt) % GAME_DAY_LENGTH_MS
        game_minutes = (self.game_time_ms / GAME_DAY_LENGTH_MS) * 24 * 60
        game_hour = int(game_minutes // 60)

        for npc in self.npcs:
            npc.update(dt, self.obstacles, game_hour)

        self.check_flower_collection()
        self.check_quest_items()
        self.check_quest_locations()

        self.camera.update(
            self.player.rect
        )

        self.update_notification(
            dt
        )

    # ============================================================
    # MENU SPARKLES
    # ============================================================

    def update_menu_sparkles(
        self,
        dt
    ):

        for sparkle in self.menu_sparkles:

            sparkle["y"] -= (
                sparkle["speed"]
                * dt
                * 0.06
            )

            sparkle["phase"] += (
                dt * 0.002
            )

            if sparkle["y"] < -10:

                sparkle["y"] = (
                    SCREEN_HEIGHT + 10
                )

                sparkle["x"] = random.randint(
                    0,
                    SCREEN_WIDTH
                )

    # ============================================================
    # NOTIFICATION
    # ============================================================

    def show_notification(
        self,
        text
    ):

        self.notification_text = text
        self.notification_timer = 3000

        print(
            f"[QUEST] {text}"
        )

    def update_notification(
        self,
        dt
    ):

        if self.notification_timer > 0:

            self.notification_timer -= dt

            if self.notification_timer <= 0:

                self.notification_timer = 0
                self.notification_text = ""

    # ============================================================
    # MAIN MENU DRAW
    # ============================================================

    def draw_main_menu(self):

        # --------------------------------------------------------
        # Gradient-style background
        # --------------------------------------------------------

        self.screen.fill(
            (55, 38, 88)
        )

        # Large decorative circles.
        pygame.draw.circle(
            self.screen,
            (90, 65, 125),
            (
                100,
                120
            ),
            260
        )

        pygame.draw.circle(
            self.screen,
            (75, 55, 110),
            (
                SCREEN_WIDTH - 100,
                180
            ),
            300
        )

        pygame.draw.circle(
            self.screen,
            (65, 45, 100),
            (
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT + 200
            ),
            500
        )

        # --------------------------------------------------------
        # Sparkles
        # --------------------------------------------------------

        for sparkle in self.menu_sparkles:

            pulse = (
                math.sin(
                    sparkle["phase"]
                )
                + 1
            ) / 2

            size = max(
                1,
                int(
                    sparkle["size"]
                    * (0.6 + pulse * 0.8)
                )
            )

            x = int(
                sparkle["x"]
            )

            y = int(
                sparkle["y"]
            )

            pygame.draw.circle(
                self.screen,
                (255, 230, 180),
                (
                    x,
                    y
                ),
                size
            )

        # --------------------------------------------------------
        # Decorative moon
        # --------------------------------------------------------

        pygame.draw.circle(
            self.screen,
            (255, 235, 180),
            (
                SCREEN_WIDTH - 130,
                110
            ),
            55
        )

        pygame.draw.circle(
            self.screen,
            (75, 55, 110),
            (
                SCREEN_WIDTH - 105,
                90
            ),
            55
        )

        # --------------------------------------------------------
        # Title
        # --------------------------------------------------------

        title_1 = self.title_font.render(
            "MEPPLE & MIPPLE",
            True,
            (255, 240, 170)
        )

        title_1_rect = title_1.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                105
            )
        )

        self.screen.blit(
            title_1,
            title_1_rect
        )

        title_2 = self.large_font.render(
            "Magical Friendship Adventure",
            True,
            (255, 255, 255)
        )

        title_2_rect = title_2.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                150
            )
        )

        self.screen.blit(
            title_2,
            title_2_rect
        )

        # --------------------------------------------------------
        # Fairy images
        # --------------------------------------------------------

        mepple = load_image(
            "mepple.png",
            (120, 145)
        )

        mipple = load_image(
            "mipple.png",
            (120, 145)
        )

        float_amount = math.sin(
            self.menu_time * 0.003
        ) * 6

        if mepple:

            rect = mepple.get_rect(
                center=(
                    SCREEN_WIDTH // 2 - 230,
                    245 + int(float_amount)
                )
            )

            self.screen.blit(
                mepple,
                rect
            )

        if mipple:

            rect = mipple.get_rect(
                center=(
                    SCREEN_WIDTH // 2 + 230,
                    245 - int(float_amount)
                )
            )

            self.screen.blit(
                mipple,
                rect
            )

        # --------------------------------------------------------
        # Menu buttons
        # --------------------------------------------------------

        mouse_pos = pygame.mouse.get_pos()

        for index, option in enumerate(
            self.main_menu_options
        ):

            rect = self.get_main_menu_button_rect(
                index
            )

            hovered = rect.collidepoint(
                mouse_pos
            )

            selected = (
                index
                == self.main_menu_selected
            )

            if selected or hovered:

                bg = (130, 95, 165)
                border = (255, 225, 140)

            else:

                bg = (75, 55, 105)
                border = (150, 130, 180)

            pygame.draw.rect(
                self.screen,
                bg,
                rect,
                border_radius=18
            )

            pygame.draw.rect(
                self.screen,
                border,
                rect,
                3,
                border_radius=18
            )

            text = self.font.render(
                option,
                True,
                (255, 255, 255)
            )

            text_rect = text.get_rect(
                center=rect.center
            )

            self.screen.blit(
                text,
                text_rect
            )

        # --------------------------------------------------------
        # Bottom text
        # --------------------------------------------------------

        hint = self.small_font.render(
            "↑ ↓ Select     ENTER / SPACE Confirm",
            True,
            (220, 210, 240)
        )

        hint_rect = hint.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT - 30
            )
        )

        self.screen.blit(
            hint,
            hint_rect
        )

    # ============================================================
    # WORLD DRAW
    # ============================================================

    def draw_world(self):

        self.screen.fill((150, 205, 135))

        random_generator = random.Random(
            100
        )

        for _ in range(500):

            x = random_generator.randint(
                0,
                WORLD_WIDTH
            )

            y = random_generator.randint(
                0,
                WORLD_HEIGHT
            )

            sx, sy = self.camera.world_to_screen(
                x,
                y
            )

            if (
                -5 <= sx <= SCREEN_WIDTH + 5
                and -5 <= sy <= SCREEN_HEIGHT + 5
            ):

                pygame.draw.line(
                    self.screen,
                    (125, 185, 110),
                    (
                        sx,
                        sy
                    ),
                    (
                        sx + 3,
                        sy - 4
                    ),
                    1
                )

        for location in self.quest_locations:

            location.draw(
                self.screen,
                self.camera
            )

        for flower in self.flowers:

            flower.draw(
                self.screen,
                self.camera
            )

        for item in self.quest_items:

            item.draw(
                self.screen,
                self.camera
            )

        for obstacle in self.obstacles:

            obstacle.draw(
                self.screen,
                self.camera
            )

        for npc in self.npcs:

            npc.draw(
                self.screen,
                self.camera,
                self
            )

        if self.companion:

            self.companion.draw(
                self.screen,
                self.camera
            )

        if self.player:

            self.player.draw(
                self.screen,
                self.camera
            )

        # Day/night tint. The world remains visible while the sky gradually
        # becomes darker at night.
        game_minutes = (self.game_time_ms / GAME_DAY_LENGTH_MS) * 24 * 60
        hour = game_minutes / 60.0
        if 6.0 <= hour < 18.0:
            darkness = 0
        elif hour < 20.0:
            darkness = int((hour - 18.0) / 2.0 * 70)
        elif hour < 6.0:
            darkness = 120
        else:
            darkness = int((20.0 - hour) / 2.0 * 50 + 70) if hour < 22.0 else 120
        if darkness > 0:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((25, 35, 80, min(145, darkness)))
            self.screen.blit(overlay, (0, 0))

    # ============================================================
    # HUD
    # ============================================================

    def draw_coin_icon(self, surface, center, radius=13):
        """Draw a small magical 3D-style gold coin without needing an asset."""
        cx, cy = center

        # Soft shadow / lower rim
        pygame.draw.circle(surface, (120, 82, 25), (cx + 1, cy + 2), radius)

        # Dark gold outer rim
        pygame.draw.circle(surface, (190, 130, 35), (cx, cy), radius)

        # Main gold face
        pygame.draw.circle(surface, (255, 205, 65), (cx, cy), radius - 2)

        # Inner embossed face
        pygame.draw.circle(surface, (255, 225, 105), (cx, cy), radius - 5)
        pygame.draw.circle(surface, (226, 166, 48), (cx, cy), radius - 6, 1)

        # Magical four-point sparkle/star in the middle
        star = [
            (cx, cy - 6),
            (cx + 2, cy - 2),
            (cx + 6, cy),
            (cx + 2, cy + 2),
            (cx, cy + 6),
            (cx - 2, cy + 2),
            (cx - 6, cy),
            (cx - 2, cy - 2),
        ]
        pygame.draw.polygon(surface, (255, 245, 175), star)

        # Small glossy highlight
        pygame.draw.circle(
            surface,
            (255, 250, 205),
            (cx - radius // 3, cy - radius // 3),
            max(2, radius // 5),
        )

    def draw_hud(self):

        if not self.player:
            return

        panel = pygame.Rect(
            15,
            15,
            270,
            95
        )

        pygame.draw.rect(
            self.screen,
            (50, 40, 70),
            panel,
            border_radius=14
        )

        pygame.draw.rect(
            self.screen,
            (255, 255, 255),
            panel,
            2,
            border_radius=14
        )

        name = self.large_font.render(
            self.player.name,
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            name,
            (
                30,
                27
            )
        )

        # Coin icon + count
        self.draw_coin_icon(
            self.screen,
            (42, 73),
            radius=13
        )

        coin_text = self.font.render(
            str(self.coins),
            True,
            (255, 225, 90)
        )

        self.screen.blit(
            coin_text,
            coin_text.get_rect(
                midleft=(62, 73)
            )
        )

        active_count = len(
            self.get_active_quests()
        )

        quest_text = self.small_font.render(
            f"Active quests: {active_count}",
            True,
            (235, 235, 255)
        )

        self.screen.blit(
            quest_text,
            (
                30,
                87
            )
        )

        game_minutes = (self.game_time_ms / GAME_DAY_LENGTH_MS) * 24 * 60
        total_minutes = int(game_minutes) % (24 * 60)
        hh = total_minutes // 60
        mm = total_minutes % 60
        period = "DAY" if 6 <= hh < 20 else "NIGHT"
        clock_text = self.large_font.render(
            f"TIME  {hh:02d}:{mm:02d}  •  {period}",
            True,
            (230, 240, 255)
        )
        clock_rect = clock_text.get_rect(
            top=18,
            right=SCREEN_WIDTH - 18
        )
        clock_bg = clock_rect.inflate(20, 10)
        pygame.draw.rect(
            self.screen,
            (45, 50, 80),
            clock_bg,
            border_radius=12
        )
        pygame.draw.rect(
            self.screen,
            (180, 190, 235),
            clock_bg,
            2,
            border_radius=12
        )
        self.screen.blit(clock_text, clock_rect)

        controls = self.small_font.render(
            (
                "WASD Move   "
                "E Interact   "
                "Q Quest Log   "
                "R Relationships   "
                "N Navigate   "
                "ESC Pause"
            ),
            True,
            (255, 255, 255)
        )

        controls_rect = controls.get_rect(
            top=62,
            right=SCREEN_WIDTH - 15
        )

        control_bg = controls_rect.inflate(
            18,
            10
        )

        pygame.draw.rect(
            self.screen,
            (55, 45, 75),
            control_bg,
            border_radius=10
        )

        self.screen.blit(
            controls,
            controls_rect
        )

        active_quests = self.get_active_quests()

        if active_quests:

            panel_x = 15
            panel_y = 125
            panel_w = 340

            preview_count = min(
                len(active_quests),
                3
            )

            panel_h = (
                45
                + preview_count * 48
            )

            quest_panel = pygame.Rect(
                panel_x,
                panel_y,
                panel_w,
                panel_h
            )

            pygame.draw.rect(
                self.screen,
                (55, 45, 75),
                quest_panel,
                border_radius=12
            )

            pygame.draw.rect(
                self.screen,
                (255, 255, 255),
                quest_panel,
                2,
                border_radius=12
            )

            title = self.font.render(
                "ACTIVE QUESTS",
                True,
                (255, 230, 130)
            )

            self.screen.blit(
                title,
                (
                    panel_x + 15,
                    panel_y + 10
                )
            )

            y = panel_y + 42

            for quest in active_quests[:3]:

                quest_name = self.small_font.render(
                    quest.title,
                    True,
                    (255, 255, 255)
                )

                self.screen.blit(
                    quest_name,
                    (
                        panel_x + 15,
                        y
                    )
                )

                progress = self.small_font.render(
                    (
                        f"{quest.progress}/"
                        f"{quest.required_amount}"
                    ),
                    True,
                    (220, 220, 240)
                )

                self.screen.blit(
                    progress,
                    (
                        panel_x + 250,
                        y
                    )
                )

                y += 48

        npc = self.get_nearby_npc()

        if npc:

            prompt = self.font.render(
                f"E  Talk to {npc.name}",
                True,
                (255, 255, 255)
            )

            rect = prompt.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    SCREEN_HEIGHT - 45
                )
            )

            bg = rect.inflate(
                30,
                15
            )

            pygame.draw.rect(
                self.screen,
                (65, 50, 85),
                bg,
                border_radius=12
            )

            pygame.draw.rect(
                self.screen,
                (255, 255, 255),
                bg,
                2,
                border_radius=12
            )

            self.screen.blit(
                prompt,
                rect
            )

        self.draw_notification()

    # ============================================================
    # NOTIFICATION DRAW
    # ============================================================

    def draw_notification(self):

        if not self.notification_text:
            return

        surface = self.font.render(
            self.notification_text,
            True,
            (255, 255, 255)
        )

        rect = surface.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                75
            )
        )

        bg = rect.inflate(
            40,
            22
        )

        pygame.draw.rect(
            self.screen,
            (70, 55, 95),
            bg,
            border_radius=12
        )

        pygame.draw.rect(
            self.screen,
            (255, 225, 120),
            bg,
            2,
            border_radius=12
        )

        self.screen.blit(
            surface,
            rect
        )

    # ============================================================
    # DIALOGUE
    # ============================================================

    def draw_dialogue(self):

        if self.dialogue_npc is None:
            return

        panel_h = 190

        panel = pygame.Rect(
            30,
            SCREEN_HEIGHT - panel_h - 25,
            SCREEN_WIDTH - 60,
            panel_h
        )

        pygame.draw.rect(
            self.screen,
            (45, 35, 65),
            panel,
            border_radius=18
        )

        pygame.draw.rect(
            self.screen,
            (255, 255, 255),
            panel,
            3,
            border_radius=18
        )

        speaker = self.title_font.render(
            self.dialogue_npc.name,
            True,
            (255, 220, 130)
        )

        self.screen.blit(
            speaker,
            (
                panel.x + 25,
                panel.y + 18
            )
        )

        relationship = self.dialogue_npc
        rel_label = self.small_font.render(
            f"Friendship: {self.get_npc_friendship_text(relationship)}",
            True,
            (245, 220, 150)
        )
        rel_rect = rel_label.get_rect(
            top=panel.y + 24,
            right=panel.right - 25
        )
        self.screen.blit(rel_label, rel_rect)

        bar = pygame.Rect(panel.right - 230, panel.y + 50, 205, 10)
        pygame.draw.rect(self.screen, (35, 30, 50), bar, border_radius=5)
        fill_width = int(bar.width * relationship.friendship / relationship.friendship_max)
        if fill_width > 0:
            fill = pygame.Rect(bar.x, bar.y, fill_width, bar.height)
            pygame.draw.rect(self.screen, (255, 190, 120), fill, border_radius=5)

        if self.dialogue_lines:

            line = self.dialogue_lines[
                min(
                    self.dialogue_index,
                    len(
                        self.dialogue_lines
                    ) - 1
                )
            ]

            lines = wrap_text(
                line,
                self.font,
                panel.width - 50
            )

            y = panel.y + 65

            for text_line in lines[:3]:

                surface = self.font.render(
                    text_line,
                    True,
                    (255, 255, 255)
                )

                self.screen.blit(
                    surface,
                    (
                        panel.x + 25,
                        y
                    )
                )

                y += 28

        if self.quest_offer_ready:

            prompt_text = (
                "E  Accept Quest     "
                "ESC  Decline"
            )

        else:

            prompt_text = "E  Continue"

        prompt = self.small_font.render(
            prompt_text,
            True,
            (230, 220, 255)
        )

        prompt_rect = prompt.get_rect(
            right=panel.right - 25,
            bottom=panel.bottom - 20
        )

        self.screen.blit(
            prompt,
            prompt_rect
        )

    # ============================================================
    # QUEST ENTRY
    # ============================================================

    def draw_quest_entry(
        self,
        quest,
        x,
        y,
        width,
        status
    ):

        if status == "ACTIVE":

            bg = (65, 55, 90)
            border = (160, 140, 255)

        elif status == "AVAILABLE":

            bg = (55, 80, 65)
            border = (140, 220, 160)

        elif status == "COMPLETED":

            bg = (65, 65, 65)
            border = (150, 150, 150)

        else:

            bg = (48, 48, 58)
            border = (105, 105, 115)

        rect = pygame.Rect(
            x,
            y,
            width,
            92
        )

        pygame.draw.rect(
            self.screen,
            bg,
            rect,
            border_radius=12
        )

        pygame.draw.rect(
            self.screen,
            border,
            rect,
            2,
            border_radius=12
        )

        title = self.font.render(
            quest.title,
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            title,
            (
                rect.x + 15,
                rect.y + 10
            )
        )

        giver = self.tiny_font.render(
            (
                f"From {quest.giver_name}  •  "
                f"{quest.chain_id}"
            ),
            True,
            (190, 185, 210)
        )

        self.screen.blit(
            giver,
            (
                rect.x + 15,
                rect.y + 37
            )
        )

        if status == "LOCKED":

            prerequisite = self.get_quest_by_id(
                quest.prerequisite
            )

            if prerequisite:

                status_text = (
                    "Locked — complete "
                    f"'{prerequisite.title}'"
                )

            else:

                status_text = "Locked"

        elif status == "COMPLETED":

            status_text = "Completed"

        elif status == "AVAILABLE":

            status_text = (
                f"Available  •  "
                f"Reward: "
                f"{quest.reward_coins} coins"
            )

        else:

            status_text = (
                f"Progress: "
                f"{quest.progress}/"
                f"{quest.required_amount}  •  "
                f"Reward: "
                f"{quest.reward_coins}"
            )

        status_surface = self.small_font.render(
            status_text,
            True,
            (235, 235, 235)
        )

        self.screen.blit(
            status_surface,
            (
                rect.x + 15,
                rect.y + 62
            )
        )

        # Click the quest entry / DETAILS button to open the
        # full quest details screen.
        details_rect = pygame.Rect(
            rect.right - 112,
            rect.y + 27,
            92,
            38
        )

        details_bg = (95, 75, 125)
        details_border = (220, 195, 120)

        pygame.draw.rect(
            self.screen,
            details_bg,
            details_rect,
            border_radius=9
        )
        pygame.draw.rect(
            self.screen,
            details_border,
            details_rect,
            1,
            border_radius=9
        )
        details_text = self.tiny_font.render(
            "DETAILS",
            True,
            (255, 255, 255)
        )
        self.screen.blit(
            details_text,
            details_text.get_rect(
                center=details_rect.center
            )
        )

        return rect.height

    # ============================================================
    # QUEST LOG
    # ============================================================

    def draw_quest_log(self):

        self.screen.fill(
            (30, 25, 45)
        )

        # Header.
        header = pygame.Rect(
            0,
            0,
            SCREEN_WIDTH,
            95
        )

        pygame.draw.rect(
            self.screen,
            (55, 45, 75),
            header
        )

        title = self.title_font.render(
            "QUEST LOG",
            True,
            (255, 230, 140)
        )

        self.screen.blit(
            title,
            (
                30,
                20
            )
        )

        subtitle = self.small_font.render(
            "Manage your magical adventures",
            True,
            (210, 205, 225)
        )

        self.screen.blit(
            subtitle,
            (
                30,
                57
            )
        )

        # Tabs.
        tab_y = 105
        tab_height = 50

        tab_left = 25

        tab_total_width = (
            SCREEN_WIDTH - 65
        )

        tab_width = (
            tab_total_width // 4
        )

        tab_data = [
            (
                "ACTIVE",
                len(
                    self.get_active_quests()
                )
            ),
            (
                "AVAILABLE",
                len(
                    self.get_available_quests()
                )
            ),
            (
                "COMPLETED",
                len(
                    self.get_completed_quests()
                )
            ),
            (
                "LOCKED",
                len(
                    self.get_locked_quests()
                )
            )
        ]

        for index, (
            name,
            count
        ) in enumerate(tab_data):

            x = (
                tab_left
                + index * tab_width
            )

            rect = pygame.Rect(
                x,
                tab_y,
                tab_width - 4,
                tab_height
            )

            if index == self.quest_tab:

                bg = (115, 90, 150)
                border = (255, 225, 130)

            else:

                bg = (55, 48, 70)
                border = (100, 90, 115)

            pygame.draw.rect(
                self.screen,
                bg,
                rect,
                border_radius=10
            )

            pygame.draw.rect(
                self.screen,
                border,
                rect,
                2,
                border_radius=10
            )

            label = self.small_font.render(
                f"{name} ({count})",
                True,
                (255, 255, 255)
            )

            label_rect = label.get_rect(
                center=rect.center
            )

            self.screen.blit(
                label,
                label_rect
            )

        # Viewport.
        viewport = (
            self.get_quest_log_view_rect()
        )

        pygame.draw.rect(
            self.screen,
            (38, 33, 52),
            viewport,
            border_radius=10
        )

        pygame.draw.rect(
            self.screen,
            (100, 90, 120),
            viewport,
            2,
            border_radius=10
        )

        quests = (
            self.get_current_quest_list()
        )

        status = self.quest_tab_names[
            self.quest_tab
        ]

        sorted_quests = sorted(
            quests,
            key=lambda q: (
                q.giver_name,
                q.chain_id,
                q.chain_order
            )
        )

        entry_height = 105
        top_padding = 20
        bottom_padding = 20

        content_height = (
            top_padding
            + len(sorted_quests)
            * entry_height
            + bottom_padding
        )

        self.quest_content_height[
            self.quest_tab
        ] = content_height

        max_scroll = max(
            0,
            content_height - viewport.height
        )

        self.quest_scroll[
            self.quest_tab
        ] = int(
            clamp(
                self.quest_scroll[
                    self.quest_tab
                ],
                0,
                max_scroll
            )
        )

        old_clip = (
            self.screen.get_clip()
        )

        self.screen.set_clip(
            viewport
        )

        x = viewport.x + 15

        y = (
            viewport.y
            + top_padding
            - self.quest_scroll[
                self.quest_tab
            ]
        )

        width = viewport.width - 45

        if not sorted_quests:

            messages = {
                0:
                    "You don't have any active quests yet.",

                1:
                    "There are no quests available right now.",

                2:
                    "You haven't completed any quests yet.",

                3:
                    "No locked quests."
            }

            empty = self.font.render(
                messages[self.quest_tab],
                True,
                (150, 145, 165)
            )

            empty_rect = empty.get_rect(
                center=viewport.center
            )

            self.screen.blit(
                empty,
                empty_rect
            )

        else:

            for quest in sorted_quests:

                self.draw_quest_entry(
                    quest,
                    x,
                    y,
                    width,
                    status
                )

                y += entry_height

        self.screen.set_clip(
            old_clip
        )

        # Scrollbar.
        scrollbar_x = SCREEN_WIDTH - 27

        scrollbar_y = (
            viewport.y + 5
        )

        scrollbar_height = (
            viewport.height - 10
        )

        pygame.draw.rect(
            self.screen,
            (55, 50, 68),
            (
                scrollbar_x,
                scrollbar_y,
                10,
                scrollbar_height
            ),
            border_radius=5
        )

        if content_height > viewport.height:

            thumb_height = max(
                40,
                int(
                    scrollbar_height
                    * viewport.height
                    / content_height
                )
            )

            scroll_range = (
                scrollbar_height
                - thumb_height
            )

            thumb_y = (
                scrollbar_y
                + int(
                    scroll_range
                    * self.quest_scroll[
                        self.quest_tab
                    ]
                    / max_scroll
                )
            )

            pygame.draw.rect(
                self.screen,
                (180, 155, 225),
                (
                    scrollbar_x,
                    thumb_y,
                    10,
                    thumb_height
                ),
                border_radius=5
            )

        # Footer.
        footer = pygame.Rect(
            0,
            SCREEN_HEIGHT - 55,
            SCREEN_WIDTH,
            55
        )

        pygame.draw.rect(
            self.screen,
            (55, 45, 75),
            footer
        )

        footer_text = self.small_font.render(
            (
                "← → Change Tab    "
                "↑ ↓ Scroll    "
                "Mouse Wheel    "
                "Home / End    "
                "Q / ESC Close"
            ),
            True,
            (235, 235, 245)
        )

        footer_rect = footer_text.get_rect(
            center=footer.center
        )

        self.screen.blit(
            footer_text,
            footer_rect
        )

    # ============================================================
    # RELATIONSHIPS
    # ============================================================

    def open_relationships(self, from_pause=False):
        if self.state not in ("playing", "pause"):
            return
        self.relationship_scroll = 0
        self.state = "relationships"

    def get_relationship_back_rect(self):
        return pygame.Rect(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT - 75, 220, 48)

    def draw_relationships(self):
        # Draw a soft backdrop so this feels like a proper game menu.
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((25, 20, 45, 245))
        self.screen.blit(overlay, (0, 0))

        title = self.title_font.render("RELATIONSHIPS", True, (255, 235, 170))
        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 55)))

        subtitle = self.small_font.render(
            "Build friendship by talking to fairies and helping with their quests",
            True,
            (225, 215, 240)
        )
        self.screen.blit(subtitle, subtitle.get_rect(center=(SCREEN_WIDTH // 2, 88)))

        npcs = list(self.npcs)
        card_w = min(860, SCREEN_WIDTH - 100)
        card_h = 105
        gap = 14
        start_x = (SCREEN_WIDTH - card_w) // 2
        start_y = 120 - self.relationship_scroll

        total_height = len(npcs) * (card_h + gap) - gap
        viewport_top = 110
        viewport_bottom = SCREEN_HEIGHT - 100

        # Clip cards to the menu viewport.
        old_clip = self.screen.get_clip()
        self.screen.set_clip(pygame.Rect(0, viewport_top, SCREEN_WIDTH, viewport_bottom - viewport_top))

        for index, npc in enumerate(npcs):
            y = start_y + index * (card_h + gap)
            card = pygame.Rect(start_x, y, card_w, card_h)

            bg = (65, 52, 88)
            border = (150, 125, 185)
            pygame.draw.rect(self.screen, bg, card, border_radius=16)
            pygame.draw.rect(self.screen, border, card, 2, border_radius=16)

            # Portrait / fairy icon.
            portrait_rect = pygame.Rect(card.x + 14, card.y + 12, 80, 80)
            pygame.draw.rect(self.screen, (45, 35, 65), portrait_rect, border_radius=14)
            if getattr(npc, "image", None) is not None:
                image = npc.image
                image_copy = image.copy()
                image_copy = pygame.transform.smoothscale(image_copy, (64, 64))
                image_rect = image_copy.get_rect(center=portrait_rect.center)
                self.screen.blit(image_copy, image_rect)

            name = self.large_font.render(npc.name, True, (255, 240, 190))
            self.screen.blit(name, (card.x + 112, card.y + 12))

            level = npc.get_friendship_level()
            level_text = self.small_font.render(level, True, (225, 210, 255))
            self.screen.blit(level_text, (card.x + 112, card.y + 43))

            # Friendship bar.
            bar = pygame.Rect(card.x + 112, card.y + 68, card_w - 230, 14)
            pygame.draw.rect(self.screen, (35, 28, 50), bar, border_radius=7)
            fill_width = int(bar.width * npc.friendship / npc.friendship_max)
            if fill_width > 0:
                fill = pygame.Rect(bar.x, bar.y, fill_width, bar.height)
                pygame.draw.rect(self.screen, (255, 190, 120), fill, border_radius=7)
            pygame.draw.rect(self.screen, (180, 165, 205), bar, 1, border_radius=7)

            points = self.small_font.render(
                f"{npc.friendship} / {npc.friendship_max}",
                True,
                (250, 240, 255)
            )
            self.screen.blit(points, points.get_rect(midright=(card.right - 18, card.y + 76)))

        self.screen.set_clip(old_clip)

        # Scroll hint.
        if total_height > viewport_bottom - viewport_top:
            hint = self.tiny_font.render("↑ ↓ / Mouse Wheel to scroll", True, (190, 180, 210))
            self.screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 92)))

        back = self.get_relationship_back_rect()
        hovered = back.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(self.screen, (120, 90, 155) if hovered else (70, 55, 95), back, border_radius=12)
        pygame.draw.rect(self.screen, (255, 225, 140) if hovered else (160, 140, 190), back, 2, border_radius=12)
        back_text = self.font.render("BACK   [R / ESC]", True, (255, 255, 255))
        self.screen.blit(back_text, back_text.get_rect(center=back.center))

    # ============================================================
    # PAUSE
    # ============================================================

    def get_pause_resume_rect(self):
        return pygame.Rect(SCREEN_WIDTH // 2 - 210, 300, 420, 55)

    def get_pause_save_rect(self):
        return pygame.Rect(SCREEN_WIDTH // 2 - 210, 370, 420, 55)

    def get_pause_relationships_rect(self):
        return pygame.Rect(SCREEN_WIDTH // 2 - 210, 440, 420, 55)

    def get_pause_menu_rect(self):
        return pygame.Rect(SCREEN_WIDTH // 2 - 210, 510, 420, 55)

    def draw_pause(self):

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 165))
        self.screen.blit(overlay, (0, 0))
        title = self.title_font.render("PAUSED", True, (255, 255, 255))
        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 220)))
        buttons = [(self.get_pause_resume_rect(), "RESUME", "ESC"), (self.get_pause_save_rect(), "SAVE GAME", "S"), (self.get_pause_relationships_rect(), "RELATIONSHIPS", "R"), (self.get_pause_menu_rect(), "SAVE & MAIN MENU", "M")]
        mouse_pos = pygame.mouse.get_pos()
        for rect, label, key in buttons:
            hovered = rect.collidepoint(mouse_pos)
            bg = (125, 95, 165) if hovered else (70, 55, 95)
            border = (255, 225, 140) if hovered else (160, 140, 190)
            pygame.draw.rect(self.screen, bg, rect, border_radius=14)
            pygame.draw.rect(self.screen, border, rect, 2, border_radius=14)
            text = self.font.render(f"{label}   [{key}]", True, (255, 255, 255))
            self.screen.blit(text, text.get_rect(center=rect.center))
        hint = self.small_font.render("ESC Resume    S Save    R Relationships    M Save & Main Menu", True, (225, 215, 240))
        self.screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 35)))

    # ============================================================
    # CHARACTER SELECT
    # ============================================================

    def draw_character_select(self):

        self.screen.fill(
            (120, 90, 150)
        )

        title = self.title_font.render(
            "Choose Your Fairy",
            True,
            (255, 255, 255)
        )

        title_rect = title.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                110
            )
        )

        self.screen.blit(
            title,
            title_rect
        )

        subtitle = self.font.render(
            (
                "Choose Mepple or Mipple "
                "to begin your adventure"
            ),
            True,
            (235, 225, 255)
        )

        subtitle_rect = subtitle.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                150
            )
        )

        self.screen.blit(
            subtitle,
            subtitle_rect
        )

        cards = [

            (
                "Mepple",
                "mepple.png",
                pygame.Rect(
                    SCREEN_WIDTH // 2 - 300,
                    260,
                    240,
                    280
                ),
                "1"
            ),

            (
                "Mipple",
                "mipple.png",
                pygame.Rect(
                    SCREEN_WIDTH // 2 + 60,
                    260,
                    240,
                    280
                ),
                "2"
            )
        ]

        mouse_pos = pygame.mouse.get_pos()

        for (
            name,
            filename,
            rect,
            key
        ) in cards:

            hovered = rect.collidepoint(
                mouse_pos
            )

            color = (
                (100, 80, 135)
                if hovered
                else (75, 60, 105)
            )

            pygame.draw.rect(
                self.screen,
                color,
                rect,
                border_radius=20
            )

            pygame.draw.rect(
                self.screen,
                (255, 255, 255),
                rect,
                3,
                border_radius=20
            )

            image = load_image(
                filename,
                (100, 120)
            )

            if image:

                image_rect = image.get_rect(
                    center=(
                        rect.centerx,
                        rect.y + 100
                    )
                )

                self.screen.blit(
                    image,
                    image_rect
                )

            name_surface = self.large_font.render(
                name,
                True,
                (255, 255, 255)
            )

            name_rect = name_surface.get_rect(
                center=(
                    rect.centerx,
                    rect.y + 195
                )
            )

            self.screen.blit(
                name_surface,
                name_rect
            )

            key_surface = self.font.render(
                f"Press {key}",
                True,
                (255, 225, 130)
            )

            key_rect = key_surface.get_rect(
                center=(
                    rect.centerx,
                    rect.y + 235
                )
            )

            self.screen.blit(
                key_surface,
                key_rect
            )

        back = self.small_font.render(
            "ESC  Back to Main Menu",
            True,
            (235, 225, 255)
        )

        back_rect = back.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                600
            )
        )

        self.screen.blit(
            back,
            back_rect
        )

    # ============================================================
    # MAIN DRAW
    # ============================================================

    def draw(self):

        if self.state == "main_menu":

            self.draw_main_menu()
            return

        if self.state == "character_select":

            self.draw_character_select()
            return

        if self.state == "relationships":

            self.draw_relationships()
            return

        if self.state == "quest_log":

            self.draw_quest_log()
            return

        if self.state == "quest_details":

            self.draw_quest_details()
            return

        self.draw_world()
        self.draw_hud()

        if self.state == "playing":
            self.draw_navigator()

        if self.dialogue_npc is not None:

            self.draw_dialogue()

        if self.state == "pause":

            self.draw_pause()
