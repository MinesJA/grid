from grid.envelopes import Tell, Ask, Response
from grid.models.actor import Actor
from grid.messages import Message
from grid.utils.utils import values_except
from functools import partial
from uuid import uuid1
from collections.abc import Sequence


async def tell(msg: Message,
               sender: Actor,
               recipients: Sequence[Actor] = None):
    recipients = recipients or sender.siblings
    tell_builder = partial(Tell, msg=msg, master_reqid=uuid1())
    _tell(recipients, tell_builder, sender)


async def forward_tell(tell: Tell,
                       sender: Actor,
                       recipients: Sequence[Actor] = None):
    recipients = recipients or values_except(sender.siblings, tell.return_id)
    tell_builder = partial(Tell, msg=tell.msg, master_reqid=tell.master_reqid)
    _tell(recipients, tell_builder, sender)


async def ask(msg: Message,
              sender: Actor,
              recipients: Sequence[Actor] = None):
    recipients = recipients or sender.siblings
    ask_builder = partial(Ask, msg=msg, master_reqid=uuid1())
    _ask(recipients, ask_builder, sender)


async def forward_ask(ask: Ask,
                      sender: Actor,
                      recipients: Sequence[Actor] = None):
    recipients = recipients or values_except(sender.siblings, ask.return_id)

    if mailroom.should_forward(ask, recipients):
        ask_builder = partial(Ask,
                              msg=ask.msg,
                              master_reqid=ask.master_reqid)
        await _ask(recipients, ask_builder, sender)
    else:
        msg = mailroom.gen_return_msg(ask, sender)
        await _respond(ask, msg, sender)


async def respond(ask: Ask,
                  msg: Message,
                  sender: Actor):
    resp = ask.build_response(msg, sender)
    await outbox.put(resp)


async def forward_response(resp: Response,
                           sender: Actor):
    package = mailroom._get_package(resp.master_reqid)

    if not package.is_ready():
        raise RuntimeError(f'Package {resp.master_reqid} is not ready to ship')

    msg = package.gen_msg(sender, resp)

    mailroom.reduce_package()

    await respond(package.org_env, msg, sender)

    # TODO:
    if package.is_ready():

        if package.req_completed():
            mailroom.close_package(resp)
            return msg
        else:


async def _tell(recipients: Sequence[Actor],
                tell_builder: partial[str],
                sender: Actor):
    # TODO: Could abstrat _tell and _ask
    for recipient in recipients:
        tell = tell_builder(recipient.address, sender.id, uuid1())
        await outbox.put(tell)


async def _ask(recipients: Sequence[Actor],
               ask_builder: partial[str],
               sender: Actor):
    for recipient in recipients:
        ask = ask_builder(recipient.address, sender.id, uuid1())
        await outbox.put(ask)
