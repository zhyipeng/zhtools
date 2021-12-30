import builtins
import logging
import typing

from zhtools.exceptions import ModuleRequired

if typing.TYPE_CHECKING:
    from pydantic import BaseModel


def make_default_model(model: typing.Type['BaseModel']) -> 'BaseModel':
    try:
        from pydantic import fields
    except ImportError:
        raise ModuleRequired('')

    attrs = {}
    for k, v in model.__fields__.items():
        if v.default:
            attrs[k] = v.get_default()
            continue

        match v.shape:
            case (fields.SHAPE_LIST
                  | fields.SHAPE_SEQUENCE
                  | fields.SHAPE_ITERABLE):
                attrs[k] = []
            case fields.SHAPE_SET:
                attrs[k] = set()
            case fields.SHAPE_MAPPING | fields.SHAPE_DICT:
                attrs[k] = {}
            case fields.SHAPE_TUPLE:
                attrs[k] = tuple()
            case fields.SHAPE_DEFAULTDICT:
                attrs[k] = dict()
            case _:
                if issubclass(v.type_, BaseModel):
                    attrs[k] = make_default_model(v.type_)
                    continue

                match v.type_:
                    case builtins.int | builtins.float:
                        attrs[k] = 0
                    case builtins.str:
                        attrs[k] = ''
                    case builtins.bool:
                        attrs[k] = False
                    case _:
                        logging.warning('unsupport type: %s-%s', k, v.type_)

    return model(**attrs)
