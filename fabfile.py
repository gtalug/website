#!/usr/bin/env python

import os

from fabric.utils import abort
from fabric.contrib.project import rsync_project
from fabric.api import env, local, task, hosts, runs_once, lcd, hide
from fabric.context_managers import settings

env.hosts = ['penguin.gtalug.org', ]
env.use_ssh_config = True
env.build_path = os.path.abspath('./build/')


@task
@hosts('localhost')
def install():
    """
    This installs all the Python dependencies.
    """
    local('./env/bin/pip install -U -r requirements.txt')


@task
@hosts('localhost')
def run():
    """
    Run the development web server so you could view your changes.
    """

    local('./env/bin/python website.py')


def clean():
    """
    This will clean the build directory.
    """

    local('rm -fr %s/*' % env.build_path)


@task
@hosts('localhost')
def build():
    """
    This will build the web site.
    """

    clean()
    local('./env/bin/python website.py build')


@task
@hosts('deploy@penguin.gtalug.org')
def deploy():
    """
    This will deploy the web site to the GTALUG server.
    """
    # check_working_dir_clean()
    build()
    rsync_project(
        local_dir=env.build_path + "/",
        remote_dir="/srv/www/org_gtalug_www/html/",
        delete=False,
        extra_opts='--exclude=".DS_Store" --exclude="static/less/" \
 --exclude="static/.webassets-cache/" --exclude="static/js/less-1.5.0.min.js"'
    )
    register_deployment(".")


def check_working_dir_clean():
    """Aborts if not everything has been committed."""
    # Inspiration:
    # http://stackoverflow.com/questions/5139290/how-to-check-if-theres-nothing-to-be-committed-in-the-current-branch
    with settings(warn_only=True):
        if not local('git diff --stat --exit-code').succeeded:
            abort('You have unstaged changes: to ignore, run with check_clean=no')
        if not local('git diff --cached --stat --exit-code').succeeded:
            abort('Your index contains uncommitted changes: to ignore, run with check_clean=no')

        r = local('git ls-files --other --exclude-standard --directory', capture=True )
        if r != '':
            abort('Untracked files exist: to ignore, run with check_clean=no')


@task
@runs_once
def register_deployment(git_path):
    with hide('warnings'):
        with(lcd(git_path)):
            local("curl https://opbeat.com/api/v1/organizations/b33f729826be44e5b889ae0a8ec88eea/apps/049496b911/releases/ -H 'Authorization: Bearer 609dd34cebcf1f830036d102cf1be8d811c70a91' -d rev=`git log -n 1 --pretty=format:%H` -d branch=`git rev-parse --abbrev-ref HEAD` -d status=completed")
