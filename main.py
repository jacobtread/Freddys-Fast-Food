from typing import NoReturn
from guiutil import *
from input import *

VERSION: str = '2.5.0'  # The current version of this program
MAX_PER_FISH: int = 7  # The maximum amount of fish per type
MAX_AMOUNT_CHIPS: int = 5  # The maximum amount of sets of chips
MAX_SCOOPS_CHIPS: float = 10  # The maximum scoop size for chips
DELIVERY_CHARGE: float = 5  # The amount to charge for delivery
FROZEN_DISCOUNT: float = 1.05  # The amount to take away from every frozen fish item
GST_AMOUNT: float = 0.15  # The amount of GST (15% = 0.15)

TITLE_MESSAGE: str = f"""
 ______            _     _            ______        _    ______              _ 
 |  ___|          | |   | |           |  ___|      | |   |  ___|            | |
 | |_ _ __ ___  __| | __| |_   _ ___  | |_ __ _ ___| |_  | |_ ___   ___   __| |
 |  _| '__/ _ \\/ _` |/ _` | | | / __| |  _/ _` / __| __| |  _/ _ \\ / _ \\ / _` |
 | | | | |  __/ (_| | (_| | |_| \\__ \\ | || (_| \\__ \\ |_  | || (_) | (_) | (_| |
 \\_| |_|  \\___|\\__,_|\\__,_|\\__, |___/ \\_| \\__,_|___/\\__| \\_| \\___/ \\___/ \\__,_|
                            __/ |                                              
                           |___/   Ordering System Version: {VERSION}
"""  # The ASCII art of "Freddy's Fast Food"

MENU: dict = {
    'types': [
        {
            'name': 'Cheap',  # The name of this type
            'price': 4.10,  # The price of this type
            'price_format': '{} each',  # The format of this price {} is where the number will be placed
            'items': [  # A list of items in this type
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
            'name': 'Chips',  # The name of this type
            'price': 2.00,  # The price of this type
            'price_format': '{} per scoop',  # The format of this price {} is where the number will be placed
            'text': 'Specify custom amount'  # A text to be displayed instead of a list of items
        }
    ],
}

order: Order  # The current order object


def menu_title() -> NoReturn:
    """
    Prints out the large ASCII art of "Freddy's Fast Food"
    along with the splitter above and below it
    """
    print(splitter())
    print(TITLE_MESSAGE)
    print(splitter())


def menu_init() -> NoReturn:
    """
    Creates a new order object and prompts the user for their
    details along with asking about frozen and delivery options
    """
    global order
    # Creates a new order object and assigns it to order
    order = Order(
        MAX_PER_FISH,
        MAX_AMOUNT_CHIPS,
        MAX_SCOOPS_CHIPS,
        FROZEN_DISCOUNT,
        GST_AMOUNT,
        DELIVERY_CHARGE
    )
    # Prompts the user for the customer name and assigns the variable order.name
    order.name = accept(create_prompt([
        'Please enter the name of the customer'
    ]), lambda value: True)  # Accepting any values
    # Prompts the user for the customer phone number and assigns the variable order.phone
    order.phone = accept(create_prompt([
        'Please enter the phone number of the customer'
    ]), lambda value: True)  # Accepting any values
    # Prompts the user for a frozen discount and assigns the variable order.frozen
    order.frozen = accept_bool(create_prompt([
        'Would you like your order frozen? [Y/N] Frozen orders',
        f'receive a discount of {format_price(FROZEN_DISCOUNT)} per fish item',
    ]))  # Accepts booleans
    # Prompts the user for delivery and assigns the variable order.delivery
    order.delivery = accept_bool(create_prompt([
        'Would the customer like delivery? [Y/N]',
        'Delivery will cost an extra ' + format_price(DELIVERY_CHARGE)
    ]))  # Accepts booleans
    if order.delivery:  # The customer wants delivery
        # Prompts the user for their address and assigns the variable order.address
        order.address = accept(create_prompt([
            'Please enter the address the customer',
            'would like to have it delivered too'
        ]), lambda value: True)  # Accepts any values


def menu_main() -> NoReturn:
    """
    Prints out the main menu and prompts
    the user for what menu they would like to go to next

    This screen is looped and will continue to be resorted to
    unless the order is cancelled and/or the user chooses to
    exit.

    """
    while True:
        # Prompts the user for which menu they would like to visit
        menu_selection: int = accept_int(create_prompt([
            '1) Display Menu "Displays a list of available goods"',
            '2) Add item "Adds an item to the order"',
            '3) Remove item "Removes an item from the order"',
            '4) List order "Displays the contents of the order"',
            '5) Finish Order "Finalizes the order"',
            '6) Cancel Order "Cancels the current order and resets"'
        ]), 1, 6)  # Accepts numbers from 1 - 6

        if menu_selection == 1:  # If the user enters 1 (Display Menu)
            menu_list()  # Enter the menu_list screen
        elif menu_selection == 2:  # If the user enters 2 (Add Item)
            menu_add()  # Enter the menu_add screen
        elif menu_selection == 3:  # If the user enters 3 (Remove Item)
            menu_remove()  # Enter the menu_remove screen
        elif menu_selection == 4:  # If the user enters 4 (List Order)
            menu_order()  # Enter the menu_order screen
        elif menu_selection == 5:  # If the user enters 5 (Finish Order)
            # Enter the menu_finish screen if this returns True
            # we are being told to exit the main loop (shutdown)
            if menu_finish():
                break  # Exit the main loop
        elif menu_selection == 6:  # If the user enters 6 (Cancel Order)
            # Enter the menu_cancel screen if this returns True
            # we are being told to exit the main loop (shutdown)
            if menu_cancel():
                break  # Exit the main loop


def menu_list() -> NoReturn:
    """
    Prints out the menu (The list of available items)
    """
    print(create_menu(MENU['types']))


def menu_add() -> NoReturn:
    """
    Prompts the user with the add menu allowing them
    to add items to their order
    """
    # Loop until break so that they can order more than one
    # item without having to keep selecting this menu over and over
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
        # Get the user input for either a menu option
        # or a number corresponding to a menu item
        user_input: str or int = accept(create_prompt([
            'Enter "menu" to display the menu',
            '"back" to go back or type the number',
            'corresponding to a menu item'
        ]), lambda value: Validation.list_or_int(
            value,  # The provided value
            ['menu', 'back'],  # The acceptable string values
            1, total_types  # The min and max int values
        )).lower()  # Convert the value to lowercase for case insensitivity

        if user_input == 'menu':  # If the user typed "menu"
            menu_list()  # Display the menu list
        elif user_input == 'back':  # If the user typed "back"
            # Break out of the menu add loop this will take us to the main menu
            break
        else:
            user_input = int(user_input)  # The item index the user provided
            item_type: str or None = None  # The type of the item
            index: int = 0  # The current item index
            for menu_type in MENU['types']:  # We need to loop the types to find the item
                if 'items' in menu_type:  # If the type has items
                    items: list = menu_type['items']
                    for item in items:
                        index += 1  # Increase the index
                        if user_input == index:  # If the user input index matches this index
                            item_type = item  # Set the item type to this item
                            break  # Break out of the loop
                    if item_type is not None:  # If the item is found
                        break  # Break out of the loop
                else:  # If the type has no items
                    index += 1  # Increase the index
                    if user_input == index:
                        item_type = menu_type['name']
            if item_type == 'Chips':  # If the type of the item is chips
                # Get the remaining amount of chips that can be added
                remaining = order.get_remaining_chips()

                if remaining <= 0:  # There is no more chips remaining to add
                    # Tell the user they cant add anymore
                    error('You cannot add anymore lots of chips')
                else:
                    # Prompts the user for how many scoops they would like
                    amount: str = accept(create_prompt([
                        'Enter "back" to go back or enter the amount of',
                        f'scoops you would like. You cannot add more',
                        f'than {MAX_SCOOPS_CHIPS} scoops'
                    ]), lambda value: Validation.list_or_float(
                        value,  # The provided value
                        ['back'],   # The acceptable string values
                        0.1, MAX_SCOOPS_CHIPS  # The min and max float values
                    )).lower()  # Convert the value to lowercase for case insensitivity

                    if amount == 'back':  # If the user chooses back
                        continue  # Continue the add loop

                    # Cast the amount to a float and round to 1dp
                    # to make sure the user cant put in numbers like 4.33333333
                    # so they will just become 4.3
                    amount: float = round(float(amount), 1)
                    # Add the amount of chips to the order
                    order.chips.append(amount)
                    # Tell the user they have been added
                    good(f'Added {amount} scoops of chips to the order')

            else:
                # Get the remaining amount of that type of fish that can be added
                remaining: int = order.get_remaining_fish(item_type)

                if remaining <= 0:  # There is no more fish remaining to add
                    # Tell the user they cant add anymore
                    error('You cannot add anymore of that type of fish!')
                else:
                    # Prompts the user for how many of that fish they would like
                    amount: str = accept(create_prompt([
                        'Enter "back" to go back or enter the amount of',
                        f'"{item_type}" you would like. You cannot add more',
                        f'than {remaining}'
                    ]), lambda value: Validation.list_or_int(
                        value,  # The provided value
                        ['back'],  # The acceptable string values
                        1, remaining  # The min and max int values
                    )).lower()  # Convert the value to lowercase for case insensitivity

                    if amount == 'back':  # If the user chooses back
                        continue  # Continue the add loop

                    # Add the amount of fish to the order
                    order.add_fish(item_type, int(amount))
                    # Tell the user they have been added
                    good(f'Added {amount} {item_type}')


def menu_remove() -> NoReturn:
    """
    Prompts the user with the remove menu allowing them
    to remove items from their order
    """
    if order.empty():  # The current order is empty
        # Tell the user the order is empty
        error('The current order is empty!')
    else:
        # Calculate the total number of items in the order
        total_items: int = len(order.fish) + len(order.chips)
        # Display the current order
        menu_order()
        # Loop until break so that they can remove more than one
        # item without having to keep selecting this menu over and over
        while True:

            # Get the user input for either a menu option
            # or a number corresponding to a order item
            user_input: str = accept(create_prompt([
                'Enter "order" to list the current order',
                '"back" to go back or type the number',
                'corresponding to a order item to remove'
            ]), lambda value: Validation.list_or_int(
                value,  # The provided value
                ['order', 'back'],  # The acceptable string values
                1, total_items  # The min and max int values
            )).lower()  # Convert the value to lowercase for case insensitivity

            if user_input == "order":  # If the user chooses "order"
                menu_order()  # Display the current order
                continue  # Continue the remove loop

            if user_input == "back":  # If the user chooses "back"
                # Break out of the menu add loop this will take us to the main menu
                break

            user_input: int = int(user_input)  # Casting the user input to an int

            total_fish: int = len(order.fish)  # Get the total number of fish
            if user_input <= total_fish:  # If the user input index is within the total fish amount
                fish_type: str = list(order.fish)[user_input - 1]  # Get the type of fish using the key index
                amount: int = order.fish[fish_type]  # Get the amount of that type of fish
                order.fish.pop(fish_type)  # Remove the fish from the order
                good(f'Removed {amount} {fish_type}')  # Tell the user it was removed
            else:  # Otherwise move on
                user_input -= total_fish + 1  # Decrease the user input to move on to the next type
                if user_input <= len(order.chips):  # If the user input is within the total chips amount
                    amount: float = order.chips[user_input]  # Get the amount of chips using the index
                    order.chips.remove(user_input)  # Remove the chips from the order
                    good(f'Removed {amount} scoops of chips')  # Tell the user it was removed


def menu_order() -> NoReturn:
    """
    Prints out the current order which contains
    all the added items and their prices
    """
    print(create_order_list(order, MENU['types']))  # Prints out the order


def menu_finish() -> bool:
    """
    Prompts the user with the finish menu
    for confirming the order then starting a new
    one if needed

    :return: Whether or not the exit
    """
    if order.empty():  # The current order is empty
        # Tell the user the order is empty
        error('The current order is empty!')
        return False  # Order has nothing in it so we must continue

    menu_order()  # Displays the current order

    # Prompt the user to make sure the order is correct
    if accept_bool(
            create_prompt(['Is the listed order correct? [Y/N]', 'Selecting no will return to the menu.'])
    ):  # The order is correct

        # Prompt the user if they would like to restart
        if accept_bool(create_prompt(['Would you like to start again? (Y/N)'])):  # They would like to start again
            menu_init()  # Initialize the order again
            return False  # They want to start again so continue the main loop
        else:
            return True  # The user does not want to start again so we will exit

    else:  # The order is not correct so continue the main loop
        return False


def menu_cancel() -> bool:
    """
    The menu function for canceling the
    order and restarting / closing the program

    :return: Whether or not the exit
    """
    global order
    # Set the order to None
    order = None
    # Inform the user that the order is cancelled
    good('Current order cancelled')
    # Prompt the user if they would like to restart
    if accept_bool(create_prompt([
        'Would you like to start again? (Y/N)'
    ])):
        menu_init()  # Initialize the order again
        return False
    else:
        return True


if __name__ == '__main__':
    # Displays the title "Freddy's Fast Food"
    menu_title()
    # Displays the init menu
    menu_init()
    # Displays the main menu
    menu_main()
