from rest_api import Server, Client
import time

from database_api import Database

class Calculation:

    def __init__(self):
        self.localhost = '0.0.0.0'
        self.db = Database()

        # docker network ls && docker network inspect <docker-compose network> 
        self.port = 6000
        self.api_endpoint = 'http://microservice_api:'+str(self.port)

    def handler(self,*args):
       Client(self).request(self.api_endpoint,{'type':'CALCULATION',\
                                               'data':self.db.queryTable(args)})

    def run(self):
        
        #TODO: Add container functionality
        
        print('Main routine of {} running'.format(self.__class__.__name__))
        while 1:
            time.sleep(2)
            print('Idling..')
        
if __name__ == '__main__':
    Server(Calculation()).run()

    