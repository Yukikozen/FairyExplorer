# # from .core import *

# # class InputMixin:
# #     def handle_event(
# #         self,
# #         event
# #     ):

# #         global SCREEN_WIDTH
# #         global SCREEN_HEIGHT

# #         if event.type == pygame.QUIT:

# #             self.running = False
# #             return

# #         if event.type == pygame.VIDEORESIZE:

# #             SCREEN_WIDTH = max(
# #                 800,
# #                 event.w
# #             )

# #             SCREEN_HEIGHT = max(
# #                 600,
# #                 event.h
# #             )

# #             self.screen = pygame.display.set_mode(
# #                 (
# #                     SCREEN_WIDTH,
# #                     SCREEN_HEIGHT
# #                 ),
# #                 pygame.RESIZABLE
# #             )

# #             return

# #         # ========================================================
# #         # MAIN MENU
# #         # ========================================================

# #         if self.state == "main_menu":

# #             self.handle_main_menu_event(
# #                 event
# #             )

# #             return

# #         # ========================================================
# #         # CHARACTER SELECT
# #         # ========================================================

# #         if self.state == "character_select":

# #             if event.type == pygame.KEYDOWN:

# #                 if event.key == pygame.K_ESCAPE:

# #                     self.state = "main_menu"

# #                 elif event.key == pygame.K_1:

# #                     self.start_new_adventure(
# #                         "Mepple"
# #                     )

# #                 elif event.key == pygame.K_2:

# #                     self.start_new_adventure(
# #                         "Mipple"
# #                     )

# #             elif event.type == pygame.MOUSEBUTTONDOWN:

# #                 if event.button == 1:

# #                     mepple_rect = pygame.Rect(
# #                         SCREEN_WIDTH // 2 - 300,
# #                         260,
# #                         240,
# #                         280
# #                     )

# #                     mipple_rect = pygame.Rect(
# #                         SCREEN_WIDTH // 2 + 60,
# #                         260,
# #                         240,
# #                         280
# #                     )

# #                     if mepple_rect.collidepoint(
# #                         event.pos
# #                     ):

# #                         self.start_adventure(
# #                             "Mepple"
# #                         )

# #                     elif mipple_rect.collidepoint(
# #                         event.pos
# #                     ):

# #                         self.start_adventure(
# #                             "Mipple"
# #                         )

# #             return

# #         # ========================================================
# #         # QUEST LOG
# #         # ========================================================

# #         if self.state == "quest_log":

# #             if event.type == pygame.KEYDOWN:

# #                 if event.key in (
# #                     pygame.K_q,
# #                     pygame.K_ESCAPE
# #                 ):

# #                     self.state = "playing"
# #                     return

# #                 elif event.key == pygame.K_LEFT:

# #                     self.change_quest_tab(-1)

# #                 elif event.key == pygame.K_RIGHT:

# #                     self.change_quest_tab(1)

# #                 elif event.key == pygame.K_UP:

# #                     self.scroll_current_quest_tab(
# #                         -70
# #                     )

# #                 elif event.key == pygame.K_DOWN:

# #                     self.scroll_current_quest_tab(
# #                         70
# #                     )

# #                 elif event.key == pygame.K_PAGEUP:

# #                     self.scroll_current_quest_tab(
# #                         -350
# #                     )

# #                 elif event.key == pygame.K_PAGEDOWN:

# #                     self.scroll_current_quest_tab(
# #                         350
# #                     )

# #                 elif event.key == pygame.K_HOME:

# #                     self.quest_scroll[
# #                         self.quest_tab
# #                     ] = 0

# #                 elif event.key == pygame.K_END:

# #                     self.quest_scroll[
# #                         self.quest_tab
# #                     ] = 999999

# #             elif event.type == pygame.MOUSEWHEEL:

# #                 self.scroll_current_quest_tab(
# #                     -event.y * 60
# #                 )

# #             elif event.type == pygame.MOUSEBUTTONDOWN:

# #                 if event.button == 4:

# #                     self.scroll_current_quest_tab(
# #                         -60
# #                     )

# #                 elif event.button == 5:

# #                     self.scroll_current_quest_tab(
# #                         60
# #                     )

# #                 elif event.button == 1:

# #                     tab = self.get_clicked_quest_tab(
# #                         event.pos
# #                     )

# #                     if tab is not None:

# #                         self.quest_tab = tab
# #                         return

# #                     quest = self.get_clicked_quest(
# #                         event.pos
# #                     )

# #                     if quest is not None:
# #                         self.selected_quest = quest
# #                         self.state = "quest_details"

# #             return

# #         # ========================================================
# #         # QUEST DETAILS
# #         # ========================================================

# #         if self.state == "quest_details":

# #             if event.type == pygame.KEYDOWN:

# #                 if event.key in (
# #                     pygame.K_ESCAPE,
# #                     pygame.K_q
# #                 ):
# #                     self.selected_quest = None
# #                     self.state = "quest_log"
# #                     return

# #                 if event.key == pygame.K_n:
# #                     self.navigate_selected_quest()
# #                     return

# #             elif event.type == pygame.MOUSEBUTTONDOWN:

# #                 if event.button == 1:
# #                     navigate_rect = self.get_quest_navigate_button_rect()

# #                     if navigate_rect.collidepoint(event.pos):
# #                         self.navigate_selected_quest()
# #                         return

# #                     back_rect = self.get_quest_details_back_rect()
# #                     if back_rect.collidepoint(event.pos):
# #                         self.selected_quest = None
# #                         self.state = "quest_log"
# #                         return

# #             return

# #         # ========================================================
# #         # DIALOGUE
# #         # ========================================================

# #         if self.dialogue_npc is not None:

# #             if event.type == pygame.KEYDOWN:

# #                 if event.key == pygame.K_ESCAPE:

# #                     self.pending_quest = None
# #                     self.quest_offer_ready = False

# #                     self.close_dialogue()

# #                     return

# #                 if event.key == pygame.K_e:

# #                     if self.quest_offer_ready:

# #                         self.accept_pending_quest()

# #                     else:

# #                         self.advance_dialogue()

# #                     return

# #             return

# #         # ========================================================
# #         # PLAYING
# #         # ========================================================

# #         if self.state == "playing":

# #             if event.type == pygame.KEYDOWN:

# #                 if event.key == pygame.K_ESCAPE:

# #                     self.state = "pause"

# #                 elif event.key == pygame.K_q:

# #                     self.open_quest_log()

# #                 elif event.key == pygame.K_n:

# #                     self.toggle_navigator()

# #                 elif event.key == pygame.K_e:

# #                     self.interact()

# #         # ========================================================
# #         # PAUSE
# #         # ========================================================

# #         elif self.state == "pause":

# #             if event.type == pygame.KEYDOWN:

# #                 if event.key == pygame.K_ESCAPE:
# #                     self.state = "playing"
# #                 elif event.key == pygame.K_s:
# #                     self.save_game()
# #                 elif event.key == pygame.K_m:
# #                     self.save_game()
# #                     self.state = "main_menu"
# #                     self.refresh_main_menu_options()

# #             elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
# #                 if self.get_pause_resume_rect().collidepoint(event.pos):
# #                     self.state = "playing"
# #                 elif self.get_pause_save_rect().collidepoint(event.pos):
# #                     self.save_game()
# #                 elif self.get_pause_menu_rect().collidepoint(event.pos):
# #                     self.save_game()
# #                     self.state = "main_menu"
# #                     self.refresh_main_menu_options()


# from .core import *


# class InputMixin:

#     def handle_event(
#         self,
#         event
#     ):

#         global SCREEN_WIDTH
#         global SCREEN_HEIGHT

#         # ========================================================
#         # QUIT
#         # ========================================================

#         if event.type == pygame.QUIT:

#             self.running = False

#             return

#         # ========================================================
#         # WINDOW RESIZE
#         # ========================================================

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
#         # MAIN MENU
#         # ========================================================

#         if self.state == "main_menu":

#             self.handle_main_menu_event(
#                 event
#             )

#             return

#         # ========================================================
#         # CHARACTER SELECT
#         # ========================================================

#         if self.state == "character_select":

#             # ----------------------------------------------------
#             # KEYBOARD
#             # ----------------------------------------------------

#             if event.type == pygame.KEYDOWN:

#                 if event.key == pygame.K_ESCAPE:

#                     self.state = "main_menu"

#                     return

#                 # ------------------------------------------------
#                 # MEPple
#                 # ------------------------------------------------

#                 elif event.key == pygame.K_1:

#                     self.start_new_adventure(
#                         "Mepple"
#                     )

#                     return

#                 # ------------------------------------------------
#                 # MIPPLE
#                 # ------------------------------------------------

#                 elif event.key == pygame.K_2:

#                     self.start_new_adventure(
#                         "Mipple"
#                     )

#                     return

#             # ----------------------------------------------------
#             # MOUSE
#             # ----------------------------------------------------

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

#                     # ============================================
#                     # MEPple
#                     # ============================================

#                     if mepple_rect.collidepoint(
#                         event.pos
#                     ):

#                         # IMPORTANT:
#                         # Use start_new_adventure()
#                         # instead of start_adventure()
#                         #
#                         # This resets the game clock to 08:00 AM.
#                         self.start_new_adventure(
#                             "Mepple"
#                         )

#                         return

#                     # ============================================
#                     # MIPPLE
#                     # ============================================

#                     elif mipple_rect.collidepoint(
#                         event.pos
#                     ):

#                         # IMPORTANT:
#                         # Use start_new_adventure()
#                         # instead of start_adventure()
#                         #
#                         # This resets the game clock to 08:00 AM.
#                         self.start_new_adventure(
#                             "Mipple"
#                         )

#                         return

#             return

#         # ========================================================
#         # QUEST LOG
#         # ========================================================

#         if self.state == "quest_log":

#             if event.type == pygame.KEYDOWN:

#                 if event.key in (
#                     pygame.K_q,
#                     pygame.K_ESCAPE
#                 ):

#                     self.state = "playing"

#                     return

#                 elif event.key == pygame.K_LEFT:

#                     self.change_quest_tab(
#                         -1
#                     )

#                 elif event.key == pygame.K_RIGHT:

#                     self.change_quest_tab(
#                         1
#                     )

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

#                 # Mouse wheel up
#                 if event.button == 4:

#                     self.scroll_current_quest_tab(
#                         -60
#                     )

#                 # Mouse wheel down
#                 elif event.button == 5:

#                     self.scroll_current_quest_tab(
#                         60
#                     )

#                 # Left click
#                 elif event.button == 1:

#                     tab = self.get_clicked_quest_tab(
#                         event.pos
#                     )

#                     if tab is not None:

#                         self.quest_tab = tab

#                         return

#                     quest = self.get_clicked_quest(
#                         event.pos
#                     )

#                     if quest is not None:

#                         self.selected_quest = quest

#                         self.state = "quest_details"

#             return

#         # ========================================================
#         # QUEST DETAILS
#         # ========================================================

#         if self.state == "quest_details":

#             if event.type == pygame.KEYDOWN:

#                 # ------------------------------------------------
#                 # BACK
#                 # ------------------------------------------------

#                 if event.key in (
#                     pygame.K_ESCAPE,
#                     pygame.K_q
#                 ):

#                     self.selected_quest = None

#                     self.state = "quest_log"

#                     return

#                 # ------------------------------------------------
#                 # NAVIGATE
#                 # ------------------------------------------------

#                 if event.key == pygame.K_n:

#                     self.navigate_selected_quest()

#                     return

#             elif event.type == pygame.MOUSEBUTTONDOWN:

#                 if event.button == 1:

#                     # ------------------------------------------------
#                     # NAVIGATE BUTTON
#                     # ------------------------------------------------

#                     navigate_rect = (
#                         self.get_quest_navigate_button_rect()
#                     )

#                     if navigate_rect.collidepoint(
#                         event.pos
#                     ):

#                         self.navigate_selected_quest()

#                         return

#                     # ------------------------------------------------
#                     # BACK BUTTON
#                     # ------------------------------------------------

#                     back_rect = (
#                         self.get_quest_details_back_rect()
#                     )

#                     if back_rect.collidepoint(
#                         event.pos
#                     ):

#                         self.selected_quest = None

#                         self.state = "quest_log"

#                         return

#             return

#         # ========================================================
#         # DIALOGUE
#         # ========================================================

#         if self.dialogue_npc is not None:

#             if event.type == pygame.KEYDOWN:

#                 # ------------------------------------------------
#                 # CLOSE DIALOGUE
#                 # ------------------------------------------------

#                 if event.key == pygame.K_ESCAPE:

#                     self.pending_quest = None

#                     self.quest_offer_ready = False

#                     self.close_dialogue()

#                     return

#                 # ------------------------------------------------
#                 # ADVANCE / ACCEPT QUEST
#                 # ------------------------------------------------

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

#                 # ------------------------------------------------
#                 # PAUSE
#                 # ------------------------------------------------

#                 if event.key == pygame.K_ESCAPE:

#                     self.state = "pause"

#                     return

#                 # ------------------------------------------------
#                 # QUEST LOG
#                 # ------------------------------------------------

#                 elif event.key == pygame.K_q:

#                     self.open_quest_log()

#                     return

#                 # ------------------------------------------------
#                 # NAVIGATOR
#                 # ------------------------------------------------

#                 elif event.key == pygame.K_n:

#                     self.toggle_navigator()

#                     return

#                 # ------------------------------------------------
#                 # INTERACT
#                 # ------------------------------------------------

#                 elif event.key == pygame.K_e:

#                     self.interact()

#                     return

#         # ========================================================
#         # PAUSE
#         # ========================================================

#         elif self.state == "pause":

#             if event.type == pygame.KEYDOWN:

#                 # ------------------------------------------------
#                 # RESUME
#                 # ------------------------------------------------

#                 if event.key == pygame.K_ESCAPE:

#                     self.state = "playing"

#                     return

#                 # ------------------------------------------------
#                 # SAVE
#                 # ------------------------------------------------

#                 elif event.key == pygame.K_s:

#                     self.save_game()

#                     return

#                 # ------------------------------------------------
#                 # SAVE + MAIN MENU
#                 # ------------------------------------------------

#                 elif event.key == pygame.K_m:

#                     self.save_game()

#                     self.state = "main_menu"

#                     self.refresh_main_menu_options()

#                     return

#             # ====================================================
#             # PAUSE MOUSE BUTTONS
#             # ====================================================

#             elif (
#                 event.type == pygame.MOUSEBUTTONDOWN
#                 and event.button == 1
#             ):

#                 # ------------------------------------------------
#                 # RESUME
#                 # ------------------------------------------------

#                 if self.get_pause_resume_rect().collidepoint(
#                     event.pos
#                 ):

#                     self.state = "playing"

#                     return

#                 # ------------------------------------------------
#                 # SAVE
#                 # ------------------------------------------------

#                 elif self.get_pause_save_rect().collidepoint(
#                     event.pos
#                 ):

#                     self.save_game()

#                     return

#                 # ------------------------------------------------
#                 # SAVE + MAIN MENU
#                 # ------------------------------------------------

#                 elif self.get_pause_menu_rect().collidepoint(
#                     event.pos
#                 ):

#                     self.save_game()

#                     self.state = "main_menu"

#                     self.refresh_main_menu_options()

#                     return


from .core import *


class InputMixin:

    def handle_event(
        self,
        event
    ):

        global SCREEN_WIDTH
        global SCREEN_HEIGHT

        # ========================================================
        # QUIT
        # ========================================================

        if event.type == pygame.QUIT:

            self.running = False

            return

        # ========================================================
        # WINDOW RESIZE
        # ========================================================

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

            # ----------------------------------------------------
            # KEYBOARD
            # ----------------------------------------------------

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    self.state = "main_menu"

                    return

                # ------------------------------------------------
                # MEPple
                # ------------------------------------------------

                elif event.key == pygame.K_1:

                    self.start_new_adventure(
                        "Mepple"
                    )

                    return

                # ------------------------------------------------
                # MIPPLE
                # ------------------------------------------------

                elif event.key == pygame.K_2:

                    self.start_new_adventure(
                        "Mipple"
                    )

                    return

            # ----------------------------------------------------
            # MOUSE
            # ----------------------------------------------------

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

                    # ============================================
                    # MEPple
                    # ============================================

                    if mepple_rect.collidepoint(
                        event.pos
                    ):

                        self.start_new_adventure(
                            "Mepple"
                        )

                        return

                    # ============================================
                    # MIPPLE
                    # ============================================

                    elif mipple_rect.collidepoint(
                        event.pos
                    ):

                        self.start_new_adventure(
                            "Mipple"
                        )

                        return

            return

        # ========================================================
        # QUEST LOG
        # ========================================================

        if self.state == "quest_log":

            if event.type == pygame.KEYDOWN:

                # ------------------------------------------------
                # CLOSE
                # ------------------------------------------------

                if event.key in (
                    pygame.K_q,
                    pygame.K_ESCAPE
                ):

                    self.state = "playing"

                    return

                # ------------------------------------------------
                # PREVIOUS TAB
                # ------------------------------------------------

                elif event.key == pygame.K_LEFT:

                    self.change_quest_tab(
                        -1
                    )

                    return

                # ------------------------------------------------
                # NEXT TAB
                # ------------------------------------------------

                elif event.key == pygame.K_RIGHT:

                    self.change_quest_tab(
                        1
                    )

                    return

                # ------------------------------------------------
                # SCROLL UP
                # ------------------------------------------------

                elif event.key == pygame.K_UP:

                    self.scroll_current_quest_tab(
                        -70
                    )

                    return

                # ------------------------------------------------
                # SCROLL DOWN
                # ------------------------------------------------

                elif event.key == pygame.K_DOWN:

                    self.scroll_current_quest_tab(
                        70
                    )

                    return

                # ------------------------------------------------
                # PAGE UP
                # ------------------------------------------------

                elif event.key == pygame.K_PAGEUP:

                    self.scroll_current_quest_tab(
                        -350
                    )

                    return

                # ------------------------------------------------
                # PAGE DOWN
                # ------------------------------------------------

                elif event.key == pygame.K_PAGEDOWN:

                    self.scroll_current_quest_tab(
                        350
                    )

                    return

                # ------------------------------------------------
                # HOME
                # ------------------------------------------------

                elif event.key == pygame.K_HOME:

                    self.quest_scroll[
                        self.quest_tab
                    ] = 0

                    return

                # ------------------------------------------------
                # END
                # ------------------------------------------------

                elif event.key == pygame.K_END:

                    self.quest_scroll[
                        self.quest_tab
                    ] = 999999

                    return

            # ----------------------------------------------------
            # MOUSE WHEEL
            # ----------------------------------------------------

            elif event.type == pygame.MOUSEWHEEL:

                self.scroll_current_quest_tab(
                    -event.y * 60
                )

                return

            # ----------------------------------------------------
            # MOUSE BUTTON
            # ----------------------------------------------------

            elif event.type == pygame.MOUSEBUTTONDOWN:

                # Mouse wheel up.
                if event.button == 4:

                    self.scroll_current_quest_tab(
                        -60
                    )

                    return

                # Mouse wheel down.
                elif event.button == 5:

                    self.scroll_current_quest_tab(
                        60
                    )

                    return

                # Left click.
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

            return

        # ========================================================
        # QUEST DETAILS
        # ========================================================

        if self.state == "quest_details":

            if event.type == pygame.KEYDOWN:

                # ------------------------------------------------
                # BACK
                # ------------------------------------------------

                if event.key in (
                    pygame.K_ESCAPE,
                    pygame.K_q
                ):

                    self.selected_quest = None

                    self.state = "quest_log"

                    return

                # ------------------------------------------------
                # NAVIGATE
                # ------------------------------------------------

                if event.key == pygame.K_n:

                    self.navigate_selected_quest()

                    return

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    # ------------------------------------------------
                    # NAVIGATE BUTTON
                    # ------------------------------------------------

                    navigate_rect = (
                        self.get_quest_navigate_button_rect()
                    )

                    if navigate_rect.collidepoint(
                        event.pos
                    ):

                        self.navigate_selected_quest()

                        return

                    # ------------------------------------------------
                    # BACK BUTTON
                    # ------------------------------------------------

                    back_rect = (
                        self.get_quest_details_back_rect()
                    )

                    if back_rect.collidepoint(
                        event.pos
                    ):

                        self.selected_quest = None

                        self.state = "quest_log"

                        return

            return

        # ========================================================
        # RELATIONSHIPS
        # ========================================================

        if self.state == "relationships":

            # ----------------------------------------------------
            # KEYBOARD
            # ----------------------------------------------------

            if event.type == pygame.KEYDOWN:

                # ------------------------------------------------
                # CLOSE
                # ------------------------------------------------

                if event.key in (
                    pygame.K_ESCAPE,
                    pygame.K_r
                ):

                    self.state = "playing"

                    return

                # ------------------------------------------------
                # SCROLL UP
                # ------------------------------------------------

                elif event.key == pygame.K_UP:

                    if not hasattr(
                        self,
                        "relationship_scroll"
                    ):

                        self.relationship_scroll = 0

                    self.relationship_scroll -= 70

                    if self.relationship_scroll < 0:

                        self.relationship_scroll = 0

                    return

                # ------------------------------------------------
                # SCROLL DOWN
                # ------------------------------------------------

                elif event.key == pygame.K_DOWN:

                    if not hasattr(
                        self,
                        "relationship_scroll"
                    ):

                        self.relationship_scroll = 0

                    self.relationship_scroll += 70

                    return

                # ------------------------------------------------
                # PAGE UP
                # ------------------------------------------------

                elif event.key == pygame.K_PAGEUP:

                    if not hasattr(
                        self,
                        "relationship_scroll"
                    ):

                        self.relationship_scroll = 0

                    self.relationship_scroll -= 350

                    if self.relationship_scroll < 0:

                        self.relationship_scroll = 0

                    return

                # ------------------------------------------------
                # PAGE DOWN
                # ------------------------------------------------

                elif event.key == pygame.K_PAGEDOWN:

                    if not hasattr(
                        self,
                        "relationship_scroll"
                    ):

                        self.relationship_scroll = 0

                    self.relationship_scroll += 350

                    return

                # ------------------------------------------------
                # HOME
                # ------------------------------------------------

                elif event.key == pygame.K_HOME:

                    self.relationship_scroll = 0

                    return

                # ------------------------------------------------
                # END
                # ------------------------------------------------

                elif event.key == pygame.K_END:

                    self.relationship_scroll = 999999

                    return

            # ----------------------------------------------------
            # MOUSE WHEEL
            # ----------------------------------------------------

            elif event.type == pygame.MOUSEWHEEL:

                if not hasattr(
                    self,
                    "relationship_scroll"
                ):

                    self.relationship_scroll = 0

                self.relationship_scroll -= (
                    event.y * 60
                )

                if self.relationship_scroll < 0:

                    self.relationship_scroll = 0

                return

            # ----------------------------------------------------
            # MOUSE BUTTON
            # ----------------------------------------------------

            elif event.type == pygame.MOUSEBUTTONDOWN:

                # Wheel up.
                if event.button == 4:

                    if not hasattr(
                        self,
                        "relationship_scroll"
                    ):

                        self.relationship_scroll = 0

                    self.relationship_scroll -= 60

                    if self.relationship_scroll < 0:

                        self.relationship_scroll = 0

                    return

                # Wheel down.
                elif event.button == 5:

                    if not hasattr(
                        self,
                        "relationship_scroll"
                    ):

                        self.relationship_scroll = 0

                    self.relationship_scroll += 60

                    return

            return

        # ========================================================
        # DIALOGUE
        # ========================================================

        if self.dialogue_npc is not None:

            if event.type == pygame.KEYDOWN:

                # ------------------------------------------------
                # CLOSE DIALOGUE
                # ------------------------------------------------

                if event.key == pygame.K_ESCAPE:

                    self.pending_quest = None

                    self.quest_offer_ready = False

                    self.close_dialogue()

                    return

                # ------------------------------------------------
                # ADVANCE / ACCEPT QUEST
                # ------------------------------------------------

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

                # ------------------------------------------------
                # PAUSE
                # ------------------------------------------------

                if event.key == pygame.K_ESCAPE:

                    self.state = "pause"

                    return

                # ------------------------------------------------
                # RELATIONSHIPS
                # ------------------------------------------------

                elif event.key == pygame.K_r:

                    self.state = "relationships"

                    self.relationship_scroll = 0

                    return

                # ------------------------------------------------
                # QUEST LOG
                # ------------------------------------------------

                elif event.key == pygame.K_q:

                    self.open_quest_log()

                    return

                # ------------------------------------------------
                # NAVIGATOR
                # ------------------------------------------------

                elif event.key == pygame.K_n:

                    self.toggle_navigator()

                    return

                # ------------------------------------------------
                # INTERACT
                # ------------------------------------------------

                elif event.key == pygame.K_e:

                    self.interact()

                    return

        # ========================================================
        # PAUSE
        # ========================================================

        elif self.state == "pause":

            if event.type == pygame.KEYDOWN:

                # ------------------------------------------------
                # RESUME
                # ------------------------------------------------

                if event.key == pygame.K_ESCAPE:

                    self.state = "playing"

                    return

                # ------------------------------------------------
                # SAVE
                # ------------------------------------------------

                elif event.key == pygame.K_s:

                    self.save_game()

                    return

                # ------------------------------------------------
                # SAVE + MAIN MENU
                # ------------------------------------------------

                elif event.key == pygame.K_m:

                    self.save_game()

                    self.state = "main_menu"

                    self.refresh_main_menu_options()

                    return

            # ====================================================
            # PAUSE MOUSE BUTTONS
            # ====================================================

            elif (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
            ):

                # ------------------------------------------------
                # RESUME
                # ------------------------------------------------

                if self.get_pause_resume_rect().collidepoint(
                    event.pos
                ):

                    self.state = "playing"

                    return

                # ------------------------------------------------
                # SAVE
                # ------------------------------------------------

                elif self.get_pause_save_rect().collidepoint(
                    event.pos
                ):

                    self.save_game()

                    return

                # ------------------------------------------------
                # SAVE + MAIN MENU
                # ------------------------------------------------

                elif self.get_pause_menu_rect().collidepoint(
                    event.pos
                ):

                    self.save_game()

                    self.state = "main_menu"

                    self.refresh_main_menu_options()

                    return