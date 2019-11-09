import datetime
import webbrowser
import re
import sched
import time
from urllib.request import urlopen, Request, urlretrieve
import argparse

from bs4 import BeautifulSoup

from utils import build_url, validate_date


def parse_args(cl_args):
	parser = argparse.ArgumentParser(description='BookMyShow shows and showtimes notifier CLI.')
	parser.add_argument('url', type=str, help='URL to the movie\'s page in in.bookmyshow.com')
	parser.add_argument('date', type=str, help='Date to check for, in format DD-MM-YYYY.')
	parser.add_argument('keywords', type=str, help='Names of multiplexes or theatres to check for.')
	args = parser.parse_args(cl_args)
	return args


def get_venue_list(url):
	user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0'
	headers = {'User-Agent': user_agent}

	req = Request(url, None, headers)
	with urlopen(req) as response:
	    html = response.read()

	soup = BeautifulSoup(html, 'html.parser')
	venue_list = soup.find_all('ul', {'id': 'venuelist'})[0].find_all('li', {'data-name': True})
	return venue_list


def check_for_keywords(venue_list, keywords):
	kws = r'|'.join(keywords)
	regex = re.compile(kws, re.IGNORECASE)
	for venue in venue_list:
		if regex.search(venue['data-name']):
			return True
	return False


def keep_checking(schdlr, url, keywords):
	venue_list = get_venue_list(url)
	if check_for_keywords(venue_list, keywords):
		webbrowser.open()
	else:
		schdlr.enter(60, 1, keep_checking, (schdlr, ))


if __name__ == '__main__':
	import sys
	args = parse_args(sys.argv[1:])
	bookmyshow_url = build_url(args.url, args.date)
	schdlr = sched.scheduler(time.time, time.sleep)
	schdlr.enter(60, 1, keep_checking, (schdlr, bookmyshow_url, keywords)) 
	schdlr.run()
