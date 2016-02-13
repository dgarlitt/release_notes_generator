import sys
import mock
from nose.tools import eq_, ok_, assert_raises
import nose.tools
# from main import load_props, sanitize_path, parse_version_number

# class TestMain:
#   @mock.patch('main.json')
#   @mock.patch('__builtin__.open', spec=open, read_data='some raw json')
#   def test_load_props(self, mock_open, mock_json):
#     json_result = 'some json'
#     mock_json.load.return_value = json_result
#     props = load_props()

#     ok_(mock_open.called)
#     mock_open.assert_called_with('props.json', 'r')

#     ok_(mock_json.load.called)
#     mock_json.load.assert_called_with(mock_open().__enter__())
#     eq_(json_result, props)

#   def test_sanitize_path_adds_slash_to_path(sefl):
#     path = "../path"
#     eq_(path + "/", sanitize_path(path))

#   @mock.patch.object(sys, 'argv', ['', '1.2.3.4'])
#   def test_parse_version_number_happy_path(self):
#     pattern = "^1\.2\.3\.4$"
#     actual = parse_version_number(pattern).__dict__
#     eq_({'tag_name': '1.2.3.4'}, actual)
