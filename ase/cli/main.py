from __future__ import print_function

import argparse
import sys

from ase import __version__
from ase.utils import import_module


commands = [
    ('info', 'ase.cli.info'),
    ('test', 'ase.test'),
    ('gui', 'ase.gui.ag'),
    ('run', 'ase.cli.run'),
    ('build', 'ase.cli.build'),
    ('db', 'ase.db.cli'),
    ('eos', 'ase.eos'),
    ('ulm', 'ase.io.ulm'),
    ('nomad-upload', 'ase.cli.nomad'),
    ('tab-completion', 'ase.cli.complete')]


def add_arguments(parser):
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-q', '--quiet', action='store_true')


def main():
    parser = argparse.ArgumentParser(
        prog='ase',
        description='ASE command line tool')
    parser.add_argument('--version', action='version',
                        version='%(prog)s-{}'.format(__version__))
    subparsers = parser.add_subparsers(title='Sub-commands',
                                       dest='command')

    subparser = subparsers.add_parser('help',
                                      description='Help',
                                      help='Help for sub-command')
    subparser.add_argument('helpcommand', nargs='?')

    functions = {}
    parsers = {}
    for command, module_name in commands:
        cmd = import_module(module_name).CLICommand
        subparser = subparsers.add_parser(
            command,
            help=cmd.short_description,
            description=getattr(cmd, 'description', cmd.short_description))
        add_arguments(subparser)
        cmd.add_arguments(subparser)
        functions[command] = cmd.run
        parsers[command] = subparser

    args = parser.parse_args()

    if args.command == 'help':
        if args.helpcommand is None:
            parser.print_help()
        else:
            parsers[args.helpcommand].print_help()
    elif args.command is None:
        parser.print_usage()
    else:
        try:
            functions[args.command](args)
        except KeyboardInterrupt:
            pass
        except Exception as x:
            if args.verbose:
                raise
            else:
                print('{}: {}'.format(x.__class__.__name__, x),
                      file=sys.stderr)
                print('To get a full traceback, use: ase --verbose',
                      file=sys.stderr)


def old():
    sys.argv[:1] = sys.argv[0].rsplit('-', 1)
    main()
