""" Server for Maxwell.

    Performs just three operations:
    1.  Receive job as a from client (POST).
    2.  Return job status or simulation result to client (GET).
    3.  Return queue status to client (HEAD).

    Defaults to use port 8008.
"""

import BaseHTTPServer
from StringIO import StringIO
import cgi, shutil, tempfile, sys, os
from SocketServer import ThreadingMixIn

my_dir = tempfile.mkdtemp() # Temporary directory that we will use.
my_dir = "/tmp/maxwell-server-debug/"

class MaxwellHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """ Handler for the server. """

    def do_POST(self):
        """ Accepts files from client. """
        form = cgi.FieldStorage( \
            fp=self.rfile, \
            headers=self.headers, \
            environ={'REQUEST_METHOD':'POST', \
                    'CONTENT_TYPE':self.headers['Content-Type']}) 

        # "{ip}-" prefix added in front of file name.
        try:
            f = open(self.my_prefix() + form['key'].value, 'w')
        except:
            self.send_error(404, "Upload failed.")
            return

        shutil.copyfileobj(form['file'].file, f)
        f.close()

        self.send_response(200)
        self.send_header('Content-type', 'maxwell!')
        self.end_headers()

    def do_GET(self):
        """ Return file to client. """

        if self.path == '/': # No file specified, treat as HEAD request.
            self.do_HEAD()
            return

        try:
            f = open(self.my_prefix() + self.path.lstrip('/'), 'rb')
        except:
            self.send_error(404, "File not found.")
            return

        self.send_response(200)
        self.send_header('Content-type', 'maxwell!')
        self.end_headers()
        shutil.copyfileobj(f, self.wfile)
        f.close()
        # print self.client_address
    
    def my_prefix(self):
        """ Produce the user-specific prefix for files. """
        return my_dir + self.client_address[0] + ':'
      
    def do_HEAD(self):
        """ Returns the number of jobs in queue. """
        self.send_response(200)
        self.send_header('Content-type', 'maxwell!')
        self.end_headers()

        num_requests = len([f for f in os.listdir(my_dir) \
                            if f[-len('.request'):] == '.request'])
        shutil.copyfileobj(StringIO("%d jobs pending" % num_requests), \
                            self.wfile)

class ThreadingHTTPServer(ThreadingMixIn, BaseHTTPServer.HTTPServer):
    """ We use a multi-process version of BaseHTTPServer. """
    pass


if __name__ == '__main__':
    
    # Determine the port to use.
    if len(sys.argv) == 2:
        port = int(sys.argv[1])
    else:
        port = 8008

    server_address = ("", port)
    print "Serving at", server_address

    httpd = ThreadingHTTPServer(server_address, MaxwellHandler)
    httpd.serve_forever()

