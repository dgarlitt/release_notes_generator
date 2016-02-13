import re


class Commits(object):

    def __init__(self, commit_list):
        self._commits = commit_list

    def __str__(self):
        out = "\n".join([
            "## Commits (" + str(len(self.commits)) + ")",
            "***",
            ""
        ])

        for commit in self.commits:
            out += str(commit)
            out += "\n***\n"

        return out

    @property
    def commits(self):
        return self._commits


class Commit(object):

    def __init__(self):
        self._cid = None
        self._name = None
        self._email = None
        self._date = None
        self._subject = None
        self._body = None
        self._props = None

    def __str__(self):
        out = "\n".join([
            "### " + self.__fmt_subject(),
            "",
            " - __commit:__ " + self.__fmt_cid(),
            " - __author:__ " + self.__fmt_author(),
            " - __date:__ " + self.date,
            "",
            self.__fmt_body(),
            ""
        ])

        return out

    def __hash__(self):
        return hash(self.cid)

    def __eq__(self, other):
        return self.cid == other.cid

    def __fmt_cid(self):
        repo_web_url = self.props.repo_web_url
        return "[" + self.cid + "](" + repo_web_url + "commit/" + self.cid + ")"

    def __fmt_author(self):
        return self.name + " <" + self.email + ">"

    def __fmt_subject(self):
        ticket_pattern = self.props.ticket_pattern
        ticket_url = self.props.ticket_url
        return re.sub(r"(" + ticket_pattern + ")",
                      r"[\1](" + ticket_url + r"\1)",
                      self.subject)

    def __fmt_body(self):
        body = self.body.strip()
        if len(body) == 0:
            return ""
        body = self.body.split("\n")
        body = ['> ' + line for line in body]
        return re.sub(r"([-{3,}|*{3,}|={3,}])", "", "\n".join(body))

    def is_formatted_correctly(self):
        subj_correct = len(self.subject) <= 50
        body_correct = len(self.body) > 1
        return subj_correct and body_correct

    def has_ticket_reference(self):
        subj = re.search(self.props.ticket_pattern, self.subject) != None
        body = re.search(self.props.ticket_pattern, self.body) != None
        return subj or body

    def get_ticket_number(self):
        pattern = "(" + self.props.ticket_pattern + ")"
        if re.search(pattern, self.subject) != None:
            return re.search(pattern, self.subject).group(0)
        if re.search(pattern, self.body) != None:
            return re.search(pattern, self.body).group(0)

        return None

    @property
    def cid(self):
        return self._cid

    @cid.setter
    def cid(self, value):
        self._cid = value

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
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    @property
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self, value):
        self._subject = value

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, value):
        self._body = value

    @property
    def props(self):
        return self._props

    @props.setter
    def props(self, value):
        self._props = value
