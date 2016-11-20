import cherrypy, os, threading

from mako.template import Template
from util import connection, htmlparser

class Index:
    @cherrypy.expose
    def index(self):
        return """
        <a href="/scrape/" >Scrape</a>
        """

class Scrape:
    @cherrypy.expose
    def index(self):
        connection.open_connections(["http://www.postimees.ee"])
        return Template(filename=getTemplatePath("templates/footemplate.html")).render()

def getTemplatePath(template_name):
    return os.path.join(template_name)

root = Index()          # "/"
root.scrape = Scrape()  # "/scrape"

if __name__ == '__main__':
    threading.Thread(target=htmlparser.startParsing, name="HTMLParser").start()
    cherrypy.quickstart(root)
