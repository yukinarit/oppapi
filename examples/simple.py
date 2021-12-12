from typing import Optional

from oppapi import from_args, oppapi


@oppapi
class Opt:
    """
    Option parser using oppapi
    """

    host: str
    """ This will be positional argument of type `str` """

    port: Optional[int] = 8000
    """ Optional argument will be option argument """


def main():
    opt = from_args(Opt)
    print(opt)


# python simple.py 0.0.0.0 -p 8000
if __name__ == "__main__":
    main()
