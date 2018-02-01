from urllib import request
# import requests
import uuid  
import pyamf
import json,datetime  
from pyamf import remoting  
from pyamf.flex import messaging
class DypzqgpjPara:
    def __init__(self,BreedInfoPo):
        self.breedInfoDl = None
        self.theCycle = '365' #控制查询周期
        self.breedInfo = BreedInfoPo
class BreedInfoPo():
    def __init__(self):
        self._children = None	
        self.parentcode = None	
        self.children = None	
        self.itemcode = 'AE01001'
        self.itemname = '大白菜' #品种名
pyamf.register_class(DypzqgpjPara, alias='com.itown.kas.pfsc.report.po.DypzqgpjPara') 
pyamf.register_class(BreedInfoPo, alias='com.itown.kas.pfsc.report.po.BreedInfoPo') 
# 此设置主要更换operation的类型
msg = messaging.RemotingMessage(messageId=str(uuid.uuid1()).upper(),clientId=str(uuid.uuid1()).upper(),operation='getDypzqgpj',destination='reportStatService',timeToLive=0,timestamp=0) 
msg.body = [DypzqgpjPara(BreedInfoPo()),None]
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
# info = amf_parse_info.bodies[3]
info = amf_parse_info.bodies[0][1].body.body['statData']
for recorde in info:
    print(recorde)
