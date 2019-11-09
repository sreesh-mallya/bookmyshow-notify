def validate_date(date):

    # TODO: Validate the date format and compare
    
    return date


def build_url(url, date):
    validated_date = validate_date(date)
    bookmyshow_url = url + ''.join(validated_date.split('-')[::-1]) # Split the validated date with `-`, reverse the obtained list, and then join it to get the inverted date
    return bookmyshow_url


def build_keywords_regex(keywords):

    # TODO: Return the keywords separated with a '|'

    pass
