import math


def get_first_n_from_left_side(num: int, n: int) -> int:
    return num // 10 ** n


def get_last_n_from_right_side(num: int, n: int) -> int:
    return num % (10 ** n)


def calculate_sum_of_digits(num: int) -> int:
    s = 0
    while num:
        s += num % 10
        num //= 10
    return s


def is_eligible(number: int) -> bool:
    first_three_digits = get_first_n_from_left_side(number, 3)
    sum_of_first_three_digits = calculate_sum_of_digits(first_three_digits)

    print(first_three_digits)

    last_three_digits = get_last_n_from_right_side(number, 3)
    sum_of_last_three_digits = calculate_sum_of_digits(last_three_digits)

    # print(first_three_digits, last_three_digits)

    if sum_of_first_three_digits == sum_of_last_three_digits:
        return True

    return False


def get_nearest_lucky_ticket(number: int) -> int:
    number_up = number
    number_down = number

    while True:
        if is_eligible(number_down):
            return number_down
        elif is_eligible(number_up):
            return number_up
        else:
            number_down -= 1
            number_up += 1


if __name__ == '__main__':
    assert get_nearest_lucky_ticket(333999) == 334019
    assert get_nearest_lucky_ticket(123322) == 123321
    assert get_nearest_lucky_ticket(111111) == 111111
