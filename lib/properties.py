import json
import re

from lib.validators import RegexValidator
from lib import util


class Properties:

    def __init__(self, script_root, property_file):
        self.__script_root = script_root
        self._property_file = property_file
        self.__load_properties()

        msg = "Version number does not match pattern: "
        msg += self.version_num_pattern
        self._version_num_validator = RegexValidator(
            self.version_num_pattern, msg)

    def __load_properties(self):
        with open(self._property_file, 'r') as property_file:
            props = json.load(property_file)

            self._version_num_pattern = props["version_number_pattern"]

            matching = props["tag_matching"]
            self._tag_prefix = prefix = matching["prefix"]
            self._tag_suffix = suffix = matching["suffix"]
            tag_pattern = prefix + self._version_num_pattern + suffix
            self._tag_pattern = "^" + tag_pattern + "$"

            exclude = props["exclude_commits"]
            self._excluded_emails = exclude["from_email"]
            self._exclude_commits_containing_version_num = exclude[
                "containing_version_number"]

            project = props["project"]
            self._project_name = project["name"]
            self._project_path = util.unify_paths(
                self.__script_root, project["path"])
            self._repo_web_url = util.sanitize_path(project["repo_web_url"])

            git = project["git"]
            self._project_remote = git["remote"]

            tickets = props["tickets"]
            self._ticket_pattern = tickets["pattern"]
            self._ticket_url = util.sanitize_path(tickets["url"])

            wiki = props["wiki"]
            self.wiki_path = util.unify_paths(self.__script_root, wiki["path"])

            release_notes = wiki["release_notes"]
            self._release_notes_index = release_notes["index"]
            self._release_notes_archive = util.sanitize_path(
                release_notes["archive"])
            self._release_notes_archive = util.sanitize_subpath(
                self.release_notes_archive)

            git = wiki["git"]
            self._wiki_remote = git["remote"]
            self._wiki_branch = git["branch"]

    def get_tag_name_from_version_num(self, version_num):
        return self.tag_prefix + version_num + self.tag_suffix

    def get_version_num_from_tag_name(self, tag_name):
        return util.get_pattern_from_string(tag_name, self.version_num_pattern)

    def validate_version_num(self, version_num):
        return self._version_num_validator(version_num)

    @property
    def version_num_pattern(self):
        return self._version_num_pattern

    @property
    def tag_pattern(self):
        return self._tag_pattern

    @property
    def tag_prefix(self):
        return self._tag_prefix

    @property
    def tag_suffix(self):
        return self._tag_suffix

    @property
    def project_name(self):
        return self._project_name

    @property
    def project_path(self):
        return self._project_path

    @property
    def project_remote(self):
        return self._project_remote

    @property
    def repo_web_url(self):
        return self._repo_web_url

    @property
    def ticket_pattern(self):
        return self._ticket_pattern

    @property
    def ticket_url(self):
        return self._ticket_url

    @property
    def wiki_path(self):
        return self._wiki_path

    @property
    def release_notes_index(self):
        return self._release_notes_index

    @property
    def release_notes_archive(self):
        return self._release_notes_archive

    @property
    def wiki_remote(self):
        return self._wiki_remote

    @property
    def wiki_branch(self):
        return self._wiki_branch

    @property
    def excluded_emails(self):
        return self._excluded_emails

    @property
    def exclude_commits_containing_version_num(self):
        return self._exclude_commits_containing_version_num
