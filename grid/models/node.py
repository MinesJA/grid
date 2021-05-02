from asyncio import Queue
from time import time
from uuid import uuid1
from grid.models.actor import Actor
from grid.models.message import *
from grid.models.envelope import *
from grid.models.mailDistr import MailDistr
from grid.models.nodeProxy import NodeProxy


class Node(Actor):

    def __init__(self,
                 name: str,
                 host: str,
                 port: str,
                 production: int,
                 consumption: int,
                 outbox: Queue):
        """Builds a Node object. Net describes the net energy
        output of the entire grid. If no siblings, then net
        is simply the net output of the invididual node.

        Args:
            address (str): http address of the node (ex. '123.123.123')
            port (str): port of the node (ex. '8080')
        """
        super().__init__(uuid1(), f'{host}:{port}')
        self.name = name
        self.siblings = {}
        # {req_id: {env_id: <Envelope ....> }}

        self.production = production
        self.consumption = consumption
        self._net = production - consumption
        self.outbox = outbox

        self.mail_routing = {}

    @property
    def net(self):
        print(f'{self.name} - Getting net: {self._net}')
        return self._net

    @net.setter
    def net(self, value):
        print(f'{self.name} - Setting net: {value}')
        self._net = value

    def personal_net(self):
        return self.production - self.consumption

    async def on_receive(self, env):
        if isinstance(env.msg, UpdateEnergy):
            self.update_energy(env)
        elif isinstance(env.msg, AddSibling):
            self.add_sibling(env)
        elif isinstance(env.msg, UpdateNet):
            self.update_net(env)
        else:
            self.print(
                f'{self.name}: Did not recognize message {env.msg}')

    async def add_sibling(self, env):
        """Adds a sibling NodeProxy to siblings. Then sends
        response message AddSibling with it's own info to maintain
        a bidirectional graph. Then sends a request to update
        the grids net output.

        Args:
            env (Envelope): envelope with add sibling details
        """

        """
        tell: {n1 addsibling n2}
        n1 ask: adds n2 internally asks n2 to add
        n2: updates n1 internally responds to n1
        """

        # env.msg.sibling_id
        # env.msg.sibling_name
        # env.msg.sibling_address

        sibling = NodeProxy(env.msg.sibling_id,
                            env.msg.sibling_name,
                            env.msg.sibling_address)

        if isinstance(env, Tell) and sibling.id not in self.siblings:
            # TODO: Do we need a seperate id and req_id? Redundant?
            req_id = uuid1()
            ask_env = Ask(id=req_id,
                          timestamp=time(),
                          to=env.msg.sibling_address,
                          msg=AddSibling.with_self(self),
                          reply_to_id=self.id,
                          req_id=req_id)

            mail_distr = MailDistr(self.id)
            mail_distr.update_awaiting(req_id, ask_env)
            self.mail_routing.update({req_id: mail_distr})
            await self.outbox.put(ask_env)

        elif isinstance(env, Ask) and sibling.id not in self.siblings:

            self.siblings.update({sibling.id: sibling})
            resp_msg = AddSibling.with_self(self)
            resp_env = Response(id=uuid1(),
                                timestamp=time(),
                                to=sibling.address,
                                msg=resp_msg,
                                req_id=env.id)

            await self.outbox.put(resp_env)

        elif isinstance(env, Response) and sibling.id not in self.siblings:
            # Once the reciprocal relationship has been established
            # then update the original Node's siblings and send
            # a request to update the Net values of each Node

            self.siblings.update({env.msg.sibling_id: sibling})

            mail_distr = self.mail_routing.get(env.req_id)

            if not mail_distr:
                raise ValueError(
                    f'{self.name} does not have a \
                        MailDistr for id: {env.master_req_id}')

            mail_distr.close_awaiting(env.req_id)
            # TODO: Currently only updates this Node's net values,
            # Does not update all other nodes
            self.forward_update()

    # TODO: Need to rename this
    async def forward_update(self,
                             master_req_id=None,
                             reply_to_id=None,
                             siblings=None):
        """Nodes send out an update message to each of their siblings which
        have not already sent an update message (to prevent forwarding
        backwards). Nodes keep track of pending replies tracking both
        the original request id as well as the envelope id from
        forwarding message:

            {req_id: {env_id: <Envelope .... > } }

        When a msg gets to a Node which already has pending messages with the
        same orig_msg_id, this indicates a path is arleady underway. The Node
        should respond to the reply_to with a tell and a response of 0 (or some
        kind of indication the actual response is None but it is in fact
        responding).

        When a Node receives a response it checks it's pending_replies and
        updates the appropriate Envelope with the response. Once all pending
        replies have been responded, it packages all the information and
        sends it back to it's reply_to.

        Nodes should check to make sure the messages they are receiving are not
        the original request they initially made. If they are, they update
        their own pending messages. Eventually, all their pending messages
        should be updated and they should update themselves.

        Args:
            req_id (uuid1): original request id
            siblings (list(NodeProxy), optional): list siblings.
                Defaults to None.
        """
        siblings = siblings if siblings else self.siblings.values()
        reply_to_id = reply_to_id if reply_to_id else self.id
        master_req_id = master_req_id if master_req_id else uuid1()

        mail_distr = MailDistr(reply_to_id)
        self.mail_routing.update({master_req_id: mail_distr})

        for sibling in siblings:
            req_id = uuid1()
            ask_env = Ask(id=uuid1(),
                          timestamp=time(),
                          to=sibling.address,
                          msg=UpdateNet(uuid1()),
                          reply_to_id=self.id,
                          req_id=req_id,
                          master_req_id=master_req_id)
            mail_distr.update_awaiting(req_id, ask_env)

            await self.outbox.put(ask_env)

    async def update_net(self, env):
        """Update net by collecting net values
        of entire grid and summing them up.

        Args:
            env (Envelope): envelope
        """

        if isinstance(env, Tell):
            # Primary Message to begin Update Net
            self.forward_update()

        elif isinstance(env, Ask):
            reply_to = self.siblings.get(env.reply_to_id)
            to_resp = self.mail_routing.get(env.master_req_id)
            siblings = [s for s in self.siblings.values() if s is not reply_to]

            if not reply_to:
                raise ValueError(
                    f'{env.reply_to} is not an established sibling')

            if not to_resp and siblings:
                # 1. This request has not been processed before
                # 2. This is not a dead end
                # Forward message to all siblings
                self.forward_update(env.master_req_id,
                                    env.reply_to_id,
                                    siblings)
            elif to_resp:
                # 1. This message has already been processed by another node
                # Respond with a 0 value to prevent duplicate counting
                resp_env = Response(to=reply_to.address,
                                    msg=UpdateNet({self.id: 0}),
                                    req_id=env.req_id)
                await self.outbox.put(resp_env)
            elif not siblings:
                # 1. This is a dead end
                # Begin retrieval process
                resp_env = Response(to=reply_to.address,
                                    msg=UpdateNet(
                                        {self.id: self.personal_net()}),
                                    req_id=env.req_id)
                await self.outbox.put(resp_env)
            else:
                raise ValueError(
                    f'{self.address}: Something bad happend in Ask UpdateNet')

        elif isinstance(env, Response):
            reply_to = self.siblings.get(env.reply_to_id)
            mail_distr = self.mail_routing.get(env.master_req_id)

            if not mail_distr:
                raise ValueError(
                    f'{self.name} does not have a \
                        MailDistr for id: {env.master_req_id}')

            if not reply_to:
                raise ValueError(
                    f'{env.reply_to} is not an established sibling')

            to_resp = mail_distr.get_awaiting(env.req_id)

            if not to_resp:
                raise ValueError(
                    f'{self.name} does not have an \
                        Awaiting Response for id: {env.req_id}')

            if mail_distr.reply_to_id == self.id:
                # 1. The response has reached the start
                # Close out request

                self.net = sum(env.msg.nets.values())
                print(f'{self.address} closed out request. Net value is {self.net}')
                mail_distr.close_awaiting(env.req_id, env)

            elif mail_distr.is_completed():
                compiled_nets = {self.id: self.personal_net()}

                for e in mail_distr.responded.values():
                    compiled_nets.update(e.msg.nets)

                forward_to = self.siblings.get(mail_distr.reply_to_id)
                resp_env = Response(to=forward_to.address,
                                    msg=UpdateNet(compiled_nets),
                                    req_id=env.req_id,
                                    master_req_id=env.master_req_id)
                await self.outbox.put(resp_env)

            elif not mail_distr.is_completed():
                # 1. Mail is still pending
                # Close out received envelope
                mail_distr.close_awaiting(env.req_id, env)

            else:
                raise ValueError(f'{self.address}: Something has gone \
                wrong in Response handling')

    def update_energy(self, env):
        """Updates the energy production and/or
        consumption of Node

        Args:
            env ([type]): [description]
        """
        x = f'NODE: Hit update energy'\
            f'consumption={env.msg.consumption if not None else 0}'\
            f'production={env.msg.production if not None else 0}'

        # TODO: Refactor to one liners
        if env.msg.consumption is not None:
            self.consumption = env.msg.consumption
        if env.msg.production is not None:
            self.production = env.msg.production

        self.net = self.production - self.consumption
        self.forward_update()

        # TODO: need to implement to make sure other siblings update their net
        # as well
        # for s in self.siblings.value():
        #     s.message(Tell(id=uuid1(), timestamp=time(),
        #       msg=UpdateNet(id=uuid1()))

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.id == other.id
        return False

    def __hash__(self):
        return id(self.id)

    def __str__(self):
        return f'Node<name={self.name} \
        id={self.id} \
        production={self.production} \
        consumption={self.consumption} \
        net={self.net}>'
