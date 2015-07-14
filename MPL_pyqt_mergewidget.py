__author__ = 'kdsouza'

from pyface.qt import QtGui, QtCore
from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'

import matplotlib as mpl
mpl.rcParams['backend.qt4'] = 'PySide'
mpl.use('Qt4Agg')
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg
from traitsui.qt4.editor import Editor
from traitsui.qt4.basic_editor_factory import BasicEditorFactory
from traitsui.api import Handler


# embedding widget editor

class _MPLFigureEditor(Editor):

    scrollable = True

    def init(self, parent):
        self.control = self._create_canvas(parent)
        self.set_tooltip()

    def update_editor(self):
        pass

    def _create_canvas(self, parent):
        """Creates MPL canvas"""
        mpl_canvas = FigureCanvas(self.value)
        return mpl_canvas


class MPLFigureEditor(BasicEditorFactory):

    klass = _MPLFigureEditor
