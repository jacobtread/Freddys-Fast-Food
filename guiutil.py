from math import floor
from re import sub
from sys import platform
from typing import List, Dict, NoReturn
from order import Order

# Box drawing chars
BOX_CTL: str = '┌'  # Corner top left line
BOX_CTR: str = '┐'  # Corner top right line
BOX_CBL: str = '└'  # Corner bottom left line
BOX_CBR: str = '┘'  # Corner bottom right line
BOX_SVL: str = "├"  # Split vertical left line
BOX_SVR: str = "┤"  # Split vertical right line
BOX_V: str = '│'  # Vertical line
BOX_H: str = '─'  # Horizontal line

ARROW: str = '»'  # A Fancy double right a arrow

# Linux ASCII control chars
COLOR_RED: str = '\033[91m'  # Sets the terminal color to red
COLOR_YELLOW: str = '\33[33m'  # Sets the terminal color to yellow
COLOR_GREEN: str = '\33[32m'  # Sets the terminal color to green
COLOR_END: str = '\033[0m'  # Clears the current terminal color

BOX_WIDTH: int = 78  # The width that boxes should be (this excludes the sides -2)


def is_linux() -> bool:
    """
    Determines whether or not the device running this
    program is using linux

    :return: Whether or not the platform is linux
    """
    return platform == "linux" or platform == "linux2"


def error(text: str) -> NoReturn:
    """
    Used for printing errors such as bad input to the console
    on linux devices it will use red color formatting

    :param text: The error text contents
    """
    if is_linux():  # We are on linux so we can use formatting codes
        # Print the message with the red formatting at the start
        # and the reset formatting at end
        print(COLOR_RED + text + COLOR_END)
    else:  # We aren't on linux so just print the text
        print(text)


def good(text: str) -> NoReturn:
    """
    Used for printing success texts such as completed
    tasks on linux devices it wil use green color
    formatting

    :param text: The text contents
    """
    if is_linux():  # We are on linux so we can use formatting codes
        # Print the message with the red formatting at the start
        # and the reset formatting at end
        print(COLOR_GREEN + text + COLOR_END)
    else:  # We aren't on linux so just print the text
        print(text)


def center(text: str, columns: int = BOX_WIDTH) -> str:
    """
    Centers text to the provided amount of columns

    :param text: The text to center
    :param columns: The number of columns (chars) to center by
    :return: The string with left padding centering it
    """
    text_length: int = len(text)
    # If the text length is the same or longer than the number of columns
    # We shouldn't do any padding to the left and should just return it as is
    if text_length >= columns:
        return text
    else:
        # The padding length is half the total space - half the text length
        padding_length: int = floor(columns / 2 - text_length / 2)
        # Return the text with the required amount of left padding (whitespace)
        return (padding_length * ' ') + text


def pad_right(text: str, columns: int) -> str:
    """
    Appends padding to a text so that it reaches
    a certain width

    :param text: The text to add padding to
    :param columns: The number of columns (chars) to padding until
    :return: The string with left padding centering it
    """
    text_length: int = len(text)
    # If the text length is the same or longer than the number of columns
    # We shouldn't do any padding to the right and should just return it as is
    if text_length >= columns:
        return text
    else:
        # The remaining length is just total length - the text length
        remaining_length: int = columns - text_length
        # Return the text with the required amount of right padding (whitespace)
        return text + (remaining_length * ' ')


def create_title(text: str, extra_width: int = 0) -> str:
    """
    Creates a centered box title

    :param text: The text to make a title out of
    :param extra_width: Any extra width to pad until
    :return: The centered title with a box outline
    """
    centered: str = center(text, BOX_WIDTH + extra_width)
    padded: str = pad_right(centered, BOX_WIDTH + extra_width)
    return BOX_V + padded + BOX_V + '\n'


def format_price(price: float) -> str:
    """
    Uses string formatting to format a float
    value as a currency (takes the first 2 decimal places e.g $4.00)

    :param price: The float price value
    :return: The formatting string value
    """
    return '${:,.2f}'.format(price)


def create_prompt(lines: List[str]) -> str:
    """
    Creates a prompt message with the provided lines
    (Used to tell the user what information we want)

    :param lines: The lines to put into the prompt
    :return: The created prompt
    """
    # The output string containing the menu
    output: str = f'{BOX_CTL}\n'
    # The current line we a printing
    line: str
    for line in lines:
        # If the software is running on linux we get
        # to use color formatting
        if is_linux():
            # Regex replace all numbers and surround them with yellow
            line = sub(r'([$]*[0-9]+[.]?[0-9]*)', f'{COLOR_YELLOW}\\{1}{COLOR_END}', line)
            # Regex replace all quoted text and surround them with yellow
            line = sub(r'"(.*)"', f'{COLOR_YELLOW}"\\{1}"{COLOR_END}', line)
        # Append the line to the output
        output += f'{BOX_V} {line}\n'
    # Append the arrow for user input
    output += f': {ARROW} '
    return output


def splitter() -> str:
    """
    Creates a divider with splits on the vertical axis
    so that it can be inside the box

    :return: The splitter
    """
    return BOX_SVL + (BOX_H * BOX_WIDTH) + BOX_SVR + '\n'


def item_padded(text: str) -> str:
    """
    Appends box chars and padding to a text so that it
    can be used inside of a box

    :param text: The item text to pad
    :return: The padded item text
    """
    return BOX_V + pad_right(text, BOX_WIDTH) + BOX_V + '\n'


def create_menu(types: List[Dict[str, float or str]]) -> str:
    """
    Creates a string representation of the menu

    :param types: The types of the menu
    :return: The string representation of the menu
    """
    # The output string containing the menu
    output: str = BOX_CTL + (BOX_H * BOX_WIDTH) + BOX_CTR + '\n'
    # The current index of the item
    index: int = 0
    # Whether or not this is the first section being added
    first: bool = True
    for menu_type in types:
        if first:  # If this is the first section change first to false then continue
            first = False
        else:
            # If this is not the first section we add a divider
            # with left and right splits
            output += BOX_SVL + (BOX_H * BOX_WIDTH) + BOX_SVR + '\n'

        name: str = menu_type['name']  # The name of the section
        price: float = menu_type['price']  # The price of the items in this section

        price_text: str = format_price(price)
        formatting_length: int = 0

        # If the price has a custom format we should
        # apply that here
        if 'price_format' in menu_type:
            price_text = menu_type['price_format'].format(price_text)

        # If we are on linux we can apply color formatting
        if is_linux():
            # Append the yellow color and the reset color to the price text
            price_text = COLOR_YELLOW + price_text + COLOR_END
            # Set the length of the formatting to the length
            # of the reset char and the yellow char
            formatting_length = len(COLOR_YELLOW) + len(COLOR_END)

        # Appending the name title to the output
        output += create_title(name)
        # Appending the price title to the output
        output += create_title(price_text, formatting_length)

        # Split the title and the content using a divider
        # with left and right splits
        output += BOX_SVL + (BOX_H * BOX_WIDTH) + BOX_SVR + '\n'

        # Ensure that this sections has items (fish not chips)
        if 'items' in menu_type:
            # The item inside the section
            items: List[str] = menu_type['items']
            for item in items:
                # Format the item with it's index and name
                item = f'{index + 1}) {item}'
                # Append the item to the output
                output += item_padded(' ' + item)
                index += 1  # Increase the index
        elif 'text' in menu_type:
            # This section doesn't have any items but it has a
            # message so this will be its object
            item_text = f'{index + 1}) {menu_type["text"]}'
            # Append the text to the output
            output += item_padded(' ' + item_text)
            index += 1  # Increase the index

    # Append the bottom of the box
    output += BOX_CBL + (BOX_H * BOX_WIDTH) + BOX_CBR
    return output


def get_item_price(types: List[dict], item_name: str, is_name: bool) -> float:
    """
    Finds the price of the specified item

    :param types: The menu type sections
    :param item_name: The name of the item
    :param is_name: If true then the item name is a name not an item
    :return: The price or 0 if not found
    """
    for menu_type in types:
        # The name of the menu item
        name: str = menu_type['name']
        # The price of these items
        price: float = menu_type['price']
        # If we are searching for type names and it matches
        if is_name and name == item_name:
            return price  # Return the price
        # Otherwise if this type has items and its in the items
        elif 'items' in menu_type and item_name in menu_type['items']:
            return price  # Return the price
    # Not found so return 0
    return 0


def create_order_list(order: Order, types: List[dict]) -> str:
    """
    Creates a string representation of an order

    :param types: The type sections of the menu
    :param order: The order object
    :return: The string representation of the order
    """
    # The output string containing the order list
    output: str = BOX_CTL + (BOX_H * BOX_WIDTH) + BOX_CTR + '\n'
    # The current index of the item
    index: int = 0

    # Append the order id
    output += create_title('Order # ' + order.order_id) + splitter()
    # Append the customer name
    output += item_padded(' Name: ' + order.name)
    # Append the customer phone
    output += item_padded(' Phone: ' + order.phone)

    if order.delivery:  # If the customer is getting it delivered
        # Append the customer address
        output += item_padded(' Address: ' + order.address)

    if order.frozen:  # If the customer wants it frozen
        # Append the message "Frozen Order Discount" indicting there is a discount
        output += item_padded(' Frozen Order Discount')

    if order.empty():
        # If we have an empty order tell the user
        output += splitter() + create_title('No Items')

    else:
        # If we have fish in our order
        if len(order.fish) > 0:
            # Append the title
            output += splitter() + create_title('Fish (Quantity):') + splitter()

            for fish in order.fish:
                amount: int = order.fish[fish]  # The amount of fish
                # Find the price of this fish type then times it by how many we have
                price: float = get_item_price(types, fish, False) * amount
                # Append the fish item
                output += item_padded(f' {index + 1}) {fish} {amount} - {format_price(price)}')
                index += 1  # Increase the index

        # If we have chips in our order
        if len(order.chips) > 0:

            # Append the title
            output += splitter() + create_title('Chips (Scoops):') + splitter()

            # Find the price of chips
            price: float = get_item_price(types, 'Chips', True)

            for chips in order.chips:
                # Append the chips item
                output += item_padded(f' {index + 1}) {chips} scoops - {format_price(price * chips)}')
                index += 1  # Increase the index

        # Calculate the prices
        frozen_discount, total_price, total_gst, total_inc_gst = order.calculate_prices(types)

        output += splitter()  # Append a splitter

        if order.delivery:  # If the order is delivery
            # Append the cost for delivery
            output += item_padded(' DELIVERY: ' + format_price(order.delivery_charge))
        if order.frozen:  # If the order is frozen
            # Append the amount taken away by the frozen discount
            output += item_padded(' DISCOUNT: ' + format_price(frozen_discount))

        # Append the total cost (after delivery and discount)
        output += item_padded(' TOTAL: ' + format_price(total_price))
        # Append the total amount of GST
        output += item_padded(' TOTAL GST: ' + format_price(total_gst))
        # Append the total inclusive of GST
        output += item_padded(' TOTAL INC GST: ' + format_price(total_inc_gst))

    # Append the bottom of the box
    output += BOX_CBL + BOX_H * BOX_WIDTH + BOX_CBR
    return output
