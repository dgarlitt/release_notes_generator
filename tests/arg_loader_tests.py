import mock
from nose.tools import eq_, ok_
from lib.arg_loader import ArgLoader, DESCRIPTION, VNUM_HELP_TEXT


class TestArgLoader:

    def setup(self):
        self.args = ["1.2.3.4"]
        self.sut = ArgLoader(self.args)

    def test_init_sets_expected_properties(self):
        eq_(self.args, self.sut.in_args)

    @mock.patch('lib.arg_loader.argparse')
    def test_get_args_operates_as_expected(self, mock_argparse):
        mock_parser = mock.MagicMock()
        mock_argparse.ArgumentParser.return_value = mock_parser
        mock_parser.parse_args.return_value = "Parsed Args"

        actual = self.sut.get_args()

        mock_argparse.ArgumentParser.assert_called_once_with(
            description=DESCRIPTION)
        mock_parser.add_argument.assert_called_once_with(
            "version_number", help=VNUM_HELP_TEXT)
        eq_("Parsed Args", actual)
