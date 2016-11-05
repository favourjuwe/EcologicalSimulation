

from dispel4py.examples.graph_testing import testing_PEs as t
from dispel4py.workflow_graph import WorkflowGraph


def testAlltoOne():
   
    graph = WorkflowGraph()
    prod = t.TestProducer()
    cons1 = t.TestOneInOneOut()
    cons2 = t.TestOneInOneOut()
    cons1.numprocesses = 5
    cons2.numprocesses = 5
    graph.connect(prod, 'output', cons1, 'input')
    cons2.inputconnections['input']['grouping'] = 'global'
    graph.connect(cons1, 'output', cons2, 'input')
    return graph



graph = testAlltoOne()
