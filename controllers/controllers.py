import cherrypy, os, connection
from mako.template import Template


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
    return os.path.join(parent_dir, template_name)

parent_dir = os.path.abspath(os.pardir)

root = Index()          # "/"
root.scrape = Scrape()  # "/scrape"

if __name__ == '__main__':
    cherrypy.quickstart(root)
