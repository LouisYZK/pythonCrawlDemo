import requests
from bs4 import BeautifulSoup
# import csv
# 获取IP代理池
cookies ={
    '_free_proxy_session':	'BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTZjZmU4MDJlNmM4YjVhYWNhMGU1MTI4MWJhMWJlZjcyBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMWNwWnRtUEgwSzV3YzJSR2hsd3BQM0JSclFxZDhSemJ2Rnh6aUJKcHdTazQ9BjsARg%3D%3D--c6951bf261459529e8ce266d86fb07eebf5075dd',
    'Hm_lvt_0cf76c77469e965d2957f0553e6ecf59':'1517219363',
    'Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59':'1517237056'
}
headers ={
    'Cache-Control':'max-age=0',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}
# r = requests.get('http://www.xicidaili.com/nn/1',cookies = cookies,headers = headers)
# print(r.text)
fp = open('proxy.txt','a')
# csvfile = csv.writer(fp)
for i in range(1,500):
    url = 'http://www.xicidaili.com/nn/' + str(i)
    r = requests.get(url,cookies = cookies,headers = headers)
    html = r.text
    soup = BeautifulSoup(html,'lxml')
    trs = soup.find_all('tr',{'class':'odd'})
    for item in trs:
        tds = item.find_all('td')
        http = tds[1].get_text()
        port = tds[2].get_text()
        try :
            r = requests.get('http://cug.edu.cn',proxies = {'http':http+':'+port})
            print('************成功添加可用的'+http+':'+port+'************')
            fp.write('\n'+http+':'+port)           
        except Exception:
            print('************'+http+':'+port+'并不能用**********')
        