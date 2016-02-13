import mock
from nose.tools import eq_, ok_
from tests.mocks.mock_release_notes_index import VER_NUM, MOCK_WITHOUT_VER_NUM
from tests.mocks.mock_release_notes_index import MOCK_WITH_VER_NUM, MOCK_EMPTY
from lib.properties import Properties
from lib.release_notes_index import ReleaseNotesIndex


class TestReleaseNotesIndex:

    @mock.patch('lib.properties.Properties')
    def setup(self, mock_props):
        mock_props.wiki_path = "../wiki/path/"
        mock_props.project_name = "PROJ"
        mock_props.version_num_pattern = r"\d\.\d\.\d\.\d"
        mock_props.release_notes_archive = "release-notes-archive/"

        self.sut = ReleaseNotesIndex(mock_props)

        self.mock_props = mock_props

    @mock.patch('lib.release_notes_index.util')
    def test__init__sets_defaults_appropriately(self, mock_util):
        sut = self.sut
        mock_util.file_exists.return_value = False

        sut.generate(VER_NUM)

        eq_(self.mock_props, sut.props)

        expected = self.mock_props.wiki_path + \
            self.mock_props.release_notes_index
        eq_(expected, sut.absolute_filepath)

        eq_([VER_NUM], sut.versions)

    @mock.patch('lib.release_notes_index.util')
    def test__init__when_file_is_empty(self, mock_util):
        mock_util.file_exists.return_value = True
        mock_util.read_file.return_value = MOCK_EMPTY

        self.sut.generate(VER_NUM)

        eq_([VER_NUM], self.sut.versions)

    @mock.patch('lib.release_notes_index.util')
    def test__init__when_file_exists_without_version(self, mock_util):
        mock_util.file_exists.return_value = True
        mock_util.read_file.return_value = MOCK_WITHOUT_VER_NUM

        self.sut.generate(VER_NUM)

        eq_(["3.4.5.6", "2.3.4.5", "1.2.3.4"], self.sut.versions)

    @mock.patch('lib.release_notes_index.util')
    def test__init__when_file_exists_with_version(self, mock_util):
        mock_util.file_exists.return_value = True
        mock_util.read_file.return_value = MOCK_WITH_VER_NUM

        self.sut.generate(VER_NUM)

        eq_(["3.4.5.6", "2.3.4.5", "1.2.3.4"], self.sut.versions)

    @mock.patch('lib.release_notes_index.time')
    @mock.patch('lib.release_notes_index.util')
    def test__str__works_as_expected(self, mock_util, mock_time):
        mock_time.strftime.return_value = "Thu Jun 11 16:47:37 2015"
        mock_util.file_exists.return_value = True
        mock_util.read_file.return_value = MOCK_WITH_VER_NUM

        self.sut.generate(VER_NUM)

        eq_(MOCK_WITH_VER_NUM, str(self.sut))
