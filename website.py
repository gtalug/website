#!/usr/bin/env python

import os
import sys
import json
import datetime
from collections import OrderedDict
from os.path import abspath, dirname, join

from flask import Flask, Response, render_template, abort, send_from_directory, request

from flask_frozen import Freezer
from flask_flatpages import FlatPages, pygmented_markdown
from flask_assets import Environment as AssetManager

import dateutil
import vobject
import html2text
from dateutil import rrule
from typogrify.templatetags import jinja_filters as typogrify_filters

# Configuration
DEBUG = True
BASE_URL = "http://gtalug.org"
ASSETS_DEBUG = False
ROOT_DIR = dirname(abspath(__file__))
FLATPAGES_AUTO_RELOAD = True
FLATPAGES_EXTENSION = ".markdown"
FLATPAGES_ROOT = join(ROOT_DIR, "pages")
TEMPLATE_ROOT = join(ROOT_DIR, "templates")
MEETINGS_ROOT = join(ROOT_DIR, "meetings")
TIMEZONE = 'America/Toronto'

class MeetingPages(FlatPages):
	@property
	def root(self):
		return MEETINGS_ROOT

app = Flask(__name__, template_folder=TEMPLATE_ROOT)
app.config.from_object(__name__)
app.jinja_env.filters['typogrify'] = typogrify_filters.typogrify
pages = FlatPages(app)
meetings = MeetingPages(app)
freezer = Freezer(app)
asset_manager = AssetManager(app)

@app.route('/')
def index():
	meeting = OrderedDict(sorted(meetings._pages.items())).values()[-1]
	template = meeting.meta.get('template', 'home.html')
	return render_template(template, meeting=meeting)

@app.route('/humans.txt')
@app.route('/robots.txt')
def static_from_root():
	return send_from_directory(TEMPLATE_ROOT, request.path[1:])

@app.route('/.htaccess')
def htaccess():
	return send_from_directory(TEMPLATE_ROOT, 'htaccess.htaccess')

@app.route('/api/upcoming_meeting.json')
def api_upcoming_meeting():
	meeting = OrderedDict(sorted(meetings._pages.items())).values()[-1]
	
	data = {
		'title': meeting.meta['meeting_title'],
		'url': 'http://gtalug.org/meeting/%s/' % meeting.path,
		'date': meeting.meta['meeting_datetime'].strftime("%v"),
		'body': html2text.html2text(meeting.html),
		'apiUrl': 'http://gtalug.org/api/meeting/%s/' % meeting.path,
	}
	
	return Response(json.dumps(data), mimetype='application/json')

@app.route('/api/meetings.json')
def api_meeting_list():
	meeting_list = OrderedDict(sorted(meetings._pages.items())).values()[:10]
	
	data = []
	
	for m in meetings:
		data += [{
			'@context': 'http://schema.org',
			'@type': 'Event',
			'name': m.meta['meeting_title'],
			'url': 'http://gtalug.org/meeting/%s/' % meeting.path,
			'startDate': meeting.meta['meeting_datetime'].strftime("%v"),
		},]
	
	return Response(json.dumps(data), mimetype='application/json')

@app.route('/api/meeting/<path:slug>.json')
def api_meeting_detail(slug):
	m = meetings.get_or_404(slug)
	
	data = {
		'@context': 'http://schema.org',
		'@type': 'Event',
		'name': m.meta['meeting_title'],
		'startDate': m.meta['meeting_datetime'].strftime("%v"),
		'url': 'http://gtalug.org/meeting/%s/' % m.path,
		'description': html2text.html2text(meeting.html),
	}
	
	if m.meta.get('meeting_location', None):
	    data['location'] = m.meta['meeting_location']
	
	return Response(json.dumps(data), mimetype='application/json')

@app.route('/gtalug.ics')
def gtalug_ics():
	meeting_list = list(reversed(OrderedDict(sorted(meetings._pages.items())).values()))
	
	cal = vobject.iCalendar()
	cal.add('method').value = 'PUBLISH'
	cal.add('VTIMEZONE').tzinfo = dateutil.tz.tzlocal()
	
	for m in meeting_list:
		event = cal.add('vevent')
		
		event.add('uid').value = "meeting-%s@GTALUG.org" % m.path
		
		event.add('summary').value = "GTALUG Meeting: %s" % m.meta['meeting_title']
		event.add('description').value = html2text.html2text(m.html)
		event.add('url').value = 'http://gtalug.org/meeting/%s/' % m.path
		
		event.add('status').value = 'CONFIRMED'
		event.add('location').value = m.meta['meeting_location']
		
		meeting_datetime = m.meta['meeting_datetime']
		
		event.add('dtstart').value = meeting_datetime
		event.add('dtend').value = meeting_datetime + datetime.timedelta(hours=2)
	
	last_meeting_date = meeting_list[0].meta['meeting_datetime']
	
	upcoming_meetings = list(rrule.rrule(
		freq = rrule.MONTHLY,
		dtstart = last_meeting_date + datetime.timedelta(days=1),
		count = 5,
		byweekday = (rrule.TU),
		bysetpos = 2
	))
	
	for m in upcoming_meetings:
		event = cal.add('vevent')
		
		event.add('uid').value = "meeting-%s@GTALUG.org" % (m.strftime("%Y-%m"))
		
		event.add('summary').value = "GTALUG Meeting"
		event.add('description').value = "An upcoming GTALUG meeting."
		event.add('url').value = 'http://gtalug.org/'
		
		event.add('status').value = 'TENTATIVE'
		
		event.add('dtstart').value = m
		event.add('dtend').value = m + datetime.timedelta(hours=2)
	
	return Response(cal.serialize(), mimetype='text/calendar')

@app.route('/meeting/')
def meeting_list():
	page = pages.get_or_404('meeting')
	template = page.meta.get('template', 'meeting_list.html')
	meeting_list = reversed(OrderedDict(sorted(meetings._pages.items())).values())
	return render_template(template, page=page, meetings=meeting_list)

@app.route('/meeting/<path:slug>/')
def meeting_detail(slug):
	meeting = meetings.get_or_404(slug)
	template = meeting.meta.get('template', 'meeting_detail.html')
	return render_template(template, meeting=meeting)

@app.route('/meeting/<path:slug>/gtalug-meeting.ics')
def meeting_detail_ics(slug):
	meeting = meetings.get_or_404(slug)
	
	cal = vobject.iCalendar()
	cal.add('method').value = 'PUBLISH'
	cal.add('VTIMEZONE').tzinfo = dateutil.tz.tzlocal()
	
	event = cal.add('vevent')
	
	event.add('uid').value = "meeting-%s@GTALUG.org" % meeting.path
	
	event.add('summary').value = "GTALUG Meeting: %s" % meeting.meta['meeting_title']
	event.add('description').value = html2text.html2text(meeting.html)
	event.add('url').value = 'http://gtalug.org/meeting/%s/' % meeting.path
	
	event.add('status').value = 'CONFIRMED'
	event.add('location').value = meeting.meta['meeting_location']
	
	meeting_datetime = meeting.meta['meeting_datetime']
	
	event.add('dtstart').value = meeting_datetime
	event.add('dtend').value = meeting_datetime + datetime.timedelta(hours=2)
	
	return Response(cal.serialize(), mimetype='text/calendar')

@app.route('/<path:path>/')
def page(path):
	page = pages.get_or_404(path)
	template = page.meta.get('template', 'page.html')
	return render_template(template, page=page)

@freezer.register_generator
def page_list():
	for p in pages:
		yield 'page', { 'path': p.path }
	for m in meetings:
		yield 'meeting_detail', { 'slug': m.path }
		yield 'meeting_detail_ics', { 'slug': m.path }

if __name__ == '__main__':
	if len(sys.argv) > 1 and sys.argv[1] == "build":
		app.testing = True
		freezer.freeze()
	else:
		port = int(os.environ.get('PORT', 8000))
		app.run(port=port)
