from oppapi import oppapi, from_args
from pathlib import Path


@oppapi
class Opt:
    """
    Option parser using oppapi
    """

    path: Path
    """ Primitive type will be positional argument """


def main():
    opt = from_args(Opt)
    print(opt)


if __name__ == "__main__":
    main()
