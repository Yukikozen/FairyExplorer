from .core import *

class PlayerMixin:
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


