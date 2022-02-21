from configparser import ConfigParser
import psycopg2
import numpy as np
import pandas as pd

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

    def queryTable(self, *args):

        table = 'example' + args[0][0]['id']
        t0 = args[0][0]['t0']
        t1 = args[0][0]['t1']

        if t0 is not None and t1 is not None:
            sql = 'SELECT '+'\"t\",'+'\"v\"'+ ' FROM ' +table+ ' WHERE ' + '\"t\"' + ' BETWEEN ' +'\''+t0+'\'' +' AND '+'\''+t1+'\''+';'
        else:
            sql = 'SELECT '+'\"t\",'+'\"v\"'+ ' FROM ' +'\"'+table+'\"'+ ' *;' 
 
        try:

            conn = psycopg2.connect(**self.params)
            cur = conn.cursor()

            cur.execute(sql)

            response = np.array(cur.fetchall())

            sum = np.sum(response[:,1])
            ave = np.mean(response[:,1])

            cur.close()

            conn.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return {'ave':ave, 'sum':sum}

if __name__ == '__main__':
    db = Database()

    db.checkTable('example1')
    print(db.version())
    print()

