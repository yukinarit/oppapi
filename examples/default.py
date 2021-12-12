from typing import Optional

from oppapi import from_args, oppapi


@oppapi
class Opt:
    """
    Option parser using oppapi
    """

    host: str = "127.0.0.1"
    """ Primitive type will be positional argument """

    port: Optional[int] = 8000
    """ Optional type will be option argument """


def main():
    opt = from_args(Opt)
    print(opt)


# python simple.py 0.0.0.0 -p 8000
if __name__ == "__main__":
    main()
