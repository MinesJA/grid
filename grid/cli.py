import argparse


def create_parser():
    parser = argparse.ArgumentParser(description='Start a node')
    parser.add_argument('--name', '-n')
    parser.add_argument('--id', '-i', type=int)
    parser.add_argument('--token', '-t')
    parser.add_argument('--host', '-s')
    parser.add_argument('--port', '-p', type=int)
    return parser


def parse_args(args):
    return create_parser().parse_args(args)
