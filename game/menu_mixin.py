from .core import *

class MenuMixin:
    def refresh_main_menu_options(self):
        if self.save_manager.has_save():
            self.main_menu_options = ["CONTINUE", "START ADVENTURE", "QUIT GAME"]
        else:
            self.main_menu_options = ["START ADVENTURE", "QUIT GAME"]
        self.main_menu_selected = int(clamp(self.main_menu_selected, 0, len(self.main_menu_options) - 1))


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


