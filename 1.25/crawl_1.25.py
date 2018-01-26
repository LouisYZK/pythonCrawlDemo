import requests
from bs4 import BeautifulSoup
import json
import random
from multiprocessing import Pool
# proxy = [
#     {
#         'http':'http://139.224.133.250:8080'
#     },
#     {
#         'http':'http://139.196.122.166:8080'
#     },
#     {
#         'http':'http://118.193.19.158:808'
#     },
#     {
#         'http':'http://139.224.133.250:8080'
#     }
# ]
def getText(begin_num):
    req_url = 'http://www.cdad-is.org.cn/module/pageCommonXMS/Brw_Tmpl.cbs'	
    cookies ={
        'dict%5Fcookieflag':'1',
        'CGISESSIONID':'SKGFAIAGUNHVWQZZ'
    }
    headers = {
        'Host':'www.cdad-is.org.cn',
        'Content-Length':'153',
        'Cache-Control':'max-age=0',
        'Origin':'http://www.cdad-is.org.cn',
        'Upgrade-Insecure-Requests':'1',
        'Content-Type':'application/x-www-form-urlencoded',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer':'http://www.cdad-is.org.cn/module/pageCommonXMS/Brw_Tmpl.cbs',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Cookie':'CGISESSIONID=SKGFAIAGUNHVWQZZ; dict%5Fcookieflag=1'
    }
    data = {
        'ResultFile':'c%3A%5Ctemp%5Ctbs%5CA2515F0%2Etmp',
        'ResName':'animalmeta',
        'DisNum':'15',
        'begin':str(begin_num),
        'condition':'',	
        'fldname':'',	
        'fldvalue':'',	
        'SortFld':'',	
        'sortorder':'',
        # 'x':'16',
        # 'y':'9'
    }
    # pr = proxy[random.randint(0,3)]
    s = requests.Session()
    r = s.post(req_url, headers =headers, data=data,cookies = cookies)
    r.encoding =None #解决编码混乱问题，禁止request自己判断，直接设置为无
    text = r.text
    return text

def getID(text):
    soup = BeautifulSoup(text,'lxml')
    trs = soup.find_all('tr',{'class':'bgcolor-gailan'})
    id = []
    for tr in trs:
        td_text = tr.find_all('td')[1].getText().strip()
        id.append(td_text)
    return id
def dowmHtml(id):
    url = 'http://www.spanimal.cn/date_list1.asp?ptzyh='+id
    html = requests.get(url)
    html.encoding =None
    file_name ='html/info_'+id+'.html'
    fp = open(file_name,'w',encoding='utf-8')
    fp.write(html.text)
    fp.close()
    print(id+'文件已经下载完毕！')
def id2json(): 
    ID_all = []
    for i in range(262):
        begin_num = 3930 - i*15
        print(begin_num)
        text = getText(begin_num)
        ID = getID(text)
        print(ID)
        ID_all.append(ID)
        fp = open('id.json','w')
        json.dump(ID_all,fp)
        fp.close()
if __name__=='__main__':
    fp = open('id.json','r')
    id_list = json.load(fp)
    fp.close
    p = Pool(4)
    for item in id_list:
        for item2 in item:
            p.apply_async(dowmHtml, args=(item2,))
    p.close()
    p.join()
                