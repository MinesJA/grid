from grid.utils.strFormatter import *


class Actor:

    def __init__(self, id: int, address: str, name: str):
        self.id = id
        self.address = address
        self.name = name

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id
        return False

    def __hash__(self):
        return id(self.id)

    def __repr__(self):
        clss_name = self.__class__.__name__
        base_attrs = format_attrs(id=self.id,
                                  address=self.address,
                                  name=self.name)

        return f'[{clss_name}] {base_attrs}'

    def __str__(self):
        return self.__repr__()
