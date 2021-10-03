import argparse
from dotenv import load_dotenv
from grid.app import start_application
import sys


def create_parser():
    parser = argparse.ArgumentParser(description='Start a node')
    subparsers = parser.add_subparsers(help='run help')
    create_run_parser(subparsers)
    create_account_parser(subparsers)
    return parser


def create_run_parser(subparsers):
    """Create the run command subparser.

    TODO: Should be able to create new address and run
    with it?
    TODO: Do we need token?
    parser.add_argument('--token', '-t', )

    Args:
        subparsers ([type]): [description]
    """

    parser = subparsers.add_parser('run', help='run help')

    parser.add_argument('--host', '-s',
                        help='Host address of Node')

    parser.add_argument('--port', '-p',
                        help='Port of node')

    parser.add_argument('--name', '-n',
                        help='Name of Node')

    parser.add_argument('--id', '-i',
                        help='Id of Node')

    parser.add_argument('--address', '-a',
                        help='Public key of Solana wallet address of Node')
    parser.parser.set_defaults(func=start_application)


def create_account_parser(subparsers):
    """Create the account command subparser.

    Args:
        subparsers ([type]): [description]
    """
    parser = subparsers.add_parser('account', help='account help')

    parser.add_argument('--address', '-a',
                        type='string',
                        help='Public key of Solana wallet address')

    parser.add_argument('--create', '-c',
                        action='store_true',
                        default=False,
                        help='generate new keypair')
    parser.set_defaults(func=account)


def parse_args(args):
    return create_parser().parse_args(args)


def run_cli(args):
    namespace = parse_args(args)
    namespace.func(args)


if __name__ == "__main__":
    load_dotenv()
    run_cli(sys.arv[1:])
