import cherrypy, os, threading

from mako.template import Template
from util import htmlparser
from util import naivebayes

prediction_data = None


def getTemplatePath(template_name):
    return os.path.join(template_name)


class Index:
    @cherrypy.expose
    def index(self):
        return "Index page. Nothing to see here :)."


class Scrape:
    @cherrypy.expose
    def index(self):
        global prediction_data

        prediction_data_temp = None
        if prediction_data:
            prediction_data_temp = prediction_data
            prediction_data = None

        return Template(filename=getTemplatePath("templates/control_page.html")) \
            .render(
            feed_urls=htmlparser.current_feeds,
            prediction_data=prediction_data_temp,
            trained = naivebayes.last_trained
        )

    @cherrypy.expose
    def retrain(self):
        naivebayes.extractFeatures()
        raise cherrypy.HTTPRedirect("index")

    @cherrypy.expose
    def add_rss(self, url, type):
        htmlparser.rss_feed_queue.append([url, type])
        raise cherrypy.HTTPRedirect("index")

    @cherrypy.expose
    def predict(self, text):
        global prediction_data
        prediction_data = naivebayes.predict(text), text
        raise cherrypy.HTTPRedirect("index")

    @cherrypy.expose
    def test_rss(self, url):
        htmlparser.testRss(url)
        raise cherrypy.HTTPRedirect("index")


# Entry point
root = Index()  # "/"
root.scrape = Scrape()  # "/scrape"

if __name__ == '__main__':
    threading.Thread(target=htmlparser.startParsing, name="RSSParser").start()
    cherrypy.quickstart(root)
