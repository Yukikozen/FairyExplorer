# # from .core import *
# # from .entities import Fairy, PartyFairy

# # class SaveMixin:
# #     def build_save_data(self):
# #         if self.player is None or self.selected_character is None:
# #             return None
# #         return {
# #             "version": 1,
# #             "selected_character": self.selected_character,
# #             "coins": self.coins,
# #             "game_time_ms": self.game_time_ms,
# #             "player": {"x": self.player.x, "y": self.player.y},
# #             "companion": ({"x": self.companion.x, "y": self.companion.y} if self.companion else None),
# #             "flowers": [bool(f.collected) for f in self.flowers],
# #             "quest_items": [bool(i.collected) for i in self.quest_items],
# #             "npcs": [{"name": n.name, "x": n.x, "y": n.y} for n in self.npcs],
# #             "quests": [{"quest_id": q.quest_id, "progress": q.progress, "accepted": q.accepted, "completed": q.completed, "reward_claimed": q.reward_claimed, "visited_targets": list(q.visited_targets)} for q in self.quests],
# #             "navigator": {"enabled": self.navigator_enabled, "quest_id": self.navigator_quest_id}
# #         }


# #     def save_game(self, silent=False):
# #         data = self.build_save_data()
# #         if data is None:
# #             if not silent:
# #                 self.show_notification("There is no active adventure to save.")
# #             return False
# #         if self.save_manager.save(data):
# #             self.refresh_main_menu_options()
# #             if not silent:
# #                 self.show_notification("Game saved successfully!")
# #             print("[SAVE] Game saved successfully.")
# #             return True
# #         if not silent:
# #             self.show_notification("Unable to save the game.")
# #         return False


# #     def load_game(self):
# #         data = self.save_manager.load()
# #         if not data:
# #             self.show_notification("No save game found.")
# #             return False
# #         try:
# #             self.obstacles = []
# #             self.flowers = []
# #             self.quest_items = []
# #             self.quest_locations = []
# #             self.npcs = []
# #             self.quests = []
# #             self.generate_world()
# #             self.create_quests()

# #             character = data.get("selected_character", "Mepple")
# #             pdata = data.get("player", {})
# #             px, py = float(pdata.get("x", 500)), float(pdata.get("y", 1000))
# #             if character == "Mipple":
# #                 self.player = Fairy("Mipple", "mipple.png", px, py)
# #                 companion_name, companion_image = "Mepple", "mepple.png"
# #             else:
# #                 self.player = Fairy("Mepple", "mepple.png", px, py)
# #                 companion_name, companion_image = "Mipple", "mipple.png"
# #             cdata = data.get("companion") or {}
# #             self.companion = PartyFairy(companion_name, companion_image, float(cdata.get("x", px - 80)), float(cdata.get("y", py)))
# #             self.selected_character = character
# #             self.coins = int(data.get("coins", 0))
# #             self.game_time_ms = float(data.get("game_time_ms", (8 * 60 / 24) * GAME_DAY_LENGTH_MS)) % GAME_DAY_LENGTH_MS

# #             for i, value in enumerate(data.get("flowers", [])):
# #                 if i < len(self.flowers): self.flowers[i].collected = bool(value)
# #             for i, value in enumerate(data.get("quest_items", [])):
# #                 if i < len(self.quest_items): self.quest_items[i].collected = bool(value)

# #             npc_by_name = {n.name: n for n in self.npcs}
# #             for saved in data.get("npcs", []):
# #                 npc = npc_by_name.get(saved.get("name"))
# #                 if npc:
# #                     npc.x = float(saved.get("x", npc.x)); npc.y = float(saved.get("y", npc.y)); npc.sync_rect(); npc.target_x = npc.x; npc.target_y = npc.y

# #             quest_by_id = {q.quest_id: q for q in self.quests}
# #             for saved in data.get("quests", []):
# #                 q = quest_by_id.get(saved.get("quest_id"))
# #                 if not q: continue
# #                 q.progress = min(int(saved.get("progress", 0)), q.required_amount)
# #                 q.accepted = bool(saved.get("accepted", False)); q.completed = bool(saved.get("completed", False)); q.reward_claimed = bool(saved.get("reward_claimed", False)); q.visited_targets = set(saved.get("visited_targets", []))

# #             nav = data.get("navigator", {})
# #             self.navigator_enabled = bool(nav.get("enabled", False)); self.navigator_quest_id = nav.get("quest_id"); self.navigator_quest_index = 0
# #             if self.navigator_quest_id:
# #                 for index, q in enumerate(self.get_active_quests()):
# #                     if q.quest_id == self.navigator_quest_id:
# #                         self.navigator_quest_index = index; break
# #                 else:
# #                     self.navigator_enabled = False; self.navigator_quest_id = None

# #             self.pending_quest = None; self.quest_offer_ready = False; self.dialogue_npc = None; self.dialogue_lines = []; self.dialogue_index = 0; self.selected_quest = None
# #             self.state = "playing"
# #             self.camera.update(self.player.rect)
# #             self.show_notification("Game loaded successfully!")
# #             print("[SAVE] Game loaded successfully.")
# #             return True
# #         except (TypeError, ValueError, KeyError) as exc:
# #             print(f"[SAVE] Invalid save data: {exc}")
# #             self.show_notification("The save game could not be loaded.")
# #             return False


# #     def start_new_adventure(self, character):
# #         self.obstacles = []; self.flowers = []; self.quest_items = []; self.quest_locations = []; self.npcs = []; self.quests = []
# #         self.generate_world(); self.create_quests()
# #         self.coins = 0; self.navigator_enabled = False; self.navigator_quest_id = None; self.navigator_quest_index = 0
# #         self.start_adventure(character)


# #     def start_adventure(
# #         self,
# #         character
# #     ):

# #         self.selected_character = character
# #         self.navigator_enabled = False
# #         self.navigator_quest_id = None
# #         self.navigator_quest_index = 0
# #         self.selected_quest = None

# #         x, y = self.find_safe_spawn()

# #         if character == "Mepple":

# #             self.player = Fairy(
# #                 "Mepple",
# #                 "mepple.png",
# #                 x,
# #                 y
# #             )

# #             self.companion = PartyFairy(
# #                 "Mipple",
# #                 "mipple.png",
# #                 x - 80,
# #                 y
# #             )

# #         else:

# #             self.player = Fairy(
# #                 "Mipple",
# #                 "mipple.png",
# #                 x,
# #                 y
# #             )

# #             self.companion = PartyFairy(
# #                 "Mepple",
# #                 "mepple.png",
# #                 x - 80,
# #                 y
# #             )

# #         self.camera.update(
# #             self.player.rect
# #         )

# #         self.state = "playing"

# #         self.show_notification(
# #             f"{character} joined the adventure!"
# #         )


# from .core import *
# from .entities import Fairy, PartyFairy


# class SaveMixin:

#     # ============================================================
#     # SAVE DATA
#     # ============================================================

#     def build_save_data(self):

#         if self.player is None or self.selected_character is None:
#             return None

#         return {
#             "version": 1,

#             "selected_character": self.selected_character,

#             "coins": self.coins,

#             # Save the current in-game time.
#             "game_time_ms": self.game_time_ms,

#             "player": {
#                 "x": self.player.x,
#                 "y": self.player.y
#             },

#             "companion": (
#                 {
#                     "x": self.companion.x,
#                     "y": self.companion.y
#                 }
#                 if self.companion
#                 else None
#             ),

#             "flowers": [
#                 bool(f.collected)
#                 for f in self.flowers
#             ],

#             "quest_items": [
#                 bool(i.collected)
#                 for i in self.quest_items
#             ],

#             "npcs": [
#                 {
#                     "name": n.name,
#                     "x": n.x,
#                     "y": n.y
#                 }
#                 for n in self.npcs
#             ],

#             "quests": [
#                 {
#                     "quest_id": q.quest_id,
#                     "progress": q.progress,
#                     "accepted": q.accepted,
#                     "completed": q.completed,
#                     "reward_claimed": q.reward_claimed,
#                     "visited_targets": list(q.visited_targets)
#                 }
#                 for q in self.quests
#             ],

#             "navigator": {
#                 "enabled": self.navigator_enabled,
#                 "quest_id": self.navigator_quest_id
#             }
#         }

#     # ============================================================
#     # SAVE GAME
#     # ============================================================

#     def save_game(self, silent=False):

#         data = self.build_save_data()

#         if data is None:

#             if not silent:
#                 self.show_notification(
#                     "There is no active adventure to save."
#                 )

#             return False

#         if self.save_manager.save(data):

#             self.refresh_main_menu_options()

#             if not silent:
#                 self.show_notification(
#                     "Game saved successfully!"
#                 )

#             print("[SAVE] Game saved successfully.")

#             return True

#         if not silent:
#             self.show_notification(
#                 "Unable to save the game."
#             )

#         return False

#     # ============================================================
#     # LOAD GAME
#     # ============================================================

#     def load_game(self):

#         data = self.save_manager.load()

#         if not data:

#             self.show_notification(
#                 "No save game found."
#             )

#             return False

#         try:

#             # ----------------------------------------------------
#             # RESET WORLD CONTAINERS
#             # ----------------------------------------------------

#             self.obstacles = []
#             self.flowers = []
#             self.quest_items = []
#             self.quest_locations = []
#             self.npcs = []
#             self.quests = []

#             # ----------------------------------------------------
#             # REGENERATE WORLD
#             # ----------------------------------------------------

#             self.generate_world()
#             self.create_quests()

#             # ----------------------------------------------------
#             # CHARACTER
#             # ----------------------------------------------------

#             character = data.get(
#                 "selected_character",
#                 "Mepple"
#             )

#             # ----------------------------------------------------
#             # PLAYER POSITION
#             # ----------------------------------------------------

#             pdata = data.get(
#                 "player",
#                 {}
#             )

#             px = float(
#                 pdata.get(
#                     "x",
#                     500
#                 )
#             )

#             py = float(
#                 pdata.get(
#                     "y",
#                     1000
#                 )
#             )

#             # ----------------------------------------------------
#             # CREATE PLAYER
#             # ----------------------------------------------------

#             if character == "Mipple":

#                 self.player = Fairy(
#                     "Mipple",
#                     "mipple.png",
#                     px,
#                     py
#                 )

#                 companion_name = "Mepple"
#                 companion_image = "mepple.png"

#             else:

#                 self.player = Fairy(
#                     "Mepple",
#                     "mepple.png",
#                     px,
#                     py
#                 )

#                 companion_name = "Mipple"
#                 companion_image = "mipple.png"

#             # ----------------------------------------------------
#             # CREATE COMPANION
#             # ----------------------------------------------------

#             cdata = data.get(
#                 "companion"
#             ) or {}

#             companion_x = float(
#                 cdata.get(
#                     "x",
#                     px - 80
#                 )
#             )

#             companion_y = float(
#                 cdata.get(
#                     "y",
#                     py
#                 )
#             )

#             self.companion = PartyFairy(
#                 companion_name,
#                 companion_image,
#                 companion_x,
#                 companion_y
#             )

#             # ----------------------------------------------------
#             # RESTORE BASIC DATA
#             # ----------------------------------------------------

#             self.selected_character = character

#             self.coins = int(
#                 data.get(
#                     "coins",
#                     0
#                 )
#             )

#             # ----------------------------------------------------
#             # RESTORE GAME TIME
#             #
#             # IMPORTANT:
#             # Loading a saved game keeps the saved time.
#             #
#             # If an old save has no game_time_ms, use 8:00 AM.
#             # ----------------------------------------------------

#             default_time = (
#                 (8 * 60 / 24)
#                 * GAME_DAY_LENGTH_MS
#             )

#             self.game_time_ms = float(
#                 data.get(
#                     "game_time_ms",
#                     default_time
#                 )
#             ) % GAME_DAY_LENGTH_MS

#             # ----------------------------------------------------
#             # RESTORE FLOWERS
#             # ----------------------------------------------------

#             for i, value in enumerate(
#                 data.get("flowers", [])
#             ):

#                 if i < len(self.flowers):

#                     self.flowers[i].collected = bool(
#                         value
#                     )

#             # ----------------------------------------------------
#             # RESTORE QUEST ITEMS
#             # ----------------------------------------------------

#             for i, value in enumerate(
#                 data.get("quest_items", [])
#             ):

#                 if i < len(self.quest_items):

#                     self.quest_items[i].collected = bool(
#                         value
#                     )

#             # ----------------------------------------------------
#             # RESTORE NPC POSITIONS
#             # ----------------------------------------------------

#             npc_by_name = {
#                 n.name: n
#                 for n in self.npcs
#             }

#             for saved in data.get(
#                 "npcs",
#                 []
#             ):

#                 npc = npc_by_name.get(
#                     saved.get("name")
#                 )

#                 if npc:

#                     npc.x = float(
#                         saved.get(
#                             "x",
#                             npc.x
#                         )
#                     )

#                     npc.y = float(
#                         saved.get(
#                             "y",
#                             npc.y
#                         )
#                     )

#                     npc.sync_rect()

#                     npc.target_x = npc.x
#                     npc.target_y = npc.y

#                     # Reset movement state if the newer
#                     # NPC movement system exists.

#                     if hasattr(
#                         npc,
#                         "velocity_x"
#                     ):
#                         npc.velocity_x = 0.0

#                     if hasattr(
#                         npc,
#                         "velocity_y"
#                     ):
#                         npc.velocity_y = 0.0

#                     if hasattr(
#                         npc,
#                         "path"
#                     ):
#                         npc.path = []

#                     if hasattr(
#                         npc,
#                         "path_index"
#                     ):
#                         npc.path_index = 0

#             # ----------------------------------------------------
#             # RESTORE QUESTS
#             # ----------------------------------------------------

#             quest_by_id = {
#                 q.quest_id: q
#                 for q in self.quests
#             }

#             for saved in data.get(
#                 "quests",
#                 []
#             ):

#                 q = quest_by_id.get(
#                     saved.get("quest_id")
#                 )

#                 if not q:
#                     continue

#                 q.progress = min(
#                     int(
#                         saved.get(
#                             "progress",
#                             0
#                         )
#                     ),
#                     q.required_amount
#                 )

#                 q.accepted = bool(
#                     saved.get(
#                         "accepted",
#                         False
#                     )
#                 )

#                 q.completed = bool(
#                     saved.get(
#                         "completed",
#                         False
#                     )
#                 )

#                 q.reward_claimed = bool(
#                     saved.get(
#                         "reward_claimed",
#                         False
#                     )
#                 )

#                 q.visited_targets = set(
#                     saved.get(
#                         "visited_targets",
#                         []
#                     )
#                 )

#             # ----------------------------------------------------
#             # RESTORE NAVIGATOR
#             # ----------------------------------------------------

#             nav = data.get(
#                 "navigator",
#                 {}
#             )

#             self.navigator_enabled = bool(
#                 nav.get(
#                     "enabled",
#                     False
#                 )
#             )

#             self.navigator_quest_id = nav.get(
#                 "quest_id"
#             )

#             self.navigator_quest_index = 0

#             if self.navigator_quest_id:

#                 for index, q in enumerate(
#                     self.get_active_quests()
#                 ):

#                     if (
#                         q.quest_id
#                         == self.navigator_quest_id
#                     ):

#                         self.navigator_quest_index = index
#                         break

#                 else:

#                     self.navigator_enabled = False
#                     self.navigator_quest_id = None

#             # ----------------------------------------------------
#             # RESET DIALOGUE
#             # ----------------------------------------------------

#             self.pending_quest = None
#             self.quest_offer_ready = False

#             self.dialogue_npc = None
#             self.dialogue_lines = []
#             self.dialogue_index = 0

#             self.selected_quest = None

#             # ----------------------------------------------------
#             # ENTER GAME
#             # ----------------------------------------------------

#             self.state = "playing"

#             self.camera.update(
#                 self.player.rect
#             )

#             self.show_notification(
#                 "Game loaded successfully!"
#             )

#             print("[SAVE] Game loaded successfully.")

#             return True

#         except (
#             TypeError,
#             ValueError,
#             KeyError
#         ) as exc:

#             print(
#                 f"[SAVE] Invalid save data: {exc}"
#             )

#             self.show_notification(
#                 "The save game could not be loaded."
#             )

#             return False

#     # ============================================================
#     # START NEW ADVENTURE
#     # ============================================================

#     def start_new_adventure(
#         self,
#         character
#     ):

#         # ========================================================
#         # RESET WORLD
#         # ========================================================

#         self.obstacles = []
#         self.flowers = []
#         self.quest_items = []
#         self.quest_locations = []
#         self.npcs = []
#         self.quests = []

#         # ========================================================
#         # GENERATE COMPLETELY NEW WORLD
#         # ========================================================

#         self.generate_world()
#         self.create_quests()

#         # ========================================================
#         # RESET PLAYER PROGRESS
#         # ========================================================

#         self.coins = 0

#         self.navigator_enabled = False
#         self.navigator_quest_id = None
#         self.navigator_quest_index = 0
#         self.selected_quest = None

#         # ========================================================
#         # IMPORTANT
#         #
#         # A NEW GAME ALWAYS STARTS AT 08:00 AM.
#         #
#         # This is deliberately here instead of relying only
#         # on Game.__init__(), because Game.__init__() only runs
#         # when the Game object itself is created.
#         #
#         # When the player selects "New Game", this method is
#         # called later, so we must reset the clock here too.
#         # ========================================================

#         self.game_time_ms = (
#             (8 * 60 / 24)
#             * GAME_DAY_LENGTH_MS
#         )

#         print(
#             "[TIME] New adventure started at 08:00 AM."
#         )

#         # ========================================================
#         # START ADVENTURE
#         # ========================================================

#         self.start_adventure(
#             character
#         )

#     # ============================================================
#     # START ADVENTURE
#     # ============================================================

#     def start_adventure(
#         self,
#         character
#     ):

#         self.selected_character = character

#         self.navigator_enabled = False
#         self.navigator_quest_id = None
#         self.navigator_quest_index = 0
#         self.selected_quest = None

#         # ========================================================
#         # FIND SAFE PLAYER SPAWN
#         # ========================================================

#         x, y = self.find_safe_spawn()

#         # ========================================================
#         # CREATE PLAYER + COMPANION
#         # ========================================================

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

#         # ========================================================
#         # UPDATE CAMERA
#         # ========================================================

#         self.camera.update(
#             self.player.rect
#         )

#         # ========================================================
#         # ENTER PLAYING STATE
#         # ========================================================

#         self.state = "playing"

#         # ========================================================
#         # SHOW START MESSAGE
#         # ========================================================

#         self.show_notification(
#             f"{character} joined the adventure!"
#         )

#         # ========================================================
#         # DEBUG
#         # ========================================================

#         total_minutes = (
#             self.game_time_ms
#             / GAME_DAY_LENGTH_MS
#             * 24
#             * 60
#         )

#         hour = int(
#             total_minutes // 60
#         )

#         minute = int(
#             total_minutes % 60
#         )

#         period = (
#             "AM"
#             if hour < 12
#             else "PM"
#         )

#         display_hour = hour % 12

#         if display_hour == 0:
#             display_hour = 12

#         print(
#             f"[TIME] Adventure time: "
#             f"{display_hour:02d}:{minute:02d} {period}"
#         )


from .core import *
from .entities import Fairy, PartyFairy


class SaveMixin:

    # ============================================================
    # NEW GAME TIME
    # ============================================================

    def reset_new_game_time(self):
        """
        Every brand-new adventure starts at 08:00 AM.

        GAME_DAY_LENGTH_MS represents the length of one full
        24-hour game day.

        08:00 / 24:00 of the day =
        8 / 24 of GAME_DAY_LENGTH_MS.
        """

        self.game_time_ms = (
            (8 * 60) / (24 * 60)
        ) * GAME_DAY_LENGTH_MS

        # Keep the value inside one complete game day.
        self.game_time_ms %= GAME_DAY_LENGTH_MS

        print(
            "[TIME] New adventure starts at 08:00 AM"
        )


    # ============================================================
    # BUILD SAVE DATA
    # ============================================================

    def build_save_data(self):

        if (
            self.player is None
            or self.selected_character is None
        ):
            return None

        return {
            "version": 1,

            "selected_character":
                self.selected_character,

            "coins":
                self.coins,

            "game_time_ms":
                self.game_time_ms,

            "player": {
                "x": self.player.x,
                "y": self.player.y
            },

            "companion": (
                {
                    "x": self.companion.x,
                    "y": self.companion.y
                }
                if self.companion
                else None
            ),

            "flowers": [
                bool(f.collected)
                for f in self.flowers
            ],

            "quest_items": [
                bool(i.collected)
                for i in self.quest_items
            ],

            "npcs": [
                {
                    "name": n.name,
                    "x": n.x,
                    "y": n.y
                }
                for n in self.npcs
            ],

            "quests": [
                {
                    "quest_id": q.quest_id,
                    "progress": q.progress,
                    "accepted": q.accepted,
                    "completed": q.completed,
                    "reward_claimed": q.reward_claimed,
                    "visited_targets":
                        list(q.visited_targets)
                }
                for q in self.quests
            ],

            "navigator": {
                "enabled":
                    self.navigator_enabled,

                "quest_id":
                    self.navigator_quest_id
            }
        }


    # ============================================================
    # SAVE GAME
    # ============================================================

    def save_game(
        self,
        silent=False
    ):

        data = self.build_save_data()

        if data is None:

            if not silent:

                self.show_notification(
                    "There is no active adventure to save."
                )

            return False

        if self.save_manager.save(data):

            self.refresh_main_menu_options()

            if not silent:

                self.show_notification(
                    "Game saved successfully!"
                )

            print(
                "[SAVE] Game saved successfully."
            )

            return True

        if not silent:

            self.show_notification(
                "Unable to save the game."
            )

        return False


    # ============================================================
    # LOAD GAME
    # ============================================================

    def load_game(self):

        data = self.save_manager.load()

        if not data:

            self.show_notification(
                "No save game found."
            )

            return False

        try:

            # ----------------------------------------------------
            # Rebuild world
            # ----------------------------------------------------

            self.obstacles = []
            self.flowers = []
            self.quest_items = []
            self.quest_locations = []
            self.npcs = []
            self.quests = []

            self.generate_world()
            self.create_quests()

            # ----------------------------------------------------
            # Character
            # ----------------------------------------------------

            character = data.get(
                "selected_character",
                "Mepple"
            )

            # ----------------------------------------------------
            # Player position
            # ----------------------------------------------------

            pdata = data.get(
                "player",
                {}
            )

            px = float(
                pdata.get(
                    "x",
                    500
                )
            )

            py = float(
                pdata.get(
                    "y",
                    1000
                )
            )

            if character == "Mipple":

                self.player = Fairy(
                    "Mipple",
                    "mipple.png",
                    px,
                    py
                )

                companion_name = "Mepple"
                companion_image = "mepple.png"

            else:

                self.player = Fairy(
                    "Mepple",
                    "mepple.png",
                    px,
                    py
                )

                companion_name = "Mipple"
                companion_image = "mipple.png"

            # ----------------------------------------------------
            # Companion
            # ----------------------------------------------------

            cdata = (
                data.get("companion")
                or {}
            )

            self.companion = PartyFairy(
                companion_name,
                companion_image,
                float(
                    cdata.get(
                        "x",
                        px - 80
                    )
                ),
                float(
                    cdata.get(
                        "y",
                        py
                    )
                )
            )

            # ----------------------------------------------------
            # General game data
            # ----------------------------------------------------

            self.selected_character = character

            self.coins = int(
                data.get(
                    "coins",
                    0
                )
            )

            # IMPORTANT:
            # CONTINUE keeps the saved game time.
            #
            # Only NEW GAME resets to 08:00.
            self.game_time_ms = float(
                data.get(
                    "game_time_ms",
                    (
                        (8 * 60)
                        / (24 * 60)
                    ) * GAME_DAY_LENGTH_MS
                )
            )

            self.game_time_ms %= GAME_DAY_LENGTH_MS

            # ----------------------------------------------------
            # Flowers
            # ----------------------------------------------------

            for i, value in enumerate(
                data.get(
                    "flowers",
                    []
                )
            ):

                if i < len(
                    self.flowers
                ):

                    self.flowers[
                        i
                    ].collected = bool(
                        value
                    )

            # ----------------------------------------------------
            # Quest items
            # ----------------------------------------------------

            for i, value in enumerate(
                data.get(
                    "quest_items",
                    []
                )
            ):

                if i < len(
                    self.quest_items
                ):

                    self.quest_items[
                        i
                    ].collected = bool(
                        value
                    )

            # ----------------------------------------------------
            # NPC positions
            # ----------------------------------------------------

            npc_by_name = {
                n.name: n
                for n in self.npcs
            }

            for saved in data.get(
                "npcs",
                []
            ):

                npc = npc_by_name.get(
                    saved.get("name")
                )

                if npc:

                    npc.x = float(
                        saved.get(
                            "x",
                            npc.x
                        )
                    )

                    npc.y = float(
                        saved.get(
                            "y",
                            npc.y
                        )
                    )

                    npc.sync_rect()

                    npc.target_x = npc.x
                    npc.target_y = npc.y

                    # Reset movement state if the NPC
                    # has these attributes.
                    if hasattr(
                        npc,
                        "velocity_x"
                    ):
                        npc.velocity_x = 0.0

                    if hasattr(
                        npc,
                        "velocity_y"
                    ):
                        npc.velocity_y = 0.0

                    if hasattr(
                        npc,
                        "path"
                    ):
                        npc.path = []

                    if hasattr(
                        npc,
                        "path_index"
                    ):
                        npc.path_index = 0

            # ----------------------------------------------------
            # Quests
            # ----------------------------------------------------

            quest_by_id = {
                q.quest_id: q
                for q in self.quests
            }

            for saved in data.get(
                "quests",
                []
            ):

                q = quest_by_id.get(
                    saved.get("quest_id")
                )

                if not q:
                    continue

                q.progress = min(
                    int(
                        saved.get(
                            "progress",
                            0
                        )
                    ),
                    q.required_amount
                )

                q.accepted = bool(
                    saved.get(
                        "accepted",
                        False
                    )
                )

                q.completed = bool(
                    saved.get(
                        "completed",
                        False
                    )
                )

                q.reward_claimed = bool(
                    saved.get(
                        "reward_claimed",
                        False
                    )
                )

                q.visited_targets = set(
                    saved.get(
                        "visited_targets",
                        []
                    )
                )

            # ----------------------------------------------------
            # Navigator
            # ----------------------------------------------------

            nav = data.get(
                "navigator",
                {}
            )

            self.navigator_enabled = bool(
                nav.get(
                    "enabled",
                    False
                )
            )

            self.navigator_quest_id = (
                nav.get(
                    "quest_id"
                )
            )

            self.navigator_quest_index = 0

            if self.navigator_quest_id:

                for index, q in enumerate(
                    self.get_active_quests()
                ):

                    if (
                        q.quest_id
                        == self.navigator_quest_id
                    ):

                        self.navigator_quest_index = (
                            index
                        )

                        break

                else:

                    self.navigator_enabled = False
                    self.navigator_quest_id = None

            # ----------------------------------------------------
            # Clear dialogue state
            # ----------------------------------------------------

            self.pending_quest = None
            self.quest_offer_ready = False
            self.dialogue_npc = None
            self.dialogue_lines = []
            self.dialogue_index = 0
            self.selected_quest = None

            # ----------------------------------------------------
            # Start loaded game
            # ----------------------------------------------------

            self.state = "playing"

            self.camera.update(
                self.player.rect
            )

            self.show_notification(
                "Game loaded successfully!"
            )

            print(
                "[SAVE] Game loaded successfully."
            )

            print(
                "[TIME] Loaded game time:",
                self.game_time_ms
            )

            return True

        except (
            TypeError,
            ValueError,
            KeyError
        ) as exc:

            print(
                f"[SAVE] Invalid save data: {exc}"
            )

            self.show_notification(
                "The save game could not be loaded."
            )

            return False


    # ============================================================
    # START NEW ADVENTURE
    # ============================================================

    def start_new_adventure(
        self,
        character
    ):

        print(
            "[NEW GAME] Creating new adventure..."
        )

        # --------------------------------------------------------
        # Clear previous game
        # --------------------------------------------------------

        self.obstacles = []
        self.flowers = []
        self.quest_items = []
        self.quest_locations = []
        self.npcs = []
        self.quests = []

        # --------------------------------------------------------
        # Generate completely fresh world
        # --------------------------------------------------------

        self.generate_world()
        self.create_quests()

        # --------------------------------------------------------
        # Reset player progression
        # --------------------------------------------------------

        self.coins = 0

        self.navigator_enabled = False
        self.navigator_quest_id = None
        self.navigator_quest_index = 0
        self.selected_quest = None

        # ========================================================
        # VERY IMPORTANT
        #
        # NEW GAME ALWAYS STARTS AT 08:00 AM
        # ========================================================

        self.reset_new_game_time()

        # --------------------------------------------------------
        # Start adventure
        # --------------------------------------------------------

        self.start_adventure(
            character
        )


    # ============================================================
    # START ADVENTURE
    # ============================================================

    def start_adventure(
        self,
        character
    ):

        self.selected_character = character

        self.navigator_enabled = False
        self.navigator_quest_id = None
        self.navigator_quest_index = 0
        self.selected_quest = None

        # --------------------------------------------------------
        # Find safe player spawn
        # --------------------------------------------------------

        x, y = self.find_safe_spawn()

        # --------------------------------------------------------
        # Create player
        # --------------------------------------------------------

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

        # --------------------------------------------------------
        # Camera
        # --------------------------------------------------------

        self.camera.update(
            self.player.rect
        )

        # --------------------------------------------------------
        # Start playing
        # --------------------------------------------------------

        self.state = "playing"

        # --------------------------------------------------------
        # Debug output
        # --------------------------------------------------------

        total_minutes = int(
            (
                self.game_time_ms
                / GAME_DAY_LENGTH_MS
            )
            * 24
            * 60
        ) % (24 * 60)

        hour = total_minutes // 60
        minute = total_minutes % 60

        print(
            f"[TIME] Adventure started at "
            f"{hour:02d}:{minute:02d}"
        )

        # --------------------------------------------------------
        # Welcome notification
        # --------------------------------------------------------

        self.show_notification(
            f"{character} joined the adventure!"
        )