import datetime
import webbrowser
import re
import sched
import time
from urllib.request import urlopen, Request, urlretrieve
import argparse

from bs4 import BeautifulSoup


def parse_args():
	parser = argparse.ArgumentParser(description='Get URL, date, and keywords to check for.')
	parser.add_argument('--url', metavar='https://in.bookmyshow.com/buytickets/<movie>-<location>/<some-string>/', type=str, 
					help='URL to the movie\'s page in in.bookmyshow.com')
	parser.add_argument('--date', dest='accumulate', type=str,
                    help='Date to check for.')


def get_venue_list(schdlr):
	print('Okay...')
	user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0'
	headers = {'User-Agent': user_agent}

	# change date accordingly
	date = '26'
	month = '04'
	year = '2019'

	# use | to add search keyword
	keywords = r'phoenix|vega|pvr'		 
	regex = re.compile(keywords, re.IGNORECASE)

	bookmyshow_url = r'https://in.bookmyshow.com/buytickets/avengers-endgame-bengaluru/movie-bang-ET00100674-MT/' + year + month + date

	req = Request(bookmyshow_url, None, headers)

	with urlopen(req) as response:
	    html = response.read()

	soup = BeautifulSoup(html, 'html.parser')
	venue_list = soup.find_all('ul', {'id': 'venuelist'})[0].find_all('li', {'data-name': True})
	for venue in venue_list:
		if regex.search(venue['data-name']):
			webbrowser.open(bookmyshow_url)
			exit()

	print('Sorry mate, not yet!')
	schdlr.enter(60, 1, get_venue_list, (schdlr, ))


if __name__ == '__main__':
	schdlr = sched.scheduler(time.time, time.sleep)
	schdlr.enter(60, 1, get_venue_list, (schdlr, )) 
	schdlr.run()
