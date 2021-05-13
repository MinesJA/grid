
from uuid import UUID
from grid.utils.valueGetters import *
from grid.messages.message import Message


class UpdateEnergy(Message):

    def __init__(self,
                 production: int = None,
                 consumption: int = None,
                 id: UUID = None):
        """UpdateEnergy message update either production
        consumption, or both.

        Args:
            production (int): new production value
            consumption (int): new consumption value
        """
        super().__init__(id)
        self.production = production
        self.consumption = consumption

    @classmethod
    def deserialize(clss, data: dict):
        id = getuuid(data, 'id')
        pro = getint(data, 'production')
        con = getint(data, 'consumption')
        return clss(pro, con, id)

    def serialize(self):
        return {
            'id': str(self.id),
            'production': self.production,
            'consumption': self.consumption,
        }
