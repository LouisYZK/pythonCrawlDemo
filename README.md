# 实习日志
> 这个库是18年寒假在武汉做数据挖掘实习生岗位上的工作日志。我的主要工作有：
- 对接数据部的建模数据需求和格式，编写爬虫程序爬取需求格式数据。主要用到的关键技术有：
    - python3 + requests/urllib + BeautifulSoup/正则表达式 
    - Chales  抓包分析 
    - Python其他相关请求编码处理库
    - 编辑器： VS code (方便提交我的服务器和github)
    - 公司版本控制与代码提交: SVN
- 前端数据可视化项目。根据一定需求编写数据可视化js，用到的js框架有：Echarts\百度地图API\lealef等

## [1.23 基于flex技术页面的爬取](https://github.com/LouisYZK/ShiXi_inWuhan/tree/master/1.23)
中国农业信息网发布每一天的价格行情，但政府网站较为古老，采用Flash呈现数据。
网址:http://jgsb.agri.cn/controller?SERVICE_ID=REGISTRY_JCSJ_MRHQ_SHOW_SERVICE&recordperpage=15&newsearch=true&login_result_sign=nologin
与正常的Ajax网站分析一样，只是请求码和返回码运用了awf技术编码，无法分析。此时用chales抓包可以分析出正常明文。据此可以写出伪造的请求头和接收数据格式，具体采用python的第三方pyawf库
pyawf库原生的并不支持3.x，需要安装Py3Awf. 此外导入时会报错，需要修改一下__init__.py文件

代码见crawl_1.23.py

## [1.24爬取国家林木种质资源品台数据](https://github.com/LouisYZK/ShiXi_inWuhan/tree/master/1.24)
今天的主要工作是爬取林木种质资源数据，网页数据是ajax加载，分析步骤并不难。

但是出现了json格式解析失败等意外状况。解决方案是舍弃requets的json()方法，直接用正则表达式解析原文档。

因为今天的数据较多有8W，所以开了python的多进程，感觉跟坐了火箭一样...

## [1.25爬取国家家养动物资源平台核心元数据]()
插曲：今天拖了一下昨天的进度，因为数据部的同事告诉我数据量质量不行，大概是不太会处理json文件吧，我看了一下数据部的同志们大多用的是Matlab,spss,stata等还有一堆我没听过名字的数据分析软件。这样的话非结构化的数据确实让他们有点为难。 

不过这不是我的锅... 经过交涉，他们愿意自学非结构处理方法...

今天的网页还算简单，ajax的post请求，用charles抓包之后构造详图的包就行。

## [1.26]()
今天武汉下起了大雪，又是周五，所以一同实习的小伙伴一整天都很躁动呀~！
