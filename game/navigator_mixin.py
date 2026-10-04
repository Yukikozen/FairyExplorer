from .core import *

class NavigatorMixin:
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


