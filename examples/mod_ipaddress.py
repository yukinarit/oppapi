from oppapi import oppapi, from_args
from ipaddress import IPv4Address
from typing import Optional


@oppapi
class Opt:
    """
    Option parser using oppapi
    """

    ip: IPv4Address
    """ Primary IP Address """

    secondary_ip: Optional[IPv4Address]
    """ Secondary IP Address """


def main():
    opt = from_args(Opt)
    print(opt)


# python mod_ipaddress.py 127.0.0.1
if __name__ == "__main__":
    main()
