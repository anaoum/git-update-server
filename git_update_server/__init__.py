from wsgiref.simple_server import make_server
from cgi import parse_qs
from json import loads
from subprocess import call
import logging

class GitUpdateServer:

    def __init__(self, port, handlers, logger=logging):
        self.port = port
        self.handlers = handlers
        self.logger = logger

    def _application(self, environ, start_response):

        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0
        request_body = environ['wsgi.input'].read(request_body_size)
        data = parse_qs(request_body)

        self.logger.debug('Received data [%s].' % data)

        try:
            payload = loads(data['payload'][0])    
            repo = payload['repository']['name']
            self.logger.info('Repository [%s] updated.' % repo)
            if repo in self.handlers:
                for handler in self.handlers[repo]:
                    rc = call(handler, shell=True)
                    log = 'Command [%s] returned code [%d].' % (handler, rc)
                    if rc != 0:
                        self.logger.warning(log)
                    else:
                        self.logger.debug(log)
            else:
                self.logger.warning('Repository [%s] is unknown.' % repo)
        except (KeyError, IndexError):
            self.logger.warning('Cannot parse request.')

        status = '200 OK'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)

        return ''

    def start(self):
        self.httpd = make_server('', self.port, self._application)
        self.logger.info('Listening on port [%d].', self.port)
        try:
            self.httpd.serve_forever()
        except BaseException as e:
            self.logger.info('Server exiting due to %s.', repr(e))
