import mock
from nose.tools import eq_, ok_, assert_is_none
from lib.properties import Properties
from lib.ticket import Ticket, Tickets


class TestTicketClass:

    def setup(self):
        self.name = "TIK-1111"
        self.sut = Ticket(self.name)

    def teardown(self):
        self.name = None
        self.sut = None

    def test_init_works_as_expected(self):
        eq_(self.name, self.sut.name)
        assert_is_none(self.sut.ticket_url)
        eq_(0, self.sut.commits)
        eq_([], self.sut.authors)

    def test_add_author_doesnt_allow_duplicates(self):
        name = "Bob Dole"
        email = "bob@dole.com"

        self.sut.add_author(name, email)
        eq_(1, len(self.sut.authors))

        self.sut.add_author(name, email)
        eq_(1, len(self.sut.authors))

    def test_increment_commits_works(self):
        eq_(0, self.sut.commits)
        self.sut.increment_commits()
        eq_(1, self.sut.commits)
        self.sut.increment_commits()
        eq_(2, self.sut.commits)

    def test_str_works_as_expected(self):
        self.sut.add_author("Bob Dole", "bob@dole.com")
        self.sut.add_author("Tommy The Cat", "tommy@thecat.com")
        self.sut.increment_commits()
        self.sut.increment_commits()
        self.sut.ticket_url = "http://tickets/"

        expected = "\n".join([
            "[__TIK-1111__](http://tickets/TIK-1111) (2 commits)",
            "   - Bob Dole <bob@dole.com>",
            "   - Tommy The Cat <tommy@thecat.com>",
            ""
        ])

        eq_(expected, str(self.sut))

    def test_eq_works_as_expected(self):
        sut1 = self.sut
        sut2 = Ticket(self.name)

        eq_(sut1, sut2)


class TestTicketsClass:

    def setup(self):

        self.t1 = Ticket("ticket1")
        self.t2 = Ticket("ticket2")

        self.sut = Tickets()

    def test_find_works_as_expected(self):
        eq_(self.t1, self.sut.find(self.t1.name))
        eq_(self.t1, self.sut.find(self.t1.name))
        eq_(self.t2, self.sut.find(self.t2.name))

    def test__str__and__cmp__works_as_expected(self):
        ticket_url = "abc/"

        t1 = self.sut.find(self.t1.name)
        t1.ticket_url = ticket_url

        t2 = self.sut.find(self.t2.name)
        t2.ticket_url = ticket_url

        expected = "\n".join([
            "## Tickets (2)",
            "***",
            ""
        ])

        expected += str(t1)
        expected += "\n***\n"
        expected += str(t2)
        expected += "\n***\n"

        eq_(expected, str(self.sut))
