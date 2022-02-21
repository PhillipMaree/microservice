from distutils.log import warn
from flask_restful import Resource, Api
from flask import Flask, request
from threading import Thread
from http import HTTPStatus
import requests

class RestApi:

    def __init__(self,container):
        self.app = Flask(__name__)
        self.api = Api(self.app)

        self.container_name = container.__class__.__name__
        self.container_localhost = container.localhost
        self.container_port = container.port

        self.container_run = container.run \
             if(hasattr(container,'run') and callable(container.run)) else None
        self.container_handler = container.handler \
             if(hasattr(container,'handler') and callable(container.handler)) else None
              
    
class Server(RestApi):

    def __init__(self,container):
        RestApi.__init__(self,container)

        #class decorator
        class classtypes(Resource):
            pass
        classtypes = (type, type(classtypes))

        attributes = ['container_name','container_handler']
        directory = [n for n in dir(self) if not n.startswith("_")]
        innerclasses = [n for n in directory if isinstance(getattr(self, n), classtypes)]
        
        for c in innerclasses:
            c = getattr(self, c)
            for a in attributes:
                if not hasattr(c, a):
                    setattr(c, a, getattr(self, a))

    class Handler(Resource):
        def put(self):
            return self.container_handler(request.json)

    def run(self):

        self.api.add_resource(self.Handler, '/handler')

        Thread(target = self.container_run).start()
        Thread(target = self.app.run,args=list([self.container_localhost, self.container_port])).start()

class Client(RestApi):

    def __init__(self,container):
        RestApi.__init__(self,container)

    def request(self,endpoint_url, data=None):
        try:
            return requests.put('{0}/handler'.format(endpoint_url), json = data).json()
        except:
            warn('Endpoint {} not responding'.format(endpoint_url))