
from dispel4py.workflow_graph import drawDot
from IPython.core.display import display_png


def display(graph):
    '''
    Visualises the input graph.
    '''
    display_png(drawDot(graph), raw=True)
