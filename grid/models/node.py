from datetime import datetime, time
from uuid import uuid1
from collections import defaultdict
from grid.models.nodeProxy import NodeProxy
from grid.models.actor import Actor
from grid.models.message import AddSibling, UpdateNet, UpdateEnergy
from grid.models.envelope import Envelope, Tell, Ask, Response
from grid.models.mailDistr import MailDistr


class Node(Actor):

    # TODO: Naming convention for address is confusing.
    # Address:Port = Address??
    def __init__(self, name: str, address: str, port: str,
                 production: int, consumption: int):
        """Builds a Node object. Net describes the net energy
        output of the entire grid. If no siblings, then net
        is simply the net output of the invididual node.

        Args:
            address (str): http address of the node (ex. '123.123.123')
            port (str): port of the node (ex. '8080')
        """
        super().__init__(uuid1(), f'{address}:{port}')
        self.name = name
        self.siblings = {}
        # {req_id: {env_id: <Envelope ....> }}

        self.production = production
        self.consumption = consumption
        self._net = production - consumption

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

    async def on_receive(self, envelope):
        if isinstance(envelope.message, UpdateEnergy):
            self.update_energy(envelope)
        elif isinstance(envelope.message, AddSibling):
            self.add_sibling(envelope)
        elif isinstance(envelope.message, UpdateNet):
            self.update_net(envelope)
        else:
            self.print(
                f'{self.name}: Did not recognize message {envelope.message}')

    async def add_sibling(self, env):
        """Adds a sibling NodeProxy to siblings. Then sends
        response message AddSibling with it's own info to maintain
        a bidirectional graph. Then sends a request to update
        the grids net output.
        # TODO: Edit per changes

        Args:
            env (Envelope): envelope with add sibling details
        """

        """
        tell: {n1 addsibling n2}
        n1 ask: adds n2 internally asks n2 to add
        n2: updates n1 internally responds to n1
        """

        sibling = env.msg.sibling

        if isinstance(env, Tell) and sibling.id not in self.siblings:
            ask_msg = AddSibling.add_self(self)
            ask_env = Ask(ask_msg, self.address)
            self.mail_distr.awaiting_responses.update({ask_env.id: ask_env})
            sibling.ask(ask_env)

        elif isinstance(env, Ask) and sibling.id not in self.siblings:
            self.siblings.update({sibling.id: sibling})
            resp_msg = AddSibling.add_self(self)
            resp_env = Response(resp_msg, env.id)
            sibling.respond(resp_env)

        elif isinstance(env, Response) and sibling.id not in self.siblings:
            # Once the reciprocal relationship has been established
            # then update the original Node's siblings and send
            # a request to update the Net values of each Node

            self.siblings.update({sibling.id: sibling})
            self.mail_distr.awaiting_responses.pop(env.req_id)
            self.update_network(req_id=uuid1())

    def forward_update(self, master_req_id=None, reply_to=None, siblings=None):
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
        reply_to = reply_to if reply_to else self.id
        master_req_id = master_req_id if master_req_id else uuid1()

        self.mail_routing.update({master_req_id: MailDistr(reply_to)})
        mail_distr = self.mail_routing.get(master_req_id)

        for sibling in siblings:
            req_id = uuid1()
            ask_env = Ask(msg=UpdateNet(), reply_to=self.id,
                          req_id=req_id, master_req_id=master_req_id)
            mail_distr.update_awaiting(req_id, ask_env)
            sibling.ask(ask_env)

    def update_net(self, env):
        """Update net by collecting net values
        of entire grid and summing them up.

        Args:
            env (Envelope): envelope
        """
        # reply_to_node = self.siblings.get(env.reply_to)
        # pending_envelopes = self.pending_replies.get(env.msg.req_id)

        # req_id = env.msg.req_id
        # forward_id = (req_id, env.id)

        # to_resp = self.mail_distr.to_respond(req_id)
        # awaiting_resp = self.mail_distr.awaiting_responses(forward_id)

        if isinstance(env, Tell):
            self.forward_update()

        elif isinstance(env, Ask):
            req_id = env.req_id
            master_req_id = env.master_req_id
            reply_to = self.siblings.get(env.reply_to)
            to_resp = self.mail_routing.get(master_req_id)
            siblings = [s for s in self.siblings.values() if s is not reply_to]

            if not reply_to:
                raise ValueError(
                    f'{env.reply_to} is not an established sibling')

            if not to_resp and siblings:
                # 1. This request has not been processed before
                # 2. This is not a dead end
                # Forward message to all siblings
                self.forward_update(master_req_id, env.reply_to, siblings)
            elif to_resp:
                # 1. This message has already been processed
                # Respond with a 0 value to prevent duplicate counting
                resp_env = Response(UpdateNet({self.id: 0}), req_id)
                reply_to.respond(resp_env)
            elif not siblings:
                # 1. This is a dead end
                # Begin retrieval process
                resp_env = Response(UpdateNet({self.id: self.net}), req_id)
                reply_to.respond(resp_env)
            else:
                raise ValueError('Something bad happend in ASK UpdateNet')

        elif isinstance(env, Response):
            reply_to = self.siblings.get(env.reply_to)
            req_id = env.req_id
            master_req_id = env.master_req_id
            mail_distr = self.mail_routing.get(master_req_id)

            if not mail_distr:
                raise ValueError(
                    f'{self.name} does not have a \
                        MailDistr for id: {master_req_id}')

            if not reply_to:
                raise ValueError(
                    f'{env.reply_to} is not an established sibling')

            awaiting_env = mail_distr.get_awaiting(req_id)

            if not awaiting_env:
                raise ValueError(
                    f'{self.name} does not have an \
                        Awaiting Env for id: {req_id}')

            if mail_distr.reply_to == self.id:
                # 1. This is the start of the chain
                # Close out request
                self.net = sum(env.msg.nets.values())
                mail_distr.close_awaiting(req_id, env)

            elif mail_distr.is_completed():
                compiled_nets = {self.id: self.personal_net()}

                for resp_env in mail_distr.responded.values():
                    compiled_nets.update(resp_env.msg.nets)

                reply_to = self.siblings.get(mail_distr.reply_to)
                resp_env = Response(UpdateNet(compiled_nets),
                                    req_id, master_req_id)
                reply_to.respond(resp_env)

            elif not mail_distr.is_completed():
                # If all awaiting_responses now have resp_msgs
                # package all nets and respond to to_respond.reply_to
                # with compiled data

                
                mail_distr.close_awaiting(req_id, env)



            elif not env.reply_to and env.resp_msg and awaiting_resp and not to_resp:
                # 1. This is a Tell request
                # 2. The incoming  Envelope has a response
                # 3. This reponse is expected
                # 4. A prior Node is expecting a response
                # Replace the existing Envelope with the response Envelope

                self.mail_distr.update_awaiting(forward_id, env)

                if not self.mail_distr.is_awaiting(req_id):
                    # If all awaiting_responses now have resp_msgs
                    # package all nets and respond to to_respond.reply_to
                    # with compiled data

                    compiled_nets = {
                        self.id: self.production - self.consumption}

                    for pend_env in self.mail_distr.awaiting_responses.values():
                        compiled_nets.update(pend_env.resp_msg.nets)

                    resp_env = gen_forward_envelope(env, compiled_nets)

            print(message.nets)

            total_net = sum(message.nets.values())
            self.net = total_net + (self.production - self.consumption)
        msg, recip_id = envelope
        all_nets = [self.pro - self.con]

        msg = UpdateNet(self.id)
        forward_msg = Forward(self.id, msg)
        self.net_messages.add(msg.id)

        for sibling in self.siblings.values():
            if msg.id not in sibling.net_messages:
                nets.append(sibling.ask(forward_msg))

        if recip_id:
            self.siblings.get(recip_id)

        # self.net = sum(flatten(vals))

    def update_energy(self, envelope: UpdateEnergy):

        message, *_ = envelope

        x = f'NODE: Hit update energy'\
            f'consumption={message.consumption if not None else 0}'\
            f'production={message.production if not None else 0}'

        print(x)
        # TODO: Refactor to one liners
        if message.consumption is not None:
            self.consumption = message.consumption
        if message.production is not None:
            self.production = message.production

        self.net = self.production - self.consumption
        # TODO: Then shoud update siblings

    def get_energy(self):
        return {'production': self.production,
                'consumption': self.consumption,
                'net': self.net}

    def handle_net_sync_req(self, msg):
        if msg.id not in self.node.messages:
            self.node.messages[msg.id] = msg
            self.net = self._calculate_net(msg.net)

            self.forward_message(self.net, msg)
            return self.net

    def forward_message(self, msg):
        # abc = {"type":"insecure","id":"1","name":"peter"}

        black_list_values = set(('timeStamp'))

        xyz = {k: v for k, v in abc.iteritems() if k not in black_list_values}
        xyz["identity"] = abc["id"]

        for node in self.siblings:
            requests.put(node._format_url('power'), data=msg)

    def _generate_msg(self, timeStamp, latest_net):
        return {
            'msgId': hash((timeStamp, self.id)),
            'timeStamp': timeStamp,
            'sender': self.id,
            'net': latest_net
        }

    def _calculate_net(self, other_net):
        """Returns personal net added to incoming net.

        Args:
            other_net (int): net to be added to personal net
        """
        return self.productionduction + self.consumptionsumption + other_net

    def _format_url(self, route: str):
        return f'http://{self.address}:{self.port}/{route}'

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.id == other.id
        return False

    def __hash__(self):
        return id(self.id)

    def __str__(self):
        return f'Node<name={self.name}'\
            f' production={self.production}'\
            f' consumption={self.consumption}'\
            f' net={self.net}>'
