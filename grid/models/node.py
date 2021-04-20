from datetime import datetime
from uuid import uuid1
from collections import defaultdict
from grid.models.nodeProxy import NodeProxy
from grid.models.actor import Actor
from grid.models.message import AddSibling, UpdateNet, UpdateEnergy
from grid.models.envelope import Envelope


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
        self.pending_replies = defaultdict({})
        self.production = production
        self.consumption = consumption

        self._net = production - consumption

    @property
    def net(self):
        print('Getting net')
        self.net

    @net.setter
    def net(self, net):
        print('Setting net')
        self._net = net

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

    async def add_sibling(self, envelope):
        """Adds a sibling NodeProxy to siblings. Then sends
        tell message AddSibling with it's own info to maintain
        a bidirectional graph. Then sends a request to update
        the grids net output.

        Args:
            sibling (Node): node sibling instance
        """
        msg, recip_id = envelope

        if msg.sibling_id not in self.siblings:
            sibling = NodeProxy(id=msg.sibling_id,
                                name=msg.sibling_name,
                                address=msg.sibling_address)

            self.siblings.update({sibling.id: sibling})

            if recip_id:
                sibling.tell(
                    AddSibling(
                        id=uuid1(),
                        timestamp=datetime(),
                        sibling_id=self.id,
                        sibling_name=self.name,
                        sibling_address=self.address)
                )
            else:
                # NOTE: Only update grid once the reciprocal
                # relationship has been established to prevent
                # sending an additional unnecessary update request
                self.update_network(sender_id=self.id, req_id=uuid1())

    def update_network(self, sender_id, req_id, siblings=None):
        """Nodes send out an update message to each of their siblings which
        have not already sent an update message (to prevent forwarding
        backwards). Nodes keep track of pending replies tracking both the 
        original request id as well as the envelope id from forwarding message:

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
            sender_id ([type]): [description]
            siblings ([type], optional): [description]. Defaults to None.
        """
        siblings = siblings if siblings else self.siblings
        for sibling in siblings.values():
            msg = UpdateNet(id=uuid1(), sender_id=sender_id, req_id=req_id)
            envelope = Envelope(env_id=uuid1(),
                                message=msg,
                                reply_to=self.id)
            self.pending_replies[req_id].update({envelope.id: envelope})
            sibling.ask(envelope)

    def update_net(self, envelope):
        """Update net by collecting net values
        of entire grid and summing them up.

        Args:
            envelope (Envelope): envelope
        """
        reply_to_node = self.siblings.get(envelope.reply_to)
        pending_envelopes = self.pending_replies.get(envelope.msg.req_id)

        if reply_to_node and not pending_envelopes:
            # 1. This is an Ask request from an established sibling
            # 2. This request has not been processed before

            # Don't forward back the way it came
            sibs = [s for s in self.siblings if s.id is not envelope.reply_to]
            self.update_network(envelope.msg.sender_id,
                                envelope.msg.req_id, sibs)

        elif reply_to_node and pending_envelopes:
            # 1. This is an Ask request from an established sibling
            # 2. This message has already been processed
            # Respond with a tell reusing the Ask envelope_id

            resp_msg = UpdateNet(id=uuid1(),
                                 sender_id=envelope.msg.sender_id,
                                 req_id=envelope.msg.req_id,
                                 nets={self.id: 0})
            new_env = Envelope(env_id=envelope.id,
                               message=envelope.msg,
                               resp_msg=resp_msg)
            reply_to_node.tell(envelope=new_env)

        elif not envelope.reply_to and pending_envelopes:
            # 1. This is a Tell request
            # 2. There is potentially a pending envelope to repsond to
            # Replace the existing Envelope with the new Envelope.
            # If all messages have been responded to, send the entire
            # package back down

            pending_env = pending_envelopes.get(envelope.id)
            if pending_env.resp_msg:
                # If there is already a response
                # something has gone wrong....
                raise ValueError('Should not be a response in envelope')

            if not pending_env:
                # If there is not a pending envelope
                # something has gone wrong....
                raise ValueError('Should be a pending reply for this tell')

            # Update the pending_replies with incoming envelope
            # which should have the resp_obj
            self.pending_replies[envelope.msg.req_id].update(
                {envelope.id: envelope})

            # Check to see if all pending_envelopes have been responded
            # to

            unanswered = [pend_env for pend_env
                          in self.pending_replies[envelope.msg.req_id].values()
                          if not pend_env.resp_msg]

            if not unanswered:
                # If all pending_envelopes now have resp_msgs
                # package all nets and respond to reply_to with data

                compiled_nets = {self.id: self.production - self.consumption}

                for pend_env in pending_envelopes.values():
                    compiled_nets.update(pend_env.resp_msg.nets)

                resp_msg = UpdateNet(id=uuid1(),
                                     req_id=envelope.msg.req_id,
                                     sender_id=envelope.msg.sender_id,
                                     nets=compiled_nets)
                new_env = Envelope(env_id=envelope.id,
                                   message=envelope.msg,
                                   resp_msg=resp_msg)

            reply_to_node.tell(envelope=new_env)

        elif envelope.reply_to is None and env_id not in self.envelopes:
            # 1. This is a Tell
            # 2. 

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

    def update_network(self):
        now = time.time()
        data = {
            'msgId': hash((now, self.id)),
            'sender': self.id,
            'timeStamp': now,
            'net': self.net
        }
        for node in self.siblings.values():
            requests.put(node._format_url('net'), data=data)

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
