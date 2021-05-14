from uuid import uuid1, UUID
from grid.envelopes import *
from grid.messages import *
from grid.models.nodeProxy import NodeProxy
from grid.models.actor import Actor
from typing import Type, Sequence, Dict
import asyncio


class Package:

    def __init__(self,
                 return_to: Type[Actor],
                 requests: Dict[UUID, Type[Envelope]],
                 env: Type[Envelope]):
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
        self.env = env
        self.responses = {}

    def get_req(self, reqid: UUID) -> Type[Envelope]:
        self.requests.get(reqid)

    def register_env(self, env: Type[Envelope]) -> None:
        if isinstance(env, Response):
            if env.msg is None:
                # NOTE: This request hit a branch that was
                # already processed. Does not get a response.
                self.requests.pop(env.reqid)
            else:
                self.responses.update({env.reqid: env})
        else:
            self.request.update({env.reqid: env})

    def req_completed(self, node) -> bool:
        self.return_to == node

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
                   recipients: Sequence[NodeProxy]):
        master_reqid = uuid1()

        requests = {}

        for node in recipients:
            tell = Tell(to=node.address,
                        msg=msg,
                        return_id=sender.id,
                        reqid=uuid1(),
                        master_reqid=master_reqid)

            requests.update({tell.reqid: tell})
            await self._outbox.put(tell)

        package = Package(sender, requests, tell)
        self._req_registry.update({master_reqid: package})

    async def respond(self,
                      ask: Ask,
                      msg: Type[Message],
                      sender: Type[Actor]):
        await self._outbox.put(Response.to_ask(ask, msg, sender))

    async def forward_tell(self, env, sender):
        siblings = [s for (i, s) in self.node.siblings.items()
                    if i != self.env.return_id]

        already_processed = self.is_registered(env.master_reqid)
        should_forward = not already_processed and siblings

        if should_forward:
            await self.tell(sender=sender,
                            msg=env.message,
                            recipients=siblings,
                            master_reqid=env.master_reqid)

    async def forward_ask(self,
                          env: Type[Envelope],
                          sender: Type[Actor]):

        siblings = [s for (i, s) in sender.siblings.items()
                    if i != env.return_id]

        already_processed = self.has_package(env.master_reqid)
        should_forward = not already_processed and len(siblings) > 0
        dead_end = not siblings

        if should_forward:
            await self.ask(ask=env,
                           sender=sender,
                           msg=env.msg,
                           recipients=siblings,
                           master_reqid=env.master_reqid)
        elif already_processed:
            self.respond(ask=env, msg=None, sender=sender)
        elif dead_end:
            self.respond(ask=env,
                         msg=env.msg.reduce(sender, {}),
                         sender=sender)
        else:
            raise ValueError(
                f'{sender.address}: ForwardAsk was not able to handle request')

    async def forward_response(self,
                               env: Type[Envelope],
                               sender: Type[Actor]):
        package = self._get_package(env.master_reqid)
        package.register_env(env)

        if env.msg is not None and package.is_ready():
            msg = env.msg.reduce(sender, package.responses)
            if package.req_completed(sender):
                return msg
            else:
                self.respond(ask=package.env,
                             msg=msg,
                             sender=sender)

    def register_env(self, resp):
        package = self._get_package(resp.master_reqid)

        package.register_env(resp)

    def is_registered(self, env):
        return self._get_package(env.master_reqid) is not None

    def close_package(self, env: Type[Envelope]):
        self._req_registry.pop(env.master_reqid)

    def _get_req(self, resp) -> Ask:
        return self._get_package(resp.master_reqid).get_req(resp.reqid)

    def _get_package(self, master_reqid) -> Package:
        package = self._req_registry.get(master_reqid)
        return package
