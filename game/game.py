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

#             pygame.draw.rect(
#                 screen,
#                 (225, 180, 140),
#                 rect,
#                 border_radius=8
#             )

#             roof_points = [
#                 (
#                     rect.left - 15,
#                     rect.top + 35
#                 ),
#                 (
#                     rect.centerx,
#                     rect.top - 30
#                 ),
#                 (
#                     rect.right + 15,
#                     rect.top + 35
#                 )
#             ]

#             pygame.draw.polygon(
#                 screen,
#                 (180, 100, 130),
#                 roof_points
#             )

#             door = pygame.Rect(
#                 rect.centerx - 15,
#                 rect.bottom - 55,
#                 30,
#                 55
#             )

#             pygame.draw.rect(
#                 screen,
#                 (110, 75, 60),
#                 door,
#                 border_radius=4
#             )

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

#         self.wander_radius = wander_radius

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

import os
import math
import random
import pygame


# ================================================================
# CONSTANTS
# ================================================================

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


# ================================================================
# PATHS
# ================================================================

GAME_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(GAME_DIR)
ASSET_DIR = os.path.join(PROJECT_DIR, "assets", "fairies")


def asset_path(filename):
    return os.path.join(ASSET_DIR, filename)


# ================================================================
# HELPERS
# ================================================================

def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


def distance(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)


def wrap_text(text, font, max_width):
    words = text.split()

    lines = []
    current = ""

    for word in words:

        test = (
            word
            if not current
            else current + " " + word
        )

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

        image = pygame.image.load(
            path
        ).convert_alpha()

        if size:

            image = pygame.transform.smoothscale(
                image,
                size
            )

        return image

    except pygame.error:

        return None


# ================================================================
# CAMERA
# ================================================================

class Camera:

    def __init__(self):

        self.x = 0
        self.y = 0

    def update(self, target_rect):

        self.x = (
            target_rect.centerx
            - SCREEN_WIDTH // 2
        )

        self.y = (
            target_rect.centery
            - SCREEN_HEIGHT // 2
        )

        self.x = clamp(
            self.x,
            0,
            max(
                0,
                WORLD_WIDTH - SCREEN_WIDTH
            )
        )

        self.y = clamp(
            self.y,
            0,
            max(
                0,
                WORLD_HEIGHT - SCREEN_HEIGHT
            )
        )

    def world_to_screen(self, x, y):

        return (
            int(x - self.x),
            int(y - self.y)
        )


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
        kind="tree"
    ):

        self.rect = pygame.Rect(
            x,
            y,
            width,
            height
        )

        self.kind = kind

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

            trunk = pygame.Rect(
                rect.centerx - 10,
                rect.bottom - 40,
                20,
                40
            )

            pygame.draw.rect(
                screen,
                (125, 82, 48),
                trunk,
                border_radius=5
            )

            pygame.draw.circle(
                screen,
                (70, 150, 80),
                (
                    rect.centerx,
                    rect.top + 25
                ),
                42
            )

            pygame.draw.circle(
                screen,
                (90, 175, 95),
                (
                    rect.centerx - 25,
                    rect.top + 38
                ),
                30
            )

            pygame.draw.circle(
                screen,
                (65, 140, 75),
                (
                    rect.centerx + 25,
                    rect.top + 40
                ),
                30
            )

        elif self.kind == "rock":

            pygame.draw.ellipse(
                screen,
                (125, 130, 145),
                rect
            )

            pygame.draw.ellipse(
                screen,
                (155, 160, 175),
                rect.inflate(
                    -10,
                    -10
                )
            )

        elif self.kind == "house":

            pygame.draw.rect(
                screen,
                (225, 180, 140),
                rect,
                border_radius=8
            )

            roof_points = [
                (
                    rect.left - 15,
                    rect.top + 35
                ),
                (
                    rect.centerx,
                    rect.top - 30
                ),
                (
                    rect.right + 15,
                    rect.top + 35
                )
            ]

            pygame.draw.polygon(
                screen,
                (180, 100, 130),
                roof_points
            )

            door = pygame.Rect(
                rect.centerx - 15,
                rect.bottom - 55,
                30,
                55
            )

            pygame.draw.rect(
                screen,
                (110, 75, 60),
                door,
                border_radius=4
            )

        elif self.kind == "fence":

            pygame.draw.rect(
                screen,
                (170, 120, 75),
                rect,
                border_radius=3
            )

            for x in range(
                rect.left + 10,
                rect.right,
                35
            ):

                pygame.draw.rect(
                    screen,
                    (195, 145, 90),
                    (
                        x,
                        rect.top - 8,
                        10,
                        rect.height + 16
                    ),
                    border_radius=3
                )


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

    def __init__(
        self,
        name,
        image_filename,
        x,
        y,
        dialogue,
        wander_radius=200
    ):

        super().__init__(
            name,
            image_filename,
            x,
            y
        )

        self.spawn_x = float(x)
        self.spawn_y = float(y)

        self.dialogue = dialogue
        self.dialogue_index = 0

        self.is_talking = False

        self.wander_radius = wander_radius

        self.target_x = self.x
        self.target_y = self.y

        self.speed = random.uniform(
            NPC_MIN_SPEED,
            NPC_MAX_SPEED
        )

        self.wait_timer = random.uniform(
            0,
            2
        )

        self.quest_ids = []

        self.choose_new_destination()

    def choose_new_destination(self):

        angle = random.uniform(
            0,
            math.pi * 2
        )

        radius = random.uniform(
            50,
            self.wander_radius
        )

        self.target_x = clamp(
            self.spawn_x
            + math.cos(angle) * radius,
            50,
            WORLD_WIDTH - 100
        )

        self.target_y = clamp(
            self.spawn_y
            + math.sin(angle) * radius,
            50,
            WORLD_HEIGHT - 100
        )

    def can_move_to(
        self,
        new_x,
        new_y,
        obstacles
    ):

        test_rect = pygame.Rect(
            int(new_x),
            int(new_y),
            self.rect.width,
            self.rect.height
        )

        for obstacle in obstacles:

            if test_rect.colliderect(
                obstacle.rect.inflate(
                    8,
                    8
                )
            ):

                return False

        return True

    def update(
        self,
        dt,
        obstacles
    ):

        if self.is_talking:
            return

        self.wait_timer -= (
            dt / 1000.0
        )

        if self.wait_timer > 0:
            return

        dx = self.target_x - self.x
        dy = self.target_y - self.y

        dist = math.hypot(
            dx,
            dy
        )

        if dist < 10:

            self.wait_timer = random.uniform(
                1,
                3
            )

            self.choose_new_destination()

            return

        dx /= dist
        dy /= dist

        step = (
            self.speed
            * dt
            / 16.67
        )

        new_x = self.x + dx * step
        new_y = self.y + dy * step

        if self.can_move_to(
            new_x,
            self.y,
            obstacles
        ):

            self.x = new_x

        else:

            self.choose_new_destination()

        if self.can_move_to(
            self.x,
            new_y,
            obstacles
        ):

            self.y = new_y

        self.sync_rect()

    def draw(
        self,
        screen,
        camera,
        game
    ):

        super().draw(
            screen,
            camera
        )

        sx, sy = camera.world_to_screen(
            self.x,
            self.y
        )

        name_surface = game.small_font.render(
            self.name,
            True,
            (255, 255, 255)
        )

        name_rect = name_surface.get_rect(
            center=(
                sx
                + self.rect.width // 2,

                sy - 14
            )
        )

        bg = name_rect.inflate(
            10,
            5
        )

        pygame.draw.rect(
            screen,
            (70, 55, 90),
            bg,
            border_radius=8
        )

        screen.blit(
            name_surface,
            name_rect
        )

        marker = game.get_npc_marker(
            self
        )

        if marker:

            marker_surface = game.title_font.render(
                marker,
                True,
                (255, 230, 100)
            )

            marker_rect = marker_surface.get_rect(
                center=(
                    sx
                    + self.rect.width // 2,

                    sy - 48
                )
            )

            screen.blit(
                marker_surface,
                marker_rect
            )


# ================================================================
# GAME
# ================================================================

class Game:

    def __init__(self, screen):

        self.screen = screen

        self.running = True

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

        self.selected_character = None

        # --------------------------------------------------------
        # Main menu
        # --------------------------------------------------------

        self.main_menu_selected = 0

        self.main_menu_options = [
            "START ADVENTURE",
            "QUIT GAME"
        ]

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

        for _ in range(100):

            x = random.randint(
                100,
                WORLD_WIDTH - 150
            )

            y = random.randint(
                100,
                WORLD_HEIGHT - 150
            )

            self.obstacles.append(
                Obstacle(
                    x,
                    y,
                    70,
                    90,
                    "tree"
                )
            )

        for _ in range(35):

            x = random.randint(
                100,
                WORLD_WIDTH - 150
            )

            y = random.randint(
                100,
                WORLD_HEIGHT - 120
            )

            self.obstacles.append(
                Obstacle(
                    x,
                    y,
                    70,
                    45,
                    "rock"
                )
            )

        houses = [
            (500, 500),
            (1800, 700),
            (2900, 500),
            (900, 2200),
            (3000, 2200)
        ]

        for x, y in houses:

            self.obstacles.append(
                Obstacle(
                    x,
                    y,
                    170,
                    130,
                    "house"
                )
            )

        fences = [
            (350, 850, 300, 20),
            (2100, 1200, 350, 20),
            (1200, 1900, 300, 20),
            (2800, 1700, 300, 20)
        ]

        for x, y, w, h in fences:

            self.obstacles.append(
                Obstacle(
                    x,
                    y,
                    w,
                    h,
                    "fence"
                )
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

    def start_adventure(
        self,
        character
    ):

        self.selected_character = character

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

                    self.start_adventure(
                        "Mepple"
                    )

                elif event.key == pygame.K_2:

                    self.start_adventure(
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

        if selected == 0:

            # Start Adventure.
            self.state = "character_select"

        elif selected == 1:

            # Quit Game.
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

    def interact(self):

        npc = self.get_nearby_npc()

        if npc is None:
            return

        self.record_talk_objectives(
            npc.name
        )

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

        for npc in self.npcs:

            npc.update(
                dt,
                self.obstacles
            )

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

        self.screen.fill(
            (150, 205, 135)
        )

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

    # ============================================================
    # HUD
    # ============================================================

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

        coins = self.font.render(
            f"★ {self.coins} coins",
            True,
            (255, 225, 90)
        )

        self.screen.blit(
            coins,
            (
                30,
                62
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

        controls = self.small_font.render(
            (
                "WASD Move   "
                "E Interact   "
                "Q Quest Log   "
                "N Navigate   "
                "ESC Pause"
            ),
            True,
            (255, 255, 255)
        )

        controls_rect = controls.get_rect(
            top=15,
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
    # PAUSE
    # ============================================================

    def draw_pause(self):

        overlay = pygame.Surface(
            (
                SCREEN_WIDTH,
                SCREEN_HEIGHT
            ),
            pygame.SRCALPHA
        )

        overlay.fill(
            (0, 0, 0, 150)
        )

        self.screen.blit(
            overlay,
            (0, 0)
        )

        title = self.title_font.render(
            "PAUSED",
            True,
            (255, 255, 255)
        )

        title_rect = title.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                230
            )
        )

        self.screen.blit(
            title,
            title_rect
        )

        instructions = [
            "ESC  Resume",
            "Q    Quest Log"
        ]

        y = 300

        for text in instructions:

            surface = self.font.render(
                text,
                True,
                (235, 235, 245)
            )

            rect = surface.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    y
                )
            )

            self.screen.blit(
                surface,
                rect
            )

            y += 45

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
