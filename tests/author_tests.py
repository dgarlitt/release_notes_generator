import mock
from nose.tools import eq_, ok_
from lib.properties import Properties
from lib.author import Author, Authors


class TestAuthorClass:

    def setup(self):
        self.sut = Author()
        self.sut.name = "Bob Dole"
        self.sut.email = "bob@dole.com"

    def test_name_and_email_in_constructor_works_and_eq_works(self):
        self.sut2 = Author("Bob Dole", "bob@dole.com")
        eq_(self.sut, self.sut2)

    def test_add_commit(self):
        self.sut.add_commit()
        eq_(1, self.sut.commits)
        self.sut.add_commit()
        eq_(2, self.sut.commits)

    def test_add_commit_with_ticket(self):
        self.sut.add_commit_with_ticket()
        eq_(1, self.sut.commits_with_tickets)
        self.sut.add_commit_with_ticket()
        eq_(2, self.sut.commits_with_tickets)

    def test_add_commit_formatted_correctly(self):
        self.sut.add_commit_formatted_correctly()
        eq_(1, self.sut.commits_formatted_correctly)
        self.sut.add_commit_formatted_correctly()
        eq_(2, self.sut.commits_formatted_correctly)

    def test_str_works_correctly(self):
        expected = "\n".join([
            "### Bob Dole <bob@dole.com>",
            "#### Commits",
            " - total: 0",
            " - with ticket number: 0",
            " - formatted correctly: 0",
            ""
        ])

        eq_(expected, str(self.sut))


class TestAuthorsClass:

    def setup(self):
        self.a1 = Author("Bob Dole", "bob@dole.com")
        self.a2 = Author("Joe Schmoe", "joe@schmoe.com")
        self.sut = Authors()

    def test_find_returns_correctly(self):
        eq_(self.a1, self.sut.find(self.a1.name, self.a1.email))
        eq_(self.a1, self.sut.find(self.a1.name, self.a1.email))
        eq_(self.a2, self.sut.find(self.a2.name, self.a2.email))

    def test_str_works_correctly(self):
        self.sut.find(self.a1.name, self.a1.email)
        self.sut.find(self.a2.name, self.a2.email)

        expected = "\n".join([
            "## Authors (2)",
            "***",
            ""
        ])

        expected += str(self.a1)
        expected += "\n***\n"
        expected += str(self.a2)
        expected += "\n***\n"

        eq_(expected, str(self.sut))
