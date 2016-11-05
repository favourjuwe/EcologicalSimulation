


import argparse
from importlib import import_module


def main(args=None):

    parser = argparse.ArgumentParser(
        description='Winnex Lab Networks.')
    parser.add_argument('target', help='target execution platform')
    args, remaining = parser.parse_known_args()
    try:
        from dispel4py.new import mappings
        # see if platform is in the mappings file as a simple name
        target = mappings.config[args.target]
    except KeyError:
        # it is a proper module name - fingers crossed...
        target = args.target
    try:
        process = getattr(import_module(target), 'main')
    except:
        # print traceback.format_exc()
        print('Unknown target: %s' % target)
        return
    process()


if __name__ == "__main__":
    main()
