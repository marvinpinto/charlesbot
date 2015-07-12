import argparse


def parse_args(args):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-c",
        "--config",
        help="config file",
        action="store",
        dest="config",
        required=True
    )

    return parser.parse_args(args)
