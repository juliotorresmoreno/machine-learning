
from keras.layers import Conv1D, MaxPooling2D
Conv1D(16, (7), activation='sigmoid', input_shape=(28, 28))

#%%
import numpy as np
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt

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


#%%
tmp = query("""
    SELECT b.IdValorParametro campo_id
      FROM paspe.paspe_campos a
INNER JOIN paspe.extidi_valorparametro b ON a.IdParametro = b.IdParametro
     WHERE a.UtilizaParaCalculo = 1
""")
campos = []
strcampos = ""
for row in tmp:
    campos.append(row[0])
    strcampos = strcampos + "`" + str(row[0]) + "`, "
strcampos = strcampos + "`conteo`"



#%%
modelo = LogisticRegression()

#%%
modelo = DecisionTreeClassifier(max_depth=30)

#%%
def aprender(steps):
    x = np.array(query("""
        SELECT {0}
            FROM encuestas
            WHERE Id_alumn_programa > 0
              AND conteo > 30
            LIMIT 0, {1}
    """.format(strcampos, str(steps * 1000))))
    y = np.array(query("""
        SELECT deserto
          FROM encuestas
         WHERE Id_alumn_programa > 0
           AND conteo > 30
         LIMIT 0, {0}
    """.format(str(steps * 1000))))
    modelo.fit(x, y)

#%%
def score(start):
    x = np.array(query("""
        SELECT {0}
          FROM encuestas
         WHERE Id_alumn_programa > 0
           AND conteo > 30
         LIMIT {1}, 1000
    """.format(
        strcampos, 
        str(start*1000))
    ))
    y = np.array(query("""
        SELECT deserto
          FROM encuestas
         WHERE Id_alumn_programa > 0
           AND conteo > 30
         LIMIT {0}, 1000
    """.format(str(start*1000))))
    return modelo.score(x, y)
#%%
def predit(start):
    x = np.array(query("""
        SELECT {0}
          FROM encuestas
         WHERE Id_alumn_programa > 0
           AND conteo > 30
         LIMIT {1}, 1000
    """.format(
        strcampos, 
        str(start*1000))
    ))
    predit = modelo.predict(x)
    return predit

#%%
aprender(20)

#%%
result = predit(8)
print(result)

#%%
result = score(11)
print(result)

#%%
modelo.feature_importances_

#%%
cnx.close()