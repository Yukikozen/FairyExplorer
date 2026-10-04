# # from .core import *
# # from .entities import Fairy

# # class FairyNPC(Fairy):

# #     def __init__(self, name, image_filename, x, y, dialogue, wander_radius=200):
# #         super().__init__(name, image_filename, x, y)
# #         self.spawn_x = float(x)
# #         self.spawn_y = float(y)
# #         self.dialogue = dialogue
# #         self.dialogue_index = 0
# #         self.is_talking = False
# #         self.wander_radius = max(700, wander_radius)
# #         self.wander_min_distance = 180.0
# #         self.target_x = self.x
# #         self.target_y = self.y
# #         self.speed = random.uniform(1.6, 2.4)
# #         self.wait_timer = random.uniform(0.2, 1.0)
# #         self.stuck_timer = 0.0
# #         self.quest_ids = []
# #         self.house = None
# #         self.is_home = False
# #         self.home_reached = False
# #         self.home_target_x = self.x
# #         self.home_target_y = self.y
# #         self.path = []
# #         self.path_index = 0
# #         self.path_rebuild_timer = 0.0
# #         self.choose_new_destination()

# #     def _fairy_rect(self, x, y):
# #         # Use the actual collision size of the fairy instead of the full
# #         # transparent 64x78 image.  The old oversized hitbox made narrow
# #         # paths around trees/fences impossible.
# #         return pygame.Rect(int(x), int(y), 44, 60).inflate(4, 4)

# #     def _obstacle_visual_rect(self, obstacle):
# #         r = obstacle.rect
# #         if obstacle.kind == "tree":
# #             # Keep a small art-clearance margin without making trees
# #             # artificially huge collision walls.
# #             return r.inflate(8, 12)
# #         if obstacle.kind == "fence":
# #             return r.inflate(8, 10)
# #         if obstacle.kind == "house":
# #             return r.inflate(16, 16)
# #         if obstacle.kind == "rock":
# #             return r.inflate(8, 8)
# #         return r.inflate(8, 8)

# #     def can_move_to(self, new_x, new_y, obstacles):
# #         test = self._fairy_rect(new_x, new_y)
# #         for obstacle in obstacles:
# #             if test.colliderect(self._obstacle_visual_rect(obstacle)):
# #                 return False
# #         return True

# #     def _build_path(self, tx, ty, obstacles):
# #         """Build a small A* path so NPCs can actually walk around obstacles."""
# #         grid = 35
# #         cols = max(1, WORLD_WIDTH // grid)
# #         rows = max(1, WORLD_HEIGHT // grid)

# #         def node_at(x, y):
# #             return (int(clamp(x // grid, 0, cols - 1)), int(clamp(y // grid, 0, rows - 1)))

# #         def center(node):
# #             gx, gy = node
# #             return gx * grid + grid // 2, gy * grid + grid // 2

# #         start = node_at(self.x, self.y)
# #         goal = node_at(tx, ty)

# #         # Find the nearest walkable goal cell if the requested point is just
# #         # beside an obstacle.
# #         def walkable(node):
# #             x, y = center(node)
# #             return self.can_move_to(x, y, obstacles)

# #         if not walkable(goal):
# #             candidates = []
# #             for radius in range(1, 5):
# #                 for dx in range(-radius, radius + 1):
# #                     for dy in range(-radius, radius + 1):
# #                         n = (goal[0] + dx, goal[1] + dy)
# #                         if 0 <= n[0] < cols and 0 <= n[1] < rows and walkable(n):
# #                             candidates.append(n)
# #                 if candidates:
# #                     goal = min(candidates, key=lambda n: abs(n[0]-goal[0]) + abs(n[1]-goal[1]))
# #                     break

# #         # NPCs can occasionally end up with their hitbox touching a fence
# #         # corner after a map transition or an earlier collision.  If the
# #         # current cell is blocked, find the nearest genuinely walkable cell
# #         # before running A*.  This prevents the "start node is blocked" loop.
# #         if not walkable(start):
# #             safe_start = None
# #             for radius in range(1, 9):
# #                 candidates = []
# #                 for dx in range(-radius, radius + 1):
# #                     for dy in range(-radius, radius + 1):
# #                         if abs(dx) != radius and abs(dy) != radius:
# #                             continue
# #                         n = (start[0] + dx, start[1] + dy)
# #                         if 0 <= n[0] < cols and 0 <= n[1] < rows and walkable(n):
# #                             candidates.append(n)
# #                 if candidates:
# #                     safe_start = min(candidates, key=lambda n: abs(n[0]-start[0]) + abs(n[1]-start[1]))
# #                     break
# #             if safe_start is not None:
# #                 sx, sy = center(safe_start)
# #                 self.x, self.y = float(sx), float(sy)
# #                 self.sync_rect()
# #                 start = safe_start
# #             else:
# #                 self.path = []
# #                 self.path_index = 0
# #                 return False

# #         if not walkable(goal):
# #             self.path = []
# #             self.path_index = 0
# #             return False

# #         open_heap = []
# #         heapq.heappush(open_heap, (0, start))
# #         came_from = {}
# #         g_score = {start: 0}
# #         visited = set()
# #         neighbors = [
# #             (-1, 0), (1, 0), (0, -1), (0, 1),
# #             (-1, -1), (-1, 1), (1, -1), (1, 1)
# #         ]

# #         while open_heap:
# #             _, current = heapq.heappop(open_heap)
# #             if current in visited:
# #                 continue
# #             visited.add(current)
# #             if current == goal:
# #                 path = []
# #                 while current != start:
# #                     path.append(center(current))
# #                     current = came_from[current]
# #                 path.reverse()
# #                 # Do not make the fairy stop exactly at the first grid center.
# #                 self.path = path
# #                 self.path_index = 0
# #                 return

# #             for dx, dy in neighbors:
# #                 nxt = (current[0] + dx, current[1] + dy)
# #                 if not (0 <= nxt[0] < cols and 0 <= nxt[1] < rows):
# #                     continue
# #                 if not walkable(nxt):
# #                     continue
# #                 # Prevent diagonal corner-cutting through two obstacles.
# #                 if dx and dy:
# #                     if not walkable((current[0] + dx, current[1])) or not walkable((current[0], current[1] + dy)):
# #                         continue
# #                 step_cost = 1.414 if dx and dy else 1.0
# #                 tentative = g_score[current] + step_cost
# #                 if tentative < g_score.get(nxt, float('inf')):
# #                     came_from[nxt] = current
# #                     g_score[nxt] = tentative
# #                     h = math.hypot(goal[0] - nxt[0], goal[1] - nxt[1])
# #                     heapq.heappush(open_heap, (tentative + h, nxt))

# #         self.path = []
# #         self.path_index = 0

# #     def _set_target(self, x, y, obstacles):
# #         self.target_x = float(x)
# #         self.target_y = float(y)
# #         return self._build_path(self.target_x, self.target_y, obstacles)

# #     def _line_is_clear(self, tx, ty, obstacles):
# #         """Return True when the fairy can travel directly to a point.

# #         NPCs deliberately choose destinations that have a clear route. This
# #         avoids the repeated path-rebuild/corner trap that made them appear
# #         stuck around trees and fences.
# #         """
# #         distance = math.hypot(tx - self.x, ty - self.y)
# #         steps = max(2, int(distance / 12))
# #         for i in range(1, steps + 1):
# #             t = i / steps
# #             px = self.x + (tx - self.x) * t
# #             py = self.y + (ty - self.y) * t
# #             if not self.can_move_to(px, py, obstacles):
# #                 return False
# #         return True

# #     def _find_free_position(self, obstacles, max_radius=220):
# #         """Find a genuinely free nearby position if an NPC gets trapped."""
# #         if self.can_move_to(self.x, self.y, obstacles):
# #             return self.x, self.y

# #         for radius in range(20, max_radius + 1, 20):
# #             for angle_deg in range(0, 360, 15):
# #                 angle = math.radians(angle_deg)
# #                 nx = clamp(
# #                     self.x + math.cos(angle) * radius,
# #                     20, WORLD_WIDTH - 70
# #                 )
# #                 ny = clamp(
# #                     self.y + math.sin(angle) * radius,
# #                     20, WORLD_HEIGHT - 70
# #                 )
# #                 if self.can_move_to(nx, ny, obstacles):
# #                     return nx, ny
# #         return None

# #     def choose_new_destination(self, obstacles=None):
# #         """Choose a nearby destination with a completely clear direct route."""
# #         if obstacles is None:
# #             obstacles = []

# #         # First make sure the NPC is not already embedded in an obstacle.
# #         safe = self._find_free_position(obstacles)
# #         if safe is not None and not self.can_move_to(self.x, self.y, obstacles):
# #             self.x, self.y = safe
# #             self.sync_rect()

# #         # Prefer destinations close enough that the NPC can freely roam
# #         # without needing a complicated global pathfinder.
# #         for _ in range(120):
# #             angle = random.uniform(0, math.tau)
# #             radius = random.uniform(100, self.wander_radius)
# #             tx = clamp(
# #                 self.x + math.cos(angle) * radius,
# #                 80, WORLD_WIDTH - 100
# #             )
# #             ty = clamp(
# #                 self.y + math.sin(angle) * radius,
# #                 80, WORLD_HEIGHT - 100
# #             )

# #             if math.hypot(tx - self.x, ty - self.y) < self.wander_min_distance:
# #                 continue

# #             if self.can_move_to(tx, ty, obstacles) and self._line_is_clear(tx, ty, obstacles):
# #                 self.target_x = tx
# #                 self.target_y = ty
# #                 self.path = []
# #                 self.path_index = 0
# #                 return

# #         # If the normal roaming area is crowded, choose the nearest short
# #         # clear movement instead of freezing in place.
# #         for radius in (45, 65, 85, 110, 140):
# #             for angle_deg in range(0, 360, 20):
# #                 angle = math.radians(angle_deg)
# #                 tx = clamp(
# #                     self.x + math.cos(angle) * radius,
# #                     30, WORLD_WIDTH - 80
# #                 )
# #                 ty = clamp(
# #                     self.y + math.sin(angle) * radius,
# #                     30, WORLD_HEIGHT - 80
# #                 )
# #                 if self.can_move_to(tx, ty, obstacles) and self._line_is_clear(tx, ty, obstacles):
# #                     self.target_x = tx
# #                     self.target_y = ty
# #                     self.path = []
# #                     self.path_index = 0
# #                     return

# #         # No clear destination was found. Try again next update instead of
# #         # locking the NPC onto a permanently blocked target.
# #         self.target_x = self.x
# #         self.target_y = self.y
# #         self.path = []
# #         self.path_index = 0

# #     def set_home(self, house):
# #         self.house = house
# #         if house is not None:
# #             # Stand just outside the front of the house, rather than inside
# #             # the house collision rectangle.
# #             self.home_target_x = float(house.rect.centerx - self.rect.width // 2)
# #             self.home_target_y = float(house.rect.bottom + 18)

# #     def update_home_state(self, game_time_hour, obstacles):
# #         night = game_time_hour >= NPC_HOME_HOUR or game_time_hour < NPC_WAKE_HOUR
# #         if night and not self.is_home:
# #             self.is_home = True
# #             self.home_reached = False
# #             if self.house is not None:
# #                 self.home_target_x = float(self.house.rect.centerx - self.rect.width // 2)
# #                 self.home_target_y = float(self.house.rect.bottom + 18)
# #                 self.path = []
# #                 self.path_index = 0
# #         elif not night and self.is_home:
# #             self.is_home = False
# #             self.home_reached = False
# #             self.choose_new_destination(obstacles)

# #     def _build_local_path(self, tx, ty, obstacles):
# #         """Build a small local A* route only when an NPC needs one.

# #         This replaces the old whole-4000x3000-world search.  The search is
# #         limited to the area between the NPC and destination, so it is fast
# #         enough to use for several wandering fairies.
# #         """
# #         grid = 35
# #         margin = 210
# #         left = int(clamp(min(self.x, tx) - margin, 0, WORLD_WIDTH - grid))
# #         top = int(clamp(min(self.y, ty) - margin, 0, WORLD_HEIGHT - grid))
# #         right = int(clamp(max(self.x, tx) + margin, grid, WORLD_WIDTH))
# #         bottom = int(clamp(max(self.y, ty) + margin, grid, WORLD_HEIGHT))

# #         cols = max(1, min(55, (right - left) // grid + 1))
# #         rows = max(1, min(55, (bottom - top) // grid + 1))

# #         def node_at(x, y):
# #             return (
# #                 int(clamp((x - left) // grid, 0, cols - 1)),
# #                 int(clamp((y - top) // grid, 0, rows - 1)),
# #             )

# #         def center(node):
# #             gx, gy = node
# #             return left + gx * grid + grid // 2, top + gy * grid + grid // 2

# #         def walkable(node):
# #             x, y = center(node)
# #             return self.can_move_to(x, y, obstacles)

# #         start = node_at(self.x, self.y)
# #         goal = node_at(tx, ty)

# #         # If the exact goal cell is blocked, choose the closest free cell.
# #         if not walkable(goal):
# #             candidates = []
# #             for radius in range(1, 5):
# #                 for gx in range(max(0, goal[0]-radius), min(cols, goal[0]+radius+1)):
# #                     for gy in range(max(0, goal[1]-radius), min(rows, goal[1]+radius+1)):
# #                         n = (gx, gy)
# #                         if walkable(n):
# #                             candidates.append(n)
# #                 if candidates:
# #                     goal = min(candidates, key=lambda n: abs(n[0]-goal[0]) + abs(n[1]-goal[1]))
# #                     break

# #         if not walkable(start) or not walkable(goal):
# #             self.path = []
# #             self.path_index = 0
# #             return False

# #         open_heap = [(0.0, start)]
# #         came_from = {}
# #         g_score = {start: 0.0}
# #         visited = set()
# #         neighbors = [
# #             (-1, 0), (1, 0), (0, -1), (0, 1),
# #             (-1, -1), (-1, 1), (1, -1), (1, 1),
# #         ]

# #         while open_heap:
# #             _, current = heapq.heappop(open_heap)
# #             if current in visited:
# #                 continue
# #             visited.add(current)
# #             if current == goal:
# #                 path = []
# #                 while current != start:
# #                     path.append(center(current))
# #                     current = came_from[current]
# #                 path.reverse()
# #                 self.path = path
# #                 self.path_index = 0
# #                 return True

# #             for ox, oy in neighbors:
# #                 nxt = (current[0] + ox, current[1] + oy)
# #                 if not (0 <= nxt[0] < cols and 0 <= nxt[1] < rows):
# #                     continue
# #                 if not walkable(nxt):
# #                     continue
# #                 if ox and oy:
# #                     if not walkable((current[0] + ox, current[1])) or not walkable((current[0], current[1] + oy)):
# #                         continue
# #                 cost = 1.414 if ox and oy else 1.0
# #                 tentative = g_score[current] + cost
# #                 if tentative < g_score.get(nxt, float('inf')):
# #                     came_from[nxt] = current
# #                     g_score[nxt] = tentative
# #                     h = math.hypot(goal[0] - nxt[0], goal[1] - nxt[1])
# #                     heapq.heappush(open_heap, (tentative + h, nxt))

# #         self.path = []
# #         self.path_index = 0
# #         return False

# #     def _move_toward(self, tx, ty, dt, obstacles):
# #         """Move smoothly while sliding around obstacles.

# #         No A* is used here. The destination was already checked for a clear
# #         route, so movement is cheap and cannot get trapped rebuilding paths.
# #         """
# #         dist = math.hypot(tx - self.x, ty - self.y)
# #         if dist < 10:
# #             self.stuck_timer = 0.0
# #             return True

# #         step = max(1.0, min(3.4, self.speed * dt / 16.67))
# #         ux = (tx - self.x) / max(0.001, dist)
# #         uy = (ty - self.y) / max(0.001, dist)

# #         # Try the intended direction first, then progressively wider slides.
# #         base_angle = math.atan2(uy, ux)
# #         angles = [
# #             0.0,
# #             0.18, -0.18,
# #             0.35, -0.35,
# #             0.60, -0.60,
# #             0.90, -0.90,
# #             1.20, -1.20,
# #             math.pi / 2, -math.pi / 2,
# #             math.pi,
# #         ]

# #         best = None
# #         best_score = float('inf')

# #         for offset in angles:
# #             a = base_angle + offset
# #             vx = math.cos(a)
# #             vy = math.sin(a)
# #             nx = clamp(self.x + vx * step, 20, WORLD_WIDTH - 70)
# #             ny = clamp(self.y + vy * step, 20, WORLD_HEIGHT - 70)

# #             if not self.can_move_to(nx, ny, obstacles):
# #                 continue

# #             remaining = math.hypot(tx - nx, ty - ny)
# #             # Strongly prefer continuing toward the target, while still
# #             # allowing a sideways slide when an obstacle blocks the way.
# #             score = remaining + abs(offset) * 4.0
# #             if score < best_score:
# #                 best_score = score
# #                 best = (nx, ny)

# #         if best is not None:
# #             old_x, old_y = self.x, self.y
# #             self.x, self.y = best
# #             moved = math.hypot(self.x - old_x, self.y - old_y)
# #             if moved > 0.05:
# #                 self.stuck_timer = 0.0
# #                 return False

# #         # Completely blocked: immediately choose another nearby clear target.
# #         self.stuck_timer += dt / 1000.0
# #         if self.stuck_timer >= 0.20:
# #             safe = self._find_free_position(obstacles, 180)
# #             if safe is not None and not self.can_move_to(self.x, self.y, obstacles):
# #                 self.x, self.y = safe
# #                 self.sync_rect()

# #             self.stuck_timer = 0.0
# #             self.choose_new_destination(obstacles)
# #             self.wait_timer = 0.0

# #         return False

# #     def update(self, dt, obstacles, game_time_hour=None):
# #         if self.is_talking:
# #             return

# #         if game_time_hour is not None:
# #             self.update_home_state(game_time_hour, obstacles)

# #         seconds = max(0.001, dt / 1000.0)

# #         # At night, every NPC goes to their assigned house and stays there.
# #         if self.is_home:
# #             if self.house is None:
# #                 self.is_home = False
# #             else:
# #                 arrived = self._move_toward(self.home_target_x, self.home_target_y, dt, obstacles)
# #                 if arrived:
# #                     self.home_reached = True
# #                     self.x = self.home_target_x
# #                     self.y = self.home_target_y
# #                 self.sync_rect()
# #                 return

# #         self.wait_timer -= seconds
# #         if self.wait_timer > 0:
# #             return

# #         dx = self.target_x - self.x
# #         dy = self.target_y - self.y
# #         dist = math.hypot(dx, dy)
# #         if dist < 10:
# #             self.wait_timer = random.uniform(0.15, 0.7)
# #             self.stuck_timer = 0.0
# #             self.choose_new_destination(obstacles)
# #             self.sync_rect()
# #             return

# #         arrived = self._move_toward(self.target_x, self.target_y, dt, obstacles)
# #         if arrived:
# #             self.wait_timer = random.uniform(0.15, 0.7)
# #             self.choose_new_destination(obstacles)
# #         elif self.stuck_timer > 0.35:
# #             self.choose_new_destination(obstacles)
# #             self.stuck_timer = 0.0
# #             self.wait_timer = 0.0

# #         self.sync_rect()

# #     def draw(self, screen, camera, game):
# #         super().draw(screen, camera)
# #         sx, sy = camera.world_to_screen(self.x, self.y)
# #         name_surface = game.small_font.render(self.name, True, (255, 255, 255))
# #         name_rect = name_surface.get_rect(center=(sx + self.rect.width // 2, sy - 14))
# #         pygame.draw.rect(screen, (70, 55, 90), name_rect.inflate(10, 5), border_radius=8)
# #         screen.blit(name_surface, name_rect)
# #         marker = game.get_npc_marker(self)
# #         if marker:
# #             marker_surface = game.title_font.render(marker, True, (255, 230, 100))
# #             marker_rect = marker_surface.get_rect(center=(sx + self.rect.width // 2, sy - 48))
# #             screen.blit(marker_surface, marker_rect)

# #         if self.is_home:
# #             home_text = "HOME" if self.home_reached else "GOING HOME"
# #             home_surface = game.tiny_font.render(home_text, True, (190, 230, 255))
# #             home_rect = home_surface.get_rect(center=(sx + self.rect.width // 2, sy + 10))
# #             bg = home_rect.inflate(10, 4)
# #             pygame.draw.rect(screen, (45, 65, 95), bg, border_radius=7)
# #             screen.blit(home_surface, home_rect)


# from .core import *
# from .entities import Fairy


# class FairyNPC(Fairy):

#     # ============================================================
#     # INITIALIZATION
#     # ============================================================

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

#         # --------------------------------------------------------
#         # BASIC INFORMATION
#         # --------------------------------------------------------

#         self.spawn_x = float(x)
#         self.spawn_y = float(y)

#         self.dialogue = dialogue
#         self.dialogue_index = 0
#         self.is_talking = False

#         # Respect the radius supplied by WorldMixin.
#         self.wander_radius = max(
#             100.0,
#             float(wander_radius)
#         )

#         self.wander_min_distance = 80.0

#         # --------------------------------------------------------
#         # MOVEMENT
#         # --------------------------------------------------------

#         # Pixels per second.
#         self.speed = random.uniform(
#             75.0,
#             100.0
#         )

#         self.max_speed = self.speed

#         # Smooth acceleration/deceleration.
#         self.acceleration = random.uniform(
#             220.0,
#             300.0
#         )

#         self.deceleration = random.uniform(
#             300.0,
#             380.0
#         )

#         self.velocity_x = 0.0
#         self.velocity_y = 0.0

#         # Used to make walking feel less robotic.
#         self.walk_time = random.uniform(
#             0.0,
#             math.pi * 2
#         )

#         # --------------------------------------------------------
#         # TARGET
#         # --------------------------------------------------------

#         self.target_x = self.x
#         self.target_y = self.y

#         self.wait_timer = random.uniform(
#             0.4,
#             1.2
#         )

#         self.stuck_timer = 0.0

#         # --------------------------------------------------------
#         # QUEST
#         # --------------------------------------------------------

#         self.quest_ids = []

#         # --------------------------------------------------------
#         # HOUSE / NIGHT
#         # --------------------------------------------------------

#         self.house = None
#         self.is_home = False
#         self.home_reached = False

#         self.home_target_x = self.x
#         self.home_target_y = self.y

#         # --------------------------------------------------------
#         # PATH
#         # --------------------------------------------------------

#         self.path = []
#         self.path_index = 0

#         self.path_target_x = None
#         self.path_target_y = None

#         # --------------------------------------------------------
#         # INITIAL TARGET
#         # --------------------------------------------------------

#         self.choose_new_destination([])

#     # ============================================================
#     # COLLISION
#     # ============================================================

#     def _fairy_rect(
#         self,
#         x,
#         y
#     ):
#         return pygame.Rect(
#             int(x),
#             int(y),
#             self.rect.width,
#             self.rect.height
#         ).inflate(
#             4,
#             4
#         )

#     def _obstacle_visual_rect(
#         self,
#         obstacle
#     ):
#         rect = obstacle.rect

#         if obstacle.kind == "tree":
#             return rect.inflate(
#                 8,
#                 12
#             )

#         if obstacle.kind == "fence":
#             return rect.inflate(
#                 8,
#                 10
#             )

#         if obstacle.kind == "house":
#             return rect.inflate(
#                 16,
#                 16
#             )

#         if obstacle.kind == "rock":
#             return rect.inflate(
#                 8,
#                 8
#             )

#         return rect.inflate(
#             8,
#             8
#         )

#     def can_move_to(
#         self,
#         new_x,
#         new_y,
#         obstacles
#     ):
#         test_rect = self._fairy_rect(
#             new_x,
#             new_y
#         )

#         if test_rect.left < 0:
#             return False

#         if test_rect.top < 0:
#             return False

#         if test_rect.right > WORLD_WIDTH:
#             return False

#         if test_rect.bottom > WORLD_HEIGHT:
#             return False

#         for obstacle in obstacles:

#             if test_rect.colliderect(
#                 self._obstacle_visual_rect(obstacle)
#             ):
#                 return False

#         return True

#     # ============================================================
#     # HOUSE ASSIGNMENT
#     # ============================================================

#     def _find_home(
#         self,
#         obstacles
#     ):
#         if self.house is not None:
#             return

#         for obstacle in obstacles:

#             if obstacle.kind != "house":
#                 continue

#             if getattr(
#                 obstacle,
#                 "owner",
#                 None
#             ) != self.name:
#                 continue

#             self.house = obstacle

#             self.home_target_x = float(
#                 obstacle.rect.centerx
#                 - self.rect.width // 2
#             )

#             self.home_target_y = float(
#                 obstacle.rect.bottom + 22
#             )

#             break

#     # ============================================================
#     # LINE OF SIGHT
#     # ============================================================

#     def _line_is_clear(
#         self,
#         tx,
#         ty,
#         obstacles
#     ):
#         dx = tx - self.x
#         dy = ty - self.y

#         distance_to_target = math.hypot(
#             dx,
#             dy
#         )

#         if distance_to_target <= 1:
#             return True

#         steps = max(
#             2,
#             int(distance_to_target / 10)
#         )

#         for i in range(
#             1,
#             steps + 1
#         ):

#             t = i / steps

#             px = self.x + dx * t
#             py = self.y + dy * t

#             if not self.can_move_to(
#                 px,
#                 py,
#                 obstacles
#             ):
#                 return False

#         return True

#     # ============================================================
#     # FIND SAFE POSITION
#     # ============================================================

#     def _find_free_position(
#         self,
#         obstacles,
#         max_radius=180
#     ):
#         if self.can_move_to(
#             self.x,
#             self.y,
#             obstacles
#         ):
#             return (
#                 self.x,
#                 self.y
#             )

#         for radius in range(
#             20,
#             max_radius + 1,
#             20
#         ):

#             for angle_deg in range(
#                 0,
#                 360,
#                 15
#             ):

#                 angle = math.radians(
#                     angle_deg
#                 )

#                 nx = clamp(
#                     self.x
#                     + math.cos(angle) * radius,
#                     20,
#                     WORLD_WIDTH - 70
#                 )

#                 ny = clamp(
#                     self.y
#                     + math.sin(angle) * radius,
#                     20,
#                     WORLD_HEIGHT - 70
#                 )

#                 if self.can_move_to(
#                     nx,
#                     ny,
#                     obstacles
#                 ):
#                     return (
#                         nx,
#                         ny
#                     )

#         return None

#     # ============================================================
#     # LOCAL A*
#     # ============================================================

#     def _build_local_path(
#         self,
#         tx,
#         ty,
#         obstacles
#     ):
#         """
#         Build a local path only when the NPC cannot walk directly
#         to its destination.
#         """

#         grid = 35
#         margin = 180

#         left = int(
#             clamp(
#                 min(self.x, tx) - margin,
#                 0,
#                 WORLD_WIDTH - grid
#             )
#         )

#         top = int(
#             clamp(
#                 min(self.y, ty) - margin,
#                 0,
#                 WORLD_HEIGHT - grid
#             )
#         )

#         right = int(
#             clamp(
#                 max(self.x, tx) + margin,
#                 grid,
#                 WORLD_WIDTH
#             )
#         )

#         bottom = int(
#             clamp(
#                 max(self.y, ty) + margin,
#                 grid,
#                 WORLD_HEIGHT
#             )
#         )

#         cols = max(
#             1,
#             min(
#                 45,
#                 (right - left) // grid + 1
#             )
#         )

#         rows = max(
#             1,
#             min(
#                 45,
#                 (bottom - top) // grid + 1
#             )
#         )

#         def node_at(
#             x,
#             y
#         ):
#             return (
#                 int(
#                     clamp(
#                         (x - left) // grid,
#                         0,
#                         cols - 1
#                     )
#                 ),
#                 int(
#                     clamp(
#                         (y - top) // grid,
#                         0,
#                         rows - 1
#                     )
#                 )
#             )

#         def center(
#             node
#         ):
#             gx, gy = node

#             return (
#                 left
#                 + gx * grid
#                 + grid // 2,

#                 top
#                 + gy * grid
#                 + grid // 2
#             )

#         def walkable(
#             node
#         ):
#             x, y = center(node)

#             return self.can_move_to(
#                 x,
#                 y,
#                 obstacles
#             )

#         start = node_at(
#             self.x,
#             self.y
#         )

#         goal = node_at(
#             tx,
#             ty
#         )

#         # --------------------------------------------------------
#         # Find a nearby walkable goal.
#         # --------------------------------------------------------

#         if not walkable(goal):

#             candidates = []

#             for radius in range(
#                 1,
#                 6
#             ):

#                 for gx in range(
#                     max(
#                         0,
#                         goal[0] - radius
#                     ),
#                     min(
#                         cols,
#                         goal[0] + radius + 1
#                     )
#                 ):

#                     for gy in range(
#                         max(
#                             0,
#                             goal[1] - radius
#                         ),
#                         min(
#                             rows,
#                             goal[1] + radius + 1
#                         )
#                     ):

#                         node = (
#                             gx,
#                             gy
#                         )

#                         if walkable(node):
#                             candidates.append(
#                                 node
#                             )

#                 if candidates:
#                     goal = min(
#                         candidates,
#                         key=lambda n:
#                         abs(
#                             n[0] - goal[0]
#                         )
#                         +
#                         abs(
#                             n[1] - goal[1]
#                         )
#                     )
#                     break

#         if not walkable(start):
#             safe = self._find_free_position(
#                 obstacles,
#                 180
#             )

#             if safe is None:
#                 self.path = []
#                 self.path_index = 0
#                 return False

#             self.x = float(
#                 safe[0]
#             )

#             self.y = float(
#                 safe[1]
#             )

#             self.sync_rect()

#             start = node_at(
#                 self.x,
#                 self.y
#             )

#         if not walkable(goal):
#             self.path = []
#             self.path_index = 0
#             return False

#         # --------------------------------------------------------
#         # A*
#         # --------------------------------------------------------

#         open_heap = []

#         heapq.heappush(
#             open_heap,
#             (
#                 0.0,
#                 start
#             )
#         )

#         came_from = {}
#         g_score = {
#             start: 0.0
#         }

#         visited = set()

#         neighbors = [
#             (-1, 0),
#             (1, 0),
#             (0, -1),
#             (0, 1),

#             (-1, -1),
#             (-1, 1),
#             (1, -1),
#             (1, 1)
#         ]

#         while open_heap:

#             _, current = heapq.heappop(
#                 open_heap
#             )

#             if current in visited:
#                 continue

#             visited.add(current)

#             if current == goal:

#                 path = []

#                 while current != start:

#                     path.append(
#                         center(current)
#                     )

#                     current = came_from[current]

#                 path.reverse()

#                 # ------------------------------------------------
#                 # Remove unnecessary waypoints.
#                 # ------------------------------------------------

#                 simplified = []

#                 if path:

#                     current_x = self.x
#                     current_y = self.y

#                     for point in path:

#                         if self._line_is_clear_from(
#                             current_x,
#                             current_y,
#                             point[0],
#                             point[1],
#                             obstacles
#                         ):
#                             continue

#                         previous = path[
#                             max(
#                                 0,
#                                 len(simplified) - 1
#                             )
#                         ] if simplified else (
#                             current_x,
#                             current_y
#                         )

#                         simplified.append(
#                             point
#                         )

#                         current_x = point[0]
#                         current_y = point[1]

#                 if not simplified and path:
#                     simplified = [
#                         path[-1]
#                     ]

#                 self.path = simplified
#                 self.path_index = 0

#                 return bool(
#                     self.path
#                 )

#             for ox, oy in neighbors:

#                 nxt = (
#                     current[0] + ox,
#                     current[1] + oy
#                 )

#                 if not (
#                     0 <= nxt[0] < cols
#                     and
#                     0 <= nxt[1] < rows
#                 ):
#                     continue

#                 if not walkable(nxt):
#                     continue

#                 # Prevent diagonal corner cutting.
#                 if ox and oy:

#                     side_a = (
#                         current[0] + ox,
#                         current[1]
#                     )

#                     side_b = (
#                         current[0],
#                         current[1] + oy
#                     )

#                     if (
#                         not walkable(side_a)
#                         or
#                         not walkable(side_b)
#                     ):
#                         continue

#                 cost = (
#                     1.414
#                     if ox and oy
#                     else 1.0
#                 )

#                 tentative = (
#                     g_score[current]
#                     + cost
#                 )

#                 if tentative < g_score.get(
#                     nxt,
#                     float("inf")
#                 ):

#                     came_from[nxt] = current
#                     g_score[nxt] = tentative

#                     h = math.hypot(
#                         goal[0] - nxt[0],
#                         goal[1] - nxt[1]
#                     )

#                     heapq.heappush(
#                         open_heap,
#                         (
#                             tentative + h,
#                             nxt
#                         )
#                     )

#         self.path = []
#         self.path_index = 0

#         return False

#     # ============================================================
#     # LINE CHECK FROM ARBITRARY POSITION
#     # ============================================================

#     def _line_is_clear_from(
#         self,
#         x1,
#         y1,
#         x2,
#         y2,
#         obstacles
#     ):
#         dx = x2 - x1
#         dy = y2 - y1

#         length = math.hypot(
#             dx,
#             dy
#         )

#         if length <= 1:
#             return True

#         steps = max(
#             2,
#             int(length / 12)
#         )

#         for i in range(
#             1,
#             steps + 1
#         ):

#             t = i / steps

#             x = x1 + dx * t
#             y = y1 + dy * t

#             if not self.can_move_to(
#                 x,
#                 y,
#                 obstacles
#             ):
#                 return False

#         return True

#     # ============================================================
#     # CHOOSE DESTINATION
#     # ============================================================

#     def choose_new_destination(
#         self,
#         obstacles=None
#     ):
#         if obstacles is None:
#             obstacles = []

#         # --------------------------------------------------------
#         # Make sure current position is valid.
#         # --------------------------------------------------------

#         if not self.can_move_to(
#             self.x,
#             self.y,
#             obstacles
#         ):

#             safe = self._find_free_position(
#                 obstacles
#             )

#             if safe is not None:

#                 self.x = float(
#                     safe[0]
#                 )

#                 self.y = float(
#                     safe[1]
#                 )

#                 self.sync_rect()

#         candidates = []

#         # --------------------------------------------------------
#         # Generate destinations around the ORIGINAL roaming area.
#         # This prevents the NPC from slowly drifting across the
#         # entire world.
#         # --------------------------------------------------------

#         for _ in range(80):

#             angle = random.uniform(
#                 0,
#                 math.tau
#             )

#             radius = random.uniform(
#                 self.wander_min_distance,
#                 self.wander_radius
#             )

#             tx = clamp(
#                 self.spawn_x
#                 + math.cos(angle) * radius,
#                 80,
#                 WORLD_WIDTH - 100
#             )

#             ty = clamp(
#                 self.spawn_y
#                 + math.sin(angle) * radius,
#                 80,
#                 WORLD_HEIGHT - 100
#             )

#             distance_from_current = math.hypot(
#                 tx - self.x,
#                 ty - self.y
#             )

#             if distance_from_current < 60:
#                 continue

#             if not self.can_move_to(
#                 tx,
#                 ty,
#                 obstacles
#             ):
#                 continue

#             candidates.append(
#                 (
#                     tx,
#                     ty
#                 )
#             )

#         # --------------------------------------------------------
#         # Prefer a direct destination.
#         # --------------------------------------------------------

#         random.shuffle(
#             candidates
#         )

#         for tx, ty in candidates:

#             if self._line_is_clear(
#                 tx,
#                 ty,
#                 obstacles
#             ):

#                 self.target_x = float(
#                     tx
#                 )

#                 self.target_y = float(
#                     ty
#                 )

#                 self.path = []
#                 self.path_index = 0

#                 return True

#         # --------------------------------------------------------
#         # If no direct destination exists, try a small number
#         # of pathfinding destinations.
#         # --------------------------------------------------------

#         for tx, ty in candidates[:12]:

#             if self._build_local_path(
#                 tx,
#                 ty,
#                 obstacles
#             ):

#                 self.target_x = float(
#                     tx
#                 )

#                 self.target_y = float(
#                     ty
#                 )

#                 self.path_target_x = self.target_x
#                 self.path_target_y = self.target_y

#                 return True

#         # --------------------------------------------------------
#         # Last resort: nearby movement.
#         # --------------------------------------------------------

#         for radius in (
#             45,
#             65,
#             90,
#             120,
#             150
#         ):

#             for angle_deg in range(
#                 0,
#                 360,
#                 30
#             ):

#                 angle = math.radians(
#                     angle_deg
#                 )

#                 tx = clamp(
#                     self.x
#                     + math.cos(angle) * radius,
#                     30,
#                     WORLD_WIDTH - 80
#                 )

#                 ty = clamp(
#                     self.y
#                     + math.sin(angle) * radius,
#                     30,
#                     WORLD_HEIGHT - 80
#                 )

#                 if not self.can_move_to(
#                     tx,
#                     ty,
#                     obstacles
#                 ):
#                     continue

#                 self.target_x = float(
#                     tx
#                 )

#                 self.target_y = float(
#                     ty
#                 )

#                 self.path = []
#                 self.path_index = 0

#                 return True

#         # No valid movement.
#         self.target_x = self.x
#         self.target_y = self.y

#         self.path = []
#         self.path_index = 0

#         return False

#     # ============================================================
#     # HOME
#     # ============================================================

#     def set_home(
#         self,
#         house
#     ):
#         self.house = house

#         if house is None:
#             return

#         self.home_target_x = float(
#             house.rect.centerx
#             - self.rect.width // 2
#         )

#         self.home_target_y = float(
#             house.rect.bottom + 22
#         )

#     def update_home_state(
#         self,
#         game_time_hour,
#         obstacles
#     ):
#         self._find_home(
#             obstacles
#         )

#         night = (
#             game_time_hour >= NPC_HOME_HOUR
#             or
#             game_time_hour < NPC_WAKE_HOUR
#         )

#         if night and not self.is_home:

#             self.is_home = True
#             self.home_reached = False

#             self.path = []
#             self.path_index = 0

#             self.velocity_x = 0.0
#             self.velocity_y = 0.0

#             if self.house is not None:

#                 self.home_target_x = float(
#                     self.house.rect.centerx
#                     - self.rect.width // 2
#                 )

#                 self.home_target_y = float(
#                     self.house.rect.bottom + 22
#                 )

#         elif not night and self.is_home:

#             self.is_home = False
#             self.home_reached = False

#             self.path = []
#             self.path_index = 0

#             self.wait_timer = random.uniform(
#                 0.5,
#                 1.2
#             )

#             self.choose_new_destination(
#                 obstacles
#             )

#     # ============================================================
#     # SMOOTH MOVEMENT
#     # ============================================================

#     def _move_smoothly(
#         self,
#         tx,
#         ty,
#         dt,
#         obstacles
#     ):
#         seconds = max(
#             0.001,
#             dt / 1000.0
#         )

#         dx = tx - self.x
#         dy = ty - self.y

#         distance_to_target = math.hypot(
#             dx,
#             dy
#         )

#         # --------------------------------------------------------
#         # Arrival
#         # --------------------------------------------------------

#         if distance_to_target <= 7:

#             self.velocity_x = 0.0
#             self.velocity_y = 0.0

#             self.x = float(tx)
#             self.y = float(ty)

#             return True

#         # --------------------------------------------------------
#         # Direction
#         # --------------------------------------------------------

#         desired_x = dx / distance_to_target
#         desired_y = dy / distance_to_target

#         # --------------------------------------------------------
#         # Slow down before reaching destination.
#         # --------------------------------------------------------

#         slow_radius = 100.0

#         if distance_to_target < slow_radius:

#             speed_ratio = (
#                 distance_to_target
#                 / slow_radius
#             )

#             speed_ratio = clamp(
#                 speed_ratio,
#                 0.20,
#                 1.0
#             )

#             desired_speed = (
#                 self.max_speed
#                 * speed_ratio
#             )

#         else:

#             desired_speed = self.max_speed

#         desired_vx = (
#             desired_x
#             * desired_speed
#         )

#         desired_vy = (
#             desired_y
#             * desired_speed
#         )

#         # --------------------------------------------------------
#         # Smooth acceleration.
#         # --------------------------------------------------------

#         if desired_speed < math.hypot(
#             self.velocity_x,
#             self.velocity_y
#         ):

#             change = (
#                 self.deceleration
#                 * seconds
#             )

#         else:

#             change = (
#                 self.acceleration
#                 * seconds
#             )

#         current_speed = math.hypot(
#             self.velocity_x,
#             self.velocity_y
#         )

#         if current_speed > 0:

#             current_angle = math.atan2(
#                 self.velocity_y,
#                 self.velocity_x
#             )

#         else:

#             current_angle = math.atan2(
#                 desired_vy,
#                 desired_vx
#             )

#         desired_angle = math.atan2(
#             desired_vy,
#             desired_vx
#         )

#         # Smoothly rotate toward desired direction.
#         angle_difference = (
#             desired_angle
#             - current_angle
#         )

#         while angle_difference > math.pi:
#             angle_difference -= math.tau

#         while angle_difference < -math.pi:
#             angle_difference += math.tau

#         max_turn = (
#             5.0
#             * seconds
#         )

#         angle_difference = clamp(
#             angle_difference,
#             -max_turn,
#             max_turn
#         )

#         new_angle = (
#             current_angle
#             + angle_difference
#         )

#         new_speed = current_speed

#         if new_speed < desired_speed:

#             new_speed = min(
#                 desired_speed,
#                 new_speed + change
#             )

#         elif new_speed > desired_speed:

#             new_speed = max(
#                 desired_speed,
#                 new_speed - change
#             )

#         self.velocity_x = (
#             math.cos(new_angle)
#             * new_speed
#         )

#         self.velocity_y = (
#             math.sin(new_angle)
#             * new_speed
#         )

#         # --------------------------------------------------------
#         # Prevent overshooting the target.
#         # --------------------------------------------------------

#         movement_distance = (
#             new_speed
#             * seconds
#         )

#         if movement_distance >= distance_to_target:

#             self.x = float(tx)
#             self.y = float(ty)

#             self.velocity_x = 0.0
#             self.velocity_y = 0.0

#             return True

#         # --------------------------------------------------------
#         # Collision-aware movement.
#         #
#         # Try full movement first.
#         # If blocked, try X and Y independently so the fairy
#         # slides smoothly along an obstacle instead of bouncing.
#         # --------------------------------------------------------

#         new_x = (
#             self.x
#             + self.velocity_x
#             * seconds
#         )

#         new_y = (
#             self.y
#             + self.velocity_y
#             * seconds
#         )

#         moved = False

#         # Full movement.
#         if self.can_move_to(
#             new_x,
#             new_y,
#             obstacles
#         ):

#             self.x = new_x
#             self.y = new_y

#             moved = True

#         else:

#             # X only.
#             if self.can_move_to(
#                 new_x,
#                 self.y,
#                 obstacles
#             ):

#                 self.x = new_x
#                 moved = True

#             else:

#                 self.velocity_x *= 0.35

#             # Y only.
#             if self.can_move_to(
#                 self.x,
#                 new_y,
#                 obstacles
#             ):

#                 self.y = new_y
#                 moved = True

#             else:

#                 self.velocity_y *= 0.35

#         if moved:

#             self.stuck_timer = 0.0

#         else:

#             self.stuck_timer += seconds

#         return False

#     # ============================================================
#     # GET CURRENT TARGET
#     # ============================================================

#     def _get_current_target(
#         self,
#         obstacles
#     ):
#         # If following a path, use the current waypoint.
#         if self.path:

#             if self.path_index >= len(
#                 self.path
#             ):

#                 self.path = []
#                 self.path_index = 0

#             else:

#                 return self.path[
#                     self.path_index
#                 ]

#         return (
#             self.target_x,
#             self.target_y
#         )

#     # ============================================================
#     # UPDATE
#     # ============================================================

#     def update(
#         self,
#         dt,
#         obstacles,
#         game_time_hour=None
#     ):

#         seconds = max(
#             0.001,
#             dt / 1000.0
#         )

#         # --------------------------------------------------------
#         # Find home automatically.
#         # --------------------------------------------------------

#         self._find_home(
#             obstacles
#         )

#         # --------------------------------------------------------
#         # Day/night.
#         # --------------------------------------------------------

#         if game_time_hour is not None:

#             self.update_home_state(
#                 game_time_hour,
#                 obstacles
#             )

#         # --------------------------------------------------------
#         # Dialogue.
#         #
#         # Don't instantly freeze. Decelerate naturally.
#         # --------------------------------------------------------

#         if self.is_talking:

#             self.velocity_x = self._approach(
#                 self.velocity_x,
#                 0.0,
#                 self.deceleration * seconds
#             )

#             self.velocity_y = self._approach(
#                 self.velocity_y,
#                 0.0,
#                 self.deceleration * seconds
#             )

#             self.x += (
#                 self.velocity_x
#                 * seconds
#             )

#             self.y += (
#                 self.velocity_y
#                 * seconds
#             )

#             self.sync_rect()

#             return

#         # --------------------------------------------------------
#         # Going home.
#         # --------------------------------------------------------

#         if self.is_home:

#             if self.house is None:

#                 self.is_home = False

#             else:

#                 # Build a path around obstacles if necessary.
#                 if (
#                     not self._line_is_clear(
#                         self.home_target_x,
#                         self.home_target_y,
#                         obstacles
#                     )
#                     and
#                     not self.path
#                 ):

#                     self._build_local_path(
#                         self.home_target_x,
#                         self.home_target_y,
#                         obstacles
#                     )

#                 target = self._get_current_target(
#                     obstacles
#                 )

#                 arrived = self._move_smoothly(
#                     target[0],
#                     target[1],
#                     dt,
#                     obstacles
#                 )

#                 if arrived:

#                     if self.path:

#                         self.path_index += 1

#                         if self.path_index >= len(
#                             self.path
#                         ):

#                             self.path = []
#                             self.path_index = 0

#                             self.x = self.home_target_x
#                             self.y = self.home_target_y

#                             self.velocity_x = 0.0
#                             self.velocity_y = 0.0

#                             self.home_reached = True

#                     else:

#                         self.home_reached = True

#                         self.x = self.home_target_x
#                         self.y = self.home_target_y

#                         self.velocity_x = 0.0
#                         self.velocity_y = 0.0

#                 self.sync_rect()

#                 return

#         # --------------------------------------------------------
#         # Waiting.
#         # --------------------------------------------------------

#         self.wait_timer -= seconds

#         if self.wait_timer > 0:

#             self.velocity_x = self._approach(
#                 self.velocity_x,
#                 0.0,
#                 self.deceleration * seconds
#             )

#             self.velocity_y = self._approach(
#                 self.velocity_y,
#                 0.0,
#                 self.deceleration * seconds
#             )

#             if abs(self.velocity_x) < 0.5:
#                 self.velocity_x = 0.0

#             if abs(self.velocity_y) < 0.5:
#                 self.velocity_y = 0.0

#             self.sync_rect()

#             return

#         # --------------------------------------------------------
#         # Make sure we have a destination.
#         # --------------------------------------------------------

#         distance_to_target = math.hypot(
#             self.target_x - self.x,
#             self.target_y - self.y
#         )

#         if distance_to_target < 10:

#             self.velocity_x = self._approach(
#                 self.velocity_x,
#                 0.0,
#                 self.deceleration * seconds
#             )

#             self.velocity_y = self._approach(
#                 self.velocity_y,
#                 0.0,
#                 self.deceleration * seconds
#             )

#             if (
#                 abs(self.velocity_x) < 0.5
#                 and
#                 abs(self.velocity_y) < 0.5
#             ):

#                 self.velocity_x = 0.0
#                 self.velocity_y = 0.0

#                 self.wait_timer = random.uniform(
#                     0.5,
#                     1.6
#                 )

#                 self.choose_new_destination(
#                     obstacles
#                 )

#             self.sync_rect()

#             return

#         # --------------------------------------------------------
#         # If the direct route is blocked and we have no path,
#         # build one.
#         # --------------------------------------------------------

#         if (
#             not self.path
#             and
#             not self._line_is_clear(
#                 self.target_x,
#                 self.target_y,
#                 obstacles
#             )
#         ):

#             self._build_local_path(
#                 self.target_x,
#                 self.target_y,
#                 obstacles
#             )

#         # --------------------------------------------------------
#         # Get movement target.
#         # --------------------------------------------------------

#         target_x, target_y = self._get_current_target(
#             obstacles
#         )

#         arrived = self._move_smoothly(
#             target_x,
#             target_y,
#             dt,
#             obstacles
#         )

#         # --------------------------------------------------------
#         # Reached path waypoint.
#         # --------------------------------------------------------

#         if arrived and self.path:

#             self.path_index += 1

#             if self.path_index >= len(
#                 self.path
#             ):

#                 self.path = []
#                 self.path_index = 0

#                 self.target_x = float(
#                     self.target_x
#                 )

#                 self.target_y = float(
#                     self.target_y
#                 )

#                 self.velocity_x = 0.0
#                 self.velocity_y = 0.0

#                 self.wait_timer = random.uniform(
#                     0.5,
#                     1.6
#                 )

#                 self.choose_new_destination(
#                     obstacles
#                 )

#         # --------------------------------------------------------
#         # Normal target reached.
#         # --------------------------------------------------------

#         elif arrived:

#             self.velocity_x = 0.0
#             self.velocity_y = 0.0

#             self.wait_timer = random.uniform(
#                 0.5,
#                 1.6
#             )

#             self.choose_new_destination(
#                 obstacles
#             )

#         # --------------------------------------------------------
#         # NPC has been unable to move for too long.
#         # --------------------------------------------------------

#         if self.stuck_timer > 0.8:

#             self.velocity_x = 0.0
#             self.velocity_y = 0.0

#             self.path = []
#             self.path_index = 0

#             self.stuck_timer = 0.0

#             self.choose_new_destination(
#                 obstacles
#             )

#             self.wait_timer = 0.2

#         self.sync_rect()

#     # ============================================================
#     # APPROACH
#     # ============================================================

#     def _approach(
#         self,
#         current,
#         target,
#         amount
#     ):
#         if current < target:

#             return min(
#                 current + amount,
#                 target
#             )

#         if current > target:

#             return max(
#                 current - amount,
#                 target
#             )

#         return target

#     # ============================================================
#     # DRAW
#     # ============================================================

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

#         # --------------------------------------------------------
#         # Name
#         # --------------------------------------------------------

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

#         pygame.draw.rect(
#             screen,
#             (70, 55, 90),
#             name_rect.inflate(
#                 10,
#                 5
#             ),
#             border_radius=8
#         )

#         screen.blit(
#             name_surface,
#             name_rect
#         )

#         # --------------------------------------------------------
#         # Quest marker
#         # --------------------------------------------------------

#         marker = game.get_npc_marker(
#             self
#         )

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

#         # --------------------------------------------------------
#         # Home indicator
#         # --------------------------------------------------------

#         if self.is_home:

#             home_text = (
#                 "HOME"
#                 if self.home_reached
#                 else
#                 "GOING HOME"
#             )

#             home_surface = game.tiny_font.render(
#                 home_text,
#                 True,
#                 (190, 230, 255)
#             )

#             home_rect = home_surface.get_rect(
#                 center=(
#                     sx + self.rect.width // 2,
#                     sy + 10
#                 )
#             )

#             bg = home_rect.inflate(
#                 10,
#                 4
#             )

#             pygame.draw.rect(
#                 screen,
#                 (45, 65, 95),
#                 bg,
#                 border_radius=7
#             )

#             screen.blit(
#                 home_surface,
#                 home_rect
#             )



from .core import *
from .entities import Fairy


class FairyNPC(Fairy):

    # ============================================================
    # INITIALIZATION
    # ============================================================

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

        # --------------------------------------------------------
        # BASIC INFORMATION
        # --------------------------------------------------------

        self.spawn_x = float(x)
        self.spawn_y = float(y)

        self.dialogue = dialogue
        self.dialogue_index = 0
        self.is_talking = False

        # Maximum distance for ONE wandering destination.
        #
        # IMPORTANT:
        # This is no longer measured from spawn_x/spawn_y.
        # It is measured from the NPC's CURRENT position.
        #
        # This allows the NPC to gradually explore the entire map.
        self.wander_radius = max(
            100.0,
            float(wander_radius)
        )

        self.wander_min_distance = 80.0

        # --------------------------------------------------------
        # MOVEMENT
        # --------------------------------------------------------

        # Pixels per second.
        self.speed = random.uniform(
            75.0,
            100.0
        )

        self.max_speed = self.speed

        # Smooth acceleration/deceleration.
        self.acceleration = random.uniform(
            220.0,
            300.0
        )

        self.deceleration = random.uniform(
            300.0,
            380.0
        )

        self.velocity_x = 0.0
        self.velocity_y = 0.0

        self.walk_time = random.uniform(
            0.0,
            math.pi * 2
        )

        # --------------------------------------------------------
        # TARGET
        # --------------------------------------------------------

        self.target_x = self.x
        self.target_y = self.y

        self.wait_timer = random.uniform(
            0.4,
            1.2
        )

        self.stuck_timer = 0.0

        # --------------------------------------------------------
        # QUEST
        # --------------------------------------------------------

        self.quest_ids = []

        # --------------------------------------------------------
        # HOUSE / NIGHT
        # --------------------------------------------------------

        self.house = None

        self.is_home = False
        self.home_reached = False

        self.home_target_x = self.x
        self.home_target_y = self.y

        # --------------------------------------------------------
        # PATH
        # --------------------------------------------------------

        self.path = []
        self.path_index = 0

        self.path_target_x = None
        self.path_target_y = None

        # --------------------------------------------------------
        # INITIAL TARGET
        # --------------------------------------------------------

        self.choose_new_destination([])

    # ============================================================
    # COLLISION
    # ============================================================

    def _fairy_rect(
        self,
        x,
        y
    ):
        return pygame.Rect(
            int(x),
            int(y),
            self.rect.width,
            self.rect.height
        ).inflate(
            4,
            4
        )

    def _obstacle_visual_rect(
        self,
        obstacle
    ):
        rect = obstacle.rect

        if obstacle.kind == "tree":
            return rect.inflate(
                8,
                12
            )

        if obstacle.kind == "fence":
            return rect.inflate(
                8,
                10
            )

        if obstacle.kind == "house":
            return rect.inflate(
                16,
                16
            )

        if obstacle.kind == "rock":
            return rect.inflate(
                8,
                8
            )

        return rect.inflate(
            8,
            8
        )

    def can_move_to(
        self,
        new_x,
        new_y,
        obstacles
    ):
        test_rect = self._fairy_rect(
            new_x,
            new_y
        )

        # --------------------------------------------------------
        # WORLD BOUNDS
        # --------------------------------------------------------

        if test_rect.left < 0:
            return False

        if test_rect.top < 0:
            return False

        if test_rect.right > WORLD_WIDTH:
            return False

        if test_rect.bottom > WORLD_HEIGHT:
            return False

        # --------------------------------------------------------
        # OBSTACLES
        # --------------------------------------------------------

        for obstacle in obstacles:

            if test_rect.colliderect(
                self._obstacle_visual_rect(obstacle)
            ):
                return False

        return True

    # ============================================================
    # HOUSE ASSIGNMENT
    # ============================================================

    def _find_home(
        self,
        obstacles
    ):
        if self.house is not None:
            return

        for obstacle in obstacles:

            if obstacle.kind != "house":
                continue

            if getattr(
                obstacle,
                "owner",
                None
            ) != self.name:
                continue

            self.house = obstacle

            self.home_target_x = float(
                obstacle.rect.centerx
                - self.rect.width // 2
            )

            self.home_target_y = float(
                obstacle.rect.bottom + 22
            )

            break

    # ============================================================
    # LINE OF SIGHT
    # ============================================================

    def _line_is_clear(
        self,
        tx,
        ty,
        obstacles
    ):
        dx = tx - self.x
        dy = ty - self.y

        distance_to_target = math.hypot(
            dx,
            dy
        )

        if distance_to_target <= 1:
            return True

        steps = max(
            2,
            int(distance_to_target / 10)
        )

        for i in range(
            1,
            steps + 1
        ):
            t = i / steps

            px = self.x + dx * t
            py = self.y + dy * t

            if not self.can_move_to(
                px,
                py,
                obstacles
            ):
                return False

        return True

    # ============================================================
    # FIND SAFE POSITION
    # ============================================================

    def _find_free_position(
        self,
        obstacles,
        max_radius=250
    ):
        # --------------------------------------------------------
        # Current position is already safe.
        # --------------------------------------------------------

        if self.can_move_to(
            self.x,
            self.y,
            obstacles
        ):
            return (
                self.x,
                self.y
            )

        # --------------------------------------------------------
        # Search outward in circles.
        # --------------------------------------------------------

        for radius in range(
            20,
            max_radius + 1,
            20
        ):

            # Randomize the search direction so NPCs don't always
            # escape obstacles in the same direction.
            angles = list(
                range(
                    0,
                    360,
                    15
                )
            )

            random.shuffle(
                angles
            )

            for angle_deg in angles:

                angle = math.radians(
                    angle_deg
                )

                nx = clamp(
                    self.x
                    + math.cos(angle) * radius,
                    20,
                    WORLD_WIDTH - 70
                )

                ny = clamp(
                    self.y
                    + math.sin(angle) * radius,
                    20,
                    WORLD_HEIGHT - 70
                )

                if self.can_move_to(
                    nx,
                    ny,
                    obstacles
                ):
                    return (
                        nx,
                        ny
                    )

        return None

    # ============================================================
    # LOCAL A*
    # ============================================================

    def _build_local_path(
        self,
        tx,
        ty,
        obstacles
    ):
        """
        Build a local A* path only when a direct route is blocked.

        The search is intentionally local instead of searching the
        entire 4000x3000 world every frame.
        """

        grid = 35
        margin = 220

        left = int(
            clamp(
                min(self.x, tx) - margin,
                0,
                WORLD_WIDTH - grid
            )
        )

        top = int(
            clamp(
                min(self.y, ty) - margin,
                0,
                WORLD_HEIGHT - grid
            )
        )

        right = int(
            clamp(
                max(self.x, tx) + margin,
                grid,
                WORLD_WIDTH
            )
        )

        bottom = int(
            clamp(
                max(self.y, ty) + margin,
                grid,
                WORLD_HEIGHT
            )
        )

        cols = max(
            1,
            min(
                55,
                (right - left) // grid + 1
            )
        )

        rows = max(
            1,
            min(
                55,
                (bottom - top) // grid + 1
            )
        )

        # --------------------------------------------------------
        # Convert world position to grid node.
        # --------------------------------------------------------

        def node_at(
            x,
            y
        ):
            return (
                int(
                    clamp(
                        (x - left) // grid,
                        0,
                        cols - 1
                    )
                ),
                int(
                    clamp(
                        (y - top) // grid,
                        0,
                        rows - 1
                    )
                )
            )

        # --------------------------------------------------------
        # Convert grid node to world position.
        # --------------------------------------------------------

        def center(
            node
        ):
            gx, gy = node

            return (
                left
                + gx * grid
                + grid // 2,

                top
                + gy * grid
                + grid // 2
            )

        # --------------------------------------------------------
        # Check whether grid node is walkable.
        # --------------------------------------------------------

        def walkable(
            node
        ):
            x, y = center(node)

            return self.can_move_to(
                x,
                y,
                obstacles
            )

        start = node_at(
            self.x,
            self.y
        )

        goal = node_at(
            tx,
            ty
        )

        # --------------------------------------------------------
        # Find nearest valid goal.
        # --------------------------------------------------------

        if not walkable(goal):

            candidates = []

            for radius in range(
                1,
                7
            ):

                for gx in range(
                    max(
                        0,
                        goal[0] - radius
                    ),
                    min(
                        cols,
                        goal[0] + radius + 1
                    )
                ):

                    for gy in range(
                        max(
                            0,
                            goal[1] - radius
                        ),
                        min(
                            rows,
                            goal[1] + radius + 1
                        )
                    ):

                        node = (
                            gx,
                            gy
                        )

                        if walkable(node):

                            candidates.append(
                                node
                            )

                if candidates:

                    goal = min(
                        candidates,
                        key=lambda n:
                        abs(
                            n[0] - goal[0]
                        )
                        +
                        abs(
                            n[1] - goal[1]
                        )
                    )

                    break

        # --------------------------------------------------------
        # Fix blocked starting position.
        # --------------------------------------------------------

        if not walkable(start):

            safe = self._find_free_position(
                obstacles,
                250
            )

            if safe is None:

                self.path = []
                self.path_index = 0

                return False

            self.x = float(
                safe[0]
            )

            self.y = float(
                safe[1]
            )

            self.sync_rect()

            start = node_at(
                self.x,
                self.y
            )

        if not walkable(goal):

            self.path = []
            self.path_index = 0

            return False

        # --------------------------------------------------------
        # A*
        # --------------------------------------------------------

        open_heap = []

        heapq.heappush(
            open_heap,
            (
                0.0,
                start
            )
        )

        came_from = {}

        g_score = {
            start: 0.0
        }

        visited = set()

        neighbors = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),

            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1)
        ]

        while open_heap:

            _, current = heapq.heappop(
                open_heap
            )

            if current in visited:
                continue

            visited.add(
                current
            )

            # ----------------------------------------------------
            # Goal reached.
            # ----------------------------------------------------

            if current == goal:

                path = []

                while current != start:

                    path.append(
                        center(current)
                    )

                    current = came_from[current]

                path.reverse()

                # ------------------------------------------------
                # Simplify the path.
                # ------------------------------------------------

                simplified = []

                current_x = self.x
                current_y = self.y

                for point in path:

                    if self._line_is_clear_from(
                        current_x,
                        current_y,
                        point[0],
                        point[1],
                        obstacles
                    ):
                        # We can skip this waypoint because the
                        # next point is still reachable.
                        continue

                    simplified.append(
                        point
                    )

                    current_x = point[0]
                    current_y = point[1]

                if not simplified and path:

                    simplified = [
                        path[-1]
                    ]

                self.path = simplified
                self.path_index = 0

                return bool(
                    self.path
                )

            # ----------------------------------------------------
            # Explore neighbors.
            # ----------------------------------------------------

            for ox, oy in neighbors:

                nxt = (
                    current[0] + ox,
                    current[1] + oy
                )

                if not (
                    0 <= nxt[0] < cols
                    and
                    0 <= nxt[1] < rows
                ):
                    continue

                if not walkable(nxt):
                    continue

                # ------------------------------------------------
                # Prevent diagonal corner cutting.
                # ------------------------------------------------

                if ox and oy:

                    side_a = (
                        current[0] + ox,
                        current[1]
                    )

                    side_b = (
                        current[0],
                        current[1] + oy
                    )

                    if (
                        not walkable(side_a)
                        or
                        not walkable(side_b)
                    ):
                        continue

                cost = (
                    1.414
                    if ox and oy
                    else 1.0
                )

                tentative = (
                    g_score[current]
                    + cost
                )

                if tentative < g_score.get(
                    nxt,
                    float("inf")
                ):

                    came_from[nxt] = current

                    g_score[nxt] = tentative

                    h = math.hypot(
                        goal[0] - nxt[0],
                        goal[1] - nxt[1]
                    )

                    heapq.heappush(
                        open_heap,
                        (
                            tentative + h,
                            nxt
                        )
                    )

        self.path = []
        self.path_index = 0

        return False

    # ============================================================
    # LINE CHECK FROM ARBITRARY POSITION
    # ============================================================

    def _line_is_clear_from(
        self,
        x1,
        y1,
        x2,
        y2,
        obstacles
    ):
        dx = x2 - x1
        dy = y2 - y1

        length = math.hypot(
            dx,
            dy
        )

        if length <= 1:
            return True

        steps = max(
            2,
            int(length / 12)
        )

        for i in range(
            1,
            steps + 1
        ):

            t = i / steps

            x = x1 + dx * t
            y = y1 + dy * t

            if not self.can_move_to(
                x,
                y,
                obstacles
            ):
                return False

        return True

    # ============================================================
    # CHOOSE NEW DESTINATION
    # ============================================================

    def choose_new_destination(
        self,
        obstacles=None
    ):
        """
        Choose a new random destination around the NPC's CURRENT
        position.

        This is the main free-roaming system.

        NPCs are no longer restricted to their original spawn
        locations.

        Example:

            Spawn at 800,800
                ↓
            walk to 950,750
                ↓
            walk to 1100,850
                ↓
            walk to 1250,700
                ↓
            walk to 1400,900
                ↓
            ...

        Over time the NPC can explore the entire world.
        """

        if obstacles is None:
            obstacles = []

        # --------------------------------------------------------
        # Make sure current position is valid.
        # --------------------------------------------------------

        if not self.can_move_to(
            self.x,
            self.y,
            obstacles
        ):

            safe = self._find_free_position(
                obstacles,
                250
            )

            if safe is not None:

                self.x = float(
                    safe[0]
                )

                self.y = float(
                    safe[1]
                )

                self.sync_rect()

            else:
                return False

        candidates = []

        # --------------------------------------------------------
        # Generate destinations around CURRENT POSITION.
        #
        # This is the important difference from the previous
        # version.
        # --------------------------------------------------------

        for _ in range(100):

            angle = random.uniform(
                0,
                math.tau
            )

            radius = random.uniform(
                self.wander_min_distance,
                self.wander_radius
            )

            tx = clamp(
                self.x
                + math.cos(angle) * radius,
                80,
                WORLD_WIDTH - 100
            )

            ty = clamp(
                self.y
                + math.sin(angle) * radius,
                80,
                WORLD_HEIGHT - 100
            )

            distance_from_current = math.hypot(
                tx - self.x,
                ty - self.y
            )

            if distance_from_current < self.wander_min_distance:
                continue

            if not self.can_move_to(
                tx,
                ty,
                obstacles
            ):
                continue

            candidates.append(
                (
                    tx,
                    ty
                )
            )

        # --------------------------------------------------------
        # Randomize candidate order.
        # --------------------------------------------------------

        random.shuffle(
            candidates
        )

        # --------------------------------------------------------
        # First preference:
        # Direct unobstructed walking.
        # --------------------------------------------------------

        for tx, ty in candidates:

            if self._line_is_clear(
                tx,
                ty,
                obstacles
            ):

                self.target_x = float(
                    tx
                )

                self.target_y = float(
                    ty
                )

                self.path = []
                self.path_index = 0

                self.path_target_x = None
                self.path_target_y = None

                return True

        # --------------------------------------------------------
        # Second preference:
        # A* around obstacles.
        # --------------------------------------------------------

        for tx, ty in candidates[:25]:

            if self._build_local_path(
                tx,
                ty,
                obstacles
            ):

                self.target_x = float(
                    tx
                )

                self.target_y = float(
                    ty
                )

                self.path_target_x = self.target_x
                self.path_target_y = self.target_y

                return True

        # --------------------------------------------------------
        # Last resort:
        # Search for a nearby valid point.
        # --------------------------------------------------------

        for radius in (
            50,
            75,
            100,
            140,
            180
        ):

            angles = list(
                range(
                    0,
                    360,
                    30
                )
            )

            random.shuffle(
                angles
            )

            for angle_deg in angles:

                angle = math.radians(
                    angle_deg
                )

                tx = clamp(
                    self.x
                    + math.cos(angle) * radius,
                    30,
                    WORLD_WIDTH - 80
                )

                ty = clamp(
                    self.y
                    + math.sin(angle) * radius,
                    30,
                    WORLD_HEIGHT - 80
                )

                if not self.can_move_to(
                    tx,
                    ty,
                    obstacles
                ):
                    continue

                self.target_x = float(
                    tx
                )

                self.target_y = float(
                    ty
                )

                self.path = []
                self.path_index = 0

                self.path_target_x = None
                self.path_target_y = None

                return True

        # --------------------------------------------------------
        # No valid destination.
        # --------------------------------------------------------

        self.target_x = self.x
        self.target_y = self.y

        self.path = []
        self.path_index = 0

        return False

    # ============================================================
    # HOME
    # ============================================================

    def set_home(
        self,
        house
    ):
        self.house = house

        if house is None:
            return

        self.home_target_x = float(
            house.rect.centerx
            - self.rect.width // 2
        )

        self.home_target_y = float(
            house.rect.bottom + 22
        )

    # ============================================================
    # UPDATE HOME STATE
    # ============================================================

    def update_home_state(
        self,
        game_time_hour,
        obstacles
    ):
        self._find_home(
            obstacles
        )

        # --------------------------------------------------------
        # NPC home hours.
        #
        # 20:00 -> go home
        # 06:00 -> leave home
        # --------------------------------------------------------

        night = (
            game_time_hour >= NPC_HOME_HOUR
            or
            game_time_hour < NPC_WAKE_HOUR
        )

        # --------------------------------------------------------
        # NIGHT STARTED
        # --------------------------------------------------------

        if night and not self.is_home:

            self.is_home = True
            self.home_reached = False

            self.path = []
            self.path_index = 0

            self.path_target_x = None
            self.path_target_y = None

            self.velocity_x = 0.0
            self.velocity_y = 0.0

            if self.house is not None:

                self.home_target_x = float(
                    self.house.rect.centerx
                    - self.rect.width // 2
                )

                self.home_target_y = float(
                    self.house.rect.bottom + 22
                )

        # --------------------------------------------------------
        # MORNING
        # --------------------------------------------------------

        elif not night and self.is_home:

            self.is_home = False
            self.home_reached = False

            self.path = []
            self.path_index = 0

            self.path_target_x = None
            self.path_target_y = None

            self.wait_timer = random.uniform(
                0.5,
                1.2
            )

            self.choose_new_destination(
                obstacles
            )

    # ============================================================
    # SMOOTH MOVEMENT
    # ============================================================

    def _move_smoothly(
        self,
        tx,
        ty,
        dt,
        obstacles
    ):
        seconds = max(
            0.001,
            dt / 1000.0
        )

        dx = tx - self.x
        dy = ty - self.y

        distance_to_target = math.hypot(
            dx,
            dy
        )

        # --------------------------------------------------------
        # ARRIVAL
        # --------------------------------------------------------

        if distance_to_target <= 7:

            self.velocity_x = 0.0
            self.velocity_y = 0.0

            self.x = float(tx)
            self.y = float(ty)

            return True

        # --------------------------------------------------------
        # DIRECTION
        # --------------------------------------------------------

        desired_x = (
            dx / distance_to_target
        )

        desired_y = (
            dy / distance_to_target
        )

        # --------------------------------------------------------
        # SLOW DOWN NEAR TARGET
        # --------------------------------------------------------

        slow_radius = 100.0

        if distance_to_target < slow_radius:

            speed_ratio = (
                distance_to_target
                / slow_radius
            )

            speed_ratio = clamp(
                speed_ratio,
                0.20,
                1.0
            )

            desired_speed = (
                self.max_speed
                * speed_ratio
            )

        else:

            desired_speed = self.max_speed

        desired_vx = (
            desired_x
            * desired_speed
        )

        desired_vy = (
            desired_y
            * desired_speed
        )

        # --------------------------------------------------------
        # ACCELERATION / DECELERATION
        # --------------------------------------------------------

        current_speed = math.hypot(
            self.velocity_x,
            self.velocity_y
        )

        if desired_speed < current_speed:

            change = (
                self.deceleration
                * seconds
            )

        else:

            change = (
                self.acceleration
                * seconds
            )

        # --------------------------------------------------------
        # CURRENT ANGLE
        # --------------------------------------------------------

        if current_speed > 0:

            current_angle = math.atan2(
                self.velocity_y,
                self.velocity_x
            )

        else:

            current_angle = math.atan2(
                desired_vy,
                desired_vx
            )

        desired_angle = math.atan2(
            desired_vy,
            desired_vx
        )

        # --------------------------------------------------------
        # SMOOTH TURNING
        # --------------------------------------------------------

        angle_difference = (
            desired_angle
            - current_angle
        )

        while angle_difference > math.pi:
            angle_difference -= math.tau

        while angle_difference < -math.pi:
            angle_difference += math.tau

        max_turn = (
            5.0
            * seconds
        )

        angle_difference = clamp(
            angle_difference,
            -max_turn,
            max_turn
        )

        new_angle = (
            current_angle
            + angle_difference
        )

        # --------------------------------------------------------
        # SPEED
        # --------------------------------------------------------

        new_speed = current_speed

        if new_speed < desired_speed:

            new_speed = min(
                desired_speed,
                new_speed + change
            )

        elif new_speed > desired_speed:

            new_speed = max(
                desired_speed,
                new_speed - change
            )

        self.velocity_x = (
            math.cos(new_angle)
            * new_speed
        )

        self.velocity_y = (
            math.sin(new_angle)
            * new_speed
        )

        # --------------------------------------------------------
        # PREVENT OVERSHOOT
        # --------------------------------------------------------

        movement_distance = (
            new_speed
            * seconds
        )

        if movement_distance >= distance_to_target:

            self.x = float(tx)
            self.y = float(ty)

            self.velocity_x = 0.0
            self.velocity_y = 0.0

            return True

        # --------------------------------------------------------
        # NEW POSITION
        # --------------------------------------------------------

        new_x = (
            self.x
            + self.velocity_x
            * seconds
        )

        new_y = (
            self.y
            + self.velocity_y
            * seconds
        )

        moved = False

        # --------------------------------------------------------
        # FULL MOVEMENT
        # --------------------------------------------------------

        if self.can_move_to(
            new_x,
            new_y,
            obstacles
        ):

            self.x = new_x
            self.y = new_y

            moved = True

        else:

            # ----------------------------------------------------
            # X ONLY
            # ----------------------------------------------------

            if self.can_move_to(
                new_x,
                self.y,
                obstacles
            ):

                self.x = new_x
                moved = True

            else:

                self.velocity_x *= 0.35

            # ----------------------------------------------------
            # Y ONLY
            # ----------------------------------------------------

            if self.can_move_to(
                self.x,
                new_y,
                obstacles
            ):

                self.y = new_y
                moved = True

            else:

                self.velocity_y *= 0.35

        # --------------------------------------------------------
        # STUCK DETECTION
        # --------------------------------------------------------

        if moved:

            self.stuck_timer = 0.0

        else:

            self.stuck_timer += seconds

        return False

    # ============================================================
    # GET CURRENT TARGET
    # ============================================================

    def _get_current_target(
        self,
        obstacles
    ):
        if self.path:

            if self.path_index >= len(
                self.path
            ):

                self.path = []
                self.path_index = 0

            else:

                return self.path[
                    self.path_index
                ]

        return (
            self.target_x,
            self.target_y
        )

    # ============================================================
    # UPDATE
    # ============================================================

    def update(
        self,
        dt,
        obstacles,
        game_time_hour=None
    ):
        seconds = max(
            0.001,
            dt / 1000.0
        )

        # --------------------------------------------------------
        # FIND HOME
        # --------------------------------------------------------

        self._find_home(
            obstacles
        )

        # --------------------------------------------------------
        # DAY / NIGHT
        # --------------------------------------------------------

        if game_time_hour is not None:

            self.update_home_state(
                game_time_hour,
                obstacles
            )

        # --------------------------------------------------------
        # DIALOGUE
        # --------------------------------------------------------

        if self.is_talking:

            self.velocity_x = self._approach(
                self.velocity_x,
                0.0,
                self.deceleration * seconds
            )

            self.velocity_y = self._approach(
                self.velocity_y,
                0.0,
                self.deceleration * seconds
            )

            self.x += (
                self.velocity_x
                * seconds
            )

            self.y += (
                self.velocity_y
                * seconds
            )

            self.sync_rect()

            return

        # --------------------------------------------------------
        # GOING HOME
        # --------------------------------------------------------

        if self.is_home:

            if self.house is None:

                self.is_home = False

            else:

                # ------------------------------------------------
                # Direct route first.
                # ------------------------------------------------

                if (
                    not self._line_is_clear(
                        self.home_target_x,
                        self.home_target_y,
                        obstacles
                    )
                    and
                    not self.path
                ):

                    self._build_local_path(
                        self.home_target_x,
                        self.home_target_y,
                        obstacles
                    )

                target = self._get_current_target(
                    obstacles
                )

                arrived = self._move_smoothly(
                    target[0],
                    target[1],
                    dt,
                    obstacles
                )

                if arrived:

                    if self.path:

                        self.path_index += 1

                        if self.path_index >= len(
                            self.path
                        ):

                            self.path = []
                            self.path_index = 0

                            self.x = (
                                self.home_target_x
                            )

                            self.y = (
                                self.home_target_y
                            )

                            self.velocity_x = 0.0
                            self.velocity_y = 0.0

                            self.home_reached = True

                    else:

                        self.home_reached = True

                        self.x = (
                            self.home_target_x
                        )

                        self.y = (
                            self.home_target_y
                        )

                        self.velocity_x = 0.0
                        self.velocity_y = 0.0

                self.sync_rect()

                return

        # --------------------------------------------------------
        # WAITING / IDLE
        # --------------------------------------------------------

        self.wait_timer -= seconds

        if self.wait_timer > 0:

            self.velocity_x = self._approach(
                self.velocity_x,
                0.0,
                self.deceleration * seconds
            )

            self.velocity_y = self._approach(
                self.velocity_y,
                0.0,
                self.deceleration * seconds
            )

            if abs(
                self.velocity_x
            ) < 0.5:

                self.velocity_x = 0.0

            if abs(
                self.velocity_y
            ) < 0.5:

                self.velocity_y = 0.0

            self.sync_rect()

            return

        # --------------------------------------------------------
        # CHECK TARGET
        # --------------------------------------------------------

        distance_to_target = math.hypot(
            self.target_x - self.x,
            self.target_y - self.y
        )

        if distance_to_target < 10:

            self.velocity_x = self._approach(
                self.velocity_x,
                0.0,
                self.deceleration * seconds
            )

            self.velocity_y = self._approach(
                self.velocity_y,
                0.0,
                self.deceleration * seconds
            )

            if (
                abs(self.velocity_x) < 0.5
                and
                abs(self.velocity_y) < 0.5
            ):

                self.velocity_x = 0.0
                self.velocity_y = 0.0

                # ------------------------------------------------
                # NPC pauses after reaching a destination.
                # ------------------------------------------------

                self.wait_timer = random.uniform(
                    0.5,
                    1.6
                )

                self.choose_new_destination(
                    obstacles
                )

            self.sync_rect()

            return

        # --------------------------------------------------------
        # DIRECT ROUTE BLOCKED
        # --------------------------------------------------------

        if (
            not self.path
            and
            not self._line_is_clear(
                self.target_x,
                self.target_y,
                obstacles
            )
        ):

            self._build_local_path(
                self.target_x,
                self.target_y,
                obstacles
            )

        # --------------------------------------------------------
        # GET MOVEMENT TARGET
        # --------------------------------------------------------

        target_x, target_y = self._get_current_target(
            obstacles
        )

        arrived = self._move_smoothly(
            target_x,
            target_y,
            dt,
            obstacles
        )

        # --------------------------------------------------------
        # REACHED PATH WAYPOINT
        # --------------------------------------------------------

        if arrived and self.path:

            self.path_index += 1

            if self.path_index >= len(
                self.path
            ):

                self.path = []
                self.path_index = 0

                self.target_x = float(
                    self.target_x
                )

                self.target_y = float(
                    self.target_y
                )

                self.velocity_x = 0.0
                self.velocity_y = 0.0

                self.wait_timer = random.uniform(
                    0.5,
                    1.6
                )

                self.choose_new_destination(
                    obstacles
                )

        # --------------------------------------------------------
        # NORMAL TARGET REACHED
        # --------------------------------------------------------

        elif arrived:

            self.velocity_x = 0.0
            self.velocity_y = 0.0

            self.wait_timer = random.uniform(
                0.5,
                1.6
            )

            self.choose_new_destination(
                obstacles
            )

        # --------------------------------------------------------
        # NPC STUCK
        # --------------------------------------------------------

        if self.stuck_timer > 0.8:

            self.velocity_x = 0.0
            self.velocity_y = 0.0

            self.path = []
            self.path_index = 0

            self.path_target_x = None
            self.path_target_y = None

            self.stuck_timer = 0.0

            self.choose_new_destination(
                obstacles
            )

            self.wait_timer = 0.2

        self.sync_rect()

    # ============================================================
    # APPROACH
    # ============================================================

    def _approach(
        self,
        current,
        target,
        amount
    ):
        if current < target:

            return min(
                current + amount,
                target
            )

        if current > target:

            return max(
                current - amount,
                target
            )

        return target

    # ============================================================
    # DRAW
    # ============================================================

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

        # --------------------------------------------------------
        # NAME
        # --------------------------------------------------------

        name_surface = game.small_font.render(
            self.name,
            True,
            (255, 255, 255)
        )

        name_rect = name_surface.get_rect(
            center=(
                sx + self.rect.width // 2,
                sy - 14
            )
        )

        pygame.draw.rect(
            screen,
            (70, 55, 90),
            name_rect.inflate(
                10,
                5
            ),
            border_radius=8
        )

        screen.blit(
            name_surface,
            name_rect
        )

        # --------------------------------------------------------
        # QUEST MARKER
        # --------------------------------------------------------

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
                    sx + self.rect.width // 2,
                    sy - 48
                )
            )

            screen.blit(
                marker_surface,
                marker_rect
            )

        # --------------------------------------------------------
        # HOME INDICATOR
        # --------------------------------------------------------

        if self.is_home:

            home_text = (
                "HOME"
                if self.home_reached
                else
                "GOING HOME"
            )

            home_surface = game.tiny_font.render(
                home_text,
                True,
                (190, 230, 255)
            )

            home_rect = home_surface.get_rect(
                center=(
                    sx + self.rect.width // 2,
                    sy + 10
                )
            )

            bg = home_rect.inflate(
                10,
                4
            )

            pygame.draw.rect(
                screen,
                (45, 65, 95),
                bg,
                border_radius=7
            )

            screen.blit(
                home_surface,
                home_rect
            )