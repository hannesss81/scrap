import time, threading, feedparser

rss_feed_queue = ["http://www.ft.com/rss/markets/europe",
                  "http://feed.businesswire.com/rss/home/?rss=G1QFDERJXkJeEFpRVQ==",
                  "https://rss.sciencedaily.com/matter_energy/engineering.xml",
                  "http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"]

def startParsing():
    global rss_feed_queue
    print("RSS Feed parsing initialized.")

    while True:
        if (rss_feed_queue):
            new_feed = rss_feed_queue.pop()
            print("Got a new feed: " + new_feed)
            threading.Thread(target=pollRss, args=[new_feed]).start()
        else:
            time.sleep(60)
            print("[{}] Waiting for new RSS feeds.".format(threading.current_thread().name))


def addOnlyNewRss(rss_feed, feed_data, entries):
    for entry in entries:
        concatenated_feed = entry.title + " " + entry.description
        if not concatenated_feed in feed_data:
            feed_data.add(concatenated_feed)
            print("[{}] Adding: {}".format(rss_feed, concatenated_feed))

def pollRss(rss_feed):
    feed_data = set()

    last_modified = None
    while True:

        feed = feedparser.parse(rss_feed, modified=last_modified)

        if len(feed.entries) > 0:
            last_modified = feed.modified
            print("[{}] #### Adding new records. ####".format(rss_feed))
            addOnlyNewRss(rss_feed, feed_data, feed.entries)
        else:
            print("[{}] Waiting for entries.".format(rss_feed))
        time.sleep(10)





