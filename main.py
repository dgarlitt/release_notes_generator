#!/usr/bin/python

import os

# standard library imports
import sys

reload(sys)
sys.setdefaultencoding('utf8')

# project imports
from lib.git import Git
from lib.properties import Properties
from lib.release_notes import ReleaseNotes
from lib.release_notes_index import ReleaseNotesIndex
from lib.arg_loader import ArgLoader
from lib.runner import Runner

script_root = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

props = Properties(script_root, script_root + '/props.json')
runner = Runner()
git = Git()

runner.props = props
runner.git = git
runner.release_notes = ReleaseNotes(props)
runner.index = ReleaseNotesIndex(props)

args = ArgLoader(sys.argv[1:]).get_args()

if args.version_number == "all":
    runner.run_all()

else:
    runner.run(args.version_number)
