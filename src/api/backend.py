from rest_api import Server, Client
import pandas as pd
import json  
import time

from database_api import Database

class Api:

    def __init__(self):
        self.localhost = '0.0.0.0'
        self.db = Database()
          
        # docker network ls && docker network inspect <docker-compose network> 
        self.port = 6000
        self.calculation_endpoint = 'http://microservice_calculation:'+str(self.port)

        self.calculation_msg=None

    def handler(self,*args):


        
        # TODO: Add handling functionality

        if args[0]['type'] == 'UPLOAD':
            df = pd.json_normalize(json.loads(args[0]['data']))
            
            while df.shape[0] != 0:

                #TODO need some error checking on ID and values

                id = df['name'][0][-1]
                df_  = df.loc[df['name'] == 'example'+id]
                df.drop(df.index[df['name'] == 'example'+id], axis=0, inplace=True)
                df = df.reset_index(drop=True)

                # table update
                if self.db.checkTable('example'+id) is False:
                    self.db.createTable('example'+id)
                self.db.insertTable(self,'example'+id, df_[['t','v']])

        elif args[0]['type'] == 'QUERY':     
            Client(self).request(self.calculation_endpoint,args[0]['data'])
            
            # TODO The code below is terrible and should be avoided !!!
            while 1:
                time.sleep(0.1)
                if self.calculation_msg is not None:
                    response = self.calculation_msg
                    self.calculation_msg = None
                    return response

    
        elif args[0]['type'] == 'CALCULATION':
            response = 'Calculation response: ave={}, sum={}'.format( args[0]['data']['ave'],args[0]['data']['sum'])
            self.calculation_msg=response
            print(response)
            return response

        else:
            print('unsupported handler argument')
            
    def run(self):
        
        #TODO: Add container functionality
        
        print('Main routine of {} running'.format(self.__class__.__name__))
        while 1:
            time.sleep(2)
            print('Idling..')
        
if __name__ == '__main__':
    Server(Api()).run()
