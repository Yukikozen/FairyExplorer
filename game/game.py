# from .core import *
# from .camera import Camera
# from .entities import Obstacle, Flower, QuestItem, QuestLocation, Fairy, PartyFairy
# from .npc import FairyNPC
# from .quests import Quest
# from .save_manager import SaveManager
# from .world_mixin import WorldMixin
# from .quests_mixin import QuestsMixin
# from .navigator_mixin import NavigatorMixin
# from .save_mixin import SaveMixin
# from .menu_mixin import MenuMixin
# from .input_mixin import InputMixin
# from .player_mixin import PlayerMixin
# from .dialogue_mixin import DialogueMixin
# from .update_mixin import UpdateMixin
# from .draw_mixin import DrawMixin

# class Game(WorldMixin, QuestsMixin, NavigatorMixin, SaveMixin, MenuMixin, InputMixin, PlayerMixin, DialogueMixin, UpdateMixin, DrawMixin):
#     def __init__(self, screen):

#         self.screen = screen

#         self.running = True
#         self.save_manager = SaveManager()

#         # --------------------------------------------------------
#         # IMPORTANT:
#         # Game now starts at MAIN MENU.
#         # --------------------------------------------------------

#         self.state = "main_menu"

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

#         # In-game clock: starts at 08:00 and loops through a full day.
#         self.game_time_ms = (8 * 60 / 24) * GAME_DAY_LENGTH_MS
#         self.selected_character = None

#         # --------------------------------------------------------
#         # Main menu
#         # --------------------------------------------------------

#         self.main_menu_selected = 0

#         self.main_menu_options = []
#         self.refresh_main_menu_options()

#         self.menu_sparkles = []

#         for _ in range(80):

#             self.menu_sparkles.append(
#                 {
#                     "x": random.randint(
#                         0,
#                         SCREEN_WIDTH
#                     ),
#                     "y": random.randint(
#                         0,
#                         SCREEN_HEIGHT
#                     ),
#                     "speed": random.uniform(
#                         0.2,
#                         0.8
#                     ),
#                     "size": random.randint(
#                         1,
#                         4
#                     ),
#                     "phase": random.uniform(
#                         0,
#                         math.pi * 2
#                     )
#                 }
#             )

#         self.menu_time = 0

#         # Animation phase used by the quest navigator target pulse.
#         self.phase = 0.0

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
#         # Quest navigator
#         # --------------------------------------------------------

#         self.navigator_enabled = False
#         self.navigator_quest_index = 0
#         self.navigator_quest_id = None

#         # Quest details screen.
#         self.selected_quest = None

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




from .core import *

from .camera import Camera
from .entities import (
    Obstacle,
    Flower,
    QuestItem,
    QuestLocation,
    Fairy,
    PartyFairy,
)
from .npc import FairyNPC
from .quests import Quest
from .save_manager import SaveManager

from .world_mixin import WorldMixin
from .quests_mixin import QuestsMixin
from .navigator_mixin import NavigatorMixin
from .save_mixin import SaveMixin
from .menu_mixin import MenuMixin
from .input_mixin import InputMixin
from .player_mixin import PlayerMixin
from .dialogue_mixin import DialogueMixin
from .update_mixin import UpdateMixin
from .draw_mixin import DrawMixin


class Game(
    WorldMixin,
    QuestsMixin,
    NavigatorMixin,
    SaveMixin,
    MenuMixin,
    InputMixin,
    PlayerMixin,
    DialogueMixin,
    UpdateMixin,
    DrawMixin,
):

    def __init__(self, screen):

        # ============================================================
        # BASIC GAME STATE
        # ============================================================

        self.screen = screen
        self.running = True

        self.save_manager = SaveManager()

        self.state = "main_menu"

        # ============================================================
        # PLAYER / COMPANION
        # ============================================================

        self.player = None
        self.companion = None

        # ============================================================
        # CAMERA
        # ============================================================

        self.camera = Camera()

        # ============================================================
        # WORLD OBJECTS
        # ============================================================

        self.obstacles = []
        self.flowers = []
        self.quest_items = []
        self.quest_locations = []

        # ============================================================
        # NPCs
        # ============================================================

        self.npcs = []

        # ============================================================
        # QUESTS
        # ============================================================

        self.quests = []

        # ============================================================
        # PLAYER CURRENCY
        # ============================================================

        self.coins = 0

        # ============================================================
        # GAME TIME
        #
        # IMPORTANT:
        # Every NEW GAME starts at exactly 8:00 AM.
        #
        # GAME_DAY_LENGTH_MS represents one complete 24-hour
        # in-game day.
        #
        # 8 hours / 24 hours gives us the position of 08:00
        # inside the complete game day.
        # ============================================================

        self.game_time_ms = (
            (8 * 60 / 24)
            * GAME_DAY_LENGTH_MS
        )

        # ============================================================
        # CHARACTER SELECTION
        # ============================================================

        self.selected_character = None

        # ============================================================
        # MAIN MENU
        # ============================================================

        self.main_menu_selected = 0
        self.main_menu_options = []

        self.refresh_main_menu_options()

        # ============================================================
        # MENU SPARKLES
        # ============================================================

        self.menu_sparkles = []

        for _ in range(80):

            self.menu_sparkles.append({
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
                ),
            })

        self.menu_time = 0

        # ============================================================
        # GENERAL ANIMATION PHASE
        # ============================================================

        self.phase = 0.0

        # ============================================================
        # DIALOGUE
        # ============================================================

        self.dialogue_npc = None
        self.dialogue_lines = []
        self.dialogue_index = 0

        # ============================================================
        # QUEST DIALOGUE / OFFER
        # ============================================================

        self.pending_quest = None
        self.quest_offer_ready = False

        # ============================================================
        # QUEST LOG
        # ============================================================

        self.quest_tab = 0

        self.quest_tab_names = [
            "ACTIVE",
            "AVAILABLE",
            "COMPLETED",
            "LOCKED",
        ]

        self.quest_scroll = [
            0,
            0,
            0,
            0,
        ]

        self.quest_content_height = [
            0,
            0,
            0,
            0,
        ]

        # ============================================================
        # NAVIGATOR
        # ============================================================

        self.navigator_enabled = False

        self.navigator_quest_index = 0

        self.navigator_quest_id = None

        self.selected_quest = None

        # ============================================================
        # NOTIFICATIONS
        # ============================================================

        self.notification_text = ""

        self.notification_timer = 0

        # ============================================================
        # FONTS
        # ============================================================

        self.title_font = pygame.font.SysFont(
            "arial",
            30,
            bold=True,
        )

        self.large_font = pygame.font.SysFont(
            "arial",
            24,
            bold=True,
        )

        self.font = pygame.font.SysFont(
            "arial",
            20,
        )

        self.small_font = pygame.font.SysFont(
            "arial",
            16,
        )

        self.tiny_font = pygame.font.SysFont(
            "arial",
            14,
        )

        # ============================================================
        # CREATE WORLD
        # ============================================================

        self.generate_world()

        # ============================================================
        # CREATE QUESTS
        # ============================================================

        self.create_quests()