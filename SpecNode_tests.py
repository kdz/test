__author__ = 'kdsouza'

from Spec import *

def test_merge():
    assert merge_spec(1, 2) == 1
    assert merge_spec(VEdit(True, BooleanEditor),
                      VEdit(False, BooleanEditor)) == VEdit(True, BooleanEditor)
    assert merge_spec({'a': 10, 'b': False},
                      {'b': False, 'c': [1, 2, 3]}) == {'a': 10, 'b': False, 'c': [1, 2, 3]}

    def my_func(receiver):
        pass

    def my_func_2(receiver):
        pass

    assert callable(merge_spec(my_func, my_func_2))
    assert merge_spec(('a', VEdit('a', CheckListEditor)),
                      ([1, 2], VEdit('c', CheckListEditor), {})) == ('a', VEdit('a', CheckListEditor), {})


def test_set_and_get_spec():

    spec = Spec({'a': 10,
                 'b': {'b1': VEdit(10, RangeEditor()),
                       'b2': VEdit(True, BooleanEditor()),
                       'b3': {'b31': False,
                              'b32': None}
                       }
                 })

    assert 1 == 1