from uuid import UUID
from grid.utils.valueGetters import getuuid
from grid.messages import Message
from grid.utils.solanaUtils import transact


class UpdateNet(Message):

    def __init__(self,
                 nets: dict = {},
                 id: UUID = None):
        """Message requesting an updated Net value.

        Args:
            id (uuid1): Id of UpdateNet message
            nets (dict): Collection of Net values from each node
        """
        super().__init__(id)
        self.nets = nets

    def reduce(self, responses, node=None):
        """[summary]

        Args:
            responses ([type]): [description]
            node ([type], optional): [description]. Defaults to None.

        Returns:
            [type]: [description]
        """
        curr = {str(node.id): node.net} if node else {}
        for resp in responses.values():
            curr.update(resp.msg.nets)

        return UpdateNet(nets=curr)

    @classmethod
    def deserialize(clss, data: dict):
        id = getuuid(data, 'id')
        nets = data.get('nets')
        return clss(nets, id)

    def serialize(self):
        return {'id': str(self.id),
                'nets': self.nets}

    async def from_tell(self, node, mailroom, env):
        siblings = node.siblings.values()
        await mailroom.ask(sender=node,
                           msg=UpdateNet(),
                           recipients=siblings)

    async def from_ask(self, node, mailroom, env):
        await mailroom.forward_ask(ask=env,
                                   sender=node)

    async def from_response(self, node, mailroom, env):

        # TODO: This is a strange way to do things...
        #   Using the fact that forward_response returns a msg
        #   if it doesn't actually need to forward the response
        #   to determine whether to end it here or not (forward_response)
        #   will return nothing if it doesn't
        
        # SHOULD BE
        # if env is done
        #   upate grid net
        # else:
        #   forward_response


        msg = await mailroom.forward_response(resp=env, sender=node)
        if msg is not None:

            gridnet = sum(msg.nets.values())
            # TODO: This isn't safe. Node net may have changed from
            #   the moment of timestamp. Need to think of better way
            #   to do this.
            #   OR does this make sense because we want to take the gridnet
            #   and node net from the same time period (so now, together)?
            nodenet = node.net

            node.update_gridnet(gridnet)

            data = {
                'gridnet': gridnet,
                'nodenet': nodenet,
                'timestamp': env.timestamp
            }

            await transact(data)
