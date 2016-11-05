

from dispel4py.workflow_graph import WorkflowGraph

from importlib import import_module
from imp import load_source
import traceback


def findWorkflowGraph(mod, attr):
    if attr is not None:
        # use the named attribute
        graph = getattr(mod, attr)
    else:
        # search for a workflow graph in the given module
        for i in dir(mod):
            attr = getattr(mod, i)
            if isinstance(attr, WorkflowGraph):
                if not hasattr(attr, 'inputmappings')\
                        and not hasattr(attr, 'outputmappings'):
                    graph = attr
    return graph


def loadGraphFromFile(module_name, path, attr=None):
    mod = load_source(module_name, path)
    attr = findWorkflowGraph(mod, attr)
    return attr


def loadGraph(module_name, attr=None):
    '''
    Loads a graph from the given module.
    '''
    mod = import_module(module_name)
    graph = findWorkflowGraph(mod, attr)
    return graph


def load_graph(graph_source, attr=None):
    # try to load from a module
    error_message = ''
    try:
        return loadGraph(graph_source, attr)
    except ImportError:
        # it's not a module
        error_message += 'No module "%s"\n' % graph_source
        pass
    except Exception:
        error_message += \
            'Error loading graph module:\n%s' % traceback.format_exc()
        pass

    # maybe it's a file?
    try:
        return loadGraphFromFile('temp', graph_source, attr)
    except IOError:
        # it's not a file
        error_message += 'No file "%s"\n' % graph_source
    except Exception:
        error_message += \
            'Error loading graph from file:\n%s' % traceback.format_exc()

    # we don't know what it is
    print('Failed to load graph from "%s":\n%s' %
          (graph_source, error_message))


from sys import getsizeof
from itertools import chain
from collections import deque


def dict_handler(d):
    return chain.from_iterable(d.items())


def total_size(o, handlers={}, verbose=False):
    
    all_handlers = {
        tuple: iter,
        list: iter,
        deque: iter,
        dict: dict_handler,
        set: iter,
        frozenset: iter,
    }
    all_handlers.update(handlers)
    seen = set()
    default_size = getsizeof(0)

    def sizeof(o):
        if id(o) in seen:
            return 0
        seen.add(id(o))
        s = getsizeof(o, default_size)

        for typ, handler in all_handlers.items():
            if isinstance(o, typ):
                s += sum(map(sizeof, handler(o)))
                break
        return s

    return sizeof(o)

import copy


def make_hash(o):

   
    if isinstance(o, (set, tuple, list)):
        return hash(tuple([make_hash(e) for e in o]))

    if not isinstance(o, dict):
        return hash(o)

    new_o = copy.deepcopy(o)
    for k, v in new_o.items():
        new_o[k] = make_hash(v)

    return hash(tuple(frozenset(sorted(new_o.items()))))
