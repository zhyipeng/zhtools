from unittest import TestCase

from zhtools.code_generator.json2model import (Json2Model, Model,
                                               ModelArray)


class TestJson2Model(TestCase):

    def test_parse_dict(self):
        testcases = [
            ({"action": 230002}, Model('test', {'action': int})),
            ({"action": "230002"}, Model('test', {'action': str})),
            ({"action": [1, 2]}, Model('test', {'action': ModelArray('action', int)})),
            ({"action": [{'key': 0}]}, Model('test', {'action': ModelArray('action', Model('action', {'key': int}))})),
            ({"action": {"key1": 1, "key2": "test"}},
             Model('test', {'action': Model('action', {'key1': int, 'key2': str})})),
            ({'action': {'key': [{'key1': 1}]}},
             Model('test', children={
                 'action': Model('action', children={
                     'key': ModelArray('key', child=Model('key', children={
                         'key1': int
                     }))
                 })
             })
             )
        ]
        for param, result in testcases:
            ret = Json2Model.parse_dict('test', data=param)
            self.assertEqual(ret, result)

    def test_render(self):
        testcases = [
            (Model('test', {'action': int}), ['class Test(BaseModel):', '    action: int']),
            (Model('test', {'action': str}), ['class Test(BaseModel):', '    action: str']),
            (Model('test', {'action': ModelArray('action', int)}), ['class Test(BaseModel):', '    action: list[int]']),
            (Model('test', {'action': ModelArray('action', Model('action', {'key': int}))}),
             ['class Action(BaseModel):', '    key: int', '', '', 'class Test(BaseModel):', '    action: list[Action]']),
            (Model('test', {'action': Model('action', {'key1': int, 'key2': str})}),
             ['class Action(BaseModel):', '    key1: int', '    key2: str', '', '', 'class Test(BaseModel):', '    action: Action']),
            (Model('test', children={
                'action': Model('action', children={
                    'key': ModelArray('key', child=Model('key', children={
                        'key1': int
                    }))
                })
            }),
             ['class Key(BaseModel):', '    key1: int', '', '', 'class Action(BaseModel):', '    key: list[Key]', '', '', 'class Test(BaseModel):', '    action: Action']
             )

        ]
        for model, result in testcases:
            ret = model._render()
            self.assertEqual(ret, result)

    def test_parse(self):
        ret = Json2Model.parse('{"action": 230002}')
        self.assertEqual(ret, 'class Model(BaseModel):\n    action: int')
