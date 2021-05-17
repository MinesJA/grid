from grid.envelopes import *
from grid.messages import *
from grid.models.nodeProxy import NodeProxy


async def addsibling_cmd(mailroom, node, env):
    siblings = node.siblings
    msg = env.msg
    sibling = NodeProxy(msg.sibling_id,
                        msg.sibling_name, msg.sibling_address)

    if isinstance(env, Tell) and sibling.id not in siblings:
        msg = AddSibling.with_node(node)

        await mailroom.ask(msg=msg,
                           sender=node,
                           recipients=[sibling])

    elif isinstance(env, Ask) and sibling.id not in siblings:
        node.add_sibling(sibling)

        await mailroom.respond(ask=env,
                               msg=AddSibling.with_node(node),
                               sender=node)

    elif isinstance(env, Response) and sibling.id not in siblings:
        node.add_sibling(sibling)
        mailroom.close_package(env)

        await mailroom.ask(msg=UpdateNet(),
                           sender=node,
                           recipients=siblings.values())

        await mailroom.tell(msg=SyncGrid(),
                            sender=node,
                            recipients=siblings.values())


async def syncgrid_cmd(mailroom, node, env):
    # TODO: Never close package....need to make sure it gets closed
    if isinstance(env, Tell):
        if not mailroom.is_registered(env):
            siblings = node.siblings.values()
            await mailroom.ask(msg=UpdateNet(),
                               sender=node,
                               recipients=siblings)

            await mailroom.forward_tell(env, node)


async def updateenergy_cmd(mailroom, node, env):
    msg = env.msg
    siblings = node.siblings.values()

    if isinstance(env, Tell):
        node.update_energy((msg.production, msg.consumption))

        if len(siblings) <= 0:
            node.update_gridnet(msg.production-msg.consumption)

        await mailroom.ask(msg=UpdateNet(),
                           sender=node,
                           recipients=siblings)

        await mailroom.tell(msg=SyncGrid(),
                            sender=node,
                            recipients=siblings)


async def updatenet_cmd(mailroom, node, env):
    if isinstance(env, Tell):
        siblings = node.siblings.values()
        await mailroom.ask(sender=node,
                           msg=UpdateNet(),
                           recipients=siblings)

    elif isinstance(env, Ask):
        await mailroom.forward_ask(ask=env,
                                   sender=node)

    elif isinstance(env, Response):
        msg = await mailroom.forward_response(resp=env, sender=node)
        if msg is not None:
            node.update_gridnet(sum(msg.nets.values()))
