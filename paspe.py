


#%%
from mysql import connector

#%%
cnx = connector.connect(
    user='root', 
    password='paramore',
    host='127.0.0.1',
    database='paspe'
)

#%%
def query(sql):
    cursor = cnx.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    return data
