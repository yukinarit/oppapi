from typing import Optional

from oppapi import from_args, oppapi, field


@oppapi
class Opt:
    host: Optional[str] = field(short="-n", long="--hostname")


def main():
    opt = from_args(Opt)
    print(opt)


# python simple.py 0.0.0.0 -p 8000
if __name__ == "__main__":
    main()
