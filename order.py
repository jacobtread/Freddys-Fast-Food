from random import random
from typing import Dict, List, NoReturn


class Order:
    order_id: str  # The id of the order
    name: str  # The name of the user
    phone: str  # The phone number of the user
    address: str  # The address of the user
    delivery: bool  # Whether or not to deliver the order

    fish: Dict[str, int]  # The fish and the amount ordered
    chips: List[float]  # The amounts of the chips ordered
    frozen: bool  # Whether or not the order is frozen

    max_per_fish: int  # The maximum amount of fish per type
    max_amount_chips: int  # The maximum sets of chips that
    max_scoops_chips: float  # The maximum amount of scoops one lot of chips can have
    frozen_discount: float  # The discount amount per frozen fish item
    gst_amount: float  # The amount of GST (Government Service Tax)
    delivery_charge: float  # The amount charged for delivery

    def __init__(self, max_per_fish: int, max_amount_chips: int, max_scoops_chips: float, frozen_discount: float,
                 gst_amount: float, delivery_charge: float) -> None:
        """

        :param max_per_fish: The maximum amount of fish per type
        :param max_amount_chips: The maximum sets of chips that
        :param max_scoops_chips: The maximum amount of scoops one lot of chips can have
        :param frozen_discount: The discount amount per frozen fish item
        :param gst_amount: The amount of GST (Government Service Tax)
        """
        # The order id is a randomly generated number between 1,000 and 10,000
        self.order_id = str(round((random() * 9000) + 1000))
        self.max_per_fish = max_per_fish
        self.max_amount_chips = max_amount_chips
        self.max_scoops_chips = max_scoops_chips
        self.frozen_discount = frozen_discount
        self.gst_amount = gst_amount
        self.delivery_charge = delivery_charge
        self.fish = {}
        self.chips = []

    def calculate_prices(self, types: List[dict]) -> (int, int, int, int):
        """
        Calculates the total price, the amount of gst and the gst inclusive price

        :param types: The menu types list (this contains pricing)
        :return: The total price, gst amount, and gst inclusive price
        """
        # The total calculated price
        total_price: float = 0
        # The total amount discounted from the order
        frozen_discount: float = 0
        if self.empty():
            # The current order is empty so we return 0 for all prices
            return 0, 0, 0, 0, self.delivery_charge
        for menu_type in types:
            # The price this type of item
            price: float = menu_type['price']
            # If this menu has items
            if 'items' in menu_type:
                for fish_type in self.fish:
                    # See if this type contains the fish type
                    if fish_type in menu_type['items']:
                        # Get the amount we have of that fish
                        amount: int = self.fish[fish_type]
                        # Increase the price by the amount * price
                        total_price += amount * price
                        if self.frozen:  # If the order is frozen we apply a discount
                            total_price -= self.frozen_discount  # Decrease the total by the discount
                            frozen_discount += self.frozen_discount  # Increase the total discount size
            elif menu_type['name'] == 'Chips':  # Special handling for the chips
                for amount in self.chips:
                    # Increase the price by the amount of chips * price
                    total_price += price * amount
        if self.delivery:  # If the order is being delivered
            total_price += self.delivery_charge  # Add the delivery charge to the price
        # The gst amount of the total (e.g $total * 0.15 aka 15%)
        total_gst: float = total_price * self.gst_amount
        # The total amount inclusive of gst (total + gst)
        total_inc_gst: float = total_price + total_gst
        # Return the totals
        return frozen_discount, total_price, total_gst, total_inc_gst

    def get_remaining_chips(self) -> int:
        """
        Calculates the remaining number of
        chips that can be added

        :return: The remaining number of chip that can be added
        """
        # The total amount of sets of scoops
        total_chips: int = len(self.chips)
        # The remaining amount is the difference between the max and total
        return self.max_amount_chips - total_chips

    def get_remaining_fish(self, fish_type: str) -> int:
        """
        Calculates the remaining number of fish
        that can be added for a specific fish type

        :param fish_type: The fish type to check
        :return: The remaining number of fish that can be added
        """
        if fish_type in self.fish:
            existing_amount: int = self.fish[fish_type]
            remaining: int = self.max_per_fish - existing_amount
            return remaining
        return self.max_per_fish

    def add_fish(self, fish_type: str, amount: int) -> NoReturn:
        """
        Adds the specified amount of fish to the order

        :param fish_type: The type of the fish to add
        :param amount: The amount of that fish to add
        """
        # If the fish type already has an amount we want
        # to add onto that instead of replacing it
        if fish_type in self.fish:
            # Retrieve the existing amount
            existing_amount: int = self.fish[fish_type]
            # Set the amount to the existing and the new
            self.fish[fish_type] = existing_amount + amount
        else:  # We don't have any already so we can just directly set it
            # Assign the fish type to the amount
            self.fish[fish_type] = amount

    def empty(self) -> bool:
        """
        Determine if the order is empty or not

        :return: Whether or not the order is empty
        """
        return len(self.fish) == 0 and len(self.chips) == 0
