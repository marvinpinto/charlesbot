import argparse


def parse_args(args):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--debug",
        help="debug logging",
        action="store_true",
        dest="debug",
        default=False
    )

    parser.add_argument(
        "-c",
        "--config",
        help="config file",
        action="store",
        dest="config",
        default=""
    )

    return parser.parse_args(args)
