from tornado import httpclient, ioloop
from util import htmlparser

http_client = httpclient.AsyncHTTPClient()
i = 0

def open_connections(urls):
    global i

    for url in urls:
        i += 1
        http_client.fetch(url, handle_request, method="GET")
    ioloop.IOLoop.instance().start()

def handle_request(response):
    global i
    htmlparser.concurrent_html.append(response)
    i -= 1
    if i == 0:
        ioloop.IOLoop.instance().stop()


