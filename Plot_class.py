__author__ = 'kdsouza'

from pyface.qt import QtGui, QtCore
from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'

from traits.api import HasTraits, Str, Instance, Button, List, Any, Property, Dict, cached_property, on_trait_change
from traitsui.api import View, Group, Item, CheckListEditor, TableEditor, ObjectColumn, InstanceEditor, HSplit
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import seaborn as sns

from MPL_pyqt_mergewidget import *
from matplotlib.widgets import RectangleSelector

# pd.DataFrame.update_plot() kwargs by update_plot kind
KIND_KWARGS = {
    'Line': {'kind': 'line',
             'title': "",
             'legend': True},
    'Bar': {'kind': 'bar',
            'title': "",
            'stacked': False},
    'Horizontal Bar': {'kind': 'barh',
                       'title': "",
                       'stacked': False},
    "Histogram": {'kind': 'hist',
                  'title': "",
                  'orientation': 'vertical',
                  'cumulative': False},
    "Box": {'kind': 'box',
            'title': "",
            'vert': True,
            'by': 'X'},
    "KDE": {'kind': 'kde',
            'title': ""},
    "Density": {'kind': 'density',
                'title': ""},
    "Area": {'kind': 'area',
             'title': "",
             'stacked': False},
    "Pie Chart": {'kind': 'pie',
                  'title': "",
                  'subplots': True,
                  'fontsize': 15},
    "Scatter": {'kind': 'scatter',
                'title': "",
                'subplots': True},
    "Hexbin": {'kind': 'hexbin',
               'title': "",
               'gridsize': 25,
               'subplots': True}
}


class Kwarg(HasTraits):
    """Row in TableEditor."""
    key = Str
    val = Any


kwarg_editor = TableEditor(
    columns=[ObjectColumn(name='key', editable=False),
             ObjectColumn(name='val', editable=True)],
    show_column_labels=False
)


class Plot(HasTraits):
    # pd.DataFrame data source
    dataframe = Instance(pd.DataFrame)
    # changing kind triggers notification that updates kind_dict
    kind = Str('Line')
    # tracks current kwargs dict
    kind_dict = Property(Dict, depends_on='kind')
    # keys and values for TableEditor
    kwargs = Property(List(Kwarg), depends_on='kind_dict')
    # widget
    update_plot = Button
    view = Instance(View)
    figure = Instance(Figure, ())

    def __init__(self):
        super(Plot, self).__init__()
        self.axes = self.figure.add_subplot(111)
        print(self.figure.axes)

    @cached_property
    def _get_kind_dict(self):
        return KIND_KWARGS[self.kind]

    @cached_property
    def _get_kwargs(self):
        return [Kwarg(key=key, val=self.kind_dict[key]) for key in self.kind_dict]

    @on_trait_change('update_plot')
    def plot(self):
        kws = self.kwargs
        pdkwargs = {kw.key: kw.val for kw in kws}
        self.figure.clear()
        self.axes = self.figure.add_subplot(111)
        axes = self.figure.axes[0]
        self.dataframe.plot(ax=axes, **pdkwargs)
        self.figure.canvas.draw()


# configure seaborn update_plot appearance
sns.despine()
sns.set_style('whitegrid')

