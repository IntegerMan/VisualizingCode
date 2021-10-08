from pydriller import Repository


def get_file_modifications(path):
    """
    Analyzes a git repository and returns a tuple containing the combinations of files modified and path combinations
    :param path: the git repository URL
    :return: a tuple containing path combinations and file modifications.
    """

    combinations = []
    modifications = []

    for commit in Repository(path).traverse_commits():
        paths = []
        for file in commit.modified_files:
            paths.append(file.new_path)
            record = {
                'path': file.new_path,
                'commit': commit.hash,
                'author': commit.author.name,
                'lines_added': file.added_lines,
                'lines_deleted': file.deleted_lines,
            }
            modifications.append(record)
        combinations.append({'hash': commit.hash, 'paths': paths}
                            )

    return combinations, modifications
