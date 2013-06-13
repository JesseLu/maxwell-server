""" Server for Maxwell.

    Performs just three operations:
    1.  Receive job as a from client (POST).
    2.  Return job status or simulation result to client (GET).
    3.  Return queue status to client (HEAD).

    Defaults to use port 8008.
"""

import BaseHTTPServer
import cgi, sys, os, shutil, uuid, time
import subprocess, shlex
from SocketServer import ThreadingMixIn

class MaxwellHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """ Handler for the server.
    """

    def do_POST(self):
        """ Just a simple file uploader. """
        form = cgi.FieldStorage( \
            fp=self.rfile, \
            headers=self.headers, \
            environ={'REQUEST_METHOD':'POST', \
                    'CONTENT_TYPE':self.headers['Content-Type']}) 

        infile = open(filename + '.i', 'w')
        shutil.copyfileobj(form['in'].file, infile)
        infile.close()


    def do_GET(self):
        """ Just a simple file downloader. """
        self.send_response(200)
        self.send_header('Content-type', 'maxwell!')
        self.end_headers()
        # print self.client_address
    
        
      
    def do_HEAD(self):
        """ Returns the number of jobs in queue. """
        pass

class ThreadingHTTPServer(ThreadingMixIn, BaseHTTPServer.HTTPServer):
    """ We use a multi-process version of BaseHTTPServer. """
    pass


if __name__ == '__main__':
    if len(sys.argv) == 2:
        port = sys.argv[1]
    else:
        port = 8008

    server_address = ("", port)
    print "Serving at", server_address

    httpd = ThreadingHTTPServer(server_address, MaxwellHandler)
    httpd.serve_forever()

