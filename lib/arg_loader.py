import argparse

DESCRIPTION = 'Generate Release Notes for Project'
VNUM_HELP_TEXT = 'A valid version number or the keyword "all" must be provided'


class ArgLoader(object):

    def __init__(self, in_args):
        self.in_args = in_args

    def get_args(self):
        parser = argparse.ArgumentParser(description=DESCRIPTION)
        parser.add_argument("version_number", help=VNUM_HELP_TEXT)

        return parser.parse_args(self.in_args)
