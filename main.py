from typing import Dict, List

from order import Order
from guiutil import create_prompt, create_indexed_menu, spacer, center, create_menu
from utils import accept_str, accept_int, parse_int, validate_min_max_int

VERSION: str = '1.0.0'
MAX_PER_ITEM: int = 7
DELIVERY_CHARGE: float = 5
FROZEN_DISCOUNT: float = 1.05

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

order = Order(MAX_PER_ITEM)

if __name__ == '__main__':
    spacer()
    print(TITLE_MESSAGE)
    spacer()
    while True:
        menu = accept_int(create_indexed_menu(None, [
            'Display Menu',
            'Add item',
            'Remove item',
            'List order',
            'Finish Order'
        ]), 1, 5)
        if menu == 1:
            print(create_menu(MENU['types']))
        if menu == 2:
            while True:
                total_types: int = 0
                for menu_type in MENU['types']:
                    if 'items' in menu_type:
                        for item in menu_type['items']:
                            total_types += 1
                    else:
                        total_types += 1
                user_input = accept_str(create_prompt([
                    'Enter "menu" to display the menu',
                    '"back" to go back or type the number',
                    'corresponding to a menu item'
                ]), lambda value: value in ['menu', 'back'] or validate_min_max_int(value, 1, total_types))
                if user_input.lower() == 'menu':
                    print(create_menu(MENU['types']))
                elif user_input.lower() == 'back':
                    break
                else:
                    item_index: int = parse_int(user_input, 1)
                    item_type: str or None = None
                    current_index: int = 1
                    for menu_type in MENU['types']:
                        if 'items' in menu_type:
                            items = menu_type['items']
                            for item in items:
                                if item_index == current_index:
                                    item_type = item
                                    break
                                current_index += 1
                            else:
                                # TODO: Unimplemented
                                print()
                            if item_type is not None:
                                break
                    if item_type is not None:
                        print(item_type)