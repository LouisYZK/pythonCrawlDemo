import re
import csv
import requests
import pymongo
# 销地
url_xiaodi = 'http://jgsb.agri.cn/controller?ifnew=false&type=2&province=&SERVICE_ID=REGISTRY_MARKET_MAP_SEARCH_SERVICE&login_result_sign=nologin' 
# 产地
url_chandi = 'http://jgsb.agri.cn/controller?ifnew=false&type=1&province=&SERVICE_ID=REGISTRY_MARKET_MAP_SEARCH_SERVICE&login_result_sign=nologin'
# 应急散地
url_yingji = 'http://jgsb.agri.cn/controller?ifnew=false&type=0&province=&SERVICE_ID=REGISTRY_MARKET_MAP_SEARCH_SERVICE&login_result_sign=nologin'  
def getHtml(url):
    r = requests.get(url)
    return r.text
def parseHtml(html):
    pattern1 = 'coordinate=\'.*\'' 
    pattern2 = 'marketName=\'.*?\''
    pattern3 = 'marketCnName=\'.*?\''
    pattern4 = 'count=\'.*?\''
    pattern5 = 'marketWeb=\'.*?\''
    coordinate = list(map(lambda s : s.split('=')[1],re.findall(pattern1,html)))
    marketName = list(map(lambda s : s.split('=')[1],re.findall(pattern2,html)))
    marketCnName  = list(map(lambda s : s.split('=')[1],re.findall(pattern3,html)))
    count = list(map(lambda s : s.split('=')[1],re.findall(pattern4,html)))
    marketWeb = list(map(lambda s : s.split('=')[1],re.findall(pattern5,html)))
    res = []
    for i in range(len(coordinate)):
        dic = {
            '地理坐标':coordinate[i],
            '市场名称':marketName[i],
            '市场全名':marketCnName[i],
            '数量':count[i],
            '网站':marketWeb[i]
        }
        res.append(dic)
    return res 
def store(res):
#     csvfile = csv.writer(fp)
#     for item in res:
#         csvfile.writerow(item)
# fp1 = open('yingJiSanDi.csv','w')
# store(parseHtml(getHtml(url_yingji)),fp1)
# fp1.close()
# fp2 = open('chanDi.csv','w')
# store(parseHtml(getHtml(url_chandi)),fp2)
# fp2.close()
# fp3 = open('xiaoDi.csv','w')
# store(parseHtml(getHtml(url_xiaodi)),fp3)
# fp3.close()
    client = pymongo.MongoClient(host = 'localhost',port =27017)
    db = client.python_map
    collection = db.map_info1
    for item in res:
        collection.insert(item)
    client.close()
res = parseHtml(getHtml(url_xiaodi))
print(res)
store(res)


    
