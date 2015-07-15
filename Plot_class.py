__author__ = 'kdsouza'

from traits.api import HasTraits, Str, Instance, Button, List, Any, Property, Dict, \
    cached_property, on_trait_change, property_depends_on
from traitsui.api import View, TableEditor, ObjectColumn
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import seaborn as sns



# pd.DataFrame.keep_plot() kwargs by kind
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
    """A row in TableEditor."""
    key = Str
    val = Any


kwarg_editor = TableEditor(
    columns=[ObjectColumn(name='key', editable=False),
             ObjectColumn(name='val', editable=True)],
    show_column_labels=False
)


class Plot(HasTraits):
    """
    Container for pd.dataframe, plot information, and MPL figure.
    View merges MPL canvas and TraitsUI widget.
    Canvas clears and re-displays on button press.


    """
    # pd.DataFrame data source
    dataframe = Instance(pd.DataFrame)
    kind = Str('Line')
    kind_dict = Property(Dict, depends_on='kind')
    # keys and values for TableEditor
    kwargs = Property(List(Kwarg), depends_on='kind_dict')

    # widget attributes
    keep_plot = Button
    update_preview = Button
    view = Instance(View)
    figure = Instance(Figure, ())
    # preview_axes = Property(Instance(Axes))

    def __init__(self):
        """Initialize with subplots"""
        super(Plot, self).__init__()
        self.static_axes = self.figure.add_subplot(212)
        self.preview_axes = self.figure.add_subplot(211)

    def plot(self, axes):
        """Clears and updates given axes with plot using current kwargs"""
        axes.cla()
        kws = self.kwargs
        pdkwargs = {kw.key: kw.val for kw in kws}
        self.dataframe.plot(ax=axes, **pdkwargs)
        self.figure.canvas.draw()

    @cached_property
    def _get_kind_dict(self):
        """Updates kind_dict based on kind selection."""
        return KIND_KWARGS[self.kind]

    @cached_property      # how to update kwargs when edited in UI? so preview may update
    def _get_kwargs(self):
        """Updates kwarg display on kind selection."""
        return [Kwarg(key=key, val=self.kind_dict[key]) for key in self.kind_dict]

    @on_trait_change('kwargs')
    def replot_preview(self):
        """
        Updates preview when kwargs is updated, which is only when kind is changed.
        Since kwargs is a cached property, edits in the UI window do not trigger udpate.
        Same lack of update when kwargs is a Property using @property_depends_on('kind_dict', settable=True).
        Does not update.

        """
        self.plot(self.preview_axes)

    def _keep_plot_fired(self):
        """Updates static plot with current kwargs, on button press."""
        self.plot(self.static_axes)

    def _update_preview_fired(self):
        """Updates preview plot with current kwargs, on button press."""
        self.plot(self.preview_axes)


# configure seaborn keep_plot appearance
sns.despine()
sb_dark = sns.dark_palette("skyblue", 8, reverse=True)
sns.set(palette=sb_dark, style='whitegrid')

