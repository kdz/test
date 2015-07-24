__author__ = 'kdsouza'


import traits.api as tr
import traitsui.api as trui
from traitsui.editors import *

class VEdit(tr.HasTraits):
    """
    Container class for value, editor type, and editor specifications.
    """

    value = tr.Any
    editor = trui.EditorFactory
    kwargs = tr.Dict(key_trait=tr.Str, value_trait=tr.Any)
    # item_kwargs = tr.Dict(key_trait=tr.Str, value_trait=tr.Any)   # default hide label, custom style?

    def __init__(self, value, editor, kwargs=dict()):
        super(VEdit, self).__init__()
        self.value, self.editor, self.kwargs = value, editor, kwargs

    def __eg__(self, other):
        return isinstance(other, VEdit) and (self.val == other.val) and (self.editor == other.editor)



