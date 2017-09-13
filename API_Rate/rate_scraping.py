#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
from urllib.error import HTTPError,URLError
import re
import pymysql

user=input("Please input your mysql user name:")
password=input("Please input your mysql password:")

conn=pymysql.connect(host='localhost',user=user,passwd=password,db='mysql',charset='utf8', port=3306)
cur=conn.cursor()
cur.execute("USE Exchange_rate_table")

#store information


def store(money,id,Bank_Name,Buying_Rate,Cash_Buying_Rate,Selling_Rate,Cash_Selling_Rate,Update_time):
    cur.execute("UPDATE %s SET Bank_Name='%s',Buying_Rate='%s',Cash_Buying_Rate='%s',Selling_Rate='%s',"
                "Cash_Selling_Rate='%s',Update_time='%s' WHERE id=%s" % (money,Bank_Name,Buying_Rate,Cash_Buying_Rate,Selling_Rate,Cash_Selling_Rate,Update_time,id))
    cur.connection.commit()


def storenew(money,Bank_Name,Buying_Rate,Cash_Buying_Rate,Selling_Rate,Cash_Selling_Rate,Update_time):
    cur.execute(
        "INSERT INTO %s (Bank_Name,Buying_Rate,Cash_Buying_Rate,Selling_Rate,Cash_Selling_Rate,Update_time) VALUES "
        "(\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")"%
        (money,Bank_Name, Buying_Rate, Cash_Buying_Rate, Selling_Rate, Cash_Selling_Rate, Update_time))
    cur.connection.commit()


def find_aims(URL):
    headers={
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4)'
                 ' AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/52.0.2743.116 Safari/537.36'
}

    try:
        middle=urllib.request.Request(URL,headers=headers)
        html=urllib.request.urlopen(middle)
    except (HTTPError,URLError) as e:
        print("can not find url!")
    finally:
        return html


def Store_According_Dollor(money,start,end):
    id=1
    if((cur.execute("SELECT * FROM %s WHERE id=1" % (money))==0)):
        for i in range(start, end):
            result = results[i]
            storenew(money,result[0],result[1],result[2],result[3],result[4],result[5])
    else:
        for i in range(start, end):
            result = results[i]
            store(money,id,result[0],result[1],result[2],result[3],result[4],result[5])
            id=id+1

html=find_aims("http://www.kuaiyilicai.com/bank/rmbfx.html")
aims=re.compile(r'glyphicon-bell.*?<td>&nbsp;(.*?)</td>.*?<td>&nbsp;(\d.\d*).*?</td>.*?<td>&nbsp;(\d.\d*).*?'
                r'</td>.*?<td>&nbsp;(\d.\d*).*?</td>.*?<td>&nbsp;(\d.\d*).*?</td>.*?center">(.*?)</td>',re.S)
results=re.findall(aims,html.read().decode('utf-8'))
#Write_Fixed
Store_According_Dollor("USD",23,38)#store or update USD datas
Store_According_Dollor("EUR",39,54)#store or update EUR datas
Store_According_Dollor("GBP",107,122)#store or update GBP datas
Store_According_Dollor("JPY",73,88)#store or update JPY datas
Store_According_Dollor("CND",123,137)#store or update CND datas
cur.close()
conn.close()

