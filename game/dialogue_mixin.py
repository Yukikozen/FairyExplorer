from .core import *

class DialogueMixin:
    def start_normal_dialogue(
        self,
        npc
    ):

        self.dialogue_npc = npc

        self.pending_quest = None
        self.quest_offer_ready = False

        self.dialogue_lines = list(
            npc.dialogue
        )

        self.dialogue_index = 0

        npc.is_talking = True


    def start_quest_offer(
        self,
        npc,
        quest
    ):

        self.dialogue_npc = npc

        self.pending_quest = quest
        self.quest_offer_ready = False

        self.dialogue_lines = [

            "Hi! I have a quest for you.",

            quest.title,

            quest.description,

            f"Reward: {quest.reward_coins} coins.",

            "Would you like to accept this quest?"
        ]

        self.dialogue_index = 0

        npc.is_talking = True


    def start_progress_dialogue(
        self,
        npc,
        quest
    ):

        self.dialogue_npc = npc

        self.pending_quest = None
        self.quest_offer_ready = False

        if quest.is_finished():

            self.dialogue_lines = [
                "You did it!",
                "Your quest is ready to turn in.",
                (
                    f"{quest.progress}/"
                    f"{quest.required_amount}"
                )
            ]

        else:

            self.dialogue_lines = [
                "You're doing great!",
                quest.title,
                (
                    f"Progress: "
                    f"{quest.progress}/"
                    f"{quest.required_amount}"
                )
            ]

        self.dialogue_index = 0

        npc.is_talking = True


    def advance_dialogue(self):

        if self.dialogue_npc is None:
            return

        if (
            self.pending_quest is not None
            and self.dialogue_index
            >= len(
                self.dialogue_lines
            ) - 1
        ):

            self.quest_offer_ready = True
            return

        self.dialogue_index += 1

        if (
            self.dialogue_index
            >= len(
                self.dialogue_lines
            )
        ):

            self.close_dialogue()


    def close_dialogue(self):

        if self.dialogue_npc:

            self.dialogue_npc.is_talking = False

        self.dialogue_npc = None

        self.dialogue_lines = []
        self.dialogue_index = 0

        self.pending_quest = None
        self.quest_offer_ready = False


    def accept_pending_quest(self):

        if self.pending_quest is None:
            return

        quest = self.pending_quest

        if self.get_quest_status(
            quest
        ) != "AVAILABLE":

            self.close_dialogue()
            return

        quest.accepted = True
        quest.completed = False

        self.show_notification(
            f"Quest accepted: {quest.title}"
        )

        self.dialogue_lines = [
            "Thank you!",
            (
                f"Quest accepted: "
                f"{quest.title}"
            ),
            "Good luck on your adventure!"
        ]

        self.dialogue_index = 0

        self.pending_quest = None
        self.quest_offer_ready = False


