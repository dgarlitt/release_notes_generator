import mock
from nose.tools import eq_, ok_, raises

import subprocess
from lib.git import TAG_CMD, LOG_CMD, CMT_CMD, ADD_CMD
from lib.git import PUSH_CMD, PULL_CMD, FETCH_CMD, CHECKOUT_CMD
from lib.git import LOG_SEPARATOR
from lib.git import Git

# def log_for_tag_side_effect(cmd):
#     if 'tag' in cmd:
#       return "\n".join(["tag2", "tag1"])
#     if 'log' in cmd:
#       return LOG_SEPARATOR.join(["log1","log2","log3"])


class TestGit():

    def setup(self):
        self.repo_path = "../repo/path/"
        self.commit_range = "tag1..tag2"
        self.file = "file.txt"
        self.message = "1.2.3.4 release notes"

        self.tag_cmd = list(TAG_CMD)
        self.tag_cmd[1] = '--git-dir=' + self.repo_path + '.git'
        self.tag_cmd[2] = '--work-tree=' + self.repo_path

        self.log_cmd = list(LOG_CMD)
        self.log_cmd[1] = '--git-dir=' + self.repo_path + '.git'
        self.log_cmd[2] = '--work-tree=' + self.repo_path
        self.log_cmd.append(self.commit_range)

        self.add_cmd = list(ADD_CMD)
        self.add_cmd[1] = '--git-dir=' + self.repo_path + '.git'
        self.add_cmd[2] = '--work-tree=' + self.repo_path
        self.add_cmd.append(self.file)

        self.cmt_cmd = list(CMT_CMD)
        self.cmt_cmd[1] = '--git-dir=' + self.repo_path + '.git'
        self.cmt_cmd[2] = '--work-tree=' + self.repo_path
        self.cmt_cmd.append('"' + self.message + '"')

        self.push_cmd = list(PUSH_CMD)
        self.push_cmd[1] = '--git-dir=' + self.repo_path + '.git'
        self.push_cmd[2] = '--work-tree=' + self.repo_path

        self.pull_cmd = list(PULL_CMD)
        self.pull_cmd[1] = '--git-dir=' + self.repo_path + '.git'
        self.pull_cmd[2] = '--work-tree=' + self.repo_path

        self.fetch_cmd = list(FETCH_CMD)
        self.fetch_cmd[1] = '--git-dir=' + self.repo_path + '.git'
        self.fetch_cmd[2] = '--work-tree=' + self.repo_path

        self.checkout_cmd = list(CHECKOUT_CMD)
        self.checkout_cmd[1] = '--git-dir=' + self.repo_path + '.git'
        self.checkout_cmd[2] = '--work-tree=' + self.repo_path

        self.sut = Git()

    def test___map_cmd_does_not_mutate_cmd_template(self):
        expected = ('git', '--git-dir=____', '--work-tree=____', 'tag')
        self.sut._Git__map_cmd(TAG_CMD, self.repo_path)
        eq_(expected, TAG_CMD)

    def test___map_cmd_replaces_git_dir_as_expected(self):
        expected = '--git-dir=' + self.repo_path + '.git'
        actual = self.sut._Git__map_cmd(TAG_CMD, self.repo_path)[1]
        eq_(expected, actual)

    def test___map_cmd_replaces_work_tree_as_expected(self):
        expected = '--work-tree=' + self.repo_path
        actual = self.sut._Git__map_cmd(TAG_CMD, self.repo_path)[2]
        eq_(expected, actual)

    @mock.patch('lib.git.subprocess')
    def test_tag_calls_subprocess_check_output_as_expected(self, mock_subprocess):
        self.sut.tag(self.repo_path)
        ok_(mock_subprocess.check_output.called)
        mock_subprocess.check_output.assert_called_once_with(self.tag_cmd)

    @mock.patch('lib.git.subprocess')
    def test_tag_returns_expected_value(self, mock_subprocess):
        mock_return = "a\nb\nc"
        expected = ["a", "b", "c"]
        mock_subprocess.check_output.return_value = mock_return
        eq_(expected, self.sut.tag(self.repo_path))

    @mock.patch('lib.git.subprocess')
    def test_log_calls_subprocess_check_output_as_expected(self, mock_subprocess):
        self.sut.log(self.commit_range, self.repo_path)
        ok_(mock_subprocess.check_output.called)
        mock_subprocess.check_output.assert_called_once_with(self.log_cmd)

    @mock.patch('lib.git.subprocess')
    def test_log_returns_expected_value(self, mock_subprocess):
        mock_return = "abc\n" + LOG_SEPARATOR + \
            "\ndef\n" + LOG_SEPARATOR + "\n"
        expected = ["abc", "def"]
        mock_subprocess.check_output.return_value = mock_return
        eq_(expected, self.sut.log(self.commit_range, self.repo_path))

    @mock.patch('lib.git.subprocess')
    def test_log_operates_as_expected(self, mock_subprocess):
        # mock_subprocess.check_output.side_effect = log_for_tag_side_effect
        self.sut.log(self.commit_range, self.repo_path)
        mock_subprocess.check_output.assert_called_once_with(self.log_cmd)

    def test_get_tag_range_operates_as_expected(self):
        tags = ["my", "dog", "fido"]

        actual = self.sut.get_tag_range("my", tags)
        eq_("my", actual)

        actual = self.sut.get_tag_range("dog", tags)
        eq_("my..dog", actual)

    @raises(ValueError)
    def test_get_tag_range_raises_ValueError_when_tag_not_found(self):
        tags = ["my", "dog", "fido"]
        self.sut.get_tag_range("tag", tags)

    @mock.patch('lib.git.subprocess')
    def test_add_calls_check_output_as_expected(self, mock_subprocess):
        self.sut.add(self.file, self.repo_path)
        ok_(mock_subprocess.check_output.called)
        mock_subprocess.check_output.assert_called_once_with(self.add_cmd)

    @mock.patch('lib.git.subprocess')
    def test_commit_calls_check_output_as_expected(self, mock_subprocess):
        self.sut.commit(self.message, self.repo_path)
        ok_(mock_subprocess.check_output.called)
        mock_subprocess.check_output.assert_called_once_with(self.cmt_cmd)

    @mock.patch('lib.git.subprocess')
    def test_push_calls_check_output_as_expected(self, mock_subprocess):
        remote = "myremote"
        branch = "mybranch"
        push_cmd = self.push_cmd
        push_cmd.append(remote)
        push_cmd.append(branch)

        self.sut.push(remote, branch, self.repo_path)
        ok_(mock_subprocess.check_output.called)
        mock_subprocess.check_output.assert_called_once_with(push_cmd)

    @mock.patch('lib.git.subprocess')
    def test_pull_calls_check_output_as_expected(self, mock_subprocess):
        remote = "myremote"
        branch = "mybranch"
        pull_cmd = self.pull_cmd
        pull_cmd.append(remote)
        pull_cmd.append(branch)

        self.sut.pull(remote, branch, self.repo_path)
        ok_(mock_subprocess.check_output.called)
        mock_subprocess.check_output.assert_called_once_with(pull_cmd)

    @mock.patch('lib.git.subprocess')
    def test_fetch_calls_check_output_as_expected(self, mock_subprocess):
        remote = "myremote"
        fetch_cmd = self.fetch_cmd
        fetch_cmd[4] = remote

        self.sut.fetch(remote, self.repo_path)
        ok_(mock_subprocess.check_output.called)
        mock_subprocess.check_output.assert_called_once_with(fetch_cmd)

    @mock.patch('lib.git.subprocess')
    def test_checkout_calls_check_output_as_expected(self, mock_subprocess):
        branch = "mybranch"
        checkout_cmd = self.checkout_cmd
        checkout_cmd.append(branch)

        self.sut.checkout(branch, self.repo_path)
        ok_(mock_subprocess.check_output.called)
        mock_subprocess.check_output.assert_called_once_with(checkout_cmd)

    @mock.patch('lib.git.util')
    def test_get_tags_by_pattern_operates_as_expected(self, mock_util):
        pattern = "tag11"
        tags = ["tag1", "tag11", "tag21"]
        self.sut.tag = mock.MagicMock()
        self.sut.tag.return_value = tags

        mock_util.string_has_pattern.side_effect = [False, True, False]

        actual = self.sut.get_tags_by_pattern(pattern, self.repo_path)
        self.sut.tag.assert_called_once_with(self.repo_path)
        eq_(3, mock_util.string_has_pattern.call_count)
        eq_([tags[1]], actual)
