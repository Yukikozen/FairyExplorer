from .core import *
from .quests import Quest

class QuestsMixin:
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


