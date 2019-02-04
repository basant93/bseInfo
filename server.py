import os
import cherrypy
import random
import string
from bse import *
from redis_server import FilterRedis

#Config for redis db
config = {
    'global' : {
        'server.socket_host' : '127.0.0.1',
        'server.socket_port' : 8085
    }
}


class App:
   
    @cherrypy.expose
    def index(self):
        """
        Include the show_data html page. It is the main page where user can search on basis 
        of name. Output is displayed below.
        """
        main()
        return open('/home/basant/Desktop/WebInfo/show_data.html')

    @cherrypy.expose
    def generate(self, length=8):
        """
        Generate a random number and return it. 
        """
        return''.join(random.sample(string.hexdigits, 8))

    @cherrypy.expose
    def process_bse_data(self):
        """
        Sample form made in cherryPy to demonstrate connection between UI and cherryPy.
        """
        return """
        <html> 
            <body>
                <form method="get" action="generate">
                <input type="text" value="8" name="length" />
                <button type="submit">Give it now!</button>
                </form>
            </body>
        </html>
        """
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def bse_response(self, search_text=None):
        """
        Query on redis db based on search text
        """
        store = FilterRedis()

        return store.search_result(search_text)
    

if __name__ == '__main__':
    cherrypy.quickstart(App(), '/', config)