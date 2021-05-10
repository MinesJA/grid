from collections import namedtuple
from uuid import uuid1, UUID
from grid.models.envelope import *
from grid.models.message import *
from grid.models.node import Node
from grid.models.actor import Actor
import asyncio


class Package:

    def __init__(self, return_to: Actor, requests: dict, og_ask: Ask = None):
        self.return_to = return_to
        self.requests = requests
        self.og_ask = og_ask
        self.responses = {}

    def get_req(self, req_id: UUID):
        self.requests.get(req_id)

    def resgister_resp(self, resp: Response):
        if resp.msg is None:
            self.requests.pop(resp.req_id)

        self.responses.update({resp.req_id: resp})

    def register_req(self, ask: Ask):
        self.requests.update({ask.req_id: ask})

    def is_completed(self):
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

        {master_req_id: Package}

        Args:
            return_id ([type]): [description]
        """
        self._outbox = outbox
        self._req_registry = {}

    async def forward_ask(self,
                          og_ask: Ask,
                          sender: Actor,
                          msg: Message,
                          recipients: list):
        requests = {}

        for node in recipients:
            ask = Ask(to=node.address,
                      msg=msg,
                      return_id=sender.id,
                      req_id=uuid1(),
                      master_req_id=og_ask.master_req_id)
            requests.update({ask.req_id: ask})
            await self._outbox.put(ask)

        return_to = sender.siblings.get(og_ask.return_id)

        package = Package(return_to, requests, og_ask)
        self._req_registry.update({og_ask.master_req_id: package})

    async def ask(self, msg, sender, recipients):
        master_req_id = uuid1()

        requests = {}

        for node in recipients:
            ask = Ask(to=node.address,
                      msg=msg,
                      return_id=sender.id,
                      req_id=uuid1(),
                      master_req_id=master_req_id)
            requests.update({ask.req_id: ask})
            await self._outbox.put(ask)

        package = Package(sender, requests)
        self._req_registry.update({master_req_id: package})

    # TODO: Should probably be called complete response...
    async def package_response(self, og_resp, msg):
        package = self._get_package(og_resp)
        responses = package.responses.values()

        await self.respond(ask=package.og_ask,
                           recipient=?????,
                           msg=msg)

        # TODO: Should probably close out package here

    async def respond(self, ask, recipient, msg):
        resp = Response(to=recipient.address,
                        msg=msg,
                        req_id=ask.req_id,
                        master_req_id=ask.master_req_id)

        await self.outbox.put(resp)

    async def forward_all(self, env, gen_msg, sender: Node):
        """Forwards a particular message to entire
        grid. If it's midway, continues, if it's
        the end, returns back. If it's the beginning,
        starts.

        Args:
            env (Envelope): envelope
        """
        if isinstance(env, Tell):
            await self.ask(msg=gen_msg(env, sender),
                           sender=sender,
                           recipients=sender.siblings.values())

        elif isinstance(env, Ask):
            siblings = [s for (i, s) in sender.siblings.items()
                        if i != env.return_id]

            resp_to = sender.siblings.get(env.return_id)

            already_processed = self.has_package(env.master_req_id)
            should_forward = not already_processed and siblings
            dead_end = not siblings

            if should_forward:
                await self.forward_ask(og_ask=env,
                                       sender=self,
                                       msg=gen_msg(env, sender),
                                       recipients=siblings)
            elif already_processed:
                self.respond(ask=env, recipient=resp_to, msg=None)
            elif dead_end:
                self.respond(ask=env,
                             recipient=resp_to,
                             msg=gen_msg(env, sender))
            else:
                raise ValueError(
                    f'{sender.address}: Something bad happend in Ask')

        elif isinstance(env, Response):
            self.close_req(env)

            package_ready = self.package_ready(env.master_req_id)
            is_complete = self.msg_returned(env.master_req_id, self)

            if env.msg is None:
                print(f'Received a response from a dead end')
            elif is_complete:
                self.gridnet = sum(self.net, env.msg.nets.values())
            elif package_ready:
                self.package_response(env, gen_msg(env, sender))
            else:
                raise ValueError(f'{self.address}: Something has gone \
                wrong in Response handling')

    def close_req(self, resp):
        self._get_package(resp.master_req_id).register_resp(resp)

    def package_ready(self, master_req_id):
        self._get_package(master_req_id).is_completed()

    def msg_returned(self, master_req_id, node):
        self._get_package(master_req_id)._return_id == node.id

    def has_package(self, master_req_id):
        return self._get_package(master_req_id) is not None

    def _get_req(self, resp):
        return self._get_package(resp.master_req_id).get_req(resp.req_id)

    def _get_package(self, master_req_id):
        package = self._req_registry.get(master_req_id)
        if package is None:
            raise ValueError("No Package exists for this master request id")
        return package


#   # TODO: START Revisit these methods
#     def register_master_req(self, ask):
#         package = Package(ask.return_id, {ask.master_req_id: ask})
#         self._req_registry.update({ask.master_req_id: package})

#     def register_req(self, ask):
#         package = self._req_registry.get(ask.master_req_id)
#         package.add_req(ask)

#     def register_resp(self, resp):
#         self._get_package(resp.master_req_id).register_resp(resp)
#     # END


# # TODO: Need to rename this
#     async def forward_update(self,
#                              master_req_id=None,
#                              return_id=None,
#                              siblings=None):


#         Args:
#             req_id (uuid1): original request id
#             siblings (list(NodeProxy), optional): list siblings.
#                 Defaults to None.
#         """
#         siblings = siblings if siblings else self.siblings.values()
#         return_id = return_id if return_id else self.id
#         master_req_id = master_req_id if master_req_id else uuid1()

#         mail_distr = MailDistr(return_id)

#         for sibling in siblings:
#             req_id = uuid1()
#             ask_env = Ask(to=sibling.address,
#                           msg=UpdateNet(),
#                           return_id=self.id,
#                           req_id=req_id,
#                           master_req_id=master_req_id)
#             mail_distr.update_awaiting(req_id, ask_env)

#             await self.outbox.put(ask_env)

#         self.mail_routing.update({master_req_id: mail_distr})
