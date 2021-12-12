from oppapi import oppapi, from_args


@oppapi
class Opt:
    a: int
    b: float
    c: str
    d: bool


def main():
    opt = from_args(Opt)
    print(opt)


# python primitive.py 10 10.0 foo True
if __name__ == "__main__":
    main()
