from sshtunnel import SSHTunnelForwarder
from config import Config
import MySQLdb as mdb
import pandas as pd

server = SSHTunnelForwarder(
    (Config.DATABASE_CONFIG['ssh-server'], Config.DATABASE_CONFIG['ssh-port']),
    ssh_username=Config.DATABASE_CONFIG['user'],
    ssh_password=Config.DATABASE_CONFIG['ssh-password'],
    remote_bind_address=(Config.DATABASE_CONFIG['server'], Config.DATABASE_CONFIG['port']))

server.start()

con = mdb.connect(
            Config.DATABASE_CONFIG['server'],
            Config.DATABASE_CONFIG['user'],
            Config.DATABASE_CONFIG['password'],
            Config.DATABASE_CONFIG['name'], 
            port=server.local_bind_port)

df = pd.read_sql("SELECT * FROM `wp_users` WHERE `user_email` LIKE '%gaiamadservice.dk%'", con)

print(df)

con.close()
server.stop()