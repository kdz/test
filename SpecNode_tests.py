__author__ = 'kdsouza'

from Spec import *

d_simple = {'a': 10,
            'b': VEdit('b', CheckListEditor, {'values': ['a', 'b', 'c']})}

d1 = {'a': VEdit(10, RangeEditor, {'low': 2, 'high': 15}),
      'b': {
          'b1': VEdit(True, BooleanEditor, {}),
          'b2': VEdit(1, EnumEditor, {'values': range(0, 20)})
      }}

d2 = {'a': 15,
      'b': {VEdit('c', None, {})}
      }

def test_complete_and_merge():
    assert merge_spec(1, 2) == 1
    merged_vedits = merge_spec(VEdit(True, BooleanEditor, {}),
                               VEdit(False, BooleanEditor, {'k': 10}))
    assert merged_vedits.value
    assert merged_vedits.editor == BooleanEditor
    assert merged_vedits.kwargs == {}

    def my_func(receiver):
        pass

    def my_func_2(receiver):
        pass

    assert callable(merge_spec(my_func, my_func_2))
    merged_specs = merge_spec(Spec(d1), Spec(d2))
    assert merged_specs.a == 10
    assert merged_specs.b.b1

def test_spec_init():

    spec_simple = Spec(d_simple)
    assert spec_simple._dict['a'].editor == trui.TextEditor
    assert spec_simple._dict['a'].kwargs == {'auto_set': False, 'enter_set': True}
    assert spec_simple._dict['b'].editor == CheckListEditor
    assert spec_simple._dict['b'].kwargs == {'values': ['a', 'b', 'c']}

def test_set_and_get_spec():

    spec_simple = Spec(d_simple)
    assert spec_simple.a == 10

    spec = Spec(d1)
    assert spec.a == 10

def test_convert_to_items():

    spec_simple = Spec(d_simple)
    items = spec_simple.convert_to_items()
    item1, item2 = items[0], items[1]
    assert isinstance(item1.editor, trui.TextEditor)
    assert isinstance(item2.editor, trui.CheckListEditor)

    spec = Spec(d1)
    items = spec.convert_to_items()
    assert len(items) == 2
    assert len(spec._dict['b'].value.convert_to_items()) == 2
