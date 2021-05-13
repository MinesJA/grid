from collections import namedtuple
from uuid import uuid1, UUID
from grid.models.envelope import *
from grid.models.message import *

from grid.models.nodeProxy import NodeProxy
from grid.models.actor import Actor
from typing import Type, Callable, Sequence, Dict, Set
import asyncio


class Package:

    def __init__(self,
                 return_to: Type[Actor],
                 requests: Dict[UUID, Ask],
                 tells: Set[UUID],
                 env: Type[Envelope] = None):
        """Package represents a group of requests sent by
        a Node to it's siblings that are waiting a response.
        When they've all been responded to the Package is
        technically ready to be reduced to a single Response
        message and sent back to the return_to Node.

        Args:
            return_to (Type[Actor]): Node to send package to
                when complete
            requests (Dict[UUID, Ask]): Requests sent, pending
                a response
            ask (Ask, optional): Ask to respond to when package
                is complete. Defaults to None.
        """
        self.return_to = return_to
        self.requests = requests
        self.tells = tells
        self.env = env
        self.responses = {}

    def get_req(self, reqid: UUID) -> Ask:
        self.requests.get(reqid)

    def register_env(self, env: Type[Envelope]) -> None:
        if isinstance(env, Response):
            if env.msg is None:
                # NOTE: This request hit a branch that was
                # already processed. Does not get a response.
                self.requests.pop(env.reqid)

            self.responses.update({env.reqid: env})

        if isinstance(env, Tell):
            self.tells.add({env.reqid})

    def req_completed(self, node) -> bool:
        self.return_to == node

    def reduce(self, reducer: Callable):
        return reducer(self.responses)

    def is_ready(self) -> bool:
        """Package has had all requests addressed
        and completed.

        Returns:
            boolean: True if Package is Completed
        """
        return len(self.requests) == len(self.responses)


class MailRoom:

    def __init__(self, outbox: asyncio.Queue):
        """Keeps track of what messages are awaiting responses
        in either direction. If a message is sent by a node and needs
        a reply and if a Node needs to respond to a message it was
        sent.

        {master_reqid: Package}

        Args:
            return_id ([type]): [description]
        """
        self._outbox = outbox
        # TODO: rename to packages?
        self._req_registry = {}

    async def ask(self,
                  msg: Type[Message],
                  sender: Type[Actor],
                  recipients: Sequence[NodeProxy],
                  master_reqid: UUID = None):
        master_reqid = master_reqid or uuid1()

        requests = {}

        for node in recipients:
            ask = Ask(to=node.address,
                      msg=msg,
                      return_id=sender.id,
                      reqid=uuid1(),
                      master_reqid=master_reqid)

            requests.update({ask.reqid: ask})
            await self._outbox.put(ask)

        package = Package(sender, requests, ask)
        self._req_registry.update({master_reqid: package})

    async def tell(self,
                   msg: Type[Message],
                   sender: Type[Actor],
                   recipients: Sequence[NodeProxy],
                   master_reqid: UUID = None):
        master_reqid = master_reqid or uuid1()

        requests = {}

        for node in recipients:
            ask = Ask(to=node.address,
                      msg=msg,
                      return_id=sender.id,
                      reqid=uuid1(),
                      master_reqid=master_reqid)

            requests.update({ask.reqid: ask})
            await self._outbox.put(ask)

        package = Package(sender, requests, ask)
        self._req_registry.update({master_reqid: package})

    async def respond(self,
                      ask: Ask,
                      msg: Type[Message],
                      recipient: NodeProxy):
        resp = Response(to=recipient.address,
                        msg=msg,
                        reqid=ask.reqid,
                        master_reqid=ask.master_reqid)

        await self._outbox.put(resp)

    async def forward_tell(self, env, msgbuilder, sender):
        siblings = [s for (i, s) in sender.siblings.items()
                    if i != env.return_id]

        already_processed = self.has_package(env.master_reqid)
        should_forward = not already_processed and siblings

        if should_forward:
            await self.tell(sender=sender,
                            msg=msgbuilder(),
                            recipients=siblings,
                            master_reqid=env.master_reqid)

    async def forward_ask(self,
                          env: Type[Envelope],
                          msgbuilder: Type[Message],
                          reducer: Callable,
                          valhandler: Callable,
                          sender: Type[Actor]):
        """Forwards a particular message to entire grid.

        If first call, begins forwarding.
        If midway, continues forwarding.
        If it reaches Node that's already seen this
        master_reqid, returns None msg. If it's a
        dead end, begins retrieval process.

        Args:
            env (Type[Envelope]): [description]
            msgbuilder (Type[Message]): [description]
            reducer (Callable): [description]
            valhandler (Callable): Callback to handle final value
            sender (Node): [description]

        Raises:
            ValueError: [description]
        """
        if isinstance(env, Tell):
            await self.ask(sender=sender,
                           msg=msgbuilder(),
                           recipients=sender.siblings.values())

        elif isinstance(env, Ask):

            siblings = [s for (i, s) in sender.siblings.items()
                        if i != env.return_id]

            resp_to = sender.siblings.get(env.return_id)

            already_processed = self.has_package(env.master_reqid)
            should_forward = not already_processed and len(siblings) > 0
            dead_end = not siblings

            if should_forward:
                await self.ask(ask=env,
                               sender=self,
                               msg=msgbuilder(),
                               recipients=siblings,
                               master_reqid=env.master_reqid)
            elif already_processed:
                self.respond(ask=env, msg=None, recipient=resp_to)
            elif dead_end:
                # import pdb; pdb.set_trace()
                self.respond(ask=env,
                             recipient=resp_to,
                             msg=UpdateNet(nets=reducer({})))
            else:
                raise ValueError(
                    f'{sender.address}: Something bad happend in Ask')

        elif isinstance(env, Response):

            package = self._get_package(env.master_reqid)
            package.register_env(env)

            if env.msg is None:
                print(f'Received a response from a dead end')

            if package.is_ready():
                msg = package.reduce(reducer)
                if package.req_completed(sender):
                    valhandler(msg)
                else:
                    self.respond(ask=package.og_ask,
                                 recipient=package.return_to,
                                 msg=msg)

    def close_req(self, resp):
        self._get_package(resp.master_reqid).register_env(resp)

    def has_package(self, master_reqid) -> bool:
        return self._get_package(master_reqid) is not None

    def _get_req(self, resp) -> Ask:
        return self._get_package(resp.master_reqid).get_req(resp.reqid)

    def _get_package(self, master_reqid) -> Package:
        package = self._req_registry.get(master_reqid)
        return package

        """
        handle: Ask-and-respond
        handle: forward-ask
        handle: forward-tell
        """
