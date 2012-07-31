import httplib, time, pycurl
size = 1024 * 1024 * 50
body = 'x' * size

while False:
    connection =  httplib.HTTPConnection('localhost:8888')
    t0 = time.time()
    connection.request('PUT', '/', body)
    result = connection.getresponse()
    t1 = time.time()
    print size/(t1-t0)/(1024*1024), 'MBytes/sec'

class Reader(object):
    def __init__(self, size):
        self.t = size

    def reader(self, size):
        s = min(size, self.t)
        self.t -= s
        return 'X'*s

#SIZE = 1024*1024*1024*10
SIZE = 1024*1024*5
while True:
    t0 = time.time()
    r = Reader(SIZE)
    c = pycurl.Curl()
    c.setopt(pycurl.URL, 'localhost:8888')
    c.setopt(pycurl.READFUNCTION, r.reader)
    c.setopt(pycurl.INFILESIZE, SIZE)
    c.setopt(pycurl.UPLOAD, 1)
    c.perform()
    c.close()
    t1 = time.time()
    print SIZE/(t1-t0)/(1024*1024), 'MBytes/sec'
