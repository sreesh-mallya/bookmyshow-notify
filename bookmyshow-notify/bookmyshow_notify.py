import datetime
import webbrowser
import re
import sched
import time
from urllib.request import urlopen, Request, urlretrieve
import argparse

from bs4 import BeautifulSoup


def parse_args():
	parser = argparse.ArgumentParser(description='BookMyShow shows and showtimes notifier CLI.')
	parser.add_argument('--url', metavar='https://in.bookmyshow.com/buytickets/<movie>-<location>/<some-string>/', type=str, 
					help='URL to the movie\'s page in in.bookmyshow.com')
	parser.add_argument('--date', type=str, help='Date to check for.', metavar='DD-MM-YYYY')
	parser.add_argument('--keywords', type=str, help='Names of multiplexes or theatres to check for.')


def get_venue_list(date, url):

	# TODO: This function should just return the list of venues after parsing the HTML

	user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0'
	headers = {'User-Agent': user_agent}

	bookmyshow_url = url + date

	req = Request(bookmyshow_url, None, headers)

	with urlopen(req) as response:
	    html = response.read()

	soup = BeautifulSoup(html, 'html.parser')
	venue_list = soup.find_all('ul', {'id': 'venuelist'})[0].find_all('li', {'data-name': True})
	return venue_list


def check_for_keywords(venue_list, keywords):

	# TODO: This function should check for keywords

	regex = re.compile(keywords, re.IGNORECASE)

	for venue in venue_list:
		if regex.search(venue['data-name']):
			return true
			

def main(args):

	# TODO: This function is the entrypoint. This function should also call parse_args(), validate the arguments, call get_venue_list() and check_for_keywords()

	arguments = parse_args()
	venue_list = get_venue_list(arguments.date, arguments.url)
	
	if check_for_keywords(venue_list):
		webbrowser.open()
	schdlr.enter(60, 1, main, (schdlr, ))


if __name__ == '__main__':
	schdlr = sched.scheduler(time.time, time.sleep)
	schdlr.enter(60, 1, main, (schdlr, )) 
	schdlr.run()
