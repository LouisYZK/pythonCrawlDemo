import requests
req_url = 'http://www.cdad-is.org.cn/module/pageCommonXMS/Brw_Tmpl.cbs'
cookies ={
    'dict%5Fcookieflag=1':'CGISESSIONID=ARUOICXMTHWJUZQX'
}
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}
data = {
    'ResultFile':'c%3A%5Ctemp%5Ctbs%5CA2515F0%2Etmp',
    'ResName':'animalmeta',
    'DisNum':'15',
    'begin':'3915',
    'x':'23',
    'y':'10'
}
s = requests.Session()
r = s.get(req_url, headers =headers, data=data,cookies = cookies)
text = r.text
fp = open('test.txt','w')
fp.write(text)
fp.close()