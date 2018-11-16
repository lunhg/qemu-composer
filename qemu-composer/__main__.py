# -*- coding: utf-8 -*-
__version__ = "0.0.1"

"qemu-composer.__main__: executed when qemu directory is called as script."""
import os, argparse
from composer import main
print "+-+-+-+-+-+-+-+-+-+-+-+-+-+"
print "|Q|e|m|u|-|C|o|m|p|o|s|e|r|"
print "+-+-+-+-+-+-+-+-+-+-+-+-+-+"
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--prefix')
parser.add_argument('-f', '--file')
parser.add_argument('-G', '--group')
parser.add_argument('-g', '--gid')
parser.add_argument('-u', '--uid')
args = parser.parse_args()

if not args.prefix:
    args.prefix = os.path.join(os.environ['PWD'], '.bin')

if not args.file:
    args.file = os.path.join(os.environ['PWD'], '.qemu.yml')

if not args.group:
    args.group = 'wheel'

if not args.gid:
    args.gid = 1000

if not args.uid:
    args.group = 1000

    
main(
    prefix=args.prefix,
    file=args.file,
    group=args.group,
    gid=args.gid,
    uid=args.uid
)
