import requests 

headers = {
    'Host':'172.16.0.2',
    'Cache-Control':'max-age=0',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer':'http://172.16.0.2/Student.aspx',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Cookie':'ASP.NET_SessionId=oqjub045uw2vctq5umbydv45'
}
cookies = {
    'ASP.NET_SessionId':'oqjub045uw2vctq5umbydv45'
}
params = {
    '__EVENTTARGET':(None,'ctl00$Main$Button2'),
    '__EVENTARGUMENT':(None,''),	
    '__VIEWSTATE':(None,'/wEPDwULLTIwMzgwOTM1OTkPZBYCZg9kFgICAw8WAh4HZW5jdHlwZQUTbXVsdGlwYXJ0L2Zvcm0tZGF0YRYEAgEQPCsADQIADxYCHgtfIURhdGFCb3VuZGdkDBQrAAIFAzA6MBQrAAIWDh4EVGV4dAUG5Li76aG1HgVWYWx1ZQUG5Li76aG1HgtOYXZpZ2F0ZVVybAUNL0RlZmF1bHQuYXNweB4HRW5hYmxlZGceClNlbGVjdGFibGVnHghEYXRhUGF0aAUNL2RlZmF1bHQuYXNweB4JRGF0YUJvdW5kZxQrAAUFDzA6MCwwOjEsMDoyLDA6MxQrAAIWDh8CBQbpobnnm64fAwUG6aG555uuHwQFDS9Qcm9qZWN0LmFzcHgfBWcfBmcfBwUNL3Byb2plY3QuYXNweB8IZ2QUKwACFg4fAgUG6IGM5belHwMFBuiBjOW3pR8EBQ4vRW1wbG95ZWUuYXNweB8FZx8GZx8HBQ4vZW1wbG95ZWUuYXNweB8IZ2QUKwACFhAfAgUG5a2m55SfHwMFBuWtpueUnx8EBQ0vU3R1ZGVudC5hc3B4HwVnHwZnHwcFDS9zdHVkZW50LmFzcHgfCGceCFNlbGVjdGVkZ2QUKwACFg4fAgUG5ZCO5YukHwMFBuWQjuWLpB8EBQ8vTG9naXN0aWNzLmFzcHgfBWcfBmcfBwUPL2xvZ2lzdGljcy5hc3B4HwhnZGRkAgUPZBYEAhUPEBYGHg1EYXRhVGV4dEZpZWxkBQRibW1jHg5EYXRhVmFsdWVGaWVsZAUEYm1kbR8BZxAVGRLlt6XnqIvnoZXlo6vpooTnp5EM572R57uc5a2m6ZmiCeWcsOWtpumZogzotYTmupDlrabpmaIM5p2Q5YyW5a2m6ZmiDOWcsOepuuWtpumZogzlt6XnqIvlrabpmaIS57uP5rWO566h55CG5a2m6ZmiDOePoOWuneWtpumZogzkv6Hlt6XlrabpmaIM5pWw55CG5a2m6ZmiD+WkluWbveivreWtpumZogzkvZPogrLor77pg6gM56CU56m255Sf6ZmiDOacuueUteWtpumZog/orqHnrpfmnLrlrabpmaIM546v5aKD5a2m6ZmiEuWFrOWFseeuoeeQhuWtpumZohXoibrmnK/kuI7kvKDlqpLlrabpmaIV6ams5YWL5oCd5Li75LmJ5a2m6ZmiD+adjuWbm+WFieWtpumZog/oh6rliqjljJblrabpmaIM6aKE56eR6YOo6ZeoJOeglOeptueUn+mZou+8iOWQjOetieWtpuWKm+WNmuWjq++8iQzmtbfmtIvlrabpmaIVGQMwMDIDMDA0AzEwMQMxMDIDMTAzAzEwNgMxMDcDMTA4AzEwOQMxMTEDMTEyAzExMwMxMTQDMTE3AzEyMAMxMjEDMTIyAzEyMwMxMjYDMTI3AzEyOAMxMjkDMTMwAzEzMwMxMzgUKwMZZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2RkAhcPEBYGHwoFBHJ4bmQfCwUEcnhuZB8BZxAVCQQyMDE3BDIwMTYEMjAxNQQyMDE0BDIwMTMEMjAxMgQyMDExBDIwMTAEMjAwORUJBDIwMTcEMjAxNgQyMDE1BDIwMTQEMjAxMwQyMDEyBDIwMTEEMjAxMAQyMDA5FCsDCWdnZ2dnZ2dnZ2RkGAIFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYIBQ5jdGwwMCRNYWluJHJiMQUOY3RsMDAkTWFpbiRyYjIFDmN0bDAwJE1haW4kcmIyBQ5jdGwwMCRNYWluJHJiMwUOY3RsMDAkTWFpbiRyYjQFDmN0bDAwJE1haW4kcmI0BQ5jdGwwMCRNYWluJHJiNQUOY3RsMDAkTWFpbiRyYjUFC2N0bDAwJG1lbnVhDw9kBQ3kuLvpobVc5a2m55SfZOhAZLJwJKkeMVBkR9gldf0eSax8'),
    'ctl00$Main$Select4':(None,'1'),
    'ctl00$Main$Text1':(None,''),	
    'ctl00$Main$Text2':(None,''),	
    'ctl00$Main$fp':(None,''),	
    'ctl00$Main$Text4':(None,'20151002353'),
    'ctl00$Main$Password1':(None,'20151002'),
    'ctl00$Main$g1':(None,'rb2'),
    'ctl00$Main$Select2':(None,'002'),
    'ctl00$Main$Select3':(None,'2017'),
    'ctl00$Main$g2':(None,'rb3'),
    '__EVENTVALIDATION':(None,'/wEWEALvrqVqAoLSy68GAuKTouAOAuKTtrsHAq3ZoPMHAuKTvpgDAuaFro4HAoH36fwIApzui8oCAq3ZlPMHAoLS068GAoLS168GArqFlNcEAte8trwJAuzT0IkDAq3ZmPMHQ8eDSPlxd5MQrK12+1et/y297lA=')
}
s = requests.Session()
r =s.post('http://172.16.0.2/Student.aspx',cookies = cookies,headers = headers,files = params)
# rr = s.get('http://172.16.0.2/Result/xs_cjmx.aspx')
print(r.text)