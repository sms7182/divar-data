
import uuid
import requests
import json
from datetime import datetime,timezone
import psycopg2
import time

connection=psycopg2.connect(database="divardb",user="postgres",password="postgres",host="localhost",port=5432)
cursor=connection.cursor()

def insert_widget(data,nt):
    sql="insert into divar_raw(id,widgets,timestr) values(%s,%s,%s)"
    
    cursor.execute(sql,(str(uuid.uuid4()),data,nt))
    cursor.connection.commit()
    

def insert_detail(id,token,tm):
    sql="insert into divar_widget(id,token,creation_date) values(%s,%s,%s)"
    cursor.execute(sql,(id,token,tm))
    cursor.connection.commit()
    
url='https://api.divar.ir/v8/postlist/w/search'

now=datetime.now()
ns=now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

while True:
    pyload={"city_ids":["1"],"pagination_data":{"@type":"type.googleapis.com/post_list.PaginationData","last_post_date":ns,"page":1,"layer_page":1,"search_uid":"58d24c4e-5cf0-432d-bfe2-0498f775c624"},"search_data":{"form_data":{"data":{"category":{"str":{"value":"ROOT"}}}}}}
    x=requests.post(url,json=pyload)

    obj=json.loads(x.text)
    insert_widget(x.text,ns)

    if obj is not None:
        widgets=obj['list_widgets']
    
        
        for widget in widgets:
            data=widget['data']
            token=data['action']['payload']['token']
            img_url=data['image_url']
            slash_sub=str.split(img_url,'/')
            lst=slash_sub[len(slash_sub)-1]
            ids=str.split(lst,'.')
            insert_detail(ids[0],token,ns)
    time.sleep(1)    