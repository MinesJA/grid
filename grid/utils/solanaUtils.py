import os
from solana.rpc.async_api import AsyncClient
from solana.publickey import PublicKey
from solana.account import Account
from solana.transaction import Transaction, TransactionInstruction, AccountMeta

SOLANA_CLIENT_URL = os.environ.get('SOLANA_DEVNET_URL')


async def transact(data):
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
            data=data,
            program_id=prog_pubkey
        )

        client.send_transaction(
            Transaction().add(instruction),
            node_acct
            # {'skip_confirmation': False} TODO: Do we need this?
        )
