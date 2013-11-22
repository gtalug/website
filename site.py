#!/usr/bin/env python

from os.path import abspath, dirname, join
import sys

from flask import Flask, render_template, abort

from flask_frozen import Freezer
from flask_flatpages import FlatPages
from flask_assets import Environment as AssetManager

# Configuration
DEBUG = True
BASE_URL = "http://gtalug.org"
ASSETS_DEBUG = False
ROOT_DIR = dirname(abspath(__file__))
FLATPAGES_AUTO_RELOAD = True
FLATPAGES_EXTENSION = ".html"
FLATPAGES_ROOT = join(ROOT_DIR, "pages")
TEMPLATE_ROOT = join(ROOT_DIR, "templates")

app = Flask(__name__, template_folder=TEMPLATE_ROOT)
app.config.from_object(__name__)
pages = FlatPages(app)
freezer = Freezer(app)
asset_manager = AssetManager(app)

@app.route('/')
def index():
	page = pages.get_or_404('index')
	template = page.meta.get('template', 'page.html')
	return render_template(template, page=page)

@app.route('/robots.txt')
def robots_txt():
	return render_template('robots.txt', mimetype='text/plain')

@app.route('/<path:path>/')
def page(path):
	page = pages.get_or_404(path)
	template = page.meta.get('template', 'page.html')
	return render_template(template, page=page)

if __name__ == '__main__':
	if len(sys.argv) > 1 and sys.argv[1] == "build":
		freezer.freeze()
	else:
		app.run(port=8000)