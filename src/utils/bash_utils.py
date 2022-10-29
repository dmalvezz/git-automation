
import subprocess
import os

class bcolors:
    """Bash colors
    Returns:
        string: color code
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    

def colorize(string, color):
    return color + string + bcolors.ENDC


def red(string):
    return colorize(string, bcolors.FAIL, )


def yellow(string):
    return colorize(string, bcolors.WARNING, )


def green(string):
    return colorize(string, bcolors.OKGREEN)

def blue(string):
    return colorize(string, bcolors.OKBLUE)

def bold(string):
    return colorize(string, bcolors.BOLD)


def process_run(cmd, env={}, **kwargs):
    """Run a process and return exit code, stdout and stderr
    Args:
        cmd (list): list of commands to execute
        env (dict): dict of environment variables for the process to run
    Returns:
        int: exit code
        string: stdout
        string: stderr
    """
    cmd_list = [c.format(**kwargs) for c in cmd]
    proc = subprocess.Popen(cmd_list, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        shell=False,
        start_new_session=True,
        env=env.update(os.environ.copy())
    )

    out, err = proc.communicate()
    return proc.returncode, out.decode('utf-8'), err.decode('utf-8')