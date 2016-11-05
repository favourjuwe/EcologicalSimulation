

from dispel4py.examples.graph_testing import testing_PEs as t
from dispel4py.workflow_graph import WorkflowGraph


def testGrouping():
   
    words = t.RandomWordProducer()
    filter1 = t.RandomFilter()
    filter2 = t.RandomFilter()
    count = t.WordCounter()
    graph = WorkflowGraph()
    graph.connect(words, 'output', filter1, 'input')
    graph.connect(words, 'output', filter2, 'input')
    graph.connect(filter1, 'output', count, 'input')
    graph.connect(filter2, 'output', count, 'input')

    return graph

graph = testGrouping()
