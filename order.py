from typing import Dict

from guiutil import BOX_V


class Order:
    order_id: str
    fish: Dict[str, int]
    chips: float
    max_per_item: int

    def __init__(self, max_per_item: int) -> None:
        self.max_per_item = max_per_item

    def can_add_fish(self, fish_type: str) -> bool:
        if fish_type in self.fish:
            amount = self.fish[fish_type]
            if amount == self.max_per_item:
                return False
        return True

    def add_fish(self, fish_type: str, amount: int) -> bool:
        if not self.can_add_fish(fish_type):
            return False
        if fish_type in self.fish:
            existing_amount: int = self.fish[fish_type]
            if existing_amount + amount > self.max_per_item:
                overflow: int = existing_amount + amount - self.max_per_item
                diff: int = amount - overflow
                print(f'{BOX_V} Cannot add "{amount}" only adding "{diff}"')
                amount = diff
            existing_amount += amount
        else:
            self.fish[fish_type] = amount
        return True
