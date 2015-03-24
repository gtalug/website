#!/usr/bin/env python

import os

from fabric.contrib.project import rsync_project
from fabric.api import env, local, task, hosts

env.hosts = ['penguin.gtalug.org', ]
env.use_ssh_config = True
env.build_path = os.path.abspath('./build/')


@task
@hosts('localhost')
def install():
    """
    This will build the virtual envoirument and install all the Python
    dependencies.
    """

    local('virtualenv env')
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

    build()
    rsync_project(
        local_dir=env.build_path + "/",
        remote_dir="/srv/www/org_gtalug_www/html/",
        delete=False,
        extra_opts='--exclude=".DS_Store" --exclude="static/less/" \
 --exclude="static/.webassets-cache/" --exclude="static/js/less-1.5.0.min.js"'
    )
