#!/usr/bin/env python

'''
Module for some common exceptions for the library.
'''
ERROR_MSG = {
    100: "General error occurred.",
    101: ("Cloudant Library not installed. Please install it"
          " using 'pip install cloudant'."),
    102: "You must provide login credentials.",
    400: "Databases '{0}' does not exists.",
    401: "Unauthorized. The credentials are not valid.",
    404: "Document '{0}' does not exist.",
    503: "Service unavailable. User '{0}' not found.",
    700: "{0} must be {1}."
}


class FlaskCloudantException(Exception):
    '''

    :param str msg: A message describing the exception.
    :param int code: A code identifying the exception.
    '''
    def __init__(self, code=100, *args):
        try:
            msg = ERROR_MSG[code].format(*args)
        except (KeyError, IndexError):
            code = 100
            msg = ERROR_MSG[code]
        super(FlaskCloudantException, self).__init__(msg)
        self.status_code = code
