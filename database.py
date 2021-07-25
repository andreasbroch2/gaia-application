from sshtunnel import SSHTunnelForwarder
from config import Config
import MySQLdb as mdb

class Database:

    def __init__(self, query):
        server = SSHTunnelForwarder(
        (Config.DATABASE_CONFIG['ssh-server'], Config.DATABASE_CONFIG['ssh-port']),
        ssh_username=Config.DATABASE_CONFIG['user'],
        ssh_password=Config.DATABASE_CONFIG['ssh-password'],
        remote_bind_address=(Config.DATABASE_CONFIG['server'], Config.DATABASE_CONFIG['port']))

        server.start()
        try:
            con = mdb.connect(
            Config.DATABASE_CONFIG['server'],
            Config.DATABASE_CONFIG['user'],
            Config.DATABASE_CONFIG['password'],
            Config.DATABASE_CONFIG['name'], 
            port=server.local_bind_port)
        except:
            print('Cant connect')
        print('Connected')

        cursor=con.cursor()
        print(query)
        resp = cursor.execute(query)
        print(resp)
        con.commit()
        con.close()
        server.stop()

