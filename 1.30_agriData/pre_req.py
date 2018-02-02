# 打开页面加载flash会先发送一个请求，返回所有批发市场和品种的编号。而这两个编号也是接下面请求的必需的input参数
from urllib import request
import uuid  
import pyamf
import json,datetime 
from pyamf import remoting  
from pyamf.flex import messaging
import csv
# 很显然operation是 getInitData 初始化数据
msg = messaging.RemotingMessage(messageId=str(uuid.uuid1()).upper(),clientId=str(uuid.uuid1()).upper(),operation='getInitData',destination='reportStatService',timeToLive=0,timestamp=0)
msg.body = []
msg.headers['DSEndpoint'] = None  
msg.headers['DSId'] = str(uuid.uuid1()).upper() 
req = remoting.Request('null',body=(msg,))
env = remoting.Envelope(amfVersion=pyamf.AMF3)
env.bodies = [('/1',req)]
data = bytes(remoting.encode(env).read())
url = 'http://jgsb.agri.cn/messagebroker/amf'
req =request.Request(url,data,headers={'Content-Type': 'application/x-amf'})
opener = request.build_opener()
response = opener.open(req).read()
amf_parse_info = remoting.decode(response)
breed_info = amf_parse_info.bodies[0][1].body.body[0]
fp = open('breed_code.csv','w')
csvFile = csv.writer(fp)
for item in breed_info:
    items_info = item['children']
    for item2 in items_info:
        csvFile.writerow((item2['itemname'],item2['itemcode']))
fp2 = open('market_code.csv','w')
market_info = amf_parse_info.bodies[0][1].body.body[1]
csvFile = csv.writer(fp2)
for item in market_info:
    items_info = item['children']
    for item2 in items_info:
        csvFile.writerow((item2['marketName'],item2['marketCode']))
# csvFile.close()
fp.close()
fp2.close()
