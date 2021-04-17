from typing import Callable, Any, List, NoReturn
from guiutil import error

BOOLEAN_YES: List[str] = ['y', 'yes', 't', 'true', '1']  # A list of the values that represent True
BOOLEAN_NO: List[str] = ['n', 'no', 'f', 'false', '0']  # A list of the values that represent False


class ValidationError(Exception):
    message: str  # The message telling the user whats wrong

    def __init__(self, message):
        """
        An exception used to handle invalid input
        from the user

        :param message: The message telling the user whats wrong
        """
        self.message = message


def accept(message: str, test: Callable[[str], Any]) -> str:
    """
    Accept a user input matching a test function
    Continues to display the message if invalid input
    is provided

    :param message: The message to display to the user
    :param test: The validation test the response must pass
    """
    # Looped so it will continue to prompt the user until
    # valid user input is provided
    while True:
        # Retrieve the user input
        user_input = input(message)
        try:
            # Make sure there's actually input and not nothing
            if len(user_input) < 1:
                raise ValidationError('You must provide something!')  # Raise a validation exception
            # Run the validation test for further validation
            test(user_input)
            # Return the user input
            return user_input
        # Catch any validation exceptions
        except ValidationError as e:
            # Print the validation exception
            error(e.message)


def accept_int(message: str, min_value: int, max_value: int) -> int:
    """
    Accepts an integer from user input that is
    within the minimum and maximum values

    :param message: The message to display to the user
    :param min_value: The minimum acceptable integer
    :param max_value: The maximum acceptable integer
    :return: The integer value provided by the user
    """
    return int(
        accept(
            message,
            lambda value:  # Validation lambda function
            Validation.min_max(  # Validate that it is within the min and max
                Validation.int(value),  # Validate that the input is an int
                min_value,
                max_value
            )
        )
    )


def accept_float(message: str, min_value: float, max_value: float) -> float:
    """
    Accepts a float from user input that is
    within the minimum and maximum values

    :param message: The message to display to the user
    :param min_value: The minimum acceptable float
    :param max_value: The maximum acceptable float
    :return: The float value provided by the user
    """
    return float(
        accept(
            message,
            lambda value:  # Validation lambda function
            Validation.min_max(  # Validate that it is within the min and max
                Validation.float(value),  # Validate that the input is a float
                min_value,
                max_value
            )
        )
    )


def accept_bool(message: str) -> bool:
    """
    Accepts a boolean value from the user
    acceptable values are in BOOLEAN_YES
    and BOOLEAN_NO

    :param message: The message to display to the user
    :return: The boolean value provided by the user
    """
    return accept(message, Validation.boolean) in BOOLEAN_YES


class Validation:

    @staticmethod
    def list_or_int(value: str, values: List[str], min_value: int, max_value: int) -> NoReturn:
        """
        Attempts to validate the input as one of the
        value or an integer between the min and max.
        Throws a validation exception if neither of
        these are True

        :param value: The value to validate
        :param values: The list of acceptable values
        :param min_value: The minimum acceptable value
        :param max_value: The maximum acceptable value
        """
        if value not in values:  # If the value is not one of the text values
            value: int = Validation.int(value)  # Validate the that the value is an int
            Validation.min_max(value, min_value, max_value)  # Validate that its within the bounds

    @staticmethod
    def list_or_float(value: str, values: List[str], min_value: float, max_value: float) -> NoReturn:
        """
        Attempts to validate the input as one of the
        value or an float between the min and max.
        Throws a validation exception if neither of
        these are True

        :param value: The value to validate
        :param values: The list of acceptable values
        :param min_value: The minimum acceptable value
        :param max_value: The maximum acceptable value
        """
        if value not in values:  # If the value is not one of the text values
            value: float = Validation.float(value)  # Validate the that the value is an float
            Validation.min_max(value, min_value, max_value)  # Validate that its within the bounds

    @staticmethod
    def int(value: str) -> int:
        """
        Attempts to validate the input as an
        integer. Throws a validation exception if
        its not an integer

        :param value: The value to validate
        :return: The integer value
        """
        try:
            return int(value)  # Cast the value to a int
        except ValueError:  # Catch the ValueError thrown if its not a number
            # Throw a validation exception because its not a valid int
            raise ValidationError('Provided input "{}" is not a valid number'.format(value))

    @staticmethod
    def float(value: str) -> float:
        """
        Attempts to validate the input as a
        float. Throws a validation exception if
        its not a float

        :param value: The value to validate
        :return: The float value
        """
        try:
            return float(value)  # Cast the value to a float
        except ValueError:  # Catch the ValueError thrown if its not a number
            # Throw a validation exception because its not a valid float
            raise ValidationError('Provided input "{}" is not a valid number'.format(value))

    @staticmethod
    def min_max(value: float or int, min_value: float or int, max_value: float or int) -> NoReturn:
        """
        Attempts to validate that the float/int input
        is within the specified minimum and maximum value.
        Throws a validation exception if the number is too small
        or large

        :param value: The value to validate
        :param min_value: The minimum acceptable value
        :param max_value: The maximum acceptable value
        """
        # Check if the number is less than min
        if value < min_value:
            # The number is too small throw a validation exception
            raise ValidationError('Number cannot be less than {} you picked {}'.format(min_value, value))
        if value > max_value:
            raise ValidationError('Number cannot be greater than {} you picked {}'.format(max_value, value))

    @staticmethod
    def boolean(value: str) -> bool:
        """
        Attempts to validate the input as
        a boolean value using the values in
        BOOLEAN_YES and BOOLEAN_NO. Throws
        a validation exception if its not valid

        :param value: The value to validate
        :return: The boolean value of the user input
        """
        value: str = value.lower()  # Convert to lowercase so that we ignore case
        if value not in BOOLEAN_YES + BOOLEAN_NO:  # Check if the value is not in the lists
            # Throw a validation exception
            raise ValidationError('You must pick yes or no!')
        # Return if its in the YES list or not
        return value in BOOLEAN_YES
