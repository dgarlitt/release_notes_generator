import mock
from nose.tools import eq_, ok_
from lib.properties import Properties
from lib.commit import Commit
from lib.release_notes import ReleaseNotes
from tests.mocks.mock_git_log import MOCK_GOOD_COMMIT_1, MOCK_BAD_COMMIT_1
from tests.mocks.mock_git_log import MOCK_GIT_LOG, MOCK_RELEASE_NOTES_STR


class TestReleaseNotes:

    def to_commit(self, email, subj, body):
        ct = Commit()
        ct.email = email
        ct.subject = subj
        ct.body = body
        return ct

    @mock.patch('lib.properties.Properties')
    def setup(self, mock_props):
        self.version = '1.2.3.4'
        self.repo_path = 'abc/'
        self.tag = 'tag-' + self.version
        self.emails = ['email1', 'email2']
        ct1 = self.to_commit("bob@dole.com", "blah", "blah, blah")
        ct2 = self.to_commit(
            "bill@murray.com", "blah blah", "blah, blah, blah")
        self.commits = [ct1, ct2]
        self.filename = "1_2_3_4.md"
        self.archive = "release-notes-archive/"
        self.wiki_path = "../wiki/path/"

        mock_props.get_project_path.return_value = self.repo_path
        mock_props.get_tag_name_from_version_num.return_value = self.tag
        mock_props.project_path = self.repo_path
        mock_props.excluded_emails = self.emails
        mock_props.exclude_commits_containing_version_num = True
        mock_props.release_notes_archive = self.archive
        mock_props.wiki_path = self.wiki_path
        mock_props.version_num = self.version

        self.mock_props = mock_props

        self.sut = ReleaseNotes(mock_props)

    @mock.patch('lib.release_notes.util')
    def test_generate_sets_properties_correctly(self, mock_util):
        self.sut.generate(self.version, MOCK_GIT_LOG)
        eq_(self.mock_props, self.sut.props)
        eq_(self.filename, self.sut.filename)
        eq_(self.wiki_path + self.archive +
            self.filename, self.sut.absolute_filepath)

    @mock.patch('lib.release_notes.util')
    def test_generate_calls_composite_methods(self, mock_util):
        mock_util.filter_commits_by_email.return_value = self.commits
        self.sut.generate(self.version, MOCK_GIT_LOG)

        ok_(mock_util.filter_commits_by_email.called)
        mock_util.filter_commits_by_version_num.assert_called_with(
            self.version, self.commits)

    @mock.patch('lib.release_notes.util')
    def test_generate_does_not_exclude_by_version_number_when_false(self, mock_util):
        self.mock_props.exclude_commits_containing_version_num = False
        self.sut.generate(self.version, MOCK_GIT_LOG)
        ok_(mock_util.filter_commits_by_email.called)
        ok_(mock_util.filter_commits_by_version_num.not_called)

    def test__to_commit_returns_as_expected(self):
        ct = self.sut._ReleaseNotes__to_commit(MOCK_GOOD_COMMIT_1)
        eq_("557fec0b69228ae803c81e38f80c3b1fb993d9cb", ct.cid)
        eq_("Bob Dole", ct.name)
        eq_("bob@dole.com", ct.email)
        eq_("2015-05-20", ct.date)
        eq_("TIK-1111 - Some important change", ct.subject)
        body = "\n".join([
            "This change affects something really important and the commit message",
            "body is formatted correctly"
        ])
        eq_(body, ct.body)
        eq_(self.mock_props, ct.props)

    def test__to_commit_adds_empty_body_for_commits_without_body(self):
        ct = self.sut._ReleaseNotes__to_commit(MOCK_BAD_COMMIT_1)
        eq_("", ct.body)

    def test__load_athors_from_commits(self):
        self.mock_props.ticket_pattern = r"TIK-\d+"
        self.sut.generate(self.version, MOCK_GIT_LOG)

        authors = list(self.sut.authors.authors)
        eq_(3, len(authors))

        a1 = authors[0]
        eq_("John Rambo", a1.name)
        eq_("john@rambo.com", a1.email)
        eq_(1, a1.commits)
        eq_(0, a1.commits_with_tickets)
        eq_(0, a1.commits_formatted_correctly)

        a2 = authors[1]
        eq_("Bob Dole", a2.name)
        eq_("bob@dole.com", a2.email)
        eq_(2, a2.commits)
        eq_(2, a2.commits_with_tickets)
        eq_(2, a2.commits_formatted_correctly)

        a3 = authors[2]
        eq_("Sammy Davis Jr.", a3.name)
        eq_("sammy@davis.jr", a3.email)
        eq_(1, a3.commits)
        eq_(1, a3.commits_with_tickets)
        eq_(0, a3.commits_formatted_correctly)

    def test__load_tickets_from_commits(self):
        self.mock_props.ticket_pattern = r"TIK-\d+"
        self.mock_props.ticket_url = "http://tickets/"
        self.sut.generate(self.version, MOCK_GIT_LOG)

        tickets = sorted(list(self.sut.tickets.tickets))
        eq_(2, len(tickets))

        t1 = tickets[0]
        eq_("TIK-1111", t1.name)
        eq_(1, t1.commits)
        eq_(1, len(t1.authors))
        eq_("Bob Dole", t1.authors[0]["name"])
        eq_("bob@dole.com", t1.authors[0]["email"])

        t1 = tickets[1]
        eq_("TIK-1234", t1.name)
        eq_(2, t1.commits)
        eq_(2, len(t1.authors))
        eq_("Bob Dole", t1.authors[0]["name"])
        eq_("bob@dole.com", t1.authors[0]["email"])
        eq_("Sammy Davis Jr.", t1.authors[1]["name"])
        eq_("sammy@davis.jr", t1.authors[1]["email"])

    def __str__setup(self):
        self.mock_props.ticket_pattern = r"TIK-\d+"
        self.mock_props.ticket_url = "http://tickets/"
        self.mock_props.repo_web_url = "http://repo_web_url/"
        self.mock_props.get_tag_name_from_version_num.return_value = "tag-1.2.3.4"
        self.mock_props.project_name = "PROJ"

    def test__str__returns_as_expected(self):
        self.__str__setup()
        self.sut.generate(self.version, MOCK_GIT_LOG)

        eq_(MOCK_RELEASE_NOTES_STR, str(self.sut))
