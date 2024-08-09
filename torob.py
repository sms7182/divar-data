
import uuid
import requests
import json
from datetime import datetime,timezone
import psycopg2
import time
import sys

connection=psycopg2.connect(database="divardb",user="postgres",password="postgres",host="localhost",port=5432)
cursor=connection.cursor()



def insert_torob(torob_id,name,domain,shop_type,city):
    sql="insert into torob_data(id,torob_id,name,domain,shop_type,city) values(%s,%s,%s,%s,%s,%s)"
    
    cursor.execute(sql,(str(uuid.uuid4()),torob_id,name,domain,shop_type,city))
    cursor.connection.commit()



    
url="https://api.torob.com/v4/internet-shop/list/?page={page}&shop_type=all&size=20"

now=datetime.now()
ns=now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

ind=1
while True:
    url=url.format(page=ind)
    print(url)
    x=requests.get(url)
    print(x.text)
    obj=json.loads(x.text)
    if obj is not None:
        if obj['results'] is not None:
            ind=ind+1
            results=obj['results']
            for rs in results:
                insert_torob(rs['id'],rs['name'],rs['domain'],rs['shop_type'],rs['city'])

    time.sleep(30)
                

