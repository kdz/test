__author__ = 'kdsouza'

from Spec import *
from collections import namedtuple

#===========  mock Receiver =============

## This opens a UI, which we do not need to do
# receiver = load_data(filename='/Users/kdsouza/Desktop/Projects/pandas_play/weather_year.csv')

weather_data = pd.read_csv("/Users/kdsouza/Desktop/Projects/pandas_play/weather_year.csv")
DataFrameSelection = namedtuple('DataFrameSelection', 'rows, cols, items')

class Receiver(tr.HasTraits):
    """Mock Receiver class to avert side effects"""
    selection = tr.Instance(DataFrameSelection)


test_receiver = Receiver(
    selection=DataFrameSelection([],
                                 [weather_data['EDT'],
                                  weather_data['Mean TemperatureF']],
                                 []))


x, y = get_x_y(test_receiver)
from pandas.util.testing import assert_series_equal
assert_series_equal(x, weather_data['EDT'])


#============= Spec demo ===============

sample_dict = {
    'a': 10,
    'b': VEdit(True, BooleanEditor, {}),
    'c': VEdit(7, EnumEditor, {'values': [7, 8, 9]}),
    'd': {
        'sub_a': VEdit(False, BooleanEditor, {}),
        'sub_b': 'sub_b_val',
        'sub_c': 10,
        'sub_dict': {'sub_sub_a': .05,
                     'sub_sub_b': VEdit('a', EnumEditor, {'values':['a', 'b', 'c']})
                     }
    }
}

def generate_sample_spec(d):
    return Spec(d)

def view_sample_spec(d):
    generate_sample_spec(d).configure_traits()
    pass

# generate_sample_spec(sample_dict)
# view_sample_spec(sample_dict)


#============== Layout demo ============

def generate_sample_layout(d):
    return PlotLayout(spec_nodes=Spec(d))

def view_sample_layout(d):
    layout = generate_sample_layout(d)
    layout.figure.add_subplot(111)
    layout.configure_traits()

view_sample_layout(sample_dict)