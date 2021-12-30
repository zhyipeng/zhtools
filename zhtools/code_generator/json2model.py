from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Union

from zhtools.data_structs.convertors import underline_to_camel_case

try:
    from pydantic import BaseModel
except ImportError:
    from zhtools.exceptions import ModuleRequired
    raise ModuleRequired('pydantic')


@dataclass
class Model:
    name: str
    children: dict[str, Union[type, Model]]

    def __eq__(self, other):
        return self.name == other.name and self.children == other.children

    def _render(self) -> list[str]:
        ret = [f'class {underline_to_camel_case(self.name)}(BaseModel):']
        for n, m in self.children.items():
            if isinstance(m, Model):
                t = m.render_type()
                rendered = m._render()
                if rendered:
                    ret = rendered + ['', ''] + ret
            else:
                t = m.__name__

            ret.append(f'    {n}: {t}')

        return ret

    def render_type(self) -> str:
        return underline_to_camel_case(self.name)

    def render_child_model(self) -> list[str]:
        ret = []
        for n, m in self.children.items():
            if isinstance(m, Model):
                rendered = m._render()
                if rendered:
                    ret = rendered + ['', ''] + ret

        return ret

    def render(self) -> str:
        return '\n'.join(self._render())


class ModelArray(Model):

    def __init__(self, name: str, child: Union[type, Model]):
        super().__init__(name, {})
        self.child = child

    def __eq__(self, other):
        return self.name == other.name and self.child == other.child

    @property
    def child_type(self) -> str:
        if isinstance(self.child, Model):
            return underline_to_camel_case(self.child.name)
        else:
            return self.child.__name__

    def _render(self) -> list[str]:
        if isinstance(self.child, Model):
            return self.child._render()
        return []

    def render_type(self) -> str:
        return f'list[{self.child_type}]'

    def render_child_model(self) -> list[str]:
        if isinstance(self.child, Model):
            return self.child._render() + ['', '']
        return []


class Json2Model:

    @staticmethod
    def parse(data: str, model_name: str = 'model') -> str:
        data = json.loads(data)
        if not isinstance(data, dict):
            raise TypeError()
        return Json2Model.parse_dict(model_name, data).render()

    @staticmethod
    def parse_dict(model_name: str, data: dict) -> Model:

        def _parse(name: str, v: Any) -> Union[type, Model]:
            if isinstance(v, list):
                return ModelArray(name, _parse(name, v[0]))
            elif isinstance(v, dict):
                return Json2Model.parse_dict(name, v)
            else:
                return type(v)

        m = Model(model_name, {})
        for k, v in data.items():
            m.children[k] = _parse(k, v)

        return m

