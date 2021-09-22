from uuid import UUID
from grid.utils.valueGetters import getuuid, getint
from grid.messages import Message, UpdateNet, SyncGrid


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

    async def from_tell(self, node, mailroom):
        siblings = node.siblings.values()
        node.update_energy((self.production, self.consumption))

        if len(siblings) < 1:
            node.update_gridnet(self.production-self.consumption)

        await mailroom.ask(msg=UpdateNet(),
                           sender=node,
                           recipients=siblings)

        # TODO: Can remove this if we're going clockcycle route
        await mailroom.tell(msg=SyncGrid(),
                            sender=node,
                            recipients=siblings)
