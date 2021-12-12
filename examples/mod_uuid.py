from oppapi import oppapi, from_args
from uuid import UUID


@oppapi
class Opt:
    value: UUID


def main():
    opt = from_args(Opt)
    print(opt)


if __name__ == "__main__":
    main()
