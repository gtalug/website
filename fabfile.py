#!/usr/bin/env python

import os

from fabric.utils import abort
from fabric.contrib.project import rsync_project
from fabric.api import env, local, task, hosts, runs_once, lcd, hide, cd
from fabric.operations import run
from fabric.context_managers import settings

env.user = 'deploy'
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
@hosts('penguin.gtalug.org')
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


@task
@hosts('penguin.gtalug.org')
def remote_build():
    """
    Build the web site on the server and deploy it their.
    """

    # If the website source doesn't exist clone it.
    if run('test -d ~/website').failed:
        run('git clone git://github.com/gtalug/website.git ~/website')

    with cd('~/website'):
        # Update the source directory to the latest version.
        run('git fetch --all')
        run('git checkout --force "master"')

        # If the build directory exists delete it. 
        if run('test -d %s' % env.build_path):
            run('rm -fr %s/*' % env.build_path)

        # Create the virtual environment directory and install the requirements.
        if run('test -d ./env/').failed:
            run('virtualenv ./env')
            run('./env/bin/pip install -U -r requirements.txt')

        # Build and deploy the website. 
        run('./env/bin/python website.py build')
        run('cp -r %s/* /srv/www/org_gtalug_www/html/' % env.build_path)
