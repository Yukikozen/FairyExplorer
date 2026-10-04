from .core import *

class Quest:

    def __init__(
        self,
        quest_id,
        title,
        description,
        objective_type,
        required_amount,
        reward_coins,
        giver_name,
        chain_id,
        chain_order,
        prerequisite=None,
        target_ids=None,
        item_type=None,
        target_npc=None
    ):

        self.quest_id = quest_id
        self.title = title
        self.description = description

        self.objective_type = objective_type
        self.required_amount = required_amount

        self.reward_coins = reward_coins
        self.giver_name = giver_name

        self.chain_id = chain_id
        self.chain_order = chain_order

        self.prerequisite = prerequisite

        self.target_ids = target_ids or []
        self.item_type = item_type
        self.target_npc = target_npc

        self.progress = 0

        self.accepted = False
        self.completed = False
        self.reward_claimed = False

        self.visited_targets = set()

    def is_finished(self):

        return (
            self.progress
            >= self.required_amount
        )

    def add_progress(
        self,
        amount=1
    ):

        if not self.accepted:
            return

        if self.completed:
            return

        self.progress += amount

        self.progress = min(
            self.progress,
            self.required_amount
        )


