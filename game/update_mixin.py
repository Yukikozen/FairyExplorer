from .core import *

class UpdateMixin:
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


