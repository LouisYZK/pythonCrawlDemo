import requests
import json
xy_dic={
    '地球科学学院':'01',
    '资源学院':'02',
    '材料与化学学院':'03',
    '环境学院':'04',
    '工程学院':'05',
    '地空学院':'06',
    '机械与电子信息学院':'07',
    '经济管理学院':'08',
    '外国语学院':'09',
    '信息工程学院':'11',
    '数学与物理学院':'12',
    '体育课部':'13',
    '珠宝学院':'14',
    '远程与继续教育学院':'15',
    '艺术与传媒学院':'16',
    '公共管理学院':'17',
    '李四光学院':'18',
    '计算机学院':'19',
    '马克思主义学院':'20',
    '自动化学院':'23',
    '海洋学院':'24'
}
url = 'http://jwgl.cug.edu.cn/jwglxt/xsxk/zzxkyzb_cxZzxkYzbPartDisplay.html?gnmkdm=N253512&su=20151002353'

headers = {
    'Host':'jwgl.cug.edu.cn',
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'Origin':'http://jwgl.cug.edu.cn',
    'X-Requested-With':'XMLHttpRequest',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8',
    'Cookie':'JSESSIONID=DE709E6EDCD7EDFF76F86784ABF6039B; _ga=GA1.3.337120488.1508641043;uaid=13dc9f19baba08d24e95d4819ca33d40; _gid=GA1.3.1068811446.1517031692'
}
cookie ={
    'JSESSIONID':'DE709E6EDCD7EDFF76F86784ABF6039B',
    '_ga':'GA1.3.337120488.1508641043',
    'uaid':'13dc9f19baba08d24e95d4819ca33d40',
    '_gid':'GA1.3.1068811446.1517031692'
}
s = requests.Session()
def getID(xy,nj):
    data = {
        'njdm_id_list[0]':nj,
        'jg_id_list[0]':xy, 
        'yl_list[0]':'1',
        'rwlx':'1',
        'bklx_id':'0',
        # 'xh_id':'20151002353',
        'xqh_id':'1',
        'jg_id':'08',
        'zyh_id':'0860',
        'zyfx_id':'wfx',
        'njdm_id':'2015',
        'bh_id':'086151',
        'xbm':'1',
        'xslbdm':'421',
        'ccdm':'3',
        'xsbj':'4294967296',
        'sfkknj':'1',
        'sfkkzy':'1',
        'sfznkx':'0',
        'zdkxms':'0',
        'sfkxq':'0',
        'kkbk':'0',
        'kkbkdj':'0',
        'sfkgbcx':'0',
        'sfrxtgkcxd':'0',
        'tykczgxdcs':'0',
        'xkxnm':'2017',
        'xkxqm':'12',
        'kklxdm':'01',
        'njdmzyh':'',	
        'kspage':'1',#开始数量
        'jspage':'100'#结束数量
    }
    r = s.post(url,headers=headers,cookies =cookie,data = data)
    r.encoding =None
    kc_json = r.json()['tmpList']
    kc_info=[]
    for item in kc_json:
        kch_id = item['kch_id']
        kcmc = item['kcmc']
        kc_info.append({'kch_id':kch_id,'kcmc':kcmc})
    return kc_info

def addTeacherInfo(dic):
    teacher_url = 'http://jwgl.cug.edu.cn/jwglxt/xsxk/zzxkyzb_cxJxbWithKchZzxkYzb.html?gnmkdm=N253512&su=20151002353'
    teacher_data ={
        'njdm_id_list[0]':'2015',
        'jg_id_list[0]':'08',
        'yl_list[0]':'1',
        'rwlx':'1',
        'bklx_id':'0',
        'xh_id':'20151002353',
        'xqh_id':'1',
        'jg_id':'08',
        'zyh_id':'0860',
        'zyfx_id':'wfx',
        'njdm_id':'2015',
        'bh_id':'086151',
        'xbm':'1',
        'xslbdm':'421',
        'ccdm':'3',
        'xsbj':'4294967296',
        'sfkknj':'1',
        'sfkkzy':'1',
        'sfznkx':'0',
        'zdkxms':'0',
        'sfkxq':'0',
        'kkbk':'0',
        'kkbkdj':'0',
        'xkxnm':'2017',
        'xkxqm'	:'12',
        'kklxdm':'01',
        'kch_id':dic['kch_id'],
        'njdmzyh':''	
    }
    r = s.post(teacher_url,headers =headers,cookies =cookie,data=teacher_data)
    r.encoding =None
    teacher_json = r.json()
    dic_new ={}
    dic_new['course_name'] = dic['kcmc']
    for item in teacher_json: #有的课程教师可能有两个
        dic_new['teacher_info'] = item['jsxx'] #教师信息
        dic_new['loc'] = item['jxdd'] #教学地点
        dic_new['time'] = item['sksj'] #上课时间
    return dic_new

id_dict = getID(xy_dic['经济管理学院'],'2015')
fp = open('./1.27/course_info_demo.json','w')
for item in id_dict:
    info = addTeacherInfo(item)
    json.dump(info,fp,indent=4,ensure_ascii=False)
fp.close()
# print(addTeacherInfo(id_dict[1]))

    