

from dispel4py.core import GenericPE, NAME


class BasePE(GenericPE):
    '''

    '''
    INPUT_NAME = 'input'
    OUTPUT_NAME = 'output'

    def __init__(self, inputs=[], outputs=[], num_inputs=0, num_outputs=0):
    
        GenericPE.__init__(self)

        for i in range(num_inputs):
            name = '%s%s' % (BasePE.INPUT_NAME, i)
            self.inputconnections[name] = {NAME: name}
        for i in range(num_outputs):
            name = '%s%s' % (BasePE.OUTPUT_NAME, i)
            self.outputconnections[name] = {NAME: name}
        for name in inputs:
            self.inputconnections[name] = {NAME: name}
        for name in outputs:
            self.outputconnections[name] = {NAME: name}


class IterativePE(GenericPE):
  
    INPUT_NAME = 'input'
    OUTPUT_NAME = 'output'

    def __init__(self):
        GenericPE.__init__(self)
        self._add_input(IterativePE.INPUT_NAME)
        self._add_output(IterativePE.OUTPUT_NAME)

    def process(self, inputs):
      
        data = inputs[IterativePE.INPUT_NAME]
        result = self._process(data)
        if result is not None:
            return {self.OUTPUT_NAME: result}

    def _process(self, data):
    
        return None


class ProducerPE(GenericPE):
   
    OUTPUT_NAME = 'output'

    def __init__(self):
        GenericPE.__init__(self)
        self._add_output(ProducerPE.OUTPUT_NAME)

    def process(self, inputs):
        
        result = self._process(inputs)
        if result is not None:
            return {self.OUTPUT_NAME: result}


class ConsumerPE(GenericPE):
   
    INPUT_NAME = 'input'

    def __init__(self):
        GenericPE.__init__(self)
        self._add_input(ConsumerPE.INPUT_NAME)

    def process(self, inputs):
       
        data = inputs[ConsumerPE.INPUT_NAME]
        self._process(data)


class SimpleFunctionPE(IterativePE):
    INPUT_NAME = IterativePE.INPUT_NAME
    OUTPUT_NAME = IterativePE.OUTPUT_NAME

    def __init__(self, compute_fn=None, params={}):
        IterativePE.__init__(self)
        if compute_fn:
            self.name = 'PE_%s' % compute_fn.__name__
        self.compute_fn = compute_fn
        self.params = params

    def _process(self, data):
        return self.compute_fn(data, **self.params)


from dispel4py.workflow_graph import WorkflowGraph


def create_iterative_chain(functions,
                           FunctionPE_class=SimpleFunctionPE,
                           name_prefix='PE_',
                           name_suffix=''):



    prev = None
    first = None
    graph = WorkflowGraph()

    for fn_desc in functions:
        try:
            fn = fn_desc[0]
            params = fn_desc[1]
        except TypeError:
            fn = fn_desc
            params = {}

        # print 'adding %s to chain' % fn.__name__
        pe = FunctionPE_class()
        pe.compute_fn = fn
        pe.params = params
        pe.name = name_prefix + fn.__name__ + name_suffix

        if prev:
            graph.connect(prev, IterativePE.OUTPUT_NAME,
                          pe, IterativePE.INPUT_NAME)
        else:
            first = pe
        prev = pe

    # Map inputs and outputs of the wrapper to the nodes in the subgraph
    graph.inputmappings = {'input': (first, IterativePE.INPUT_NAME)}
    graph.outputmappings = {'output': (prev, IterativePE.OUTPUT_NAME)}

    return graph


class CompositePE(WorkflowGraph):
    
    def __init__(self, create_graph=None, params={}):
      
        WorkflowGraph.__init__(self)
        self.inputmappings = {}
        self.outputmappings = {}
        if create_graph:
            create_graph(self, **params)

    def _map_input(self, input_name, internal_pe, internal_input):
        '''
        Map the composite PE input to the named input of a PE that is contained
        in the graph.
        '''
        self.inputmappings[input_name] = (internal_pe, internal_input)

    def _map_output(self, output_name, internal_pe, internal_output):
        '''
        Map the composite PE output to the named output of a PE that is
        contained in the graph.
        '''
        self.outputmappings[output_name] = (internal_pe, internal_output)
