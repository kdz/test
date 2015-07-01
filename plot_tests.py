__author__ = 'kdsouza'

from Plot_class import *

# instances for testing
df = pd.DataFrame([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]],
                  columns=['first', 'second', 'third'])
plot = Plot()
# plot.dataframe = df   # simple data  # block when using weather data


plot.dataframe = pd.read_csv(
    "/Users/kdsouza/Desktop/Projects/pandas_play/weather_year.csv")   # weather data  # block if using simple data


# Tests on Plot class
def test_plot_init():
    assert plotR

def test_kind_changed():
    plot.kind = "Line"
    plot._kind_changed()
    assert plot.kind_dict == KIND_KWARGS['Line']


plot.configure_traits(view=plot.view)
