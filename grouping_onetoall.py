

from dispel4py.examples.graph_testing import testing_PEs as t
from dispel4py.workflow_graph import WorkflowGraph


def testOnetoAll():
    graph = WorkflowGraph()
    prod = t.TestProducer()
    cons = t.TestOneInOneOut()
    cons.numprocesses = 2
    cons.inputconnections['input']['grouping'] = 'all'
    graph.connect(prod, 'output', cons, 'input')
    return graph


graph = testOnetoAll()
