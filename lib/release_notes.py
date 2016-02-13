import json
from lib import util
from lib.commit import Commit, Commits
from lib.author import Author, Authors
from lib.ticket import Ticket, Tickets
from lib.git import SEP


class ReleaseNotes(object):

    def __init__(self, props):
        self._props = props
        self._version_num = None
        self._commits = None
        self._authors = None
        self._tickets = None
        self._filename = None
        self._absolute_filepath = None

    def __str__(self):
        props = self.props
        tag_name = props.get_tag_name_from_version_num(self.version_num)
        tag_url = props.repo_web_url + "commits/" + tag_name
        tag_link = "[" + self.version_num + "](" + tag_url + ")"

        out = "# " + props.project_name + " " + tag_link + " Release Notes"
        out += "\n***"
        out += "\n  "
        out += "\n"
        out += str(self.tickets)
        out += "\n"
        out += str(self.commits)
        out += "\n"
        out += str(self.authors)

        return out

    def generate(self, version_num, log):
        props = self.props
        self._version_num = version_num
        self._filename = self.version_num.replace(".", "_") + ".md"
        self._absolute_filepath = (props.wiki_path +
                                   props.release_notes_archive +
                                   self.filename)

        self.__load_commits_from_log(log)
        self.__load_authors_from_commits()
        self.__load_tickets_from_commits()

    @property
    def props(self):
        return self._props

    @property
    def version_num(self):
        return self._version_num

    @property
    def commits(self):
        return self._commits

    @property
    def authors(self):
        return self._authors

    @property
    def tickets(self):
        return self._tickets

    @property
    def filename(self):
        return self._filename

    @property
    def absolute_filepath(self):
        return self._absolute_filepath

    #######################
    ### Private Methods ###
    #######################

    def __load_commits_from_log(self, log):
        commits = [self.__to_commit(i) for i in log]
        commits = Commits(self.__filter_commits(commits))
        self._commits = commits

    def __to_commit(self, commit_str):
        commit_list = commit_str.split(SEP, 6)
        commit = Commit()
        commit.cid = commit_list[0]
        commit.name = commit_list[1]
        commit.email = commit_list[2]
        commit.date = commit_list[3]
        commit.subject = commit_list[4]
        commit.body = commit_list[5]
        commit.props = self.props
        return commit

    def __filter_commits(self, commits):
        emails = self.props.excluded_emails
        commits = util.filter_commits_by_email(emails, commits)

        if self.props.exclude_commits_containing_version_num:
            vnum = self.version_num
            commits = util.filter_commits_by_version_num(vnum, commits)

        return commits

    def __load_authors_from_commits(self):
        self._authors = Authors()
        for commit in self.commits.commits:
            author = self.authors.find(commit.name, commit.email)
            self.__update_author_stats(author, commit)

    def __update_author_stats(self, author, commit):
        author.add_commit()
        if commit.is_formatted_correctly():
            author.add_commit_formatted_correctly()
        if commit.has_ticket_reference():
            author.add_commit_with_ticket()

    def __load_tickets_from_commits(self):
        tickets = Tickets()
        for commit in self.commits.commits:
            if commit.has_ticket_reference():
                ticket_name = commit.get_ticket_number()
                ticket = tickets.find(ticket_name)
                ticket.increment_commits()
                ticket.add_author(commit.name, commit.email)
                ticket.ticket_url = self.props.ticket_url

        self._tickets = tickets
