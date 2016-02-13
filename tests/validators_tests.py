import mock
from nose.tools import eq_, assert_raises
from lib.validators import RegexValidator
import argparse


class TestRegexValidator:

    def setup(self):
        pattern = "1.2.3.4"
        self.sut = RegexValidator(pattern)

    def test_call_happy_path(self):
        eq_("1.2.3.4", self.sut.__call__("1.2.3.4"))

    def test_call_raises_error(self):
        assert_raises(ValueError, self.sut.__call__, "a.b.c.d")
