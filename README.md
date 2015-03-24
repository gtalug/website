website
=======

The [GTALUG](http://gtalug.org/ "Greater Toronto Area Linux User Group") web site.

## Develop

Install `python-virtualenv`, `node-less` and `fabric` and :

	$ apt-get install python-virtualenv node-less
	$ pip install fabric

Then setup the virutal envoirment:

	$ fab install

## Run

To run an local server for development:

	$ fab run

## Deploy

To deploy the web site:

	$ fab deploy


