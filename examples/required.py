from typing import Optional
from oppapi import from_args, oppapi, field


@oppapi
class Opt:
    port: Optional[int] = field(required=True)


def main():
    opt = from_args(Opt)
    print(opt)


if __name__ == "__main__":
    main()
