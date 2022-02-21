from configparser import ConfigParser
import psycopg2
import numpy as np

class Database():

    def __init__(self):
        self.params = self.config() # postgresql confic defined in database.ini

    def config(self, filename='./database.ini', section='postgresql'):
        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(filename)

        # get section, default to postgresql
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))

        return db

    def version(self):

        sql = 'SELECT version()'

        conn = None

        try:

            conn = psycopg2.connect(**self.params)
            cur = conn.cursor()

            cur.execute(sql)

            print('PostgreSQL database version:')
            print(cur.fetchone())

            cur.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def checkTable(self, table):

        sql = 'SELECT COUNT(*) FROM information_schema.tables WHERE table_name = \''+table+'\';'

        conn = None
        table_exists = False

        try:

            conn = psycopg2.connect(**self.params)
            cur = conn.cursor()

            cur.execute(sql)

            table_exists = (cur.fetchone()[0] == 1)

            cur.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return table_exists

    def createTable(self, table):

        sql = 'CREATE TABLE IF NOT EXISTS \"'+table+'\" ( t bigint, v float(53) NOT NULL );'

        conn = None

        try:

            conn = psycopg2.connect(**self.params)
            cur = conn.cursor()

            cur.execute(sql)

            cur.close()

            conn.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()    

    def insertTable(self, *args):

        # build insert query. #TODO how to handle large insert operations

        table = args[1]
        columns ='(\"'+args[2].columns[0]+'\"'+','+'\"'+args[2].columns[1]+'\")'
        values = '(\''+str(args[2]['t'][0])+'\',\''+str(args[2]['v'][0])+'\')'

        for i in range(1,args[2].shape[0]):
            values += ',(\''+str(args[2]['t'][i])+'\',\''+str(args[2]['v'][i])+'\')'

        sql = 'INSERT INTO '+table+' '+columns+' VALUES '+values+';'

        conn = None

        try:

            conn = psycopg2.connect(**self.params)
            cur = conn.cursor()

            cur.execute(sql)

            cur.close()

            conn.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

if __name__ == '__main__':
    db = Database()

    db.checkTable('example1')
    print(db.version())
    print()

