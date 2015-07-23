__author__ = 'kdsouza'

from traits.api import HasTraits, Instance
from collections import namedtuple
import pandas as pd

from MPL_pyqt_mergewidget import *
from MPL_style_formatting import *
from MPL_dicts import *
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.figure import Figure as MPLFigure
from canopy_data_import.commands.command import Command

from traits.api import Str, Bool, List, Int, Range, Any, Dict, on_trait_change, Enum
from traitsui.api import View, Item, Group, TextEditor, InstanceEditor, CheckListEditor, BooleanEditor, RangeEditor, HSplit, EnumEditor


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

def get_item_editor(val):
    """
    (val: Any) -> Editor

    Returns customized View editor type for given attribute value.
    """
    if isinstance(val, list):   # later might need tuple with label case
        if isinstance(val[0], str):
            return CheckListEditor(values=val)
        else:
            return CheckListEditor(values=[str(item) for item in val])
    if isinstance(val, bool):
        return BooleanEditor()
    else:
        return TextEditor(auto_set=False, enter_set=True)


##### Container classes ########

VEdit = namedtuple('VEdit', 'value editor')

class Spec(HasTraits):    # <- just inherit from Dict?
    """Container class for mpl plot keys and values"""

    _dict = Dict    # can remove and use .__dict__ if initialized correctly so new attributes register in __init__

    def __init__(self, d):
        # super(Spec, self).__init__()
        self._dict = d
        for key, val in d.items():
            if isinstance(val, dict):
                self.add_trait(key, Spec(val))
            else:
                self.add_trait(key, val)
        for key, val in d.items():
            getattr(self, key)   # some other form of asserting existence of attr?

    def __getattr__(self, item):
        """
        Returns value of corresponding key in _dict.
        Treats items in dict as attributes of the Spec object.
        """
        return self._dict[tap(item, '_getattr_ item')]

    def __setattr__(self, key, value):
        """
        Sets value in _dict.
        Treats items in dict as attributes of the Spec object.
        """
        self._dict[tap(key, 'key of _setattr_')] = value

    def convert_to_items(self):
        """Returns list of nested items in Spec."""
        items = []
        for attr, dict_val in self._dict.items():
            val = getattr(self, attr)
            if isinstance(val, Spec):
                items.append(Item(attr, editor=InstanceEditor(), style='custom'))
            elif isinstance(val, int):
                items.append(Item(attr))
            else:
                items.append(Item(attr, editor=get_item_editor(val)))
        return items

    def default_traits_view(self):
        items = self.convert_to_items()
        return View(Group(*items),
                    resizable=True)

    def _anytrait_changed(self, attr_name, old_val, new_val):
        print("%s: %s -> %s" % (attr_name, old_val, new_val))


class PlotLayout(HasTraits):
    """Mutable container for all plots, axes, and plot specs"""

    spec_nodes = Instance(Spec)
    figure = Instance(MPLFigure, ())

    def default_traits_view(self):    # later perhaps switch to TreeEditor for collapsing
        return View(HSplit(Item('figure', editor=MPLFigureEditor(), show_label=False),
                           Item('spec_nodes', editor=InstanceEditor(), style='custom')),
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
        return [complete(spec, receiver) for val in spec]
    if callable(spec):
        return spec(receiver)
    if isinstance(spec, Spec):
        d = spec.__dict__
        return Spec(complete(d, receiver))


def merge_spec(c1, c2):
    """
    (c1: Spec, c2: Spec) -> Spec

    Merges Spec (Dict {Str: Spec}, builtin, VEdit), defaulting to c1 in cases on conflict.
    Returns collection of same type.
    """

    if c1 is None:
        return c2
    if c2 is None:
        return c1

    if isinstance(c1, list) and isinstance(c2, list):
        return [merge_spec(x, y) for x, y in map(None, c1, c2)]

    if isinstance(c1, VEdit) and isinstance(c2, VEdit):   # uses c1 editor
        return VEdit(merge_spec(c1.value, c2.value), c1.editor)

    if isinstance(c1, tuple) and isinstance(c2, tuple):
        return tuple(merge_spec(x, y) for x, y in map(None, c1, c2))

    if isinstance(c1, dict) and isinstance(c2, dict):
        all_keys = set(c1.iterkeys()) | set(c2.iterkeys())
        return {key: merge_spec(c1.get(key), c2.get(key)) for key in all_keys}

    if callable(c1) or callable(c2):
        return lambda receiver: merge_spec(complete(c1, receiver),
                                           complete(c2, receiver))

    if isinstance(c1, Spec) and isinstance(c2, Spec):
        d1 = c1.__dict__
        d2 = c2.__dict__
        return Spec(merge_spec(d1, d2))

    return c1


##### Command classes #####

class PlotCMD(Command):
    """apply() displays a plot on the layout"""
    def apply(self, d, layout):
        pass

    def undo(self):
        pass


class UpdatePlot(PlotCMD):
    """apply() updates given plot figure using the difference between new and old dicts"""
    def apply(self, d_new, d_old, plot):
        pass

    def undo(self):
        pass
