#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
from urllib.error import HTTPError,URLError
import re
import pymysql
#The password and uer need to be change.
conn=pymysql.connect(host='localhost',user='root',passwd='password',db='mysql',charset='utf8', port=3306)
cur=conn.cursor()
cur.execute("USE Exchange_rate_table")
#store information
def store(Currency_Name,Buying_Rate,Cash_Buying_Rate,Selling_Rate,Cash_Selling_Rate,Exchange_Rate_Base_Price):
    cur.execute("INSERT INTO LatestInformation (Currency_Name,Buying_Rate,Cash_Buying_Rate,Selling_Rate,Cash_Selling_Rate,Exchange_Rate_Base_Price) VALUES (\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")",
                (Currency_Name,Buying_Rate,Cash_Buying_Rate,Selling_Rate,Cash_Selling_Rate,Exchange_Rate_Base_Price))
    cur.connection.commit()

headers={
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
}

aims=re.compile(r'height="30".*?#F7F7F7.*?href=".*?">(.*?)</td>.*?#F7F7F7">(.*?)</td>.*?#F7F7F7">(.*?)</td>.*?#F7F7F7">(.*?)</td>.*?#F7F7F7">(.*?)</td>.*?#F7F7F7">(.*?)</td>',re.S)
try:
    middle=urllib.request.Request("http://www.usd-cny.com",headers=headers)
    html=urllib.request.urlopen(middle)
except (HTTPError,URLError) as e:
    print("can not find url!")
results=re.findall(aims,html.read().decode('gbk'))
len=len(results)
for result in results:
    store(result[0],result[1],result[2],result[3],result[4])

cur.close()
conn.close()

