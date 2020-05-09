import random
import string


def random_string(string_length):
    # Получение случайной строки
    letters = string.ascii_lowercase + string.ascii_uppercase
    return ''.join(random.choice(letters) for _ in range(string_length))
