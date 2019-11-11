import datetime
import webbrowser
import re
import sched
import time
from urllib.request import urlopen, Request, urlretrieve
import argparse
import logging

from bs4 import BeautifulSoup

from .utils import build_url, validate_date

logger_handle = 'bookmyshow_notify'
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] [%(levelname)s] \t %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S')
logger = logging.getLogger(logger_handle)


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
    logger.info('Checking for shows.')
    venue_list = get_venue_list(url)
    if check_for_keywords(venue_list, keywords):
        logger.info('Successfully found match.')
        webbrowser.open(url)
        exit()
    else:
        logger.info('Couldn\'t find any match. Trying again.')
        schdlr.enter(60, 1, keep_checking, (schdlr, url, keywords))


def main():
    import sys
    args = parse_args(sys.argv[1:])
    logger.debug('Recieved arguments \nURL: {}\nDate: {}\nKeywords: {}\n'.format(args.url, args.date, args.keywords))
    bookmyshow_url = build_url(args.url, args.date)
    logger.debug('BookMyShow booking page URL: ' + bookmyshow_url)
    schdlr = sched.scheduler(time.time, time.sleep)
    schdlr.enter(60, 1, keep_checking, (schdlr, bookmyshow_url, args.keywords))
    try:
        schdlr.run()
    except KeyboardInterrupt:
        logger.info("Exiting.")


if __name__ == '__main__':
    main()
