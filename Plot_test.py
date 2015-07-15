__author__ = 'kdsouza'

from MPL_pyqt_mergewidget import *
from Plot_class import *
from traitsui.api import Group, Item, CheckListEditor, InstanceEditor, HSplit

# instances for testing
df = pd.DataFrame([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]],
                  columns=['first', 'second', 'third'])
plot = Plot()
plot.dataframe = df   # simple data  # block when using weather data
plot.view = View(HSplit(Item('figure', editor=MPLFigureEditor(), show_label=False),
                        Group(Item('kind', editor=CheckListEditor(values=sorted(KIND_KWARGS.keys()))),
                              Item('kwargs', editor=kwarg_editor, show_label=False),
                              Item('update_preview', show_label=False),
                              Item('keep_plot', show_label=False))),
                 resizable=True)

# TO USE: must press "update plot" for plots to appear. Edit plot kind by drop-down, kwargs by text
plot.configure_traits(view=plot.view)


# Tests on Plot class
def test_plot_init():
    assert plot()

def test_kind_changed():
    plot.kind = "Line"
    plot._kind_changed()
    assert plot.kind_dict == KIND_KWARGS['Line']

def test_kwarg_update():
    pass