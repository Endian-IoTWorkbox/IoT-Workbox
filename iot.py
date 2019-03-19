#!/usr/bin/python3


from core import cli
from helpers import banner
import sys

if __name__ == "__main__":
    print(banner.banner() + "\n")
    if len(sys.argv) != 2:
        print("Please insert the log file path")
        sys.exit(1)

    cli = cli.Cli("main", sys.argv[1])
    try:
        cli.run()
    except KeyboardInterrupt:
        print("\n[*] Exiting..")
        sys.exit(0)
    except EOFError:
        print("\n[*] Exiting..")
        sys.exit(0)
