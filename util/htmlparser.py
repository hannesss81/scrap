import time, threading, lxml.html

concurrent_html = []

def startParsing():
    global concurrent_html
    print("HTML Parsing initialized.")

    while True:
        if (concurrent_html):
            threading.Thread(target=parseHtml, args=[concurrent_html.pop()]).start()
        else:
            time.sleep(1)
            print("Waiting for new html pages.")

def parseHtml(html_response):
    root = lxml.html.fromstring(html_response.body)
    for link in root.xpath("//a"):
        print(link.get("href"))


