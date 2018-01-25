import requests
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
    'DisNum':'3930',
    'begin':'3930',
    'condition':'',	
    'fldname':'',	
    'fldvalue':'',	
    'SortFld':'',	
    'sortorder':'',	
    'x':'16',
    'y':'9'
}
s = requests.Session()
r = s.post(req_url, headers =headers, data=data,cookies = cookies)
r.encoding =None #解决编码混乱问题，禁止request自己判断，直接设置为无
text = r.text
print(text)
# fp = open('test.txt','w')
# fp.write(text)
# fp.close()