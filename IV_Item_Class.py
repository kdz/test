__author__ = 'kdsouza'


from IV_Dim_class import *
from traits.api import Instance, List, Str, Any

# Only two dimensional plots

class Item(HasTraits):
    """Base class for all dimensioned view components."""

    def _convert_to(self, item_type):
        """"""
        pass


################
class Column(Item):
    """List of values (pandas series) with a dimension."""
    name = Str
    vals = List
    dim = Str


def convert_pd_dataframe(df, cols_dict):
    """Reads pandas DataFrame into columns with respective dimensions."""
    dset = DataSet()
    for name in cols_dict:
        col = Column()
        col.name = name
        col.vals = df[name]
        col.dim = cols_dict[name].name   # col type
        dset._add_col(col)
    return dset


################
class DataSet(Item):
    """Data container of columns."""
    cols = List(Column)

    def _add_col(self, col):
        self.cols += col


class TwoDimSet(DataSet):
    """Two dimensional DataSet."""
    pass


class NDSet(DataSet):
    pass


################
class Plot(Item):
    """Graphical item that displays relationships between columns in DataSet."""

    name = Str
    indep_cols = List(Column)
    dep_cols = List(Column)

    class KWarg(HasTraits):
        """Row in TableEditor."""
        key = Str
        val = Any


class TwoDimPlot(Plot):
    indep = Instance(Column)
    dep = Instance(Column)


class LinePlot(TwoDimPlot):
    pass


class BarPlot(TwoDimPlot):
    pass


class TwoDimHist(TwoDimPlot):
    pass


class PlotND(Plot):
    pass