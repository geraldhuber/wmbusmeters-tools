import argparse
import sys


EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def readCommandlineArgs() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
            description='What the program does',
            epilog='Text at the bottom of help')
    parser.add_argument(
        '-f', '--file',
        help='JSON input file. If \'-\' then stdin is used.',
        type=argparse.FileType('r'),
    )

    args = parser.parse_args()

    if args.file:
         input = args.file
    if not args.file:
        parser.print_usage()
        return sys.exit(EXIT_FAILURE)
    
    return args