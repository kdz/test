__author__ = 'kdsouza'

from SpecNode import *

#=================  test receiver data pulling ===================

## This opens a UI, which we do not need to do
# receiver = load_data(filename='/Users/kdsouza/Desktop/Projects/pandas_play/weather_year.csv')

weather_data = pd.read_csv("/Users/kdsouza/Desktop/Projects/pandas_play/weather_year.csv")
DataFrameSelection = namedtuple('DataFrameSelection', 'rows, cols, items')

class Receiver(HasTraits):
    """Mock Receiver class to avert side effects"""
    selection = Instance(DataFrameSelection)


test_receiver = Receiver(
    selection=DataFrameSelection([],
                                 [weather_data['EDT'],
                                  weather_data['Mean TemperatureF']],
                                 []))


x, y = get_x_y(test_receiver)
from pandas.util.testing import assert_series_equal
assert_series_equal(x, weather_data['EDT'])


#====================== test pure functions ========================






#============= test SpecNode initialization and view ===============

sample_dict = {
    'a': Range(0, 100),
    'b': Bool(True),
    'c': List([7, 8, 9]),
    'd': {
        'sub_a': Bool(False),
        'sub_b': Str('sub_b_val'),
        'sub_dict': {'sub_sub_a': Float(.05),
                     'sub_sub_b': Str
                     }
    }
}


sample_specs = SpecNode(sample_dict)
assert isinstance(sample_specs.d, SpecNode)

# check convert_to_items
# print(sample_specs.convert_to_items())
# sample_specs.configure_traits()   # uncomment for interactive NodeSpec View


# assert get_item_editor(range(5)) == CheckListEditor(values=[0, 1, 2, 3, 4])
# assert get_item_editor(10) == TextEditor(auto_set=False, enter_set=True)


#============== test PlotLayout Initialization and View ===============

layout = PlotLayout(spec_nodes=sample_specs)

# layout.figure.add_subplot(111)   # uncomment to view empty grid
# layout.configure_traits()     # uncomment for interactive Layout view