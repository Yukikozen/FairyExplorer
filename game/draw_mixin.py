# from .core import *

# class DrawMixin:
#     def draw_main_menu(self):

#         # --------------------------------------------------------
#         # Gradient-style background
#         # --------------------------------------------------------

#         self.screen.fill(
#             (55, 38, 88)
#         )

#         # Large decorative circles.
#         pygame.draw.circle(
#             self.screen,
#             (90, 65, 125),
#             (
#                 100,
#                 120
#             ),
#             260
#         )

#         pygame.draw.circle(
#             self.screen,
#             (75, 55, 110),
#             (
#                 SCREEN_WIDTH - 100,
#                 180
#             ),
#             300
#         )

#         pygame.draw.circle(
#             self.screen,
#             (65, 45, 100),
#             (
#                 SCREEN_WIDTH // 2,
#                 SCREEN_HEIGHT + 200
#             ),
#             500
#         )

#         # --------------------------------------------------------
#         # Sparkles
#         # --------------------------------------------------------

#         for sparkle in self.menu_sparkles:

#             pulse = (
#                 math.sin(
#                     sparkle["phase"]
#                 )
#                 + 1
#             ) / 2

#             size = max(
#                 1,
#                 int(
#                     sparkle["size"]
#                     * (0.6 + pulse * 0.8)
#                 )
#             )

#             x = int(
#                 sparkle["x"]
#             )

#             y = int(
#                 sparkle["y"]
#             )

#             pygame.draw.circle(
#                 self.screen,
#                 (255, 230, 180),
#                 (
#                     x,
#                     y
#                 ),
#                 size
#             )

#         # --------------------------------------------------------
#         # Decorative moon
#         # --------------------------------------------------------

#         pygame.draw.circle(
#             self.screen,
#             (255, 235, 180),
#             (
#                 SCREEN_WIDTH - 130,
#                 110
#             ),
#             55
#         )

#         pygame.draw.circle(
#             self.screen,
#             (75, 55, 110),
#             (
#                 SCREEN_WIDTH - 105,
#                 90
#             ),
#             55
#         )

#         # --------------------------------------------------------
#         # Title
#         # --------------------------------------------------------

#         title_1 = self.title_font.render(
#             "MEPPLE & MIPPLE",
#             True,
#             (255, 240, 170)
#         )

#         title_1_rect = title_1.get_rect(
#             center=(
#                 SCREEN_WIDTH // 2,
#                 105
#             )
#         )

#         self.screen.blit(
#             title_1,
#             title_1_rect
#         )

#         title_2 = self.large_font.render(
#             "Magical Friendship Adventure",
#             True,
#             (255, 255, 255)
#         )

#         title_2_rect = title_2.get_rect(
#             center=(
#                 SCREEN_WIDTH // 2,
#                 150
#             )
#         )

#         self.screen.blit(
#             title_2,
#             title_2_rect
#         )

#         # --------------------------------------------------------
#         # Fairy images
#         # --------------------------------------------------------

#         mepple = load_image(
#             "mepple.png",
#             (120, 145)
#         )

#         mipple = load_image(
#             "mipple.png",
#             (120, 145)
#         )

#         float_amount = math.sin(
#             self.menu_time * 0.003
#         ) * 6

#         if mepple:

#             rect = mepple.get_rect(
#                 center=(
#                     SCREEN_WIDTH // 2 - 230,
#                     245 + int(float_amount)
#                 )
#             )

#             self.screen.blit(
#                 mepple,
#                 rect
#             )

#         if mipple:

#             rect = mipple.get_rect(
#                 center=(
#                     SCREEN_WIDTH // 2 + 230,
#                     245 - int(float_amount)
#                 )
#             )

#             self.screen.blit(
#                 mipple,
#                 rect
#             )

#         # --------------------------------------------------------
#         # Menu buttons
#         # --------------------------------------------------------

#         mouse_pos = pygame.mouse.get_pos()

#         for index, option in enumerate(
#             self.main_menu_options
#         ):

#             rect = self.get_main_menu_button_rect(
#                 index
#             )

#             hovered = rect.collidepoint(
#                 mouse_pos
#             )

#             selected = (
#                 index
#                 == self.main_menu_selected
#             )

#             if selected or hovered:

#                 bg = (130, 95, 165)
#                 border = (255, 225, 140)

#             else:

#                 bg = (75, 55, 105)
#                 border = (150, 130, 180)

#             pygame.draw.rect(
#                 self.screen,
#                 bg,
#                 rect,
#                 border_radius=18
#             )

#             pygame.draw.rect(
#                 self.screen,
#                 border,
#                 rect,
#                 3,
#                 border_radius=18
#             )

#             text = self.font.render(
#                 option,
#                 True,
#                 (255, 255, 255)
#             )

#             text_rect = text.get_rect(
#                 center=rect.center
#             )

#             self.screen.blit(
#                 text,
#                 text_rect
#             )

#         # --------------------------------------------------------
#         # Bottom text
#         # --------------------------------------------------------

#         hint = self.small_font.render(
#             "↑ ↓ Select     ENTER / SPACE Confirm",
#             True,
#             (220, 210, 240)
#         )

#         hint_rect = hint.get_rect(
#             center=(
#                 SCREEN_WIDTH // 2,
#                 SCREEN_HEIGHT - 30
#             )
#         )

#         self.screen.blit(
#             hint,
#             hint_rect
#         )


#     def draw_world(self):

#         self.screen.fill((150, 205, 135))

#         random_generator = random.Random(
#             100
#         )

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

#         # Day/night tint. The world remains visible while the sky gradually
#         # becomes darker at night.
#         game_minutes = (self.game_time_ms / GAME_DAY_LENGTH_MS) * 24 * 60
#         hour = game_minutes / 60.0
#         if 6.0 <= hour < 18.0:
#             darkness = 0
#         elif hour < 20.0:
#             darkness = int((hour - 18.0) / 2.0 * 70)
#         elif hour < 6.0:
#             darkness = 120
#         else:
#             darkness = int((20.0 - hour) / 2.0 * 50 + 70) if hour < 22.0 else 120
#         if darkness > 0:
#             overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
#             overlay.fill((25, 35, 80, min(145, darkness)))
#             self.screen.blit(overlay, (0, 0))


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

#         # --------------------------------------------------------
#         # Coin icon + coin count
#         # --------------------------------------------------------
#         # Draw the coin directly with Pygame so it is always visible
#         # even when no external coin image asset exists.
#         coin_cx = 48
#         coin_cy = 74

#         # Soft shadow / depth.
#         pygame.draw.ellipse(
#             self.screen,
#             (150, 105, 35),
#             pygame.Rect(
#                 coin_cx - 13,
#                 coin_cy - 9,
#                 26,
#                 20
#             )
#         )

#         # Dark gold outer edge.
#         pygame.draw.circle(
#             self.screen,
#             (190, 135, 35),
#             (coin_cx, coin_cy),
#             14
#         )

#         # Main gold face.
#         pygame.draw.circle(
#             self.screen,
#             (255, 205, 65),
#             (coin_cx, coin_cy - 1),
#             11
#         )

#         # Bright highlight.
#         pygame.draw.circle(
#             self.screen,
#             (255, 235, 125),
#             (coin_cx - 4, coin_cy - 5),
#             3
#         )

#         # Magical star emblem.
#         star_points = []
#         for i in range(10):
#             angle = -math.pi / 2 + i * math.pi / 5
#             radius = 6 if i % 2 == 0 else 2.7
#             star_points.append((
#                 coin_cx + math.cos(angle) * radius,
#                 coin_cy - 1 + math.sin(angle) * radius
#             ))
#         pygame.draw.polygon(
#             self.screen,
#             (225, 165, 35),
#             star_points
#         )

#         coins = self.font.render(
#             f"{self.coins} coins",
#             True,
#             (255, 225, 90)
#         )

#         self.screen.blit(
#             coins,
#             (
#                 70,
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

#         game_minutes = (self.game_time_ms / GAME_DAY_LENGTH_MS) * 24 * 60
#         total_minutes = int(game_minutes) % (24 * 60)
#         hh = total_minutes // 60
#         mm = total_minutes % 60
#         period = "DAY" if 6 <= hh < 20 else "NIGHT"
#         clock_text = self.large_font.render(
#             f"TIME  {hh:02d}:{mm:02d}  •  {period}",
#             True,
#             (230, 240, 255)
#         )
#         clock_rect = clock_text.get_rect(
#             top=18,
#             right=SCREEN_WIDTH - 18
#         )
#         clock_bg = clock_rect.inflate(20, 10)
#         pygame.draw.rect(
#             self.screen,
#             (45, 50, 80),
#             clock_bg,
#             border_radius=12
#         )
#         pygame.draw.rect(
#             self.screen,
#             (180, 190, 235),
#             clock_bg,
#             2,
#             border_radius=12
#         )
#         self.screen.blit(clock_text, clock_rect)

#         controls = self.small_font.render(
#             (
#                 "WASD Move   "
#                 "E Interact   "
#                 "Q Quest Log   "
#                 "N Navigate   "
#                 "ESC Pause"
#             ),
#             True,
#             (255, 255, 255)
#         )

#         controls_rect = controls.get_rect(
#             top=62,
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
#                     len(
#                         self.dialogue_lines
#                     ) - 1
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
#                 f"Reward: "
#                 f"{quest.reward_coins} coins"
#             )

#         else:

#             status_text = (
#                 f"Progress: "
#                 f"{quest.progress}/"
#                 f"{quest.required_amount}  •  "
#                 f"Reward: "
#                 f"{quest.reward_coins}"
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

#         # Click the quest entry / DETAILS button to open the
#         # full quest details screen.
#         details_rect = pygame.Rect(
#             rect.right - 112,
#             rect.y + 27,
#             92,
#             38
#         )

#         details_bg = (95, 75, 125)
#         details_border = (220, 195, 120)

#         pygame.draw.rect(
#             self.screen,
#             details_bg,
#             details_rect,
#             border_radius=9
#         )
#         pygame.draw.rect(
#             self.screen,
#             details_border,
#             details_rect,
#             1,
#             border_radius=9
#         )
#         details_text = self.tiny_font.render(
#             "DETAILS",
#             True,
#             (255, 255, 255)
#         )
#         self.screen.blit(
#             details_text,
#             details_text.get_rect(
#                 center=details_rect.center
#             )
#         )

#         return rect.height


#     def draw_quest_log(self):

#         self.screen.fill(
#             (30, 25, 45)
#         )

#         # Header.
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

#         # Tabs.
#         tab_y = 105
#         tab_height = 50

#         tab_left = 25

#         tab_total_width = (
#             SCREEN_WIDTH - 65
#         )

#         tab_width = (
#             tab_total_width // 4
#         )

#         tab_data = [
#             (
#                 "ACTIVE",
#                 len(
#                     self.get_active_quests()
#                 )
#             ),
#             (
#                 "AVAILABLE",
#                 len(
#                     self.get_available_quests()
#                 )
#             ),
#             (
#                 "COMPLETED",
#                 len(
#                     self.get_completed_quests()
#                 )
#             ),
#             (
#                 "LOCKED",
#                 len(
#                     self.get_locked_quests()
#                 )
#             )
#         ]

#         for index, (
#             name,
#             count
#         ) in enumerate(tab_data):

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

#         # Viewport.
#         viewport = (
#             self.get_quest_log_view_rect()
#         )

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

#         quests = (
#             self.get_current_quest_list()
#         )

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

#         old_clip = (
#             self.screen.get_clip()
#         )

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
#                 0:
#                     "You don't have any active quests yet.",

#                 1:
#                     "There are no quests available right now.",

#                 2:
#                     "You haven't completed any quests yet.",

#                 3:
#                     "No locked quests."
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

#         # Scrollbar.
#         scrollbar_x = SCREEN_WIDTH - 27

#         scrollbar_y = (
#             viewport.y + 5
#         )

#         scrollbar_height = (
#             viewport.height - 10
#         )

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

#         # Footer.
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


#     def get_pause_resume_rect(self):
#         return pygame.Rect(SCREEN_WIDTH // 2 - 210, 300, 420, 55)


#     def get_pause_save_rect(self):
#         return pygame.Rect(SCREEN_WIDTH // 2 - 210, 370, 420, 55)


#     def get_pause_menu_rect(self):
#         return pygame.Rect(SCREEN_WIDTH // 2 - 210, 440, 420, 55)


#     def draw_pause(self):

#         overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
#         overlay.fill((0, 0, 0, 165))
#         self.screen.blit(overlay, (0, 0))
#         title = self.title_font.render("PAUSED", True, (255, 255, 255))
#         self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 220)))
#         buttons = [(self.get_pause_resume_rect(), "RESUME", "ESC"), (self.get_pause_save_rect(), "SAVE GAME", "S"), (self.get_pause_menu_rect(), "SAVE & MAIN MENU", "M")]
#         mouse_pos = pygame.mouse.get_pos()
#         for rect, label, key in buttons:
#             hovered = rect.collidepoint(mouse_pos)
#             bg = (125, 95, 165) if hovered else (70, 55, 95)
#             border = (255, 225, 140) if hovered else (160, 140, 190)
#             pygame.draw.rect(self.screen, bg, rect, border_radius=14)
#             pygame.draw.rect(self.screen, border, rect, 2, border_radius=14)
#             text = self.font.render(f"{label}   [{key}]", True, (255, 255, 255))
#             self.screen.blit(text, text.get_rect(center=rect.center))
#         hint = self.small_font.render("ESC Resume    S Save Game    M Save & Main Menu", True, (225, 215, 240))
#         self.screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 35)))


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

#         for (
#             name,
#             filename,
#             rect,
#             key
#         ) in cards:

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

#         back = self.small_font.render(
#             "ESC  Back to Main Menu",
#             True,
#             (235, 225, 255)
#         )

#         back_rect = back.get_rect(
#             center=(
#                 SCREEN_WIDTH // 2,
#                 600
#             )
#         )

#         self.screen.blit(
#             back,
#             back_rect
#         )


#     def draw_quest_details(self):
#         quest = self.selected_quest

#         if quest is None:
#             self.state = "quest_log"
#             return

#         self.screen.fill((30, 25, 45))

#         panel = pygame.Rect(
#             45,
#             45,
#             SCREEN_WIDTH - 90,
#             SCREEN_HEIGHT - 90
#         )

#         pygame.draw.rect(
#             self.screen,
#             (48, 40, 65),
#             panel,
#             border_radius=18
#         )
#         pygame.draw.rect(
#             self.screen,
#             (150, 125, 190),
#             panel,
#             2,
#             border_radius=18
#         )

#         title = self.title_font.render(
#             quest.title,
#             True,
#             (255, 230, 140)
#         )
#         self.screen.blit(title, (75, 75))

#         status = self.get_quest_status(quest)
#         status_text = self.font.render(
#             f"{status}  •  From {quest.giver_name}",
#             True,
#             (220, 215, 235)
#         )
#         self.screen.blit(status_text, (75, 120))

#         # Description.
#         desc_y = 175
#         words = quest.description.split()
#         line = ""
#         lines = []
#         for word in words:
#             test = (line + " " + word).strip()
#             if self.font.size(test)[0] > SCREEN_WIDTH - 180:
#                 lines.append(line)
#                 line = word
#             else:
#                 line = test
#         if line:
#             lines.append(line)

#         for line in lines:
#             surf = self.font.render(
#                 line,
#                 True,
#                 (240, 235, 245)
#             )
#             self.screen.blit(surf, (75, desc_y))
#             desc_y += 34

#         objective = self.font.render(
#             f"Objective: {quest.progress}/{quest.required_amount}",
#             True,
#             (255, 220, 150)
#         )
#         self.screen.blit(objective, (75, desc_y + 25))

#         reward = self.font.render(
#             f"Reward: {quest.reward_coins} coins",
#             True,
#             (255, 220, 150)
#         )
#         self.screen.blit(reward, (75, desc_y + 65))

#         target_npc = self.get_navigator_npc_for_quest(quest)
#         target_name = target_npc.name if target_npc else quest.giver_name

#         current_target, current_target_type, current_target_name = self.get_navigator_target(quest)

#         if current_target_name:
#             target_label = f"Current Navigator Target: {current_target_name}"
#         else:
#             target_label = f"Quest NPC: {target_name}"

#         target = self.small_font.render(
#             target_label,
#             True,
#             (205, 195, 225)
#         )
#         self.screen.blit(target, (75, desc_y + 105))

#         if status == "ACTIVE":
#             button = self.get_quest_navigate_button_rect()
#             pygame.draw.rect(
#                 self.screen,
#                 (115, 90, 150),
#                 button,
#                 border_radius=12
#             )
#             pygame.draw.rect(
#                 self.screen,
#                 (255, 225, 130),
#                 button,
#                 2,
#                 border_radius=12
#             )
#             if current_target_name:
#                 if current_target_type == "npc" and quest.is_finished():
#                     button_label = f"RETURN TO {current_target_name}"
#                 else:
#                     button_label = f"NAVIGATE TO {current_target_name}"
#             else:
#                 button_label = f"NAVIGATE TO {target_name}"

#             label = self.font.render(
#                 button_label,
#                 True,
#                 (255, 255, 255)
#             )
#             self.screen.blit(label, label.get_rect(center=button.center))
#         else:
#             hint = self.small_font.render(
#                 "Accept this quest first to enable navigation.",
#                 True,
#                 (170, 165, 185)
#             )
#             self.screen.blit(
#                 hint,
#                 hint.get_rect(
#                     center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 115)
#                 )
#             )

#         back = self.get_quest_details_back_rect()
#         pygame.draw.rect(
#             self.screen,
#             (65, 55, 80),
#             back,
#             border_radius=10
#         )
#         back_text = self.small_font.render(
#             "← BACK TO QUEST LOG",
#             True,
#             (240, 235, 245)
#         )
#         self.screen.blit(back_text, back_text.get_rect(center=back.center))

#         hint = self.small_font.render(
#             "Click Navigate, or press N",
#             True,
#             (180, 175, 195)
#         )
#         self.screen.blit(
#             hint,
#             hint.get_rect(
#                 center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 55)
#             )
#         )


#     def draw(self):

#         if self.state == "main_menu":

#             self.draw_main_menu()
#             return

#         if self.state == "character_select":

#             self.draw_character_select()
#             return

#         if self.state == "quest_log":

#             self.draw_quest_log()
#             return

#         if self.state == "quest_details":

#             self.draw_quest_details()
#             return

#         self.draw_world()
#         self.draw_hud()

#         if self.state == "playing":
#             self.draw_navigator()

#         if self.dialogue_npc is not None:

#             self.draw_dialogue()

#         if self.state == "pause":

#             self.draw_pause()


from .core import *


class DrawMixin:

    # ============================================================
    # MAIN MENU
    # ============================================================

    def draw_main_menu(self):

        self.screen.fill(
            (55, 38, 88)
        )

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
        # SPARKLES
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
        # MOON
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
        # TITLE
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
        # FAIRY IMAGES
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
        # MENU BUTTONS
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
        # BOTTOM TEXT
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
    # WORLD
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

        # --------------------------------------------------------
        # QUEST LOCATIONS
        # --------------------------------------------------------

        for location in self.quest_locations:

            location.draw(
                self.screen,
                self.camera
            )

        # --------------------------------------------------------
        # FLOWERS
        # --------------------------------------------------------

        for flower in self.flowers:

            flower.draw(
                self.screen,
                self.camera
            )

        # --------------------------------------------------------
        # QUEST ITEMS
        # --------------------------------------------------------

        for item in self.quest_items:

            item.draw(
                self.screen,
                self.camera
            )

        # --------------------------------------------------------
        # OBSTACLES
        # --------------------------------------------------------

        for obstacle in self.obstacles:

            obstacle.draw(
                self.screen,
                self.camera
            )

        # --------------------------------------------------------
        # NPCS
        # --------------------------------------------------------

        for npc in self.npcs:

            npc.draw(
                self.screen,
                self.camera,
                self
            )

        # --------------------------------------------------------
        # COMPANION
        # --------------------------------------------------------

        if self.companion:

            self.companion.draw(
                self.screen,
                self.camera
            )

        # --------------------------------------------------------
        # PLAYER
        # --------------------------------------------------------

        if self.player:

            self.player.draw(
                self.screen,
                self.camera
            )

        # --------------------------------------------------------
        # DAY / NIGHT
        # --------------------------------------------------------

        game_minutes = (
            self.game_time_ms
            / GAME_DAY_LENGTH_MS
        ) * 24 * 60

        hour = game_minutes / 60.0

        if 6.0 <= hour < 18.0:

            darkness = 0

        elif hour < 20.0:

            darkness = int(
                (hour - 18.0)
                / 2.0
                * 70
            )

        elif hour < 6.0:

            darkness = 120

        else:

            darkness = (
                int(
                    (
                        20.0 - hour
                    )
                    / 2.0
                    * 50
                    + 70
                )
                if hour < 22.0
                else 120
            )

        if darkness > 0:

            overlay = pygame.Surface(
                (
                    SCREEN_WIDTH,
                    SCREEN_HEIGHT
                ),
                pygame.SRCALPHA
            )

            overlay.fill(
                (
                    25,
                    35,
                    80,
                    min(
                        145,
                        darkness
                    )
                )
            )

            self.screen.blit(
                overlay,
                (
                    0,
                    0
                )
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

        # --------------------------------------------------------
        # COIN
        # --------------------------------------------------------

        coin_cx = 48
        coin_cy = 74

        pygame.draw.ellipse(
            self.screen,
            (150, 105, 35),
            pygame.Rect(
                coin_cx - 13,
                coin_cy - 9,
                26,
                20
            )
        )

        pygame.draw.circle(
            self.screen,
            (190, 135, 35),
            (
                coin_cx,
                coin_cy
            ),
            14
        )

        pygame.draw.circle(
            self.screen,
            (255, 205, 65),
            (
                coin_cx,
                coin_cy - 1
            ),
            11
        )

        pygame.draw.circle(
            self.screen,
            (255, 235, 125),
            (
                coin_cx - 4,
                coin_cy - 5
            ),
            3
        )

        star_points = []

        for i in range(10):

            angle = (
                -math.pi / 2
                + i * math.pi / 5
            )

            radius = (
                6
                if i % 2 == 0
                else 2.7
            )

            star_points.append(
                (
                    coin_cx
                    + math.cos(angle)
                    * radius,

                    coin_cy
                    - 1
                    + math.sin(angle)
                    * radius
                )
            )

        pygame.draw.polygon(
            self.screen,
            (225, 165, 35),
            star_points
        )

        coins = self.font.render(
            f"{self.coins} coins",
            True,
            (255, 225, 90)
        )

        self.screen.blit(
            coins,
            (
                70,
                62
            )
        )

        # --------------------------------------------------------
        # QUEST COUNT
        # --------------------------------------------------------

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

        # --------------------------------------------------------
        # CLOCK
        # --------------------------------------------------------

        game_minutes = (
            self.game_time_ms
            / GAME_DAY_LENGTH_MS
        ) * 24 * 60

        total_minutes = (
            int(game_minutes)
            % (24 * 60)
        )

        hh = total_minutes // 60
        mm = total_minutes % 60

        period = (
            "DAY"
            if 6 <= hh < 20
            else "NIGHT"
        )

        clock_text = self.large_font.render(
            f"TIME  {hh:02d}:{mm:02d}  •  {period}",
            True,
            (230, 240, 255)
        )

        clock_rect = clock_text.get_rect(
            top=18,
            right=SCREEN_WIDTH - 18
        )

        clock_bg = clock_rect.inflate(
            20,
            10
        )

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

        self.screen.blit(
            clock_text,
            clock_rect
        )

        # --------------------------------------------------------
        # CONTROLS
        # --------------------------------------------------------

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

        # --------------------------------------------------------
        # ACTIVE QUEST PREVIEW
        # --------------------------------------------------------

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

        # --------------------------------------------------------
        # NPC INTERACTION
        # --------------------------------------------------------

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
    # NOTIFICATION
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

        # --------------------------------------------------------
        # TABS
        # --------------------------------------------------------

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

        # --------------------------------------------------------
        # VIEWPORT
        # --------------------------------------------------------

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

        # --------------------------------------------------------
        # SCROLLBAR
        # --------------------------------------------------------

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

        # --------------------------------------------------------
        # FOOTER
        # --------------------------------------------------------

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

    def draw_relationships(self):

        self.screen.fill(
            (30, 25, 45)
        )

        # --------------------------------------------------------
        # HEADER
        # --------------------------------------------------------

        header = pygame.Rect(
            0,
            0,
            SCREEN_WIDTH,
            105
        )

        pygame.draw.rect(
            self.screen,
            (55, 45, 75),
            header
        )

        title = self.title_font.render(
            "RELATIONSHIPS",
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
            "Your magical friendships",
            True,
            (210, 205, 225)
        )

        self.screen.blit(
            subtitle,
            (
                30,
                62
            )
        )

        # --------------------------------------------------------
        # NPCS
        # --------------------------------------------------------

        npc_names = [
            "Lumi",
            "Pipi",
            "Coco",
            "Ruru",
            "Nana"
        ]

        # --------------------------------------------------------
        # SCROLL
        # --------------------------------------------------------

        card_height = 125
        card_gap = 15

        content_top = 125
        content_bottom = SCREEN_HEIGHT - 70

        viewport = pygame.Rect(
            20,
            content_top,
            SCREEN_WIDTH - 40,
            content_bottom - content_top
        )

        if not hasattr(
            self,
            "relationship_scroll"
        ):

            self.relationship_scroll = 0

        total_height = (
            len(npc_names)
            * (
                card_height
                + card_gap
            )
        )

        max_scroll = max(
            0,
            total_height
            - viewport.height
        )

        self.relationship_scroll = int(
            clamp(
                self.relationship_scroll,
                0,
                max_scroll
            )
        )

        # --------------------------------------------------------
        # CLIP
        # --------------------------------------------------------

        old_clip = (
            self.screen.get_clip()
        )

        self.screen.set_clip(
            viewport
        )

        y = (
            viewport.y
            - self.relationship_scroll
        )

        # --------------------------------------------------------
        # DRAW NPC CARDS
        # --------------------------------------------------------

        for npc_name in npc_names:

            npc = None

            for current_npc in self.npcs:

                if current_npc.name == npc_name:

                    npc = current_npc

                    break

            # ----------------------------------------------------
            # FRIENDSHIP
            # ----------------------------------------------------

            friendship = 0

            if npc is not None:

                friendship = int(
                    clamp(
                        getattr(
                            npc,
                            "friendship",
                            0
                        ),
                        0,
                        100
                    )
                )

            # ----------------------------------------------------
            # LEVEL
            # ----------------------------------------------------

            if friendship >= 80:

                relationship_level = (
                    "Best Friends"
                )

            elif friendship >= 60:

                relationship_level = (
                    "Close Friends"
                )

            elif friendship >= 40:

                relationship_level = (
                    "Good Friends"
                )

            elif friendship >= 20:

                relationship_level = (
                    "Friends"
                )

            else:

                relationship_level = (
                    "Acquaintances"
                )

            # ----------------------------------------------------
            # CARD
            # ----------------------------------------------------

            card = pygame.Rect(
                30,
                y,
                SCREEN_WIDTH - 80,
                card_height
            )

            pygame.draw.rect(
                self.screen,
                (48, 40, 65),
                card,
                border_radius=16
            )

            pygame.draw.rect(
                self.screen,
                (120, 100, 145),
                card,
                2,
                border_radius=16
            )

            # ----------------------------------------------------
            # IMAGE
            # ----------------------------------------------------

            filename = None

            if npc is not None:

                filename = getattr(
                    npc,
                    "image_filename",
                    None
                )

            image = None

            if filename:

                image = load_image(
                    filename,
                    (75, 85)
                )

            if image is None:

                fallback_files = {
                    "Lumi": "lumi.png",
                    "Pipi": "mepple.png",
                    "Coco": "mipple.png",
                    "Ruru": "lumi.png",
                    "Nana": "lumi.png"
                }

                fallback = fallback_files.get(
                    npc_name
                )

                if fallback:

                    image = load_image(
                        fallback,
                        (75, 85)
                    )

            image_rect = pygame.Rect(
                card.x + 15,
                card.y + 20,
                75,
                85
            )

            if image:

                image_rect_centered = image.get_rect(
                    center=image_rect.center
                )

                self.screen.blit(
                    image,
                    image_rect_centered
                )

            else:

                pygame.draw.circle(
                    self.screen,
                    (105, 85, 130),
                    image_rect.center,
                    32
                )

            # ----------------------------------------------------
            # NAME
            # ----------------------------------------------------

            name_surface = self.large_font.render(
                npc_name,
                True,
                (255, 255, 255)
            )

            self.screen.blit(
                name_surface,
                (
                    card.x + 110,
                    card.y + 16
                )
            )

            # ----------------------------------------------------
            # LEVEL
            # ----------------------------------------------------

            level_surface = self.small_font.render(
                relationship_level,
                True,
                (255, 220, 140)
            )

            self.screen.blit(
                level_surface,
                (
                    card.x + 110,
                    card.y + 52
                )
            )

            # ----------------------------------------------------
            # POINTS
            # ----------------------------------------------------

            points_surface = self.small_font.render(
                f"{friendship} / 100",
                True,
                (220, 215, 235)
            )

            self.screen.blit(
                points_surface,
                (
                    card.x + 110,
                    card.y + 82
                )
            )

            # ----------------------------------------------------
            # PROGRESS BAR
            # ----------------------------------------------------

            bar_x = card.x + 290
            bar_y = card.y + 58

            bar_width = min(
                300,
                card.width - 390
            )

            bar_height = 18

            if bar_width < 100:

                bar_width = 100

            pygame.draw.rect(
                self.screen,
                (30, 27, 40),
                (
                    bar_x,
                    bar_y,
                    bar_width,
                    bar_height
                ),
                border_radius=9
            )

            fill_width = int(
                bar_width
                * friendship
                / 100
            )

            if fill_width > 0:

                pygame.draw.rect(
                    self.screen,
                    (220, 110, 170),
                    (
                        bar_x,
                        bar_y,
                        fill_width,
                        bar_height
                    ),
                    border_radius=9
                )

            pygame.draw.rect(
                self.screen,
                (180, 155, 205),
                (
                    bar_x,
                    bar_y,
                    bar_width,
                    bar_height
                ),
                2,
                border_radius=9
            )

            # ----------------------------------------------------
            # HEARTS
            # ----------------------------------------------------

            heart_count = min(
                5,
                max(
                    1,
                    (friendship // 20) + 1
                )
            )

            hearts = ""

            for i in range(5):

                if i < heart_count:

                    hearts += "♥ "

                else:

                    hearts += "♡ "

            heart_surface = self.font.render(
                hearts,
                True,
                (255, 150, 190)
            )

            self.screen.blit(
                heart_surface,
                (
                    bar_x,
                    card.y + 82
                )
            )

            # ----------------------------------------------------
            # NEXT LEVEL
            # ----------------------------------------------------

            if friendship < 20:

                next_text = (
                    f"{20 - friendship} points "
                    "to Friends"
                )

            elif friendship < 40:

                next_text = (
                    f"{40 - friendship} points "
                    "to Good Friends"
                )

            elif friendship < 60:

                next_text = (
                    f"{60 - friendship} points "
                    "to Close Friends"
                )

            elif friendship < 80:

                next_text = (
                    f"{80 - friendship} points "
                    "to Best Friends"
                )

            else:

                next_text = (
                    "Maximum friendship!"
                )

            next_surface = self.tiny_font.render(
                next_text,
                True,
                (175, 170, 195)
            )

            self.screen.blit(
                next_surface,
                (
                    bar_x,
                    card.y + 103
                )
            )

            y += (
                card_height
                + card_gap
            )

        # --------------------------------------------------------
        # RESTORE CLIP
        # --------------------------------------------------------

        self.screen.set_clip(
            old_clip
        )

        # --------------------------------------------------------
        # SCROLLBAR
        # --------------------------------------------------------

        if max_scroll > 0:

            scrollbar_x = (
                SCREEN_WIDTH - 18
            )

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
                    8,
                    scrollbar_height
                ),
                border_radius=4
            )

            thumb_height = max(
                35,
                int(
                    scrollbar_height
                    * viewport.height
                    / total_height
                )
            )

            thumb_range = (
                scrollbar_height
                - thumb_height
            )

            thumb_y = (
                scrollbar_y
                + int(
                    thumb_range
                    * self.relationship_scroll
                    / max_scroll
                )
            )

            pygame.draw.rect(
                self.screen,
                (180, 155, 225),
                (
                    scrollbar_x,
                    thumb_y,
                    8,
                    thumb_height
                ),
                border_radius=4
            )

        # --------------------------------------------------------
        # FOOTER
        # --------------------------------------------------------

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
                "R / ESC  Back     "
                "↑ ↓ Scroll     "
                "Mouse Wheel"
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
    # QUEST DETAILS
    # ============================================================

    def draw_quest_details(self):

        quest = self.selected_quest

        if quest is None:

            self.state = "quest_log"

            return

        self.screen.fill(
            (30, 25, 45)
        )

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

        self.screen.blit(
            title,
            (
                75,
                75
            )
        )

        status = self.get_quest_status(
            quest
        )

        status_text = self.font.render(
            f"{status}  •  From {quest.giver_name}",
            True,
            (220, 215, 235)
        )

        self.screen.blit(
            status_text,
            (
                75,
                120
            )
        )

        # --------------------------------------------------------
        # DESCRIPTION
        # --------------------------------------------------------

        desc_y = 175

        words = quest.description.split()

        line = ""

        lines = []

        for word in words:

            test = (
                line
                + " "
                + word
            ).strip()

            if self.font.size(
                test
            )[0] > SCREEN_WIDTH - 180:

                lines.append(
                    line
                )

                line = word

            else:

                line = test

        if line:

            lines.append(
                line
            )

        for line in lines:

            surf = self.font.render(
                line,
                True,
                (240, 235, 245)
            )

            self.screen.blit(
                surf,
                (
                    75,
                    desc_y
                )
            )

            desc_y += 34

        objective = self.font.render(
            (
                f"Objective: "
                f"{quest.progress}/"
                f"{quest.required_amount}"
            ),
            True,
            (255, 220, 150)
        )

        self.screen.blit(
            objective,
            (
                75,
                desc_y + 25
            )
        )

        reward = self.font.render(
            (
                f"Reward: "
                f"{quest.reward_coins} coins"
            ),
            True,
            (255, 220, 150)
        )

        self.screen.blit(
            reward,
            (
                75,
                desc_y + 65
            )
        )

        target_npc = (
            self.get_navigator_npc_for_quest(
                quest
            )
        )

        target_name = (
            target_npc.name
            if target_npc
            else quest.giver_name
        )

        (
            current_target,
            current_target_type,
            current_target_name
        ) = self.get_navigator_target(
            quest
        )

        if current_target_name:

            target_label = (
                "Current Navigator Target: "
                f"{current_target_name}"
            )

        else:

            target_label = (
                f"Quest NPC: {target_name}"
            )

        target = self.small_font.render(
            target_label,
            True,
            (205, 195, 225)
        )

        self.screen.blit(
            target,
            (
                75,
                desc_y + 105
            )
        )

        # --------------------------------------------------------
        # NAVIGATION
        # --------------------------------------------------------

        if status == "ACTIVE":

            button = (
                self.get_quest_navigate_button_rect()
            )

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

                if (
                    current_target_type == "npc"
                    and quest.is_finished()
                ):

                    button_label = (
                        "RETURN TO "
                        f"{current_target_name}"
                    )

                else:

                    button_label = (
                        "NAVIGATE TO "
                        f"{current_target_name}"
                    )

            else:

                button_label = (
                    "NAVIGATE TO "
                    f"{target_name}"
                )

            label = self.font.render(
                button_label,
                True,
                (255, 255, 255)
            )

            self.screen.blit(
                label,
                label.get_rect(
                    center=button.center
                )
            )

        else:

            hint = self.small_font.render(
                (
                    "Accept this quest first "
                    "to enable navigation."
                ),
                True,
                (170, 165, 185)
            )

            self.screen.blit(
                hint,
                hint.get_rect(
                    center=(
                        SCREEN_WIDTH // 2,
                        SCREEN_HEIGHT - 115
                    )
                )
            )

        # --------------------------------------------------------
        # BACK
        # --------------------------------------------------------

        back = (
            self.get_quest_details_back_rect()
        )

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

        self.screen.blit(
            back_text,
            back_text.get_rect(
                center=back.center
            )
        )

        hint = self.small_font.render(
            "Click Navigate, or press N",
            True,
            (180, 175, 195)
        )

        self.screen.blit(
            hint,
            hint.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    SCREEN_HEIGHT - 55
                )
            )
        )

    # ============================================================
    # PAUSE
    # ============================================================

    def get_pause_resume_rect(self):

        return pygame.Rect(
            SCREEN_WIDTH // 2 - 210,
            300,
            420,
            55
        )

    def get_pause_save_rect(self):

        return pygame.Rect(
            SCREEN_WIDTH // 2 - 210,
            370,
            420,
            55
        )

    def get_pause_menu_rect(self):

        return pygame.Rect(
            SCREEN_WIDTH // 2 - 210,
            440,
            420,
            55
        )

    def draw_pause(self):

        overlay = pygame.Surface(
            (
                SCREEN_WIDTH,
                SCREEN_HEIGHT
            ),
            pygame.SRCALPHA
        )

        overlay.fill(
            (0, 0, 0, 165)
        )

        self.screen.blit(
            overlay,
            (
                0,
                0
            )
        )

        title = self.title_font.render(
            "PAUSED",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            title,
            title.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    220
                )
            )
        )

        buttons = [
            (
                self.get_pause_resume_rect(),
                "RESUME",
                "ESC"
            ),
            (
                self.get_pause_save_rect(),
                "SAVE GAME",
                "S"
            ),
            (
                self.get_pause_menu_rect(),
                "SAVE & MAIN MENU",
                "M"
            )
        ]

        mouse_pos = pygame.mouse.get_pos()

        for rect, label, key in buttons:

            hovered = rect.collidepoint(
                mouse_pos
            )

            bg = (
                (125, 95, 165)
                if hovered
                else (70, 55, 95)
            )

            border = (
                (255, 225, 140)
                if hovered
                else (160, 140, 190)
            )

            pygame.draw.rect(
                self.screen,
                bg,
                rect,
                border_radius=14
            )

            pygame.draw.rect(
                self.screen,
                border,
                rect,
                2,
                border_radius=14
            )

            text = self.font.render(
                f"{label}   [{key}]",
                True,
                (255, 255, 255)
            )

            self.screen.blit(
                text,
                text.get_rect(
                    center=rect.center
                )
            )

        hint = self.small_font.render(
            (
                "ESC Resume    "
                "S Save Game    "
                "M Save & Main Menu"
            ),
            True,
            (225, 215, 240)
        )

        self.screen.blit(
            hint,
            hint.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    SCREEN_HEIGHT - 35
                )
            )
        )

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
    # MAIN DRAW DISPATCH
    # ============================================================

    def draw(self):

        # --------------------------------------------------------
        # MAIN MENU
        # --------------------------------------------------------

        if self.state == "main_menu":

            self.draw_main_menu()

            return

        # --------------------------------------------------------
        # CHARACTER SELECT
        # --------------------------------------------------------

        if self.state == "character_select":

            self.draw_character_select()

            return

        # --------------------------------------------------------
        # QUEST LOG
        # --------------------------------------------------------

        if self.state == "quest_log":

            self.draw_quest_log()

            return

        # --------------------------------------------------------
        # QUEST DETAILS
        # --------------------------------------------------------

        if self.state == "quest_details":

            self.draw_quest_details()

            return

        # --------------------------------------------------------
        # RELATIONSHIPS
        # --------------------------------------------------------

        if self.state == "relationships":

            self.draw_relationships()

            return

        # --------------------------------------------------------
        # WORLD
        # --------------------------------------------------------

        self.draw_world()

        self.draw_hud()

        # --------------------------------------------------------
        # NAVIGATOR
        # --------------------------------------------------------

        if self.state == "playing":

            self.draw_navigator()

        # --------------------------------------------------------
        # DIALOGUE
        # --------------------------------------------------------

        if self.dialogue_npc is not None:

            self.draw_dialogue()

        # --------------------------------------------------------
        # PAUSE
        # --------------------------------------------------------

        if self.state == "pause":

            self.draw_pause()