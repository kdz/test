__author__ = 'kdsouza'


from traits.api import HasTraits, Str, Instance, Button, List, Any, Property, Dict, cached_property
from traitsui.api import View, Item, CheckListEditor, TableEditor, ObjectColumn
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

# pd.DataFrame.plot() kwargs by plot kind
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
                  'alpha': 0.5,
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
    plot = Button
    view = Instance(View)

    @cached_property
    def _get_kind_dict(self):
        return KIND_KWARGS[self.kind]

    @cached_property
    def _get_kwargs(self):
        return [Kwarg(key=key, val=self.kind_dict[key]) for key in self.kind_dict]

    traits_View = View(Item(name='kind', editor=CheckListEditor(values=sorted(KIND_KWARGS.keys()))),
                       Item(name='kwargs', editor=kwarg_editor, show_label=False),
                       Item(name='plot', show_label=False),
                       title='Plot Editor'
                       )

    def _plot_fired(self):
        """Creates plt figure based on current plot attributes"""
        kws = self.kwargs
        pdkwargs = {kw.key: kw.val for kw in kws}
        self.dataframe.plot(**pdkwargs)     # uncomment to generate plots
        plt.show()


# configure seaborn plot appearance
sns.despine()
sns.set_style('whitegrid')
