import argparse

parser = argparse.ArgumentParser(description='Python Templater')
parser.add_argument(
    'repo',
    help='git repository'
)
parser.add_argument(
    '--dst',
    help='where to place the template'
)
parser.add_argument(
    '--verbose',
    help='increase output verbosity',
    action="store_true"
)


def prompt_values(values, fmt='%s [%s]: '):
    return dict([
        (key, raw_input(fmt % (key, value)))
        for key, value in values.iteritems()
    ])
