# -*- coding: utf-8 -*-

"""
abode.cli
~~~~~~~~~

This module contains the abode command-line interface.

"""

import os
import tempfile
import sys

import clint
from clint.utils import tsplit, mkdir_p
from clint.textui import indent, puts
import envoy


def upload(remote='heroku'):

    if len(clint.args):
        remote = clint.args.get(0)

    #: Git remote collector.
    remotes = dict()

    #: for testing.
    os.chdir('/Users/kreitz/httpbintest')

    # The current path to the application.
    app_path = os.getcwd()

    # Remember Git Remote
    git_snap = envoy.run('git remote -v').std_out.strip()
    for remote_line in git_snap.split('\n'):
        r = tsplit(remote_line, (' ', '\t'))

        r_name = r[0]
        r_path = r[1]

        remotes[r_name] = r_path

    if not remote in remotes:
        raise RuntimeError


    print 'Uploading {0} to {1}.'.format(
        app_path.split('/').pop(),
        remotes[remote]
    )

    # Create a new upload directory.
    # mkdir_p('.abode/{0}'.format(remote))

    repo_dir = tempfile.mkdtemp(prefix="abode-upload-{0}".format(remote))

    # Copy everything into it.
    envoy.run('cp -R . {0}'.format(repo_dir))

    # Move on in.
    os.chdir(repo_dir)

    envoy.run('git init')
    envoy.run('git add -A')
    envoy.run('git commit --no-message --allow-empty-message -m abode')
    # os.system('pwd')
    os.system('git push {0} master --force'.format(remotes[remote]))


def display_help():
    os.system('heroku help')
    print 'Abode add-ons: \n '
    with indent(2):
        puts('upload  # deploy your app')


command_map = {
    'upload': upload,
    'up': upload,
    'help': display_help
}



def main():
    """The main dispatch."""

    if not len(clint.args):
        print 'Usage.'
        sys.exit(1)

    command = clint.args.get(0)

    if command not in command_map:
        h_cmd = ' '.join(clint.args._args)
        os.system('heroku {0}'.format(h_cmd))
    else:
        clint.args.pop(0)

    command_map.get(command).__call__()

