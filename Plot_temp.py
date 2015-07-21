__author__ = 'kdsouza'

from traits.api import HasTraits, Instance
from collections import namedtuple
import pandas as pd

def get_x_y(receiver):
    """
    Returns x column and y column tuple.
    Assumes Receiver has at least two columns, takes first two.
    """

    selection = receiver.selection
    return selection[1][0], selection[1][1]


from MPL_pyqt_mergewidget import *
from MPL_style_formatting import *
from MPL_dicts import *
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.figure import Figure as MPLFigure
from canopy_data_import.commands.command import Command

from traits.api import Str, Bool, List, Int, Range, Any, Dict, on_trait_change
from traitsui.api import View, Item, Group, TextEditor, InstanceEditor, CheckListEditor, BooleanEditor, HSplit


def tap(x, label):
    print("%s: %s" % (label, x))
    return x

def get_item_editor(val):
    """Returns customized View editor type for given attribute value."""
    if isinstance(tap(val, 'get_item_editor val'), list):   # later might need tuple with label case
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
        for key, val in tap(d.items(), '__init__ d.items'):
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
                items.append(Item(attr, editor=tap(get_item_editor(val), 'converting item_editor')))
        return items

    def default_traits_view(self):
        items = self.convert_to_items()
        return View(Group(*items),
                    resizable=True)

    def _anytrait_changed(self, attr_name, old_val, new_val):
        print("%s changed from %s to %s" % (attr_name, old_val, new_val))


def merge_specs(spec1, spec2):
    """Merges dictionaries of spec1 and spec 2, returns new SpecNode."""
    pass


class PlotLayout(HasTraits):
    """Mutable container for all plots, axes, and plot specs"""

    spec_nodes = Instance(SpecNode)
    figure = Instance(MPLFigure, ())

    def default_traits_view(self):
        specs_items = self.spec_nodes.convert_to_items()
        return View(HSplit(Item('figure', editor=MPLFigureEditor(), show_label=False),
                           Group(*specs_items)),
                    resizable=True)


##### Command classes #####

class PlotCMD(Command):
    """Calling apply() displays a plot on the layout"""
    def apply(self, d, layout):
        pass

    def undo(self):
        pass


class UpdatePlot(PlotCMD):
    """Calling apply() updates given plot figure using the difference between new and old dicts"""
    def apply(self, d_new, d_old, plot):
        pass

    def undo(self):
        pass
