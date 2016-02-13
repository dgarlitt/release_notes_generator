import re
import time
from lib import util

SEPARATOR = "\n<!-- *** -->\n"


class ReleaseNotesIndex(object):

    def __init__(self, props):
        self._props = props
        self._absolute_filepath = props.wiki_path + props.release_notes_index
        self._versions = []

    def __str__(self):
        props = self.props
        out = "\n".join([
            "# " + props.project_name + " Release Notes Index", "---",
            SEPARATOR
        ])

        for version in self.versions:
            out += "\n##### [" + version + "]"
            out += "(" + props.release_notes_archive
            out += version.replace(".", "_") + ".md)\n"

        out += "\n".join([
            SEPARATOR,
            "---", "", "Updated: " + time.strftime("%c"), ""
        ])

        return out

    def generate(self, version_num):
        self._version_num = version_num
        body = self.__get_body_from_file()
        self._versions = self.__get_version_list(body)

    @property
    def version_num(self):
        return self._version_num

    @property
    def props(self):
        return self._props

    @property
    def absolute_filepath(self):
        return self._absolute_filepath

    @property
    def versions(self):
        return self._versions

    #######################
    ### Private Methods ###
    #######################

    def __get_version(self, string):
        found = re.search(self.props.version_num_pattern, string)
        if found != None:
            return found.group(0)

    def __get_version_list(self, body):
        if len(body) == 0:
            return [self.version_num]

        items = body.split("\n")
        items = [item for item in items if len(item) > 0]
        versions = [self.__get_version(item) for item in items]
        if self.version_num not in versions:
            versions.append(self.version_num)

        return sorted(versions)[::-1]

    def __get_body_from_file(self):
        if not util.file_exists(self.absolute_filepath):
            return ""

        file_content = util.read_file(self.absolute_filepath)
        sections = file_content.split(SEPARATOR)

        if len(sections) > 1:
            return sections[1]

        return ""
