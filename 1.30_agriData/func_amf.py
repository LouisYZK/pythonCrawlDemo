from urllib import request
import requests
import uuid  
import pyamf
import json,datetime 
import socket 
from pyamf import remoting  
from pyamf.flex import messaging,ArrayCollection
# 注册body类
class DyscdpzPara():
    def __init__(self,StartDate,EndDate,SelectedBreeds,PMarketInfo,breedInfo):
        self.startDate = StartDate#2008-1-1 0:00:00 date类型
        self.endDate = EndDate #2008-1-2 0:00:00 date类型
        self.selectedBreeds	=SelectedBreeds #对象
        self.theDateType = '1'
        self.theSorting = '0'
        self.marketInfo	= PMarketInfo #对象
        self.theCycle = '7'
        self.breedInfo = breedInfo # 对象
class SelectedBreeds():
    def __init__(self,BreedInfoPo):
        pass
class BreedInfoPo():
    def __init__(self,item_code,item_name,children0,children1):
        self._children = children0	
        self.parentcode	= None	
        self.children = children1	
        self.itemcode = item_code	#String	AA01002
        self.itemname = item_name #String	面粉
class BreedInfo():
    def __init__(self,itemcode,itemname):
        self._children = None	
        self.parentcode = None	
        self.children = None	
        self.itemcode = itemcode #AA01002
        self.itemname = itemname #面粉
class PMarketInfo():
    def __init__(self,market_code,market_name):
        self.marketCode	= market_code
        self.marketName = market_name

pyamf.register_class(DyscdpzPara, alias='com.itown.kas.pfsc.report.po.DyscdpzPara')
# pyamf.register_class(SelectedBreeds, alias='flex.messaging.io.ArrayCollection')
pyamf.register_class(BreedInfoPo, alias='com.itown.kas.pfsc.report.po.BreedInfoPo')
pyamf.register_class(PMarketInfo, alias='com.itown.kas.pfsc.report.po.PMarketInfo')
pyamf.register_class(BreedInfo, alias='com.itown.kas.pfsc.report.po.BreedInfoPo')
def construct_request(startDate,endDate,market_code,market_name,item_code,item_name):
    breedInfoPo = BreedInfoPo(None,None,None,None)
    select_breed = BreedInfoPo(item_code,item_name,None,None)
    select = ArrayCollection([select_breed])
    market = PMarketInfo(market_code,market_name)
    msg = messaging.RemotingMessage(messageId=str(uuid.uuid1()).upper(),clientId=str(uuid.uuid1()).upper(),operation='getDyscDpzData',destination='reportStatService',timeToLive=0,timestamp=0)
    msg.body = [DyscdpzPara(startDate,endDate,select,market,breedInfoPo)]
    msg.headers['DSEndpoint'] = None  
    msg.headers['DSId'] = str(uuid.uuid1()).upper()
    req = remoting.Request('null',body = (msg,))
    env = remoting.Envelope(amfVersion=pyamf.AMF3)
    env.bodies = [('/1',req)]
    data = bytes(remoting.encode(env).read())
    return data
# data即为构造出amf编码后的请求结构
def getResponse(data):
    url = 'http://jgsb.agri.cn/messagebroker/amf'
    req =request.Request(url,data,headers={'Content-Type': 'application/x-amf'})
    opener = request.build_opener()
    response = opener.open(req,timeout = 5).read()
    return response
def amfParse(response):
    amf_parse_info = remoting.decode(response)
    info = amf_parse_info.bodies[0][1].body.body['statData']
    date = amf_parse_info.bodies[0][1].body.body['dateStr']
    return info,date
timeout = 3
# socket.setdefaulttimeout(timeout)
Date = datetime.datetime(2012,1,1,16,00,00) 
finalEndDate = datetime.datetime(2018,1,30,16,00,00)
while Date < finalEndDate:
    startDate = Date
    endDate = Date + datetime.timedelta(days = 1) 
    # 输入的后四个参数的编码对照表见 breed_code.csv 和 market_code.csv
    data = construct_request(startDate,endDate,'4101016','豫万邦国际','AE01001','大白菜')
    try:
        resp = getResponse(data)
        print(amfParse(resp))
    except Exception:
        print('等待超时')
    Date = endDate

    









    


    
    