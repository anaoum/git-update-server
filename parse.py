import sys
import argparse
import logging

LOG_LEVEL = {'DEBUG': logging.DEBUG, 'INFO': logging.INFO}

parser = argparse.ArgumentParser(description='This program runs a web server to receive POST notifications when a git repository is updated on GitHub (or BitBucket). You can configure this server to git pull local clones of the repositories, or even run your own command whenever a repository is updated.')
parser.add_argument('--port', metavar='port', help='the port on which to listen for HTTP POST requests from GitHub or BitBucket (default: 51249)', default=51249, type=int)
parser.add_argument('--no-daemon', action='store_const', const=False, default=True, help='don\'t run the server as a daemon')
actions_group = parser.add_argument_group('actions', 'Actions to take when a repository is updated. You should specify at least one of these actions, otherwise the server will be quite useless. You can add multiple actions for multiple repositories.')
actions_group.add_argument('--git-pull', nargs=2, metavar=('repo', 'path'), help='run `git pull` in `path` when repository `repo` is updated', action='append')
actions_group.add_argument('--command', nargs=2, metavar=('repo', 'command'), help='run `command` when repository `repo` is updated', action='append')
logging_group = parser.add_argument_group('logging')
logging_group.add_argument('--log-level', metavar='level', type=lambda l: LOG_LEVEL[l], choices=('DEBUG', 'INFO'), default='DEBUG', help='log level (default: DEBUG)')
logging_group.add_argument('--log-output', metavar='output', type=argparse.FileType('w'), default=sys.stdout, help='where to log output (default: stdout)')

args = parser.parse_args()

print args
