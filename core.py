

import uuid
# Connection-level dict elements
NAME = 'name'
TYPE = 'type'
DESCRIPTION = 'descr'
META = 'meta'
GROUPING = 'grouping'
WRITER = 'writer'


class GenericPE(object):
   

    def __init__(self, numprocesses=1):
        self.inputconnections = {}
        self.outputconnections = {}
        self.wrapper = 'simple'
        self.pickleIgnore = []
        self.pickleIgnore = list(vars(self).keys())
        self.numprocesses = numprocesses
        self.name = self.__class__.__name__
        self.id = self.name + str(uuid.uuid4())

    def _add_input(self, name, grouping=None, tuple_type=None):
     
        self.inputconnections[name] = {NAME: name}
        if grouping:
            self.inputconnections[name][GROUPING] = grouping
        if tuple_type:
            self.inputconnections[name][TYPE] = tuple_type

    def _add_output(self, name, tuple_type=None):
        
        self.outputconnections[name] = {NAME: name}
        if tuple_type:
            self.outputconnections[name][TYPE] = tuple_type

    def setInputTypes(self, types):
       
        pass

    def getOutputTypes(self):
        
        ret = {}
        # print '%s: %s' % (self.id, self.outputconnections)
        for name, output in self.outputconnections.items():
            try:
                ret[name] = output[TYPE]
            except KeyError:
                raise Exception("%s: No output type defined for '%s'"
                                % (self.id, name))
        return ret

    def _preprocess(self):
        '''
        Subclasses may override this method for variable and data
        initialisation before data processing commences.
        '''
        None

    def preprocess(self):
        '''
        This method called once before processing commences.
        '''
        self._preprocess()

    def _process(self, data):
      
        None

    def process(self, inputs):
      
        return self._process(inputs)

    def _postprocess(self):
        None

    def postprocess(self):
        
        self._postprocess()

    def write(self, name, data, **kwargs):
        
        self._write(name, data)

    def _write(self, name, data, **kwargs):
       
        try:
            output = self.outputconnections[name]
            output[WRITER].write(data)
        except KeyError:
            raise Exception("Can't write data: Unknown output connection\
                            '%s' for PE '%s'" % (name, type(self).__name__))
