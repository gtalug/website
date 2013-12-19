#!/usr/bin/env python

from os.path import abspath, dirname, join
import sys

from flask import Flask, render_template, abort, send_from_directory, request

from flask_frozen import Freezer
from flask_flatpages import FlatPages, pygmented_markdown
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
MEETINGS_ROOT = join(ROOT_DIR, "meetings")

class MeetingPages(FlatPages):
	
	@property
	def root(self):
		return MEETINGS_ROOT

app = Flask(__name__, template_folder=TEMPLATE_ROOT)
app.config.from_object(__name__)
pages = FlatPages(app)
meetings = MeetingPages(app)
freezer = Freezer(app)
asset_manager = AssetManager(app)

@app.route('/')
def index():
	meeting = meetings._pages.values()[0] # This is a really dirty way of doing this.
	template = meeting.meta.get('template', 'home.html')
	return render_template(template, meeting=meeting)

@app.route('/robots.txt')
def static_from_root():
	return send_from_directory(TEMPLATE_ROOT, request.path[1:])

@app.route('/meeting/<path:slug>/')
def meeting(slug):
	meeting = meetings.get_or_404(slug)
	template = meeting.meta.get('template', 'meeting.html')
	return render_template(template, meeting=meeting)

@app.route('/<path:path>/')
def page(path):
	page = pages.get_or_404(path)
	template = page.meta.get('template', 'page.html')
	return render_template(template, page=page)

@freezer.register_generator
def page_list():
    for p in pages:
		yield 'page', { 'path': p.path }

if __name__ == '__main__':
	if len(sys.argv) > 1 and sys.argv[1] == "build":
		app.testing = True
		freezer.freeze()
	else:
		app.run(port=8000)