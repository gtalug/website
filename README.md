website
=======

The [GTALUG](http://gtalug.org/ "Greater Toronto Area Linux User Group") web site.

## Develop

Install git and clone this repository

    # apt-get install git
    # git pull https://github.com/gtalug/website.git


If you are running Debian Wheezy, add backports repository that contains node-less

    # echo "
deb http://ftp.debian.org/debian wheezy-backports main" >> /etc/apt/sources.list
    # apt-get update

Install `python-virtualenv`, `python-dev` and `node-less`. Pass `-t wheezy-backports` parameter if you're installing the server on Debian Wheezy :

	# apt-get install python-virtualenv python-dev node-less


Create and activate virtual environment

    $ cd website
    $ virtualenv env
    $ source env/bin/activate

Install `fabric` in local virtual environment

	(env)$ pip install fabric

Then setup the virutal envoirment:

	(env)$ fab install

## Run

To run an local server for development:

	(env)$ fab run

## Deploy

To deploy the web site:

	(env)$ fab deploy

