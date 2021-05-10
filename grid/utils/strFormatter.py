
__all__ = ['format_attrs']


def format_attrs(**kwargs):
    lst_str = []

    for k, v in kwargs.items():
        lst_str.append(f'{k}={v.__str__()}')

    return ' '.join(lst_str)
