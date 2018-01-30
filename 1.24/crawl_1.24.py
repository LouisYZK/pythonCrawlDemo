import requests
import json
import re
from multiprocessing import Pool
import queue
url_queue = queue.Queue()
fp_queue = []   
# fp = open('./zhongzhi_info.json','w',encoding='utf-8')
for i in range(9):
    name = './zhongzhi_info_'+str(i)+'.json'
    fp_queue.append(open(name,'w',encoding='utf-8')) 
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
    for item in kid:
        item = item.split(':')[1]
        item = re.sub('\"','',item)
        url_queue.put(item)
    return url_queue
def getContent(id,file_tag,count):
    url_pre = 'http://www.nfgrp.cn/pageclass/list0.ashx?_ptype=query0&_psql=%20%20select%20b.ename,b.cnname%20,a.c1,b.status%20,b.bz,b.pxh,b.endstr%20from%20[f_getresource_detail](%27'
    url_post = '%27)%20a%20join%20[resource_detail_ex0]%20b%20%20on%20a.c0=b.[ename]%20%20where%20b.status%3E0%20and%20b.type=1%20%20and%20%20len(isnull(c1,%27%27))%3E0%20order%20by%20b.pxh'
    url = url_pre + id + url_post
    r = requests.get(url)
    res = r.json()
    fp = fp_queue[file_tag]
    # print(res)
    json.dump(res,fp,indent=4,ensure_ascii=False)
    print('正在写入'+id+'的数据.......当前是第：'+str(count)+'条')
if __name__=='__main__':
    count = 0
    id_queue  = getID()
    p = Pool(4)
    while not id_queue.empty():
        for i in range(10):
            id = id_queue.get()
            file_tag = count//10000
            p.apply_async(getContent, args=(id,file_tag,count,))
            count = count+1
    for item in fp_queue:
        item.close()
    p.close()
    p.join()


