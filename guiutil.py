from math import floor
from typing import List, Dict

BOX_CTL = '┌'
BOX_CTR = '┐'
BOX_CBL = '└'
BOX_CBR = '┘'
BOX_SVL = "├"
BOX_SVR = "┤"
BOX_V = '│'
BOX_H = '─'
DD_RA = '»'


def spacer(columns: int = 78) -> None:
    print(BOX_SVL + BOX_H * (columns - 2) + BOX_SVR)


def create_indexed_menu(title: str or None, values: List[str]) -> str:
    output: str = f'{BOX_CTL}\n'
    if title is not None:
        title: str
        title = title.replace('\n', f'\n{BOX_V}')
        output += f'{BOX_V} {title}\n'
    for (index, value) in enumerate(values):
        output += f'{BOX_V} {index + 1}) {value}\n'
    output += f': {DD_RA} '
    return output


def pad_right(text: str, length: int) -> str:
    return text + ' ' * (length - len(text))


def create_menu(sections: List[Dict[str, float or str]]) -> str:
    output: str = ''
    longest_str: int = 0
    for section in sections:
        name: str = section['name']
        if len(name) > longest_str:
            longest_str = len(name)
        if 'items' in section:
            items: List[str] = section['items']
            item: str
            for item in items:
                if len(item) > longest_str:
                    longest_str = len(item)
        elif 'text' in section:
            text = section['text']
            if len(text) > longest_str:
                longest_str = len(text)
    box_size: int = 76
    center_size: int = box_size - 2
    output += BOX_CTL + BOX_H * box_size + BOX_CTR + '\n'
    index: int = 0
    first: bool = True
    for section in sections:
        name = section['name']
        if not first:
            output += BOX_SVL + BOX_H * box_size + BOX_SVR + '\n'
        name = center(name, center_size)
        output += BOX_V + ' ' + pad_right(name, center_size + 1) + BOX_V + '\n'
        price: float = section['price']
        price_text: str = '${:,.2f}'.format(price)
        if 'price_format' in section:
            price_format: str = section['price_format']
            price_text = price_format.format(price_text)
        price_text = center(price_text, center_size)
        output += BOX_V + ' ' + pad_right(price_text, center_size + 1) + BOX_V + '\n'
        output += BOX_SVL + BOX_H * box_size + BOX_SVR + '\n'
        if 'items' in section:
            items = section['items']
            for item in items:
                item_text = f'{index + 1}) {item}'
                output += BOX_V + ' ' + pad_right(item_text, center_size + 1) + BOX_V + '\n'
                index += 1
        else:
            item_text = f'{index + 1}) {section["text"]}'
            output += BOX_V + ' ' + pad_right(item_text, center_size + 1) + BOX_V + '\n'
        first = False
    output += BOX_CBL + BOX_H * box_size + BOX_CBR
    return output


def create_prompt(lines: List[str]) -> str:
    output: str = f'{BOX_CTL}\n'
    line: str
    for line in lines:
        output += f'{BOX_V} {line}\n'
    output += f': {DD_RA} '
    return output


def center(message: str, columns: int = 78) -> str:
    message_length: int = len(message)
    if message_length == columns:
        return message
    else:
        num_spaces: int = floor(columns / 2 - message_length / 2)
        if num_spaces < 0:
            return message
        else:
            return (num_spaces * ' ') + message
