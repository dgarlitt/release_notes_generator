class Tickets(object):

    def __init__(self):
        self._tickets = set()

    def __str__(self):
        out = "\n".join([
            "## Tickets (" + str(len(self.tickets)) + ")",
            "***",
            ""
        ])

        for ticket in sorted(list(self.tickets)):
            out += str(ticket)
            out += "\n***\n"

        return out

    def find(self, name):
        for ticket in self.tickets:
            if ticket.name == name.upper():
                return ticket
        ticket = Ticket(name)
        self.tickets.add(ticket)
        return ticket

    @property
    def tickets(self):
        return self._tickets


class Ticket(object):

    def __init__(self, name):
        self._name = name.upper()
        self._ticket_url = None

        self._commits = 0
        self._authors = []

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __cmp__(self, other):
        return cmp(self.name, other.name)

    def __str__(self):
        out = self.__fmt_name() + " (" + str(self.commits) + " commits)"

        for author in self.authors:
            out += self.__fmt_author(author)

        return out + "\n"

    def __fmt_name(self):
        author = "[__" + self.name.upper() + "__]"
        author += "(" + self.ticket_url + self.name.upper() + ")"
        return author

    def __fmt_author(self, author):
        return "\n   - " + author["name"] + " <" + author["email"] + ">"

    def add_author(self, name, email):
        author = {
            "name": name,
            "email": email
        }
        if author not in self.authors:
            self.authors.append(author)

    def increment_commits(self):
        self._commits += 1

    @property
    def authors(self):
        return self._authors

    @property
    def name(self):
        return self._name

    @property
    def ticket_url(self):
        return self._ticket_url

    @ticket_url.setter
    def ticket_url(self, value):
        self._ticket_url = value

    @property
    def commits(self):
        return self._commits
