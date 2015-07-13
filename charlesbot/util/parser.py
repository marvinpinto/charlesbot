import argparse
import sys
from contextlib import contextmanager
from io import StringIO


def parse_args(args):
    parser = argparse.ArgumentParser(
        description="CharlesBOT is a Slack RTM robot!",
        epilog="See https://github.com/marvinpinto/charlesbot for details"
    )
    return parser.parse_args(args)


@contextmanager
def capture_sys_output():
    caputure_out, capture_err = StringIO(), StringIO()
    current_out, current_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = caputure_out, capture_err
        yield caputure_out, capture_err
    finally:
        sys.stdout, sys.stderr = current_out, current_err
