#!/usr/bin/env python

from wsgiref.simple_server import make_server
from cgi import parse_qs
from json import loads
from subprocess import call

import logging
import logging.handlers

logger = logging.getLogger('git-update-server')
logger.setLevel(logging.DEBUG)

handler = logging.handlers.SysLogHandler(address='/dev/log')
formatter = logging.Formatter(fmt='%(name)s: %(levelname)s: %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

handlers = {
        'sites': '/root/sites/setup.sh',
        'conf': '/root/conf/setup.sh',
        }

def application(environ, start_response):

    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0
    request_body = environ['wsgi.input'].read(request_body_size)
    data = parse_qs(request_body)

    logger.debug('Received data [%s].' % data)

    try:
        payload = loads(data['payload'][0])    
        repo = payload['repository']['name']
        logger.info('Repository [%s] updated.' % repo)
        if repo in handlers:
            rc = call(handlers[repo], shell=True)
            log = 'Command [%s] returned code [%d].' % (handlers[repo], rc)
            if rc != 0:
                logger.warning(log)
            else:
                logger.debug(log)
        else:
            logger.warning('Repository [%s] is unknown.' % repo)
    except (KeyError, IndexError):
        logger.warning('Cannot parse request.')

    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    start_response(status, headers)

    return 'OK'

port = 51249
httpd = make_server('', 51249, application)
logger.info('Listening on port [%d].', 51249)

try:
    httpd.serve_forever()
except BaseException as e:
    logger.info('Server exiting due to %s.', repr(e))
