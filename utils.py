from typing import Callable

from guiutil import BOX_V

BOOLEAN_YES = ['y', 'yes', 't', 'true', '1']
BOOLEAN_NO = ['n', 'no', 'f', 'false', '0']


def accept_str(message: str, validator: Callable[[str], bool],
               err_message: None or str = 'The provided value "{}" is not a valid option!') -> str:
    while True:
        response = input(message)
        if validator(response):
            return response
        else:
            if err_message is not None:
                print(err_message.format(response))


def accept_bool(message: str) -> bool:
    value = accept_str(message, validate_bool)
    if value in BOOLEAN_YES:
        return True
    else:
        return False


def accept_int(message: str, min_value: int or None = None, max_value: int or None = None,
               min_err_message: str or None = BOX_V + ' The provided value "{}" cannot be less than {}',
               max_err_message: str or None = BOX_V + ' The provided value "{}" cannot be greater than {}') -> int:
    while True:
        def validate(v: str) -> bool:
            if not validate_int(v):
                print(BOX_V + f'The provided value "{v}" is not a valid number')
                return False
            if not validate_min_max_float(v, min_value, max_value,
                                          min_err_message,
                                          max_err_message):
                return False
            return True

        value = accept_str(message, validate, None)
        value = parse_int(value, 0)
        return value


def accept_float(message: str, min_value: float or None = None, max_value: float or None = None,
                 min_err_message: str or None = BOX_V + ' The provided value "{}" cannot be less than {}',
                 max_err_message: str or None = BOX_V + ' The provided value "{}" cannot be greater than {}') -> float:
    while True:
        def validate(v: str) -> bool:
            if not validate_float(v):
                print(BOX_V + f'The provided value "{v}" is not a valid number')
                return False
            if not validate_min_max_float(v, min_value, max_value,
                                          min_err_message,
                                          max_err_message):
                return False
            return True

        value = accept_str(message, validate, None)
        value = parse_float(value, 0)
        return value


def validate_min_max_int(value: str, min_value: int or None = None, max_value: int or None = None,
                         min_err_message: str or None = BOX_V + ' The provided value "{}" cannot be less than {}',
                         max_err_message: str or None = BOX_V + ' The provided value "{}" cannot be greater than {}') -> bool:
    value: int = parse_int(value, -1)
    if value == -1:
        return False
    if min_value is not None and value < min_value:
        if min_err_message is not None:
            print(min_err_message.format(value, min_value))
        return False
    if max_value is not None and value > max_value:
        if max_err_message is not None:
            print(min_err_message.format(value, min_value))
        return False
    return True


def validate_min_max_float(value: str, min_value: float or None = None, max_value: float or None = None,
                           min_err_message: str or None = BOX_V + ' The provided value "{}" cannot be less than {}',
                           max_err_message: str or None = BOX_V + ' The provided value "{}" cannot be greater than {}') -> bool:
    value: int = parse_int(value, -1)
    if value == -1:
        return False
    if min_value is not None and value < min_value:
        if min_err_message is not None:
            print(min_err_message.format(value, min_value))
        return False
    if max_value is not None and value > max_value:
        if max_err_message is not None:
            print(min_err_message.format(value, min_value))
        return False
    return True


def validate_int(value: str) -> bool:
    return parse_int(value, -1) != -1


def validate_float(value: str) -> bool:
    return parse_float(value, -1) != -1


def parse_float(value: str, default_value: float) -> float:
    try:
        return float(value)
    except ValueError:
        return default_value


def parse_int(value: str, default_value: int) -> int:
    try:
        return int(value)
    except ValueError:
        return default_value


def validate_bool(value: str) -> bool:
    value: str = value.lower()
    return value in BOOLEAN_NO or value in BOOLEAN_YES
