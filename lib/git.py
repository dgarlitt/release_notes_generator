import subprocess
import re
from lib.commit import Commit
from lib import util

SEP = '|||<<<(((ooo+++ooo)))>>>|||'
LOG_SEPARATOR = '---END-COMMIT-FOR-RELEASE-NOTES---'
LOG_PRETTY = '--pretty=format:%H' + SEP
LOG_PRETTY += '%an' + SEP + '%ae' + SEP + '%cd' + SEP + '%s' + SEP + '%b'
LOG_PRETTY += LOG_SEPARATOR

GIT_PREF = ['git', '--git-dir=____', '--work-tree=____']

TAG_CMD = tuple(GIT_PREF + ['tag'])
LOG_CMD = tuple(GIT_PREF + ['log', '--date=short', LOG_PRETTY, '--no-merges'])
ADD_CMD = tuple(GIT_PREF + ['add'])
CMT_CMD = tuple(GIT_PREF + ['commit', '-m'])
PUSH_CMD = tuple(GIT_PREF + ['push'])
PULL_CMD = tuple(GIT_PREF + ['pull', '--ff-only'])
FETCH_CMD = tuple(GIT_PREF + ['fetch', '', '--tags'])
CHECKOUT_CMD = tuple(GIT_PREF + ['checkout'])


class Git:

    def __map_cmd(self, cmd, path):
        cmd = list(cmd)
        cmd[1] = cmd[1].replace('____', path + '.git')
        cmd[2] = cmd[2].replace('____', path)
        return cmd

    def tag(self, repo_path):
        cmd = self.__map_cmd(TAG_CMD, repo_path)
        tags = subprocess.check_output(cmd)
        return tags.split("\n")

    def log(self, commit_range, repo_path):
        cmd = self.__map_cmd(LOG_CMD, repo_path)
        cmd.append(commit_range)
        log_str = subprocess.check_output(cmd)
        log = [item.strip() for item in log_str.split(LOG_SEPARATOR)]
        return log[:-1]  # trim the empty element from the end

    def add(self, filename, repo_path):
        cmd = self.__map_cmd(ADD_CMD, repo_path)
        cmd.append(str(filename))
        subprocess.check_output(cmd)

    def commit(self, message, repo_path):
        cmd = self.__map_cmd(CMT_CMD, repo_path)
        cmd.append('"' + message + '"')
        subprocess.check_output(cmd)

    def push(self, remote, branch, repo_path):
        cmd = self.__map_cmd(PUSH_CMD, repo_path)
        cmd.append(remote)
        cmd.append(branch)
        subprocess.check_output(cmd)

    def pull(self, remote, branch, repo_path):
        cmd = self.__map_cmd(PULL_CMD, repo_path)
        cmd.append(remote)
        cmd.append(branch)
        subprocess.check_output(cmd)

    def fetch(self, remote, repo_path):
        cmd = self.__map_cmd(FETCH_CMD, repo_path)
        cmd[4] = remote
        subprocess.check_output(cmd)

    def checkout(self, branch, repo_path):
        cmd = self.__map_cmd(CHECKOUT_CMD, repo_path)
        cmd.append(branch)
        subprocess.check_output(cmd)

    def get_tags_by_pattern(self, pattern, repo_path):
        tags = self.tag(repo_path)
        return [t for t in tags if util.string_has_pattern(t, pattern)]

    def get_tag_range(self, tag, tags):
        for idx, val in enumerate(tags):
            if val == tag:
                # if it's the first tag, just use the tag name
                # otherwise, use "previous_tag..tag"
                return tag if idx == 0 else tags[idx - 1] + ".." + tag

        raise ValueError('tag ' + tag + ' could not be found')
