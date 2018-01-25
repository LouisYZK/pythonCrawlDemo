import requests
import json
import re
from multiprocessing import Pool
import queue
url_queue = queue.Queue()
fp = open('./1.24/zhongzhi_info.json','w',encoding='utf-8') 
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
    # kid = kid[::2]
    for item in kid:
        item = item.split(':')[1]
        item = re.sub('\"','',item)
        url_queue.put(item)
    return url_queue
def getContent(id):
    url_pre = 'http://www.nfgrp.cn/pageclass/list0.ashx?_ptype=query0&_psql=%20%20select%20b.ename,b.cnname%20,a.c1,b.status%20,b.bz,b.pxh,b.endstr%20from%20[f_getresource_detail](%27'
    url_post = '%27)%20a%20join%20[resource_detail_ex0]%20b%20%20on%20a.c0=b.[ename]%20%20where%20b.status%3E0%20and%20b.type=1%20%20and%20%20len(isnull(c1,%27%27))%3E0%20order%20by%20b.pxh'
    url = url_pre + id + url_post
    r = requests.get(url)
    res = r.json()
    json.dump(res,fp,indent=4,ensure_ascii=False)
    print('正在写入'+id+r'的数据')
if __name__=='__main__':
    id_queue  = getID()
    p = Pool(4)
    while not id_queue.empty():
        for i in range(5):
            id = id_queue.get()
            p.apply_async(getContent, args=(id,))
    p.close()
    p.join()
    fp.close()