import cherrypy, os, threading

from mako.template import Template
from util import htmlparser

class Index:
    @cherrypy.expose
    def index(self):
        return "Index page. Nothing to see here :)."

class Scrape:
    @cherrypy.expose
    def index(self):
        return Template(filename=getTemplatePath("templates/footemplate.html")).render()


# Entry point
root = Index()          # "/"
root.scrape = Scrape()  # "/scrape"

if __name__ == '__main__':
    threading.Thread(target=htmlparser.startParsing, name="RSSParser").start()
    cherrypy.quickstart(root)

def getTemplatePath(template_name):
    return os.path.join(template_name)