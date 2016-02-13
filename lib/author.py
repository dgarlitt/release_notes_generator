class Authors(object):

    def __init__(self):
        self._authors = set()

    def __str__(self):
        out = "\n".join([
            "## Authors (" + str(len(self.authors)) + ")",
            "***",
            ""
        ])

        for author in sorted(list(self.authors)):
            out += str(author)
            out += "\n***\n"

        return out

    def find(self, name, email):
        for author in self.authors:
            if author.email == email:
                return author
        author = Author(name, email)
        self.authors.add(author)
        return author

    @property
    def authors(self):
        return self._authors


class Author(object):

    def __init__(self, name=None, email=None):
        self._name = name
        self._email = email
        self._commits = 0
        self._commits_with_tickets = 0
        self._commits_formatted_correctly = 0

    def __str__(self):
        return "\n".join([
            "### " + self.name + " <" + self.email + ">",
            "#### Commits",
            " - total: " + str(self.commits),
            " - with ticket number: " + str(self.commits_with_tickets),
            " - formatted correctly: " + str(self.commits_formatted_correctly),
            ""
        ])

    def __hash__(self):
        return hash((self.name, self.email))

    def __eq__(self, other):
        return self.email == other.email

    def __cmp__(self, other):
        return cmp(self.name, other.name)

    def add_commit(self):
        self._commits += 1

    def add_commit_with_ticket(self):
        self._commits_with_tickets += 1

    def add_commit_formatted_correctly(self):
        self._commits_formatted_correctly += 1

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def commits(self):
        return self._commits

    @property
    def commits_with_tickets(self):
        return self._commits_with_tickets

    @property
    def commits_formatted_correctly(self):
        return self._commits_formatted_correctly
