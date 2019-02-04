import os
import cherrypy
import random
import string
from bse import *
from redis_server import FilterRedis
config = {
    'global' : {
        'server.socket_host' : '127.0.0.1',
        'server.socket_port' : 8085
    }
}


class App:
   
    @cherrypy.expose
    def index(self):
        #return self.html_string
        main()
        return open('/home/basant/Desktop/WebInfo/show_data.html')

    @cherrypy.expose
    def generate(self, length=8):
        return''.join(random.sample(string.hexdigits, 8))

    @cherrypy.expose
    def process_bse_data(self):
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
        store = FilterRedis()

        return store.search_result(search_text)
        #return {'key': 'value'}
    

if __name__ == '__main__':
    cherrypy.quickstart(App(), '/', config)