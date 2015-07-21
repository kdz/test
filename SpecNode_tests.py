__author__ = 'kdsouza'

from Plot_temp import *

################ test receiver data pulling

## This opens a UI, which we do not need to do
# receiver = load_data(filename='/Users/kdsouza/Desktop/Projects/pandas_play/weather_year.csv')

weather_data = pd.read_csv("/Users/kdsouza/Desktop/Projects/pandas_play/weather_year.csv")
DataFrameSelection = namedtuple('DataFrameSelection', 'rows, cols, items')

class Receiver(HasTraits):
    """Mock Receiver class to avert side effects"""
    selection = Instance(DataFrameSelection)


test_receiver = Receiver(selection=DataFrameSelection( [], [weather_data['EDT'], weather_data['Mean TemperatureF']], [] ))


x, y = get_x_y(test_receiver)
from pandas.util.testing import assert_series_equal
assert_series_equal(x, weather_data['EDT'])

############### test Node operations

sample_dict = {
    'a': Int(10),
    'b': Bool(True),
    'c': List([7, 8, 9]),
    'd': {
        'sub_a': Bool(False),
        'sub_b': Str('sub_b_val')
    }

}


plotspec = SpecNode(sample_dict)
assert isinstance(plotspec.d, SpecNode)

# check convert_to_items
# print(plotspec.convert_to_items())
plotspec.configure_traits()



# assert get_item_editor(range(5)) == CheckListEditor(values=[0, 1, 2, 3, 4])
# assert get_item_editor(10) == TextEditor(auto_set=False, enter_set=True)


# layout = PlotLayout()
# layout.spec_nodes = SpecNode({'key1': 10,
#                               'key2': 10})
# layout.figure.add_subplot(111)
# layout.configure_traits()