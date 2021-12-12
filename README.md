# `oppapī`

*Ergonomic option parser on top of [dataclasses](https://docs.python.org/3/library/dataclasses.html), inspired by [structopt](https://github.com/TeXitoi/structopt).*

<p align="center">
  <img src="logo.png" width=25% />
</p>

## Usage

```python
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

opt = from_args(Opt)
print(opt)
```

The code above generates such option parser that
* Generates parser description from class's docstring
* Generates argument description from field's docstring
* A field will be a positional argument
* An optional field will be an optional argument

See the parser help message:

```
$ python simple.py -h
usage: simple.py [-h] [-p PORT] host

Option parser using oppapi

positional arguments:
  host                  This will be positional argument of type `str`

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Optional argument will be option argument
```

Running the program deserializes the command line arguments into an object of the declared class.

```
$ python simple.py localhost -p 20000
Opt(host='localhost', port=20000)
```

## Supported types

* Primitives (`int`, `float`, `str`, `bool`)
* Containers (`List`, `Tuple`)
* [`typing.Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)
* [`Enum`](https://docs.python.org/3/library/enum.html#enum.Enum) and [`IntEnum`](https://docs.python.org/3/library/enum.html#enum.IntEnum)
* [`datetime`](https://github.com/yukinarit/oppapi/blob/main/examples/mod_datetime.py)
* [`decimal`](https://github.com/yukinarit/oppapi/blob/main/examples/mod_decimal.py)
* [`ipaddress`](https://github.com/yukinarit/oppapi/blob/main/examples/mod_ipaddress.py)
* [`pathlib`](https://github.com/yukinarit/oppapi/blob/main/examples/mod_path.py)
* [`uuid`](https://github.com/yukinarit/oppapi/blob/main/examples/mod_uuid.py)


## `short`/`long`

`oppapi` generates flag names automatically, but you can specify arbitrary short/long names.

```python
from typing import Optional
from oppapi import from_args, oppapi, field

@oppapi
class Opt:
    host: Optional[str] = field(short="-n", long="--hostname")
```

## `enum`

`enum.Enum` and `enum.IntEnum` will be an argument with [choices](https://docs.python.org/3/library/argparse.html#choices) parameter.

```python
class Food(Enum):
    A = "Apple"
    B = "Beer"
    C = "Chocolate"

class Price(IntEnum):
    A = 10
    B = 20
    C = 30

@oppapi
class Opt:
    food: Food
    price: Optional[Price]
```

usage will be like this:
```
positional arguments:
  {Apple,Beer,Chocolate}

optional arguments:
  -h, --help            show this help message and exit
  -p {10,20,30}, --price {10,20,30}
```

oppapi converts the command line arguments back to Enum.

```python
$ python choice.py Apple --price 20
Opt(food=<Food.A: 'Apple'>, price=<Price.B: 20>)
```

## `List`/`Tuple`

`List` will be an arbitrary number of arguments (`nargs="+"`). `Tuple` will be a fixed number of arguments (`nargs=NUM`).

```python
@oppapi
class Opt:
    values: List[int]
    opts: Optional[Tuple[int, str, float, bool]]
```

```
$ python nargs.py 1 2 3 --opts 10 foo 10.0 True
Opt(values=[1, 2, 3], opts=(10, 'foo', 10.0, True))
```

## SubCommand

`Union` will be subcommands.

```python
from typing import Optional, Union
from oppapi import from_args, oppapi

@oppapi
class Foo:
    a: int

@oppapi
class Bar:
    b: Optional[int]

@oppapi
class Opt:
    cmd: str
    sub: Union[Foo, Bar]

def main():
    opt = from_args(Opt)
```

```
$ python subcommand.py -h

usage: subcommand.py [-h] cmd {foo,bar} ...

positional arguments:
  cmd
  {foo,bar}

optional arguments:
  -h, --help  show this help message and exit
```

## Flatten

TODO

## LICENSE

This project is licensed under the [MIT license](https://github.com/yukinarit/oppapi/blob/main/LICENSE)
