# -*- coding: utf-8 -*-
__version__ = "0.0.1"

"qemu-composer.__main__: executed when qemu directory is called as script."""
import os, argparse
from composer import main as qemu

# CLI parser
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--prefix', help='where will be the "root" file of the build')
parser.add_argument('-f', '--file', help='the qemu-composer file to be readed (defaults to .qemu.yml)')
parser.add_argument('-G', '--group', help="add a system group's name to user")
parser.add_argument('-g', '--gid', help='the system group id of the user')
parser.add_argument('-u', '--uid', help='the system user id ')
parser.add_argument('-v', '--version', help='show current version')
parser.add_argument('up', help='up generated docker images (similar to docker-compose up)', action='store_true')
parser.add_argument('build', help='build generated docker images (similar to docker-compose build)', action='store_true')
parser.add_argument('push', help='push generated docker images (similar to docker-compose push)', action='store_true')

# Export a main function to tests
def main(**kwargs):
    return qemu(**kwargs)

# Run if this script is called directly
if __name__ is '__main__':
    args = parser.parse_args()

    if args.version:
        main(version=__version__)
    if not args.version and not args.help:
        main(
            prefix=args.prefix or os.path.join(os.environ['PWD']),
            file=args.file or '.qemu.yml',
            group=args.group or 'wheel',
            gid=args.gid or 1000,
            uid=args.uid or 1000,
            build=args.build or True,
            up=args.up or False,
            push=args.push or False
        )
        sys.exit()
