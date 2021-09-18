from uuid import uuid1, UUID
from grid.envelopes import *
from grid.messages import *
from grid.models.nodeProxy import NodeProxy
from grid.models.actor import Actor
from typing import Type, Sequence, Dict
import asyncio


class Package:

    def __init__(self,
                 requests: Dict[UUID, Type[Envelope]],
                 org_env: Type[Envelope] = None):
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
            org_env (Type[Envelope], optional): Original envelope that
                triggered package. If none, then this Package began with
                initial request. Defaults to None.
        """
        self.requests = requests
        self.org_env = org_env
        self.responses = {}

    def gen_msg(self, sender, resp):
        """Packages up responses according to reduce of original
        request.

        Args:
            sender ([type]): [description]

        Raises:
            ValueError: [description]

        Returns:
            [type]: [description]
        """
        if not self.is_ready():
            raise ValueError('{self.org_env} Package is not ready to ship')

        return resp.msg.reduce(self.responses, sender)

    def get_req(self, reqid: UUID) -> Type[Envelope]:
        self.requests.get(reqid)

    def register_env(self, env: Type[Envelope]) -> None:
        if isinstance(env, Response):
            self.responses.update({env.reqid: env})
        else:
            self.requests.update({env.reqid: env})

    def req_completed(self) -> bool:
        return self.org_env is None

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
        self._packages = {}

    # TODO: Refactor the Tell's and Askss
    # Lot of unnecessary stuff going on

    async def ask(self,
                  msg: Type[Message],
                  sender: Type[Actor],
                  recipients: Sequence[NodeProxy]):
        await self._ask(recipients, sender, msg, uuid1())

    async def forward_ask(self,
                          ask: Ask,
                          sender: Type[Actor]):
        siblings = [s for (i, s) in sender.siblings.items()
                    if i != ask.return_id]

        already_processed = self.is_registered(ask)
        should_forward = not already_processed and len(siblings) > 0
        dead_end = len(siblings) <= 0

        if should_forward:
            await self._ask(siblings, sender, ask.msg, ask.master_reqid, ask)

        elif already_processed or dead_end:
            # TODO: Convoluted. Refactor. dead_end means collect nodes value
            # already_processed means send back empty data. Should be clearer
            node = sender if not already_processed else None
            msg = ask.msg.reduce({}, node)
            await self.respond(ask=ask, msg=msg, sender=sender)
        else:
            raise ValueError(
                f'{sender.address}: ForwardAsk was not able to handle request')

    async def _ask(self, recipients, sender, msg, master_reqid, org_env=None):
        requests = {}

        for node in recipients:
            new_ask = Ask(to=node.address,
                          msg=msg,
                          return_id=sender.id,
                          reqid=uuid1(),
                          master_reqid=master_reqid)

            requests.update({new_ask.reqid: new_ask})
            await self._outbox.put(new_ask)

        self._register(requests, master_reqid, org_env)

    async def tell(self,
                   msg: Type[Message],
                   sender: Type[Actor],
                   recipients: Sequence[NodeProxy]):
        await self._tell(recipients, sender, msg, uuid1())

    async def forward_tell(self, tell, sender):
        siblings = [s for (i, s) in sender.siblings.items()
                    if i != tell.return_id]

        if len(siblings) > 0 and not self.is_registered(tell):
            await self._tell(siblings, sender, tell.msg,
                             tell.master_reqid, tell)

    async def _tell(self, recipients, sender, msg, master_reqid, env=None):
        requests = {}
        for node in recipients:
            new_tell = Tell(to=node.address,
                            msg=msg,
                            return_id=sender.id,
                            reqid=uuid1(),
                            master_reqid=master_reqid)

            requests.update({new_tell.reqid: new_tell})
            await self._outbox.put(new_tell)

        self._register(requests, master_reqid, env)

    async def respond(self,
                      ask: Ask,
                      msg: Type[Message],
                      sender: Type[Actor]):
        await self._outbox.put(Response.to_ask(ask, msg, sender))

    async def forward_response(self,
                               resp: Response,
                               sender: Type[Actor]):
        package = self._get_package(resp.master_reqid)
        package.register_env(resp)

        if package.is_ready():
            msg = package.gen_msg(sender, resp)
            if package.req_completed():
                self.close_package(resp)
                return msg
            else:
                await self.respond(ask=package.org_env,
                                   msg=msg,
                                   sender=sender)

    def should_forward(self,
                       resp: Response):
        package = self._get_package(resp.master_reqid)
        package.is_ready()

    def _register(self, requests, master_reqid, org_env=None):
        package = Package(requests, org_env)
        self._packages.update({master_reqid: package})

    def is_registered(self, env):
        return self._get_package(env.master_reqid) is not None

    def close_package(self, env: Type[Envelope]):
        self._packages.pop(env.master_reqid)

    def _get_req(self, resp) -> Ask:
        return self._get_package(resp.master_reqid).get_req(resp.reqid)

    def _get_package(self, master_reqid) -> Package:
        package = self._packages.get(master_reqid)
        return package
