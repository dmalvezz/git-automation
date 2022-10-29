
def get_staged_files(repo):
    return [item.a_path for item in repo.index.diff('HEAD')]

def get_changed_files(repo):
    return [item.a_path for item in repo.index.diff(None)]

def get_untracked_files(repo):
    return repo.untracked_files