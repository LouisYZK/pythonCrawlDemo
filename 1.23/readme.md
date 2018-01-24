# 爬取基于Flex技术的网站数据
Flex技术是网站运用flash方法与客户端进行数据通信，数据的格式可以是txt,json或amf等。
AMF是一种二进制编码方式，其在flash传输效率高,以农业信息网数据为例，爬取的方式与一般ajax分析相同。通过抓包分析请求头和响应数据，然后构造请求、接受返回数据。

下面我以中国农产品批发市场每日价格行情http://jgsb.agri.cn/controller?SERVICE_ID=REGISTRY_JCSJ_MRHQ_SHOW_SERVICE&recordperpage=15&newsearch=true&login_result_sign=nologin为例来分析爬取方法
## 请求包分析
目前Chales抓包工具能够支持将AMF编码解析成明文形式，便于我们分析。请求截图如下：

![](https://ws1.sinaimg.cn/large/6af92b9fgy1fnrp6i3gcej20i608f0tf.jpg)

图中可以看到请求的body包含一个com.itown.kas.pfsc.report.po.HqPara对象和四个参数，结合网页可知为flash上的四个选择菜单，可以选择省份和批发市场名称等。对此结合pyawf的文档可以写出构造请求函数如下：
```python
from urllib import request
import uuid  
import pyamf
import json,datetime  
from pyamf import remoting  
from pyamf.flex import messaging  
class HqPara:    
    def __init__(self):  
        self.marketInfo = None  
        self.breedInfoDl = None  
        self.breedInfo = None  
        self.provice = None   
# registerClassAlias("personTypeAlias", Person);  
# 注册自定义的Body参数类型，这样数据类型com.itown.kas.pfsc.report.po.HqPara就会在后面被一并发给服务端（否则服务端就可能返回参数不是预期的异常Client.Message.Deserialize.InvalidType）  
pyamf.register_class(HqPara, alias='com.itown.kas.pfsc.report.po.HqPara')    
# 构造flex.messaging.messages.RemotingMessage消息
msg = messaging.RemotingMessage(messageId=str(uuid.uuid1()).upper(),  
                                    clientId=str(uuid.uuid1()).upper(),  
                                    operation='getHqSearchData',  
                                    destination='reportStatService',  
                                    timeToLive=0,  
                                    timestamp=0)  
# 第一个是查询参数，第二个是页数，第三个是控制每页显示的数量（默认每页只显示15条）但爬取的时候可以一下子设置成全部的数量
# 构造请求数据
def getRequestData(page_num,total_num):
    msg.body = [HqPara(),str(page_num), str(total_num)]  
    msg.headers['DSEndpoint'] = None  
    msg.headers['DSId'] = str(uuid.uuid1()).upper()  
    # 按AMF协议编码数据  
    req = remoting.Request('null', body=(msg,))  
    env = remoting.Envelope(amfVersion=pyamf.AMF3)  
    env.bodies = [('/1', req)]  
    data = bytes(remoting.encode(env).read())
    return data
# 返回一个请求的数据格式
```
需要说明的是，pyamf不支持python3，需要替换为Py3AMF,但调用方法与原来相同。
## 返回包分析
### 获得相应：
```python
def getResponse(data):
    url = 'http://jgsb.agri.cn/messagebroker/amf'
    req = request.Request(url, data, headers={'Content-Type': 'application/x-amf'})
    # 解析返回数据  
    opener = request.build_opener()          
    return opener.open(req).read()
```
![](https://ws1.sinaimg.cn/large/6af92b9fgy1fnrp9qrkprj20if07iq3k.jpg)
结合页面分析可以看出，body[0]包含了请求条数的所有数据，remoting对象可以直接将其解析为字典。body[2]是当前的页数，body[3]返回的是当前信息的总条数。
### 解析
那么就可以写出解析函数：
```python
def getContent(response):
    amf_parse_info = remoting.decode(response)
    # 数据总条数
    total_num = amf_parse_info.bodies[0][1].body.body[3]
    info = amf_parse_info.bodies[0][1].body.body[0]
    return total_num, info
```
返回的total_num是当前页面数据的总量，可以请求一次后获取，然后直接一次性地获取全部数据。（经过测试这个网站的服务器连续请求容易返回503error,所以最好一次性请求所有数据）
### 存储
因为解析出的数据格式是字典，所以直接存为json格式：
```python
def store2json(info):
    res = []
    for record in info:
        record['reportDate'] = record['reportDate'].strftime('%Y-%m-%d %H:%M:%S')
        record['auditDate'] = record['auditDate'].strftime('%Y-%m-%d %H:%M:%S')
        res.append(record)
    fp = open('info.json','w') 
    json.dump(res,fp,indent=4)
    fp.close()
```
## 测试
对今天（18.1.24）的界面进行了测试：
```python
# 获取数据量
reqData = getRequestData(1,15)
rep = getResponse(reqData)
total_num,info = getContent(rep)
# 一次请求完成
reqData = getRequestData(1,total_num)
rep = getResponse(reqData)
total_num,info = getContent(rep)
store2json(info)
```