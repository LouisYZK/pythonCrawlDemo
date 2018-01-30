import requests
from bs4 import BeautifulSoup 
cookies = {
    'dt_ssuid':'4320315560',
    'pex':'C864C03270DED3DD8A06887A372DA219231FFAC25A9D64AE09E82AED12E416AC',
    'usid':'Kx0AtkVMTT_bRxE-',	
    'SUID':'03D624773220910A0000000059D8D827',
    'ad':'Gkllllllll2z4$lFlllllVI20zclllllNhFQlZllll9lllllxVxlw@@@@@@@@@@@',
    'ld':'JZllllllll2zUacKlllllVIWc$llllllNhFQjkllll9lllll9ylll5@@@@@@@@@@',
    'ABTEST':'0|1517230645|v1',
    'SNUID':'67B447146367008AABCCCA136318BB6B',
    'weixinIndexVisited':'1',
    'sct':'1',
    'JSESSIONID':'aaagSn62HwiZ_hz426Bew'
}

headers ={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}
url = 'http://weixin.sogou.com/weixin?'

def getHtml(query,page_num):
    param = {
    'query':query,
    '_sug_type_':'',	
    'sut':'2693',
    'lkt':'7,1517230659849,1517230661316',
    's_from':'input',
    '_sug_':'y',
    'type':'2', #标记搜索类型，2代表文章，1代表公众号
    'sst0':'1517230661417',
    'page':page_num,
    'ie':'utf8',
    'w':'01019900',
    'dr':'1'
    }
    s= requests.Session()
    r =s.get(url,params = param,headers = headers,cookies=cookies)
    print('成功爬取'+page_num+' '+str(r.status_code))
    print(r.url)
    return r.text
# for i in range(100):
#     getHtml('python',str(i))
def parseHtml(html):
    soup = BeautifulSoup(html,'lxml')
    lists =[]
    for i in range(10):
        info ={}
        item_id = 'sogou_vr_11002601_box_' + str(i)
        li = soup.find('li',{'id':item_id})
        txt = li.find('div',{'class':'txt-box'})
        title = txt.a.get_text()
        href = txt.a['href']
        summary =  txt.find('p',{'class':'txt-info'}).get_text()
        s_p = txt.find('div',{'class':'s-p'})
        author = s_p.a.get_text()
        date = s_p.find('span',{'class':'s2'}).get_text()
        info['title'] = title
        info['href'] = href
        info['summary'] = summary
        info['author'] = author
        info['date'] = date
        lists.append(info)
    return lists
html = getHtml('python','1')
# print(html)
print(parseHtml(html))

         
    