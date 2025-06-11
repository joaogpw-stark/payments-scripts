# -*- coding: utf-8 -*-
import datetime

dateutil_parser = None
try:
    import dateutil.parser
except ImportError:
    pass

def parseDatetime(dt_string):
    if not isinstance(dt_string, basestring):
        raise TypeError("Input must be a string or unicode.")
    if not dt_string.strip():
        raise ValueError("Input string cannot be empty or just whitespace.")

    if dateutil_parser:
        try:
            return dateutil_parser.parse(dt_string)
        except Exception as e:
            pass

    formats_to_try = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d",
    ]

    for fmt in formats_to_try:
        try:
            return datetime.datetime.strptime(dt_string, fmt)
        except ValueError:
            continue

    raise ValueError("Could not parse datetime string '{}' with known formats.".format(dt_string))