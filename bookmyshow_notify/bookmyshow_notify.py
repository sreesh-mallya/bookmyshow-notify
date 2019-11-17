import datetime
import webbrowser
import re
import sys
import sched
import time
from urllib.request import urlopen, Request
import argparse
import logging

from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] [%(levelname)s] %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S')

LOGGER = logging.getLogger('bookmyshow_notify')
BASE_URL = r'https://in.bookmyshow.com'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0'
HEADERS = {'User-Agent': USER_AGENT}


def parse_args(cl_args):
    parser = argparse.ArgumentParser(description='BookMyShow shows and showtimes notifier CLI.')
    parser.add_argument('--url', type=str, help='URL to the movie\'s page on in.bookmyshow.com')
    parser.add_argument('date', type=str, help='Date to check for, in format DD-MM-YYYY.')
    parser.add_argument('--keywords', type=str, nargs='*',
                        help='Names of multiplexes or theatres to check for. '
                        'If no arguments are passed, it checks for any venue '
                        'on the given date.')
    parser.add_argument('--seconds', metavar='S', type=float,
                        help='Time in seconds to keep checking after (default: 60s).')
    parser.add_argument('--movie', metavar='MOVIE', type=str, 
                        help='Name of the show you\'re searching for.')
    parser.add_argument('--location', metavar='LOCATION', type=str, 
                        help='Your location. Eg: bengaluru, kochi, trivandrum.')

    # TODO: Multiple format support
    parser.add_argument('--format', metavar='FORMAT', type=str,
                        help='Your location. Eg: bengaluru, kochi, trivandrum.')
    args = parser.parse_args(cl_args)
    return args


def validate_date(date):
    try:
        datetime.datetime.strptime(date, '%d-%m-%Y')
    except ValueError:
        LOGGER.exception('Incorrect date format! Expected format is DD-MM-YYYY.')
        sys.exit()
    return date


def build_url(url, date):
    # TODO: In case date is not passed, either take the date of the same day or the next day
    validated_date = validate_date(date)

    # Split the validated date with `-`, reverse the obtained list, 
    # and then join it to get the inverted date
    bookmyshow_url = url + ''.join(validated_date.split('-')[::-1])
    return bookmyshow_url


def get_movie_id(name, location):
    url = BASE_URL + location.lower()
    req = Request(url, None, HEADERS)
    with urlopen(req) as response:
        html = response.read()

    soup = BeautifulSoup(html, 'html.parser')
    movie_url_regex = re.compile("{}/movies/".format(location.lower()), re.IGNORECASE)
    movie_anchors = soup.find_all('a', href=movie_url_regex)
    for a in movie_anchors:
        path = a.get('href')
        if name.lower() in path:

            # TODO: Handle a case where no match found

            return path


def get_movie_page_url(path, location):
    movie_page_url = '{}/{}/{}'.format(BASE_URL, location, path)
    LOGGER.info('Movie page URL: %s', movie_page_url)

    # TODO: Add some sort of validation for fields if needed

    return movie_page_url


def get_buytickets_page_url(movie_page_url, format):
    req = Request(movie_page_url, None, HEADERS)
    with urlopen(req) as response:
        html = response.read()

    soup = BeautifulSoup(html, 'html.parser')
    anchor_elements = soup.find_all('a', {'class': 'dimension-pill'})
    for element in anchor_elements:
        contents = [content.lower() for content in element.contents]
        if format.lower() in contents:
            # TODO: Handle a case when content not found
            return BASE_URL + element.get('href')


def get_venue_list(url):
    req = Request(url, None, HEADERS)
    with urlopen(req) as response:
        html = response.read()

    soup = BeautifulSoup(html, 'html.parser')
    venue_list = soup.find_all('ul', {'id': 'venuelist'})[0].find_all('li', {'data-name': True})
    venue_list = [venue['data-name'] for venue in venue_list]
    return venue_list


def check_for_keywords(venue_list, keywords):
    if not keywords:
        LOGGER.info('No keywords for venues specified. Available venues: %s', venue_list)
        return True

    kws = r'|'.join(keywords)
    regex = re.compile(kws, re.IGNORECASE)
    for venue in venue_list:
        if regex.search(venue):
            LOGGER.info('Successfully found match. Venue: %s', venue_list)
            return True
    return False


def keep_checking(schdlr, url, keywords, seconds):
    LOGGER.info('Checking for venues with matching keywords...')
    venue_list = get_venue_list(url)
    if check_for_keywords(venue_list, keywords):
        webbrowser.open(url)
        sys.exit()
    else:
        LOGGER.info('Couldn\'t find any match. Trying again.')
        schdlr.enter(60, 1, keep_checking, (schdlr, url, keywords, seconds))


def main():
    args = parse_args(sys.argv[1:])

    if not args.url and not args.location and not args.movie and not args.format:
        LOGGER.error('You need to specify the `--location`, `--format`, and `--movie` arguments if you\'re not specifying the URL directly. Exiting.')
        sys.exit()

    LOGGER.debug('Received arguments \nURL: '
                 '%s\nDate: %s\nKeywords: %s\nKeep checking after: %d seconds',
                 args.url, args.date, args.keywords, args.seconds)
    bookmyshow_url = build_url(args.url, args.date)
    LOGGER.debug('BookMyShow booking page URL: %s', bookmyshow_url)
    schdlr = sched.scheduler(time.time, time.sleep)
    schdlr.enter(args.seconds, 1, keep_checking, (schdlr, bookmyshow_url,
                                                  args.keywords, args.seconds))
    try:
        schdlr.run()
    except KeyboardInterrupt:
        LOGGER.info("Exiting.")


if __name__ == '__main__':
    main()
