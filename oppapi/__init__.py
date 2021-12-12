import sys
import argparse
import enum
import dataclasses
import functools
import logging
from typing import Type, TypeVar, Optional, Callable, Dict, Any

import okome
import serde.compat
import serde.de

T = TypeVar("T")

log = logging.getLogger("oppapi")


def _generate_parser(cls) -> argparse.ArgumentParser:
    """
    Generate `argparse.ArgumentParser` from a class declaration.
    """
    log.debug("Generating command line parser.")

    class_comment = okome.parse(cls).comment
    if class_comment:
        parser_description = "\n".join(class_comment)
    else:
        parser_description = ""

    parser = argparse.ArgumentParser(description=parser_description)
    _add_arguments_and_options(parser, cls)

    return parser


class SubParserAction(argparse.Action):
    def __init__(self, *args, subns: str = "", **kwargs):
        self.subns = subns
        super().__init__(*args, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        log.debug(f"SubParserAction: {namespace}, {values}, {option_string}, {self.subns}")
        del namespace.a
        setattr(namespace, self.subns, {"a": values})


def _add_arguments_and_options(parser: argparse.ArgumentParser, cls, subns=None):
    # Inspect fields of dataclass.
    # `f`  conveys pyserde field attributes as well as dataclass's
    # `of` conveys docstring comments declared in dataclass fields
    for f, of in zip(serde.de.defields(cls), okome.fields(cls)):
        log.debug(f"Inspecting field: {f}, {of}")

        if serde.compat.is_opt(f.type):
            typ = serde.compat.get_args(f.type)[0]
        else:
            typ = f.type

        opts: Dict[str, Any] = {}
        if not isinstance(f.default, dataclasses._MISSING_TYPE):
            opts["default"] = f.default
        if of.comment:
            opts["help"] = " ".join(of.comment)
        if serde.compat.is_list(typ):
            opts["nargs"] = "+"
        elif serde.compat.is_tuple(typ):
            opts["nargs"] = len(serde.compat.get_args(typ))
            opts["type"] = _gen_tuple_converter(typ)
        elif serde.compat.is_enum(typ):
            opts["choices"] = [e.value for e in typ]
        elif serde.compat.is_union(typ):
            sub = parser.add_subparsers(dest=f.name)
            for subcls in serde.compat.get_args(typ):
                sub_parser = sub.add_parser(_subcommand(subcls))
                # sub_action = functools.partial(SubParserAction, subns=_subnamespace(subcls))
                # _add_arguments_and_options(sub_parser, subcls, action=sub_action)
                _add_arguments_and_options(sub_parser, subcls, f.name)
            continue

        if _determine_option(f):
            _add_option(parser, f, **opts)
        else:
            _add_argument(parser, f, **opts)


def _gen_tuple_converter(typ) -> Callable:
    """
    Generate a converter that deserialize tuple in string into the declared type.

    argparse doesn't accept `typing.Tuple`. The args parsed by `argparse` will be
    tuple in str regardless of the declared type.

    e.g.
      type: Tuple[int, str, float, bool]
      parsed args: ("10", "foo", "10.0", "True")

    The function generates such converter that converts `("10", "foo", "10.0", "True")`
    into `(10, "foo", 10.0, True)`.
    """
    inner_types = serde.compat.get_args(typ)
    index = 0

    def conv(val):
        nonlocal index
        val = inner_types[index](val)
        index += 1
        return val
    return conv


def _add_argument(parser: argparse.ArgumentParser, f: serde.de.DeField, subns=None, **opts):
    """
    Add positional argument to parser.
    """
    command = _command(f)
    typ = _get_type_for_argparse(f.type)
    if typ:
        opts["type"] = typ

    if subns:
        opts["dest"] = f.name

    log.debug(f"Add argument to parser: command={command}, type={typ}, opts={opts}")
    parser.add_argument(command, **opts)


def _add_option(parser: argparse.ArgumentParser, f: serde.de.DeField, subns=None, **opts):
    """
    Add optional argument to parser.
    """
    short = _short(f)
    long = _long(f)
    typ = _get_type_for_argparse(f.type)
    if typ is bool:
        opts["action"] = "store_true"
    elif typ:
        # NOTE: Specifying both "type" and "action" raises an error
        opts["type"] = typ

    opts["required"] = f.metadata.get("oppapi_required", False)

    opts["dest"] = f.name

    log.debug(f"Add option to parser: short={short}, long={long}, type={typ}, opts={opts}")
    parser.add_argument(short, long, **opts)


def _get_type_for_argparse(typ: Type):
    """
    Get type supported by `argparse.Parser`.

    * Get inner type T from Optional[T]
    * Use `str` for Date, Time and DateTime
    * Use `str` for other string serializable types e.g. `pathlib.Path`
    * Use inner type T from List[T]
    """
    log.debug(f"_get_type_for_argparse {typ}")
    if serde.compat.is_opt(typ):
        return _get_type_for_argparse(serde.compat.get_args(typ)[0])
    if serde.compat.is_list(typ):
        return serde.compat.get_args(typ)[0]
    if serde.compat.is_tuple(typ):
        return None
    elif typ in serde.de.StrSerializableTypes or typ in serde.de.DateTimeTypes:
        return str
    elif issubclass(typ, enum.IntEnum):
        return int
    elif issubclass(typ, enum.Enum):
        return str
    else:
        return typ


def _determine_option(f: serde.de.DeField):
    return (
        f.metadata.get(
            "oppapi_option",
        )
        or serde.compat.is_opt(f.type)
    )


def _snake_to_kebab(s: str) -> str:
    return s.replace("_", "-")


def _command(f: serde.de.DeField) -> str:
    return _snake_to_kebab(f.conv_name("snakecase"))


def _subcommand(cls) -> str:
    return _snake_to_kebab(cls.__name__).lower()


def _subnamespace(cls) -> str:
    return cls.__name__


def _short(f: serde.de.DeField) -> str:
    return f.metadata.get("oppapi_short") or "-" + f.conv_name("snakecase")[0]


def _long(f: serde.de.DeField) -> str:
    return f.metadata.get("oppapi_long") or "--" + _snake_to_kebab(f.conv_name("snakecase"))


def _update_parsed_args(cls, dic: Dict):
    for f in serde.de.defields(cls):
        if serde.compat.is_union(f.type):
            attr = {}
            union_class_name = dic.pop(f.name)
            dic[f.name] = attr
            for inner_cls in serde.compat.get_args(f.type):
                if union_class_name != _subcommand(inner_cls):
                    continue
                for ff in serde.de.defields(inner_cls):
                    if ff.name in dic:
                        attr[ff.name] = dic[ff.name]


def from_args(cls: Type[T]) -> T:
    try:
        parser = _generate_parser(cls)
        args = parser.parse_args()
        args = vars(args)  # type: ignore
        log.debug(f"Parsed: {args}")

        _update_parsed_args(cls, args)
        log.debug(f"Updated: {args}")

        return serde.from_dict(cls, args)

    except Exception as e:
        log.debug(e)
        parser.print_usage()
        sys.exit(1)


def oppapi(_cls):
    @functools.wraps(_cls)
    def wrap(cls):
        if not dataclasses.is_dataclass(cls):
            cls = dataclasses.dataclass(cls)
        serde.deserialize(cls, reuse_instances_default=False)
        return cls

    if _cls is None:
        return wrap  # type: ignore
    else:
        return wrap(_cls)


@dataclasses.dataclass
class Field(serde.de.DeField):
    """
    Represents a field in oppapi class.

    It inherits `dataclasses` and `pyserde` attributes.
    """
    option: bool = False


def field(*args, short: Optional[str] = None, long: Optional[str] = None,
          required: bool = False, option=False,
          metadata=None, **kwargs):
    """
    Declare a field with parameters.
    """
    if not metadata:
        metadata = {}
    metadata["oppapi_option"] = option

    if short:
        metadata["oppapi_short"] = short
    if long:
        metadata["oppapi_long"] = long

    metadata["oppapi_required"] = required

    return dataclasses.field(*args, metadata=metadata, **kwargs)


def argument(*args, short=None, long=None, **kwargs):
    return field(*args, option=False, short=short, long=long, **kwargs)


def option(*args, short=None, long=None, **kwargs):
    return field(*args, option=True, short=short, long=long, **kwargs)
