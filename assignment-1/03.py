import math
import random


def get_count_of_digits_in_int(number: int) -> int:
    return int(math.log10(number)) + 1


def get_digits_list(number: int):
    number = divmod(number, 10)

    while number != (0, 0):
        yield number[1]
        number = divmod(number[0], 10)


def get_checksum_int(card_number: int, parity_determinant: int = None) -> int:
    sum_of_digits = 0
    _parity_determinant = parity_determinant or (get_count_of_digits_in_int(card_number) - 1) % 2

    digits = reversed(list(get_digits_list(card_number)))

    for i, digit in enumerate(digits):
        _digit = int(digit)

        if (i + 1) % 2 == _parity_determinant:
            _digit *= 2
            if _digit > 9:
                _digit = _digit - 9

        sum_of_digits += _digit

    return sum_of_digits


def get_checksum_str(card_number: str, parity_determinant: int = None) -> int:
    sum_of_digits = 0
    _parity_determinant = parity_determinant or (len(card_number) - 1) % 2

    for i, digit in enumerate(card_number):
        _digit = int(digit)

        if (i + 1) % 2 == _parity_determinant:
            _digit *= 2
            if _digit > 9:
                _digit -= 9

        sum_of_digits += _digit

    return sum_of_digits


def get_check_digit_str(card_number: str):
    check_digit = get_checksum_str(card_number, 1) % 10

    if check_digit == 0:
        return 0

    return 10 - check_digit


def check_card_number_str(card_number: str) -> bool:
    result_sum = get_checksum_str(card_number)

    return result_sum % 10 == 0


def check_card_number(card_number: int, parity_determinant: int = None) -> bool:
    result_sum = get_checksum_int(card_number)

    return result_sum % 10 == 0


def generate_card_number(card_type: str) -> str:
    if card_type.lower() == 'visa':
        prefix = '4'
    elif card_type.lower() == 'mastercard':
        prefix = '5'
    else:
        raise ValueError('Invalid card type! Supported card types: Visa, Mastercard')

    card_number = [prefix]

    for i in range(0, 14):
        digit = random.randint(0, 9)
        card_number.append(str(digit))

    card_number = ''.join(card_number)
    check_digit = str(get_check_digit_str(card_number))

    return card_number + check_digit


if __name__ == '__main__':
    assert check_card_number_str('4561261212345467')
    assert not check_card_number_str('4601496706376197')
    assert check_card_number(5082337440657928)
    assert not check_card_number(4601496706376197)

    generated_visa_card_number = generate_card_number('visa')
    check_card_number_str(generated_visa_card_number)
