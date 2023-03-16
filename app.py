from flask import Flask, redirect, url_for, request,render_template
from celery import Celery
from celery import chain
import pandas as pd
import json
import psycopg2
from access_secrets import postgres_Secrets,cs_secrets,redis_secrets
from table import table_shema,columns,columns_consumer
from cassandra.cluster import Cluster,ConsistencyLevel
from cassandra.auth import PlainTextAuthProvider
from table import cassandra_table
import joblib

import ast

app = Flask(__name__)


#app = Flask(name)

#Configure the redis server
app.config['CELERY_BROKER_URL'] =redis_secrets.get('BROKER')          
app.config['CELERY_RESULT_BACKEND'] =redis_secrets.get('BACKEND')
#creates a Celery object
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'],backend=['CELERY_RESULT_BACKEND'])
celery.conf.update(app.config)


model = joblib.load('mobileBrain.pipeline')
postgres_table ='credit_card'

def connect_to_aws_cassandra():                                                                          
                                                                     
        auth_provider = PlainTextAuthProvider(username=cs_secrets.get('USERNAME'),password=cs_secrets.get('PASSWORD'))
        cluster = Cluster([cs_secrets.get('ADDRESS')],auth_provider= auth_provider)
        session = cluster.connect()
        return session

def write_Df_to_cassandra(df):
     cur =connect_to_aws_cassandra()
     for item in df.values:
         print(item[29])
     
         query ="""INSERT INTO machine_learning.credit_card(tx_id,v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12,v13,v14,v15,v16,v17,v18,v19,v20,v21,v22,v23,v24,v25,v26,v27,v28,amount,p)  VALUES(now(),?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"""

         prepared = cur.prepare(query)
         #prepared.consistency_level=ConsistencyLevel.LOCAL_QUORUM
      
         cur.execute(prepared,(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8],item[9],item[10],item[11],item[12],item[13],item[14],item[15],item[16],item[17],item[18],item[19],item[20],item[21],item[22],item[23],item[24],item[25],item[26],item[27],item[28],int(item[29])))
         

         print('table loaded')






# postgres Database for extracting information for kafka
def connect_postgres():

        conn = psycopg2.connect(
       host=postgres_Secrets.get('HOST'),
       database=postgres_Secrets.get('DATABASE'),
       user=postgres_Secrets.get('USER'),
       port=postgres_Secrets.get('PORT')
       )
        return conn.cursor()
    

@celery.task 
def row_for_prediction(id):
           cur =  connect_postgres()
        # This gets a row in postgres and converts to json
           query = f"select row_to_json(row)from (select * from credit_card WHERE tx_id= '{id}') row;"
           record = cur.execute(query)
           new =   cur.fetchall()
           #print(new)
        
           for r in new:
              my_json= json.dumps(r[0])
              new_data = my_json
              print(new_data)
              res =ast.literal_eval(new_data) #this converted dict string to dictionary
              print(type(res))
              
              df = pd.DataFrame.from_dict([res]) #
              #print(df)
              df = df.drop(['tx_id','time'],axis=1)
              outcome =model.best_estimator_.predict(df)[0]
              df['p'] = outcome
              write_Df_to_cassandra(df)
              
              


@app.route('/', methods=['POST', 'GET'])
def home():
     
     if request.method == 'POST':
          id = request.form['client']
          print(id)
         
          row_for_prediction.delay(id)
          
           
          
       
    
     return render_template('home.html')


      




if __name__ == '__main__':
  
    app.run(host='0.0.0.0', debug=True, port=5000)














"""
Developer: chibueze onejeme
Full Stack Web Developer [ Python Flask & Django]
Data and Machine Learning Engineer
Stay in touch with me: 
GitHub:https://github.com/ChibuezeOnejeme
LinkedIn: https://www.linkedin.com/in/chibueze-onejeme-b9756549/
Gmail:onejemechibueze33@gmail.com 
"""







































