import re
import argparse


class RegexValidator(object):

    """
    Performs regular expression match on value.
    If match fails a ValueError is raised
    """

    def __init__(self, pattern, statement=None):
        self.pattern = re.compile(pattern)
        self.statement = statement
        if not self.statement:
            self.statement = "must match pattern %s" % self.pattern

    def __call__(self, string):
        match = self.pattern.search(string)
        if not match:
            raise ValueError(self.statement)
        return string
