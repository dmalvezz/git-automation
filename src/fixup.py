import argparse
import cli_ui
from fuzzywuzzy import fuzz
from git import Repo, InvalidGitRepositoryError

from utils.bash_utils import process_run
from utils.cli_utils import *
from utils.git_utils import *



def search_commit_by_message(repo, search, min_score=50):
    commit_list = []

    for commit in repo.iter_commits(repo.active_branch):
        score = fuzz.partial_ratio(search, commit.message)
        if score > min_score:
            option = "[{}][{}] {}".format(commit.hexsha[0:8], commit.author, commit.message[0:min(len(commit.message)-1, 100)])
            commit_list.append((commit.hexsha[0:8], option))

    return commit_list


if __name__ == '__main__':
    # Args
    ap = argparse.ArgumentParser()
    ap.add_argument("-x", "--dry-run", required=False, action='store_true', help="Print git commands but don't execute<")
    ap.add_argument("-g", "--grep", required=True, help="Keyword to search the commit to fixup")
    args = ap.parse_args()

    # List of git commands to execute
    command_queue = []

    # Open repo
    try:
        repo = Repo('.')
    except InvalidGitRepositoryError:
        cli_ui.fatal("Not in a git repository", exit_code=1)

    # Get all changed files
    staged_files = get_staged_files(repo)
    changed_files = get_changed_files(repo)
    untracked_files = get_untracked_files(repo)

    if len(staged_files) == 0 and len(changed_files) == 0 and len(untracked_files) == 0:
        cli_ui.fatal("No changes to commit", exit_code=1)

    # Ask which files to commit
    ans = checkbox_select('Select files to add', {
        'Staged':    { 'options': staged_files,    'checked': True  },
        'Changed':   { 'options': changed_files,   'checked': False },
        'Untracked': { 'options': untracked_files, 'checked': False }
    })

    # Add files to commit
    for f in ans['Changed']:
        command_queue.append('git add {}'.format(f))

    for f in ans['Untracked']:
        command_queue.append('git add {}'.format(f))

    # Unstage files
    for f in staged_files:
        if f not in ans['Staged']:
            command_queue.append('git restore --staged {}'.format(f))
    
    # Search commit to fixup
    search = args.grep
    commit_list = search_commit_by_message(repo, search)
    while len(commit_list) == 0:
        if search is not None:
            cli_ui.error('No fixup commit found for search {}"'.format(search))
        search = ask_input("Perform new search")
        if search is not None:
            commit_list = search_commit_by_message(repo, search)

    # Ask which commit to fixup
    ans = list_select('Which commit to fixup?', [opt for _, opt in commit_list])
    command_queue.append('git commit --fixup={}'.format(commit_list[ans][0]))

    # Execute commands
    for c in command_queue:
        cli_ui.info(c)
        if not args.dry_run:
            exit_code, stdout, stderr = process_run(c.split())
            if exit_code != 0:
                cli_ui.error("STDOUT:\n" + stdout)
                cli_ui.error("STDERR:\n" + stderr)
                cli_ui.fatal("Command exited with code {}".format(exit_code))
