import __builtin__
import __main__
import mock
from nose.tools import eq_, ok_, raises, assert_false
from lib.commit import Commit
from lib import util


class TestFormatters:

    def to_commit(self, email, subj, body):
        ct = Commit()
        ct.email = email
        ct.subject = subj
        ct.body = body
        return ct

    def setup(self):
        ct1 = self.to_commit("bob@dole.com", "blah", "blah, blah")
        ct2 = self.to_commit(
            "bill@murray.com", "blah blah", "blah, blah, blah")
        ct3 = self.to_commit(
            "dan@aykroyd.com", "subj has vnum 1.2.3.4", "blah")
        ct4 = self.to_commit(
            "chevy@chase.com", "blah", "body has vnum 1.2.3.4")

        self.commits = [ct1, ct2, ct3, ct4]

    def test_string_has_pattern_returns_as_expected(self):
        pattern = "abc"
        string1 = "abc"
        string2 = "123"
        ok_(util.string_has_pattern(string1, pattern))
        assert_false(util.string_has_pattern(string2, pattern))

    def test_get_pattern_from_string_returns_as_expected(self):
        pattern = "\\d\\.\\d\\.\\d\\.\\d"
        string = "stringcontainin1.2.3.4init"
        eq_("1.2.3.4", util.get_pattern_from_string(string, pattern))

    def test_sanitize_path(self):
        path = "../path/to/sanitize"
        eq_(path + "/", util.sanitize_path(path))

    def test_sanitize_subpath(self):
        subpath = "/subpath/to/sanitize"
        eq_(subpath[1:], util.sanitize_subpath(subpath))

    def test_filter_commits_by_email(self):
        emails = ['bob@dole.com', 'bill@murray.com']
        actual = util.filter_commits_by_email(emails, self.commits)
        eq_(self.commits[2:], actual)

    def test_filter_commits_by_version_num(self):
        vnum = '1.2.3.4'
        actual = util.filter_commits_by_version_num(vnum, self.commits)
        eq_(self.commits[:-2], actual)

    def test_unify_paths(self):
        root = "/the/root/of/all/evil"
        path = "../good"
        actual = util.unify_paths(root, path)
        eq_("/the/root/of/all/good/", actual)

    def test_read_file(self):
        filepath = "/some/file/path/file_name.txt"
        file_content = "file content"
        mock_open = mock.mock_open(read_data=file_content)
        with mock.patch('__builtin__.open', mock_open):
            actual = util.read_file(filepath)

        mock_open.assert_called_once_with(filepath)
        eq_(file_content, actual)

    @mock.patch('util.os.path.exists')
    def test_write_file_directory_exists(self, mock_exists):
        path = "/some/file/path/"
        filepath = path + "file_name.txt"
        content = "some content"

        mock_exists.return_value = True

        mock_open = mock.mock_open()
        with mock.patch('__builtin__.open', mock_open, create=True):
            util.write_file(filepath, content)

        mock_exists.assert_called_once_with(path)
        mock_open.assert_called_once_with(filepath, 'w')

    @mock.patch('util.os.path.exists')
    @mock.patch('util.os.makedirs')
    def test_write_file_directory_not_exists(self, mock_makedirs, mock_exists):
        path = "/some/file/path/"
        filepath = path + "file_name.txt"
        content = "some content"

        mock_exists.return_value = False

        mock_open = mock.mock_open()
        with mock.patch('__builtin__.open', mock_open, create=True):
            util.write_file(filepath, content)

        mock_exists.assert_called_once_with(path)
        mock_makedirs.called_once_with(path)
        mock_open.assert_called_once_with(filepath, 'w')

    def test_get_path_from_filepath(self):
        path = "/some/file/path/"
        filepath = path + "file_name.txt"

        actual = util.get_path_from_filepath(filepath)
        eq_(path, actual)

        path = "some/file/path/"
        filepath = path + "file_name.txt"

        actual = util.get_path_from_filepath(filepath)
        eq_(path, actual)

    @mock.patch('util.os.path.exists')
    def test_directory_exists(self, mock_exists):
        directory = "/some/directory/"
        util.directory_exists(directory)
        mock_exists.assert_called_once_with(directory)

    @mock.patch('util.os.path.isfile')
    def test_directory_exists(self, mock_isfile):
        filepath = "/some/file/path/filename.txt"
        util.file_exists(filepath)
        mock_isfile.assert_called_once_with(filepath)
