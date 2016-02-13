import mock
from nose.tools import eq_, ok_, assert_is_none
from lib.properties import Properties
from lib.commit import Commit, Commits


class TestCommitClass:

    @mock.patch('lib.properties.Properties')
    def setup(self, mock_props):
        mock_props.ticket_pattern = 'TIK-1111'
        mock_props.ticket_url = 'http://tikurl/'
        mock_props.repo_web_url = 'http://repourl/'

        self.sut = Commit()
        self.sut.cid = 'abcdef1234567890'
        self.sut.name = 'Bob Dole'
        self.sut.email = 'bob@dole.com'
        self.sut.date = '01/02/03'
        self.sut.subject = 'TIK-1111 - The commit subject'
        self.sut.body = 'This is the body\nthis is more of the body\nand more'
        self.sut.props = mock_props

    def test_to_str_formats_output_as_expected(self):
        expected = "\n".join([
            "### [TIK-1111](http://tikurl/TIK-1111) - The commit subject",
            "",
            " - __commit:__ [abcdef1234567890](http://repourl/commit/abcdef1234567890)",
            " - __author:__ Bob Dole <bob@dole.com>",
            " - __date:__ 01/02/03",
            "",
            "> This is the body",
            "> this is more of the body",
            "> and more",
            ""
        ])

        eq_(expected, str(self.sut))

    def test_is_formatted_correctly_returns_true(self):
        ok_(self.sut.is_formatted_correctly())

    def test_is_formatted_correctly_returns_false(self):
        self.sut.subject = "This subject is way too damn long! It just keeps going!"
        ok_(not self.sut.is_formatted_correctly())

        self.sut.subject = "This is a shorter subject"
        self.sut.body = ""
        ok_(not self.sut.is_formatted_correctly())

    def test_has_ticket_reference_returns_as_expected(self):
        ok_(self.sut.has_ticket_reference())

        self.sut.subject = "This is a subject"
        ok_(not self.sut.has_ticket_reference())

        self.sut.body = "This is a body with a ticket reference TIK-1111 in it"
        ok_(self.sut.has_ticket_reference)

    def test_get_ticket_number_returns_as_expected(self):
        eq_("TIK-1111", self.sut.get_ticket_number())

        self.sut.subject = "This is a subject"
        assert_is_none(self.sut.get_ticket_number())

        self.sut.body = "This is a body with a ticket reference TIK-1111 in it"
        eq_("TIK-1111", self.sut.get_ticket_number())

    def test_eq_works_as_expected(self):
        sut1 = self.sut
        sut2 = Commit()
        sut2.cid = sut1.cid

        eq_(sut1, sut2)

    def test_hash_works_as_expected(self):
        eq_(hash("abcdef1234567890"), hash(self.sut))


class TestCommitsClass:

    def setup(self):
        self.mock_c1 = "Commit One"
        self.mock_c2 = "Commit Two"
        self.commits = [self.mock_c1, self.mock_c2]
        self.sut = Commits(self.commits)

    def test_str_formats_output_as_expected(self):
        expected = "\n".join([
            "## Commits (2)",
            "***",
            "Commit One",
            "***",
            "Commit Two",
            "***",
            ""
        ])

        eq_(expected, str(self.sut))
