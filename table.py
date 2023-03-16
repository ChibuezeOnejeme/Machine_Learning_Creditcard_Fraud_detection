from uuid import uuid4
#tx_id uuid PRIMARY KEY Default uuid_generate_v4()  , 
table_shema = """Create Table IF NOT EXISTS  credit_card ( tx_id uuid PRIMARY KEY Default uuid_generate_v4(),
    time        integer,
    V1          Float,
    V2          Float,
    V3          Float,
    V4          Float,
    V5          Float,
    V6          Float,
    V7          Float,
    V8          Float,
    V9          Float,
    V10         Float,
    V11         Float,
    V12         Float,
    V13         Float,
    V14         Float,
    V15         Float,
    V16         Float,
    V17         Float,
    V18         Float,
    V19         Float,
    V20         Float,
    V21         Float,
    V22         Float,
    V23         Float,
    V24         Float,
    V25         Float,
    V26         Float,
    V27         Float,
    V28         Float,
    amount      Float
   
   );"""





cassandra_table = """Create Table IF NOT EXISTS  credit_card( tx_id UUID PRIMARY KEY ,
    V1          Float,
    V2          Float,
    V3          Float,
    V4          Float,
    V5          Float,
    V6          Float,
    V7          Float,
    V8          Float,
    V9          Float,
    V10         Float,
    V11         Float,
    V12         Float,
    V13         Float,
    V14         Float,
    V15         Float,
    V16         Float,
    V17         Float,
    V18         Float,
    V19         Float,
    V20         Float,
    V21         Float,
    V22         Float,
    V23         Float,
    V24         Float,
    V25         Float,
    V26         Float,
    V27         Float,
    V28         Float,
    amount      Float,
    p           int
   );"""

#columns for updated_table in postgres
columns =('time','v1','v2','v3','v4','v5','v6','v7','v8','v9','v10','v11','v12','v13','v14','v15','v16','v17','v18','v19','v20','v21','v22','v23','v24','v25','v26','v27','v28','amount')

columns_consumer =('tx_id','time','v1','v2','v3','v4','v5','v6','v7','v8','v9','v10','v11','v12','v13','v14','v15','v16','v17','v18','v19','v20','v21','v22','v23','v24','v25','v26','v27','v28','amount')

