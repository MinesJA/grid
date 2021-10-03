from grid.models.mailRoom import Mailroom
from uuid import uuid1
from grid.envelopes import Envelope, Tell, Ask, Response
from grid.messages import Message
from grid.models.nodeProxy import NodeProxy
from grid.models.actor import Actor
from typing import Type, Sequence, Dict


class Executor:

    def __init__(self, outbox):
        self.mailroom = Mailroom()
        self._outbox = outbox


    async def execute(self):
        

    async def tell(self,
                   msg: Type[Message],
                   sender: Type[Actor],
                   recipients: Sequence[NodeProxy]):
        await self._tell(recipients, sender, msg, uuid1())

   

   

    async def respond(self,
                      ask: Ask,
                      msg: Type[Message],
                      sender: Type[Actor]):
        await self._outbox.put(Response.to_ask(ask, msg, sender))

    async def forward_response(self,
                               resp: Response,
                               sender: Type[Actor]):

        # 1. Register
        package = self.mailroom.register_env(resp)
        # 2. Check if ready
        # 3. Check if request is completed

        if package.is_ready():
            msg = package.gen_msg(sender, resp)
            if package.req_completed():
                self.close_package(resp)
                return msg
            else:
                await self.respond(ask=package.org_env,
                                   msg=msg,
                                   sender=sender)

    def should_forward(self, resp: Response):
        package = self._get_package(resp.master_reqid)
        package.is_ready()
