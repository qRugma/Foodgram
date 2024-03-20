from django.core.exceptions import ValidationError


def color_code(value):
    if len(value) != 7 or value[0] != '#':
        raise ValidationError(
            f'Задан некоректрый цветовой код: {value}'
        )
