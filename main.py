from guiutil import *
from input import *

VERSION: str = '2.0.0'
MAX_PER_FISH: int = 7
MAX_AMOUNT_CHIPS: int = 5
MAX_SCOOPS_CHIPS: float = 10
DELIVERY_CHARGE: float = 5
FROZEN_DISCOUNT: float = 1.05
GST_AMOUNT: float = 0.15

TITLE_MESSAGE: str = f"""
 ______            _     _            ______        _    ______              _ 
 |  ___|          | |   | |           |  ___|      | |   |  ___|            | |
 | |_ _ __ ___  __| | __| |_   _ ___  | |_ __ _ ___| |_  | |_ ___   ___   __| |
 |  _| '__/ _ \\/ _` |/ _` | | | / __| |  _/ _` / __| __| |  _/ _ \\ / _ \\ / _` |
 | | | | |  __/ (_| | (_| | |_| \\__ \\ | || (_| \\__ \\ |_  | || (_) | (_) | (_| |
 \\_| |_|  \\___|\\__,_|\\__,_|\\__, |___/ \\_| \\__,_|___/\\__| \\_| \\___/ \\___/ \\__,_|
                            __/ |                                              
                           |___/   Ordering System Version: {VERSION}
"""

MENU: dict = {
    'types': [
        {
            'name': 'Cheap',
            'price': 4.10,
            'price_format': '{} each',
            'items': [
                'Shark', 'Flounder', 'Cod',
                'Gurnet', 'Blue Moki', 'Arrow Squid'
            ]
        },
        {
            'name': 'Delux',
            'price': 7.20,
            'price_format': '{} each',
            'items': [
                'Snapper', 'Pink Salmon', 'Tuna',
                'Smoked Marlin', 'Kingfish', 'Trevally'
            ]
        },
        {
            'name': 'Chips',
            'price': 2.00,
            'price_format': '{} per scoop',
            'text': 'Specify custom amount'
        }
    ],
}

order: Order


def menu_init():
    global order
    order = Order(
        MAX_PER_FISH,
        MAX_AMOUNT_CHIPS,
        MAX_SCOOPS_CHIPS,
        FROZEN_DISCOUNT,
        GST_AMOUNT,
        DELIVERY_CHARGE
    )
    # Prompts the user for their name
    order.name = accept(create_prompt([
        'Please enter the name of the customer'
    ]), lambda value: True)  # Accepting any values
    # Prompts the user for their phone number
    order.phone = accept(create_prompt([
        'Please enter the phone number of the customer'
    ]), lambda value: True)  # Accepting any values
    # Prompts the user with the choice of cooked or frozen
    order.frozen = accept_bool(create_prompt([
        'Would you like your order frozen? [Y/N] Frozen orders',
        f'receive a discount of {format_price(FROZEN_DISCOUNT)} per fish item',
    ]))  # Accepts booleans
    order.delivery = accept_bool(create_prompt([
        'Would the customer like delivery? [Y/N]',
        'Delivery will cost an extra ' + format_price(DELIVERY_CHARGE)
    ]))  # Accepts booleans
    if order.delivery:
        order.address = accept(create_prompt([
            'Please enter the address the customer',
            'would like to have it delivered too'
        ]), lambda value: True)


def menu_main():
    while True:
        menu_selection: int = accept_int(create_prompt([
            '1) Display Menu "Displays a list of available goods"',
            '2) Add item "Adds an item to the order"',
            '3) Remove item "Removes an item from the order"',
            '4) List order "Displays the contents of the order"',
            '5) Finish Order "Finalizes the order"',
            '6) Cancel "Cancels the current order and resets"'
        ]), 1, 6)

        if menu_selection == 1:
            # Prints out the menu
            print(create_menu(MENU['types']))
        elif menu_selection == 2:
            menu_add()
        elif menu_selection == 3:
            menu_remove()
        elif menu_selection == 4:
            menu_order()
        elif menu_selection == 5:
            menu_finish()
        elif menu_selection == 6:
            if menu_cancel():  # If the user didn't want to restart
                break  # Break out of the main loop (Exits the program)
            else:
                menu_init()  # Display the init menu


def menu_add() -> None:
    while True:
        # The total number of types and items
        total_types: int = 0
        for menu_type in MENU['types']:
            menu_type: dict  # The menu type is a dictionary
            if 'items' in menu_type:  # If we have items
                # Increase the total types by the amount of items
                total_types += len(menu_type['items'])
            else:
                # Increase the total types
                total_types += 1

        def test(value: str):
            """
            A Validation test for making sure the value
            is "menu", "back", or an integer between 1
            and the total types

            :param value: The value to validate
            """
            if value not in ['menu', 'back']:  # If the value is not one of the text values
                value: int = Validation.int(value)  # Validate the that the value is an int
                Validation.min_max(value, 1, total_types)  # Validate that its within the bounds

        user_input = accept(create_prompt([
            'Enter "menu" to display the menu',
            '"back" to go back or type the number',
            'corresponding to a menu item'
        ]), test).lower()

        if user_input == 'menu':
            print(create_menu(MENU['types']))
        elif user_input == 'back':
            # Break out of the menu add loop this will take us to the main menu
            break
        else:
            item_index: int = int(user_input)
            item_type: str or None = None
            current_index: int = 1
            for menu_type in MENU['types']:
                if 'items' in menu_type:
                    items: list = menu_type['items']
                    item: str
                    for item in items:
                        if item_index == current_index:
                            item_type = item
                            break
                        current_index += 1
                    if item_type is not None:
                        break
                else:
                    if item_index == current_index:
                        item_type = menu_type['name']
                    current_index += 1
            if item_type == 'Chips':
                remaining = order.get_remaining_chips()
                if remaining <= 0:
                    error('You cannot add anymore lots of chips')
                else:
                    def test(value: str):
                        """
                        A Validation test for making sure the value
                        is "back", or a float between 0.1
                        and MAX_SCOOPS_CHIPS (the maximum scoop size)

                        :param value: The value to validate
                        """
                        if value != "back":  # If the value is not one of the text values
                            value: float = Validation.float(value)  # Validate the that the value is an float
                            Validation.min_max(value, 0.1, MAX_SCOOPS_CHIPS)  # Validate that its within the bounds

                    amount: str = accept(create_prompt([
                        'Enter "back" to go back or enter the amount of',
                        f'scoops you would like. You cannot add more',
                        f'than {MAX_SCOOPS_CHIPS} scoops'
                    ]), test)
                    if amount != 'back':
                        amount: float = round(float(amount), 1)
                        order.chips.append(amount)
                        good(f'Added {amount} scoops of chips to the order')
            else:
                remaining: int = order.get_remaining_fish(item_type)

                if remaining <= 0:
                    error('You cannot add anymore of that type of fish!')
                else:

                    def test(value: str):
                        if value != "back":
                            value: int = Validation.int(value)
                            Validation.min_max(value, 1, remaining)

                    amount: str = accept(create_prompt([
                        'Enter "back" to go back or enter the amount of',
                        f'"{item_type}" you would like. You cannot add more',
                        f'than {remaining}'
                    ]), test)
                    if amount != 'back':
                        order.add_fish(item_type, int(amount))
                        good(f'Added {amount} {item_type}')


def menu_remove():
    total_items: int = len(order.fish) + len(order.chips)
    if total_items == 0:
        print('The current order is empty!')
        return

    def test(value: str):
        if value not in ['order', 'back']:
            value: int = Validation.int(value)
            Validation.min_max(value, 1, total_items)

    menu_order()
    while True:
        user_input: str = accept(create_prompt([
            'Enter "order" to list the current order',
            '"back" to go back or type the number',
            'corresponding to a order item to remove'
        ]), test).lower()
        if user_input == "order":
            menu_order()
            continue
        if user_input == "back":
            break
        user_input: int = int(user_input)
        total_fish = len(order.fish)
        if 0 < user_input <= total_fish:
            fish_type = list(order.fish)[user_input - 1]
            amount = order.fish[fish_type]
            order.fish.pop(fish_type)
            good(f'Removed {amount} {fish_type}')
        else:
            user_input -= total_fish + 1
            if user_input <= len(order.chips):
                amount = order.chips[user_input]
                order.chips.remove(user_input)
                good(f'Removed {amount} scoops of chips')


def menu_order():
    print(create_order_list(order, MENU['types']))


def menu_finish():
    if order.empty():
        error('The current order is empty!')
        return False
    menu_order()
    if accept_bool(create_prompt([
        'Is the listed order correct? [Y/N]',
        'Selecting no will return to the menu.'
    ])):
        print('')


def menu_cancel():
    """
    The menu function for canceling the
    order and restarting / closing the program

    :return: Whether or not the exit
    """
    global order
    # Set the order to None
    order = None
    # Inform the user
    print('Current order cancelled ')
    # Prompt the user if they would like to restart
    return not accept_bool(create_prompt([
        'Would you like to start again? (Y/N)'
    ]))


if __name__ == '__main__':
    print(splitter())
    print(TITLE_MESSAGE)
    print(splitter())
    # Displays the init menu
    menu_init()
    # Displays the main menu
    menu_main()
