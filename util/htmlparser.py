import time, threading, feedparser
from util import naivebayes
from bs4 import BeautifulSoup

logger_name = None

rss_feed_queue = []
current_feeds = {}


def fillInitialQueue(filename):
    with open(filename, "r") as file:
        for row in file:
            rss_feed_queue.append(row.strip().split(","))


def startParsing():
    global rss_feed_queue, logger_name
    logger_name = threading.current_thread().name
    print("[{}] RSS Feed parsing initialized.".format(logger_name))

    fillInitialQueue("feeds.props")

    while True:
        if (rss_feed_queue):
            new_feed = rss_feed_queue.pop()
            print("[{}] Got a new feed: {}, type: {}".format(logger_name, new_feed[0], new_feed[1]))
            threading.Thread(target=pollRss, args=[new_feed]).start()
        else:
            time.sleep(60)
            print("[{}] Waiting for new RSS feeds.".format(logger_name))


def addOnlyNewRss(feed_url, feed_type, feed_data, entries):
    for entry in entries:
        concatenated_feed = entry.title + " " + BeautifulSoup(entry.description, "html.parser").get_text().strip()
        if not concatenated_feed in feed_data:
            feed_data.add(concatenated_feed)

            naivebayes.raw_data.append(concatenated_feed)
            naivebayes.class_labels.append(feed_type)

            current_feeds[feed_url][1] += 1
            print("[{}] [{}] Adding article ({}):  {}".format(logger_name, feed_url, feed_type, concatenated_feed))


def pollRss(rss_feed):
    feed_data = set()

    feed_url = rss_feed[0]
    feed_type = rss_feed[1]

    current_feeds[feed_url] = [feed_type, 0]

    last_modified = None
    while True:

        feed = feedparser.parse(feed_url, modified=last_modified)

        if len(feed.entries) > 0:
            last_modified = feed.modified
            addOnlyNewRss(feed_url, feed_type, feed_data, feed.entries)
        else:
            print("[{}] [{}] Waiting for entries.".format(logger_name, feed_url))
        time.sleep(10)


def testRss(url):
    last_modified = None
    for i in range(3):
        print("Round nr: " + str(i))
        feed = feedparser.parse(url, modified=last_modified)
        if len(feed.entries) > 0:
            last_modified = feed.modified
            for entry in feed.entries:
                print(entry)
    time.sleep(1)
