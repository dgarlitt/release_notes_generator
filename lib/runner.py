from lib import util


class Runner(object):

    def __init__(self):
        self._commit_and_push = True
        self._version_num = None
        self._props = None
        self._git = None
        self._release_notes = None
        self._index = None
        self._repos_updated = False

    def run(self, version_num):
        self._version_num = self.props.validate_version_num(version_num)

        self.__update_local_repos()
        self.__generate_release_notes()
        self.__generate_index()

        if self.commit_and_push:
            self.__commit_and_push()

    def run_all(self):
        self.__generate_all_release_notes()

    @property
    def commit_and_push(self):
        return self._commit_and_push

    @property
    def version_num(self):
        return self._version_num

    @property
    def props(self):
        return self._props

    @property
    def git(self):
        return self._git

    @property
    def release_notes(self):
        return self._release_notes

    @property
    def index(self):
        return self._index

    @property
    def repos_updated(self):
        return self._repos_updated

    @commit_and_push.setter
    def commit_and_push(self, value):
        self._commit_and_push = value

    @props.setter
    def props(self, value):
        self._props = value

    @git.setter
    def git(self, value):
        self._git = value

    @release_notes.setter
    def release_notes(self, value):
        self._release_notes = value

    @index.setter
    def index(self, value):
        self._index = value

    #######################
    ### Private Methods ###
    #######################

    def __update_local_repos(self):
        if not self.repos_updated:
            props = self.props
            git = self.git

            git.fetch(props.project_remote, props.project_path)
            git.checkout(props.wiki_branch, props.wiki_path)
            git.pull(props.wiki_remote, props.wiki_branch, props.wiki_path)

            self._repos_updated = True

    def __get_commit_log(self):
        props = self.props
        git = self.git

        tag = props.get_tag_name_from_version_num(self.version_num)
        tags = git.get_tags_by_pattern(props.tag_pattern, props.project_path)
        commit_range = git.get_tag_range(tag, tags)
        log = git.log(commit_range, props.project_path)

        return log

    def __generate_release_notes(self):
        log = self.__get_commit_log()
        self.release_notes.generate(self.version_num, log)
        util.write_file(self.release_notes.absolute_filepath,
                        str(self.release_notes))
        self.git.add(self.release_notes.absolute_filepath,
                     self.props.wiki_path)

    def __generate_index(self):
        self.index.generate(self.version_num)
        util.write_file(self.index.absolute_filepath, str(self.index))
        self.git.add(self.index.absolute_filepath, self.props.wiki_path)

    def __commit_and_push(self):
        prop = self.props
        message = "Add release notes for " + self.version_num
        self.git.commit(message, prop.wiki_path)
        self.git.push(prop.wiki_remote, prop.wiki_branch, prop.wiki_path)

    def __generate_all_release_notes(self):
        props = self.props
        git = self.git

        self.commit_and_push = False

        tags = git.get_tags_by_pattern(props.tag_pattern, props.project_path)
        for idx, tag in enumerate(tags):
            vnum = props.get_version_num_from_tag_name(tag)
            if idx == len(tags) - 1:
                self.commit_and_push = True
            self.run(vnum)
