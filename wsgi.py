#!/usr/bin/env python

import os

from web import app as application

#DEBUG='true'
#application.config['PROPAGATE_EXCEPTIONS'] = True

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    httpd = make_server('localhost', 8051, application)

    httpd.serve_forever()
