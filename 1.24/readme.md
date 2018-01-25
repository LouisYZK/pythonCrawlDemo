# 爬取国家林木种质资源品台数据
[页面链接](http://www.nfgrp.cn/data/list/resource_detailpl_sy.shtml)
国家林木资源平台收录了我国目前林木种质的信息，信息涵盖完全。
## 数据生成方式分析
js渲染翻页 + 详细数据json传递
无论是翻页的数据还是进入链接的详细数据都是json格式传递，所以找出渲染规律后是非常方便爬取的。
### 翻页请求：
![翻页请求XHR信息](https://ws1.sinaimg.cn/large/6af92b9fly1fnsowg042kj20ss07c3z2.jpg)
多次翻页观察，request_url 是不变的，改变的是提交的表单数据page(页数)和rows(条数)。
那么就可以方便的用requests构造请求：
### 详细数据界面
![](https://ws1.sinaimg.cn/large/6af92b9fly1fnsp37pm1ej20w707h0tq.jpg)
仔细分析这两段几乎变态的代码，找详细数据界面请求url生成的规律.(在这里不得不佩服我的leader,找他他看了1分钟就看了出来，我配合着页面js代码看还是一头雾水....)
```sql
select b.ename,b.cnname ,a.c1,b.status ,b.bz,b.pxh,b.endstr 
from [f_getresource_detail]('A75B00E34E77') a join [resource_detail_ex0] b  on a.c0=b.[ename]  where b.status>0 and b.type=1  and  len(isnull(c1,''))>0 order by b.pxh

http://www.nfgrp.cn/pageclass/list0.ashx?_ptype=query0&_psql=%20%20select%20b.ename,b.cnname%20,a.c1,b.status%20,b.bz,b.pxh,b.endstr%20from%20[f_getresource_detail](%27A75B00E34E77%27)%20a%20join%20[resource_detail_ex0]%20b%20%20on%20a.c0=b.[ename]%20%20where%20b.status%3E0%20and%20b.type=1%20%20and%20%20len(isnull(c1,%27%27))%3E0%20order%20by%20b.pxh
```
嗯，识别sql语句中的该变字段，可以发现每次详细数据的渲染只改变了(%27A75B00E34E77%27)这样一个字段，结合前面数据的对比，可知中间嵌套的是种质的平台唯一识别码。
## 爬取策略
分析完数据的js渲染方式后，爬取策略很简单：

爬取翻页界面json数据 --> 解析出所有种质的ID --> 构造详细数据请求url --> 获取所有种质详细数据的json
### 意外情况
原本以为翻页返回的就是json格式数据，用requests.json()方法直接下载，然后提取'JSON_id'字段获取id会很方便。暗自窃喜时，程序报了json解析的异常，因为网页源数据中混入了json不能decode的\uXXX...

我的天，字符串中咋会混入unicode???，好，我尝试用正则替换，好了，这次没有\uXXX ,又出现了\异常...
喔？原文还有\\不成??? ,z再去替换'\\',这下子某些地方又却了',' 我放弃了...

事实再次证明了 正则表达式才是解析届的王道。没办法的我只好用正则匹配原字符串了...requests.json()方法在这里成功作废...
## 源码
```python
import requests
import json
import re
def getID():
    url = 'http://www.nfgrp.cn/pageclass/list0.ashx?_ptype=query1&_sqlkid=A5C9018985E5&_jsondata=&searchcondition=%20&_porder=%20tuxiangshuliang%20desc'
    data ={
        'action':'query',
        'page':'1',
        'rows':'88471',
        'sort':'JSON_tuxiangshuliang',
        'order':'desc'
    }
    r = requests.get(url,data=data)
    text = r.text
    kid = re.findall("\"JSON_kid\":\".*?\"",text)
    kid = kid[::2]
    IDS = []
    for item in kid:
        IDS.append(item.split(':')[1])
    return IDS
def getContent(id):
    url_pre = 'http://www.nfgrp.cn/pageclass/list0.ashx?_ptype=query0&_psql=%20%20select%20b.ename,b.cnname%20,a.c1,b.status%20,b.bz,b.pxh,b.endstr%20from%20[f_getresource_detail](%27'
    url_post = '%27)%20a%20join%20[resource_detail_ex0]%20b%20%20on%20a.c0=b.[ename]%20%20where%20b.status%3E0%20and%20b.type=1%20%20and%20%20len(isnull(c1,%27%27))%3E0%20order%20by%20b.pxh'
    url = url_pre + id + url_post
    r = requests.get(url)
    print('正在爬取'+id+'的数据')
    return r.json()
# print(getID())
IDS = getID()
content_all = [] 
for id in IDS:
    content_all.append(getContent(id))
# print(content_all)
fp = open('zhongzhi_info.json','w')
json.dump(content_all,fp,indent=4)
fp.close()

```