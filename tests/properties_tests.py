import mock
from nose.tools import eq_, ok_, raises
from lib.properties import Properties


def unify_paths_side_effect(root, path):
    return root + path


def sanitize_path_side_effect(path):
    return path + "/"


def sanitize_subpath_side_effect(path):
    return path[1:]


class TestProperties():

    @mock.patch('lib.properties.util')
    @mock.patch('lib.properties.json')
    @mock.patch('__builtin__.open', spec=open, read_data='some raw json')
    def setup(self, mock_open, mock_json, mock_util):
        self.prop_file = '/path/to/props.json'
        self.file_action = 'r'
        self.prefix = "proj-"
        self.suffix = ""
        self.script_root = "/script/root/"
        self.props = {
            "version_number_pattern": "1\.2\.3\.4",
            "tag_matching": {
                "prefix": self.prefix,
                "suffix": self.suffix
            },
            "exclude_commits": {
                "from_email": ["bob@dole.com"],
                "containing_version_number": True
            },
            "tickets": {
                "pattern": "ticket pattern",
                "url": "ticket url"
            },
            "project": {
                "name": "PROJ",
                "path": "../proj/path",
                "repo_web_url": "http://repo_web_url",
                "git": {
                    "remote": "origin"
                }
            },
            "wiki": {
                "path": "../wiki/path",
                "release_notes": {
                    "index": "/release/notes/index.md",
                    "archive": "/release/notes/archive"
                },
                "git": {
                    "remote": "origin",
                    "branch": "master"
                }
            }
        }

        mock_json.load.return_value = self.props
        mock_util.unify_paths.side_effect = unify_paths_side_effect
        mock_util.sanitize_path.side_effect = sanitize_path_side_effect
        mock_util.sanitize_subpath.side_effect = sanitize_subpath_side_effect
        self.sut = Properties(self.script_root, self.prop_file)

        self.mock_open = mock_open
        self.mock_json = mock_json
        self.mock_util = mock_util

    def test_init_loads_props(self):
        ok_(self.mock_open.called)
        self.mock_open.assert_called_with(self.prop_file, self.file_action)

        ok_(self.mock_json.load.called)
        self.mock_json.load.assert_called_with(self.mock_open().__enter__())

    def test_init_load_props_sets_values_as_expected(self):
        expected = self.props["version_number_pattern"]
        eq_(expected, self.sut.version_num_pattern)

        expected = "^" + self.prefix + expected + self.suffix + "$"
        eq_(expected, self.sut.tag_pattern)

        excl = self.props["exclude_commits"]
        eq_(excl["from_email"], self.sut.excluded_emails)
        eq_(excl["containing_version_number"],
            self.sut.exclude_commits_containing_version_num)

        proj = self.props["project"]
        eq_(proj["name"], self.sut.project_name)
        eq_(self.script_root + proj["path"], self.sut.project_path)
        eq_(proj["repo_web_url"] + "/", self.sut.repo_web_url)

        git = proj["git"]
        eq_(git["remote"], self.sut.project_remote)

        tick = self.props["tickets"]
        eq_(tick["pattern"], self.sut.ticket_pattern)
        eq_(tick["url"] + "/", self.sut.ticket_url)

        wiki = self.props["wiki"]
        eq_(self.script_root + wiki["path"], self.sut.wiki_path)

        release_notes = wiki["release_notes"]
        expected = release_notes["index"]
        eq_(expected, self.sut.release_notes_index)
        expected = release_notes["archive"][1:] + "/"
        eq_(expected, self.sut.release_notes_archive)

        git = wiki["git"]
        eq_(git["remote"], self.sut.wiki_remote)
        eq_(git["branch"], self.sut.wiki_branch)

    def test_get_tag_name_from_version_num_returns_as_expected(self):
        expected = self.prefix + "1.2.3.4" + self.suffix
        actual = self.sut.get_tag_name_from_version_num("1.2.3.4")
        eq_(expected, actual)

    def test_get_version_num_from_tag_name_returns_as_expected(self):
        string = "tagnamewith1.2.3.4init"
        eq_("1.2.3.4", self.sut.get_version_num_from_tag_name(string))

    def test_validate_version_num_returns_as_expected(self):
        vnum = "1.2.3.4"
        eq_(vnum, self.sut.validate_version_num(vnum))
