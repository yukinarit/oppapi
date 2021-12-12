from oppapi import oppapi, field, from_args


@oppapi
class Nested:
    c: float
    d: bool


@oppapi
class Opt:
    a: int
    b: str
    bar: Nested = field(metadata={'serde_flatten': True})


def main():
    opt = from_args(Opt)
    print(opt)


if __name__ == '__main__':
    main()
