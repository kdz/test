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

from traits.api import Str, Bool, List, Int, Range, Any, Dict, on_trait_change
from traitsui.api import View, Item, Group, TextEditor, InstanceEditor, CheckListEditor, BooleanEditor, HSplit, TreeEditor


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

class SpecNode(HasTraits):    # <- just inherit from Dict?
    """Container class for mpl plot keys and values"""

    # dict = Dict    # can remove and use .__dict__ if initialized correctly so new attributes register in __init__

    def __init__(self, d):
        # super(SpecNode, self).__init__()
        # self.dict = d
        for key, val in d.items():
            if isinstance(val, dict):
                self.add_trait(key, SpecNode(val))
            else:
                self.add_trait(key, val)
        for key, val in d.items():
            getattr(self, key)   # some other form of asserting existence of attr?

    def convert_to_items(self):
        """Returns generator of nested items in SpecNode."""
        items = []
        for attr, val in self.__dict__.items():
            if isinstance(val, SpecNode):
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
        print("%s changed from %s to %s" % (attr_name, old_val, new_val))


class PlotLayout(HasTraits):
    """Mutable container for all plots, axes, and plot specs"""

    spec_nodes = Instance(SpecNode)
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
    if isinstance(spec, SpecNode):
        d = spec.__dict__
        return SpecNode(complete(d, receiver))


def merge_collection(c1, c2):
    """
    (c1: CollectionTypeA, c2: CollectionTypeA) -> CollectionTypeA

    Merges Collections (List, Dict, SpecNode), defaulting to c1 in cases on conflict.
    Returns collection of same type.
    """

    if c1 is None:
        return c2
    if c2 is None:
        return c1

    if isinstance(c1, list) and isinstance(c2, list):
        return [merge_collection(x, y) for x, y in map(None, c1, c2)]

    if isinstance(c1, dict) and isinstance(c2, dict):
        all_keys = set(c1.__dict__.iterkeys()) | set(c2.__dict__.iterkeys())
        return {key: merge_collection(c1.get(key), c2.get(key)) for key in all_keys}

    if callable(c1) or callable(c2):
        return lambda receiver: merge_collection(complete(c1, receiver),
                                                 complete(c2, receiver))

    if isinstance(c1, SpecNode) and isinstance(c2, SpecNode):
        d1 = c1.__dict__
        d2 = c2.__dict__
        return SpecNode(merge_collection(d1, d2))


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
