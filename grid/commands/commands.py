from grid.envelopes import *
from grid.messages import *
from grid.models.nodeProxy import NodeProxy
from grid.app import (SOLANA_CLIENT_URL, Account,
                      AsyncClient, PublicKey,
                      Transaction, AccountMeta,
                      TransactionInstruction)


# TODO: Need docs for these commands

async def addsibling_cmd(mailroom, node, env):
    siblings = node.siblings
    msg = env.msg
    sibling = NodeProxy(msg.sibling_id,
                        msg.sibling_name,
                        msg.sibling_address)

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

        # TODO: Can remove this if we're goin clockcycle route
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
        # TODO: This is a strange way to do things...
        #   Using the fact that forward_response returns a msg
        #   if it doesn't actually need to forward the response
        #   to determine whether to end it here or not (forward_response)
        #   will return nothing if it doesn't

        msg = await mailroom.forward_response(resp=env, sender=node)
        if msg is not None:

            gridnet = sum(msg.nets.values())
            # TODO: This isn't safe. Node net may have changed from
            #   the moment of timestamp. Need to think of better way
            #   to do this.
            nodenet = node.net

            node.update_gridnet(gridnet)

            data_packet = {
                'gridnet': node.gridnet,
                'nodenet': node.net,
                'timestamp': env.timestamp
            }

            # Start the Solana Transaction process here
            async with AsyncClient(SOLANA_CLIENT_URL) as client:
                await client.is_connected()

                # TODO: Need to figure out keypair storage
                #   Best guess is storing it per machine in environment vars
                #   Or would get from registering the account initially?
                # https://michaelhly.github.io/solana-py/solana.html?highlight=keypair#solana.account.Account.keypair
                node_acct = Account('Keypair of Node')

                # TODO: This is another thing the Node should just know
                #   Should know how how to access the main Smart Contract
                #   Could make Smart Contract specific to Grid instance.
                #   For example, when you add a sibling, you get the program_id
                #   indicating you're part of the grid, all calling the same
                #   contract as your neighbors
                prog_pubkey = PublicKey('Programs PublicKey')

                acct_meta = AccountMeta(
                    pubkey=node_acct.public_key(),
                    is_signer=False,
                    is_writable=True
                )

                instruction = TransactionInstruction(
                    keys=[acct_meta],
                    data=data_packet,
                    program_id=prog_pubkey
                )

                client.send_transaction(
                    Transaction().add(instruction),
                    node_acct
                    # {'skip_confirmation': False} TODO: Do we need this?
                )
