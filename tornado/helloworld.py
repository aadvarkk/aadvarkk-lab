#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import traceback

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

import threading, time



lock = threading.Lock()
last = time.time()
payload = 0
cnt = 0

class MainHandler(tornado.web.ChunkedRequestHandler):
    def __init__(self, application, request, **kwargs):
        self.size = 0
        tornado.web.RequestHandler.__init__(self, application, request, **kwargs)

    def get(self):
        self.write('hello world')

    def put(self, *args, **kwargs):
        pass

    def on_chunk_rcvd(self, chunk):
        chunk_size = len(chunk)
        self.size += chunk_size
        
        global lock, last, payload, cnt
        with lock:
            payload += chunk_size
            cnt += 1
            t = time.time()
            if t - last > 5.0:
                tp = payload/(t - last)/(1024*1024)
                print tp, 'MB/sec'
                last = t
                payload = 0
                cnt = 0

    def on_chunk_finished(self, data):
        self.finish()

def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([ (r"/", MainHandler), ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
