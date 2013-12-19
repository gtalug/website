#!/usr/bin/env python

import os

from fabric.contrib.project import rsync_project
from fabric.api import env, puts, local, task, hosts, execute, runs_once

env.hosts = ['gold',]
env.use_ssh_config = True
env.build_path = os.path.abspath('./build/')

@task
@hosts('localhost')
def install():
	local('virtualenv env')
	local('./env/bin/pip install -U -r requirments.txt')

@task
@hosts('localhost')
def run():
	local('./env/bin/python website.py')

def clean():
	local('rm -fr %s/*' % env.build_path)

@task
@hosts('localhost')
def build():
	clean()
	local('./env/bin/python website.py build')

@task
@hosts('gold')
def deploy():
	build()
	rsync_project(
		local_dir=env.build_path + "/",
		remote_dir="/home/myles/gtalug.org/",
		delete=True,
		extra_opts='--exclude=".DS_Store" --exclude="static/less/" --exclude="static/.webassets-cache/"'
	)