from sshtunnel import SSHTunnelForwarder
import MySQLdb as mdb
import pandas as pd

server = SSHTunnelForwarder(
    ('34.89.176.38', 15315),
    ssh_username="gaiamadservice",
    ssh_password="6jEaDYxw1p5oUnP",
    remote_bind_address=('127.0.0.1', 3306))

server.start()

con = mdb.connect('127.0.0.1', "gaiamadservice", "oWCQ95skCuIA6CB", "gaiamadservice", port=server.local_bind_port)

df = pd.read_sql("SELECT * FROM `wp_users` WHERE `user_email` LIKE '%gaiamadservice.dk%'", con)

print(df)

con.close()
server.stop()