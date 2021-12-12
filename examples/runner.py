import sys
from typing import Optional

import simple
import primitive
import rename
import mod_datetime
import mod_ipaddress
import mod_path
import oppapi
import nargs
import choice
import required
import short_long
import subcommand

import logging


@oppapi.oppapi
class Opt:
    verbose: Optional[bool]


def cmd(s: str):
    print("--------------------------------")


def main(opt: Opt):
    sys.argv[1:] = "0.0.0.0 -p8000".split()
    simple.main()

    sys.argv[1:] = "10 10.0 foo True".split()
    primitive.main()

    sys.argv[1:] = "--bar 100".split()
    rename.main()

    sys.argv[1:] = "127.0.0.1".split()
    mod_ipaddress.main()

    sys.argv[1:] = "2021-10-23T11:11:11 -d 2021-10-23 -t 11:11:11".split()
    mod_datetime.main()

    sys.argv[1:] = "/tmp".split()
    mod_path.main()

    sys.argv[1:] = "1 2 3 --opts 10 foo 10.0 True".split()
    nargs.main()

    sys.argv[1:] = "Apple --price 20".split()
    choice.main()

    sys.argv[1:] = "-p 80".split()
    required.main()

    sys.argv[1:] = "-n 127.0.0.1".split()
    short_long.main()

    sys.argv[1:] = "Bar -a 100".split()
    subcommand.main()


if __name__ == "__main__":
    opt = oppapi.from_args(Opt)
    print(opt)
    logging.basicConfig(level=logging.DEBUG if opt.verbose else logging.INFO)
    main(opt)
