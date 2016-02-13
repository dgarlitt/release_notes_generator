import mock
from nose.tools import eq_, ok_, assert_false
from lib.runner import Runner


class TestRunner:

    def setup(self):
        self.mock_props = mock.MagicMock()
        self.mock_git = mock.MagicMock()
        self.mock_release_notes = mock.MagicMock()
        self.mock_index = mock.MagicMock()

        self.sut = Runner()

        self.sut.props = self.mock_props
        self.sut.git = self.mock_git
        self.sut.release_notes = self.mock_release_notes
        self.sut.index = self.mock_index

    @mock.patch.object(Runner, '_Runner__commit_and_push')
    @mock.patch.object(Runner, '_Runner__generate_index')
    @mock.patch.object(Runner, '_Runner__generate_release_notes')
    @mock.patch.object(Runner, '_Runner__update_local_repos')
    def test_run_calls_composites(self, mock_ulr, mock_grn, mock_gi, mock_cap):
        ver_num = "1.2.3.4"
        self.mock_props.validate_version_num.return_value = ver_num

        self.sut.run(ver_num)

        eq_(ver_num, self.sut.version_num)
        mock_ulr.assert_called_once()
        mock_grn.assert_called_once()
        mock_gi.assert_called_once()
        mock_ulr.assert_called_once()

    @mock.patch.object(Runner, '_Runner__generate_all_release_notes')
    def test_run_all_calls_composites(self, mock_garn):
        self.sut.run_all()
        mock_garn.assert_called_once

    def test__update_local_repos_operates_as_expected(self):
        git = self.mock_git
        p = self.mock_props

        assert_false(self.sut.repos_updated)

        self.sut._Runner__update_local_repos()

        git.fetch.assert_called_once_with(p.project_remote, p.project_path)
        git.checkout.assert_called_once_with(p.wiki_branch, p.wiki_path)
        git.pull.assert_called_once_with(
            p.wiki_remote, p.wiki_branch, p.wiki_path)
        ok_(self.sut.repos_updated)

        self.sut._Runner__update_local_repos()

        eq_(1, git.fetch.call_count)
        eq_(1, git.checkout.call_count)
        eq_(1, git.pull.call_count)

    def test__get_commit_log_operates_as_expected(self):
        git = self.mock_git
        p = self.mock_props

        vnum = self.sut._version_num = "2.3.4.5"
        tag = p.get_tag_name_from_version_num.return_value = "tag1.2.3.4"
        tags = git.get_tags_by_pattern.return_value = [
            "tag1.2.3.4", "tag2.3.4.5"]
        crange = git.get_tag_range.return_value = "tag1.2.3.4..tag2.3.4.5"
        log = git.log.return_value = "the log"

        actual = self.sut._Runner__get_commit_log()

        eq_(log, actual)

        p.get_tag_name_from_version_num.assert_called_once_with(vnum)
        git.get_tags_by_pattern.assert_called_once_with(
            p.tag_pattern, p.project_path)
        git.get_tag_range.assert_called_once_with(tag, tags)
        git.log.assert_called_once_with(crange, p.project_path)

    @mock.patch.object(Runner, '_Runner__get_commit_log')
    @mock.patch('lib.runner.util')
    def test__generate_release_notes_operates_as_expected(self, mock_util, mock_gcl):
        p = self.mock_props
        rn = self.mock_release_notes
        git = self.mock_git

        vnum = self.sut._version_num = "2.3.4.5"
        rn_str = rn.__str__.return_value = "rn as string"
        log = mock_gcl.return_value = "the log"

        self.sut._Runner__generate_release_notes()

        mock_gcl.assert_called_once
        rn.generate.assert_called_once_with(vnum, log)
        mock_util.write_file.assert_called_once_with(
            rn.absolute_filepath, rn_str)
        git.add.assert_called_once_with(rn.absolute_filepath, p.wiki_path)

    @mock.patch('lib.runner.util')
    def test__generate_index_operates_as_expected(self, mock_util):
        p = self.mock_props
        i = self.mock_index

        i_str = i.__str__.return_value = "i as string"
        vnum = self.sut._version_num = "2.3.4.5"

        self.sut._Runner__generate_index()

        self.mock_index.generate.assert_called_once_with(vnum)
        mock_util.write_file.assert_called_once_with(
            i.absolute_filepath, i_str)
        self.mock_git.add.assert_called_once_with(
            i.absolute_filepath, p.wiki_path)

    def test__commit_and_push_operates_as_expected(self):
        p = self.mock_props

        vnum = self.sut._version_num = "2.3.4.5"
        msg = "Add release notes for " + vnum

        self.sut._Runner__commit_and_push()

        self.mock_git.commit.assert_called_once_with(msg, p.wiki_path)
        self.mock_git.push.assert_called_once_with(
            p.wiki_remote, p.wiki_branch, p.wiki_path)

    @mock.patch.object(Runner, 'run')
    def test__generate_all_release_notes_operates_as_expected(self, mock_run):
        tags = ["tag1", "tag2", "tag3", "tag4"]
        self.mock_git.get_tags_by_pattern.return_value = tags
        self.mock_props.get_version_num_from_tag_name.side_effect = [
            "1", "2", "3", "4"]

        self.sut._Runner__generate_all_release_notes()

        calls = [mock.call("1"), mock.call(
            "2"), mock.call("3"), mock.call("4")]
        mock_run.assert_has_calls(calls)
