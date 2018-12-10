#!/usr/bin/python3


from core import cli
from helpers import banner
import sys

if __name__ == "__main__":
    print(banner.banner() + "\n")
    cli = cli.Cli("main")
    try:
        cli.run()
    except KeyboardInterrupt:
        sys.exit(0)

