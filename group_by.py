

from dispel4py.examples.graph_testing import testing_PEs as t
from dispel4py.workflow_graph import WorkflowGraph


def testGrouping():
   
    words = t.RandomWordProducer()
    cons1 = t.TestOneInOneOut()
    cons2 = t.TestOneInOneOut()
    cons3 = t.TestOneInOneOut()
    count = t.WordCounter()
    graph = WorkflowGraph()
    graph.connect(words, 'output', cons1, 'input')
    graph.connect(cons1, 'output', cons2, 'input')
    graph.connect(cons2, 'output', cons3, 'input')
    graph.connect(cons3, 'output', count, 'input')

    graph.partitions = [[words], [cons1, cons2, cons3], [count]]
    return graph

graph = testGrouping()
