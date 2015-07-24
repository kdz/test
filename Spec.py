__author__ = 'kdsouza'

from functools import reduce
import pandas as pd

from MPL_pyqt_mergewidget import *
from MPL_style_formatting import *
from VEdit import *
from MPL_dicts import *
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.figure import Figure as MPLFigure
from canopy_data_import.commands.command import Command


def get_x_y(receiver):
    """
    (receiver: Receiver) -> (Column, Column)

    Returns x column and y column tuple.
    Assumes Receiver has at least two columns, takes first two.
    """

    selection = receiver.selection
    return selection[1][0], selection[1][1]

def tap(x, label):
    print("%s: %s" % (label, x))
    return x

def get_editor(val):
    """
    Any -> EditorFactory, {Str: Any}

    Returns customized Editor, kwargs for given attribute value.
    Customizing editor style done in self-defined VEdits.

    dict -> InstanceEditor
    list(str) -> CheckListEditor, {'values: val}
    list(other) -> EnumEditor, {'values': val}
    bool -> BooleanEditor
    rest -> TextEditor, {'auto_set': False, 'enter_set': True}
    """
    if isinstance(val, dict):
        return InstanceEditor, {}
    if isinstance(val, list):
        if isinstance(val[0], str):
            return CheckListEditor, {'values': val}
        else:
            return EnumEditor, {'values': val}
    if isinstance(val, bool):
        return BooleanEditor, {}
    else:
        return TextEditor, {'auto_set': False, 'enter_set': True}

##### Container classes ########

class Spec(tr.HasTraits):    # <- just inherit from Dict?
    """Container class for mpl plot keys and values."""

    _dict = tr.Dict(key_trait=tr.Str, value_trait=VEdit)

    def __init__(self, d):
        """
        dict{Str: builtin, Dict, or VEdit} -> dict{Str: VEdit}

        Digests given dict into Spec instance of nested VEdits,
        nested dictionaries digested into nested VEdits with Spec values.
        """
        self._dict = {key: (val if isinstance(val, VEdit)
                            else VEdit(Spec(val) if isinstance(val, dict) else val, *get_editor(val)))
                      for key, val in d.items()}

    def __getattr__(self, attr):
        """
        Returns value of corresponding key in _dict.
        """
        if attr == '_dict':
            return self._dict
        elif attr in self._dict:
            return self._dict[attr].value

    def __setattr__(self, attr, new_value):
        """
        Sets value of VEdit at specified attribute key in _dict.
        """
        if attr == '_dict':
            super(Spec, self).__setattr__(attr, new_value)
        elif attr in self._dict:
            self._dict[attr].value = new_value

    def convert_to_items(self):
        """
        Returns list of TraitsUI Items with corresponding editors for each key in _dict.
        Editors are either specified in original dictionary or computed through get_editor.
        """
        items = []
        for key, vedit in self._dict.items():
            val, editor, kwargs = vedit.value, vedit.editor, vedit.kwargs
            if isinstance(val, Spec):
                items.append(trui.Item(key, editor=editor(**kwargs), style='custom'))
            else:
                items.append(trui.Item(key, editor=editor(**kwargs)))
        return items

    def default_traits_view(self):
        items = self.convert_to_items()
        return trui.View(trui.Group(*items),
                    resizable=True)

    def _anytrait_changed(self, attr_name, old_val, new_val):
        print("%s: %s -> %s" % (attr_name, old_val, new_val))


class PlotLayout(tr.HasTraits):
    """Mutable container for all plots, axes, and plot specs"""

    spec_nodes = tr.Instance(Spec)
    figure = tr.Instance(MPLFigure, ())

    def default_traits_view(self):    # later perhaps switch to TreeEditor for collapsing
        return trui.View(trui.HSplit(trui.Item('figure', editor=MPLFigureEditor(), show_label=False),
                           trui.Item('spec_nodes', editor=InstanceEditor(), style='custom')),
                    resizable=True)


##### Pure Functions

def complete(spec, receiver):
    """
    (spec: AType, receiver: Receiver) -> AType

    Returns same input spec type with computed values in place of receiver functions.
    """
    if isinstance(spec, dict):
        return {key: complete(val, receiver) for key, val in spec.items()}
    if isinstance(spec, list):
        return [complete(val, receiver) for val in spec]
    if callable(spec):
        return spec(receiver)
    if isinstance(spec, Spec):
        d = spec.__dict__
        return Spec(complete(d, receiver))
    else:
        return spec


def merge_spec(c1, c2):
    """
    (c1: Spec, c2: Spec) -> Spec

    Merges Spec (Dict {Str: Spec}, builtin, VEdit), defaulting to c1 in cases of conflict.
    Returns collection of same type.
    """

    if c1 is None:
        return c2
    if c2 is None:
        return c1

    if isinstance(c1, list) and isinstance(c2, list):
        return [merge_spec(x, y) for x, y in map(None, c1, c2)]

    if isinstance(c1, tuple) and isinstance(c2, tuple):
        return tuple(merge_spec(x, y) for x, y in map(None, c1, c2))

    if isinstance(c1, VEdit) and isinstance(c2, VEdit):   # uses c1 editor
        return VEdit(merge_spec(c1.value, c2.value), c1.editor, c1.kwargs)

    if isinstance(c1, dict) and isinstance(c2, dict):
        all_keys = set(c1.iterkeys()) | set(c2.iterkeys())
        return {key: merge_spec(c1.get(key), c2.get(key)) for key in all_keys}

    if callable(c1) or callable(c2):
        return lambda receiver: merge_spec(complete(c1, receiver),
                                           complete(c2, receiver))

    if isinstance(c1, Spec) and isinstance(c2, Spec):
        d1 = c1._dict
        d2 = c2._dict
        return Spec(merge_spec(d1, d2))

    return c1


##### Command classes #####

import pandas as pd

class Plot(Command):
    """Displays a plot on the layout"""

    default_spec = tr.Instance(Spec)
    edited_spec = tr.Instance(Spec)
    x = tr.Any
    y = tr.List()

    def apply(self, receiver):
        out_spec = merge_spec(self.edited_spec, self.default_spec)
        filled_out_spec = complete(out_spec, receiver)


    def undo(self):
        pass


class UpdatePlot(Plot):
    """apply() updates given plot figure using the difference between new and old dicts"""
    def apply(self, receiver):
        pass

    def undo(self):
        pass
