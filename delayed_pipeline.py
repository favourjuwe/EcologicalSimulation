

from dispel4py.examples.graph_testing import testing_PEs as t
from dispel4py.workflow_graph import WorkflowGraph
from dispel4py.new.monitoring import ProcessTimingPE

prod = t.TestProducer()
cons1 = t.TestOneInOneOut()

cons2 = ProcessTimingPE(t.TestDelayOneInOneOut())


graph = WorkflowGraph()
graph.connect(prod, 'output', cons1, 'input')
graph.connect(cons1, 'output', cons2, 'input')
