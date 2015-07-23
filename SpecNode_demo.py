__author__ = 'kdsouza'

from Spec import *

#======================  test Receiver data accessing ========================

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


#============= test container Initialization and Pure Functions ===============

sample_dict = {
    'a': VEdit(10, RangeEditor(0, 20)),
    'b': VEdit(True, BooleanEditor()),
    'c': VEdit(7, EnumEditor(values=[7, 8, 9])),
    'd': {
        'sub_a': VEdit(False, BooleanEditor()),
        'sub_b': 'sub_b_val',
        'sub_c': 10,
        'sub_dict': {'sub_sub_a': .05,
                     'sub_sub_b': VEdit('a', EnumEditor(values=['a', 'b', 'c']))
                     }
    }
}

sample_tuple = (
    ('a', Range(0, 100)),
    ('b', Bool(True)),
    ('c', List([7, 8, 9])),
    ('d', (('sub_a', Bool(False)),
           ('sub_b', Str('sub_b_val')),
           ('sub_c', Range(1, 5)),
           ('sub_d', (('sub_sub_a', Float(0.05)),
                      ('sub_sub_b', List(['a', 'b', 'c'])))
            )
           )
     )

)


sample_specs = Spec(sample_dict)
assert isinstance(sample_specs.d, Spec)


layout = PlotLayout(spec_nodes=Spec(sample_dict))


#====================== test container View generation ========================

# sample_specs.configure_traits()   # uncomment for interactive NodeSpec View

# assert get_item_editor(range(5)) == CheckListEditor(values=[0, 1, 2, 3, 4])
# assert get_item_editor(10) == TextEditor(auto_set=False, enter_set=True)


layout.figure.add_subplot(111)   # uncomment to view empty grid
layout.configure_traits()     # uncomment for interactive Layout view