import os
import re


def string_has_pattern(string, pattern):
    found = re.search(pattern, string)
    return found != None


def get_pattern_from_string(string, pattern):
    found = re.search(pattern, string)
    return found.group(0) if found != None else None


def filter_commits_by_email(emails, commits):
    for email in emails:
        commits = [c for c in commits if email != c.email]

    return commits


def filter_commits_by_version_num(vnum, commits):
    commits = [c for c in commits if vnum not in c.subject]
    return [c for c in commits if vnum not in c.body]


def unify_paths(root, path):
    result = os.path.join(root, path)
    result = os.path.normpath(result)
    return sanitize_path(result)


def sanitize_path(path):
    path = path.encode('utf-8')
    return path if path.endswith("/") else path + "/"


def sanitize_subpath(path):
    path = path.encode('utf-8')
    return path[1:] if path.startswith("/") else path


def read_file(filename):
    with open(filename) as f:
        content = f.read()

    return content


def write_file(filepath, content):
    path = get_path_from_filepath(filepath)

    if not directory_exists(path):
        os.makedirs(path)

    with open(filepath, 'w') as f:
        f.write(content)


def get_path_from_filepath(filepath):
    return "/".join(filepath.split("/")[:-1]) + "/"


def directory_exists(directory):
    return os.path.exists(directory)


def file_exists(filepath):
    result = os.path.isfile(filepath)
    return result
