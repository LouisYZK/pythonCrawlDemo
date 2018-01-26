# 爬取国家家养动物资源平台核心元数据
昨天的悲伤，今天的延续
![](https://ws1.sinaimg.cn/large/6af92b9fly1fnu23l66rlj20c209m752.jpg)
>昨天的的数据真是要了老命，不过也增加了对大量数据采集的项目经验吧。这时感觉python的能力还是有限的，虽然代码不多，使用简介，但是在加速上还是局限的很。

>没办法，多线程、进程什么的都试过了。就差跟公司申请使用分布式了。我的小破四核做不来。。。但是leader说数据量不够用分布式......好吧，从上午十点开始跑，下班能完不？？？

今天的网站是[国家家养动物资源平台核心元数据](http://www.cdad-is.org.cn/page/framelimit.cbs?ResName=animalmeta)
![](https://ws1.sinaimg.cn/large/6af92b9fly1fnu3puzsr7j20s305ztc4.jpg)
从头部可以看出，网页自动登录了，这样cookie的设置是少不了了。没什么好说的，按照抓包结果分析构造就ok.
## 爬取策略：
我们的目标页面是的url构成是：http://www.spanimal.cn/date_list1.asp?ptzyh=1322C0001000003210 因为他的数据最详细，里面使用表格填写的，结构化也不错。最重要的是他没有用ajax渲染。 通过分析这个url，也很简单，前缀固定，后面加上每个品种的平台统一识别码。

爬取策略：
- 分析统一识别码ajax请求的参数构造
- 伪造ajax请求获取3930个物种的识别码
- 构造目标url直接下载出html文档
识别码的页面如下：
![](https://ws1.sinaimg.cn/large/6af92b9fly1fnufwwwzlsj20fi09cq38.jpg)
这是一个ajax翻页处理的网站，前天已经处理过类似的网站。但是这次是直接请求的后端一个cbs的东西，并没有访问权限（也就是我从前端看不到里面的东西），只能填参数请求出来数据。
```python
data = {
        'ResultFile':'c%3A%5Ctemp%5Ctbs%5CA2515F0%2Etmp',
        'ResName':'animalmeta',
        'DisNum':'15',# 这里我真的很想一下子设置成总条数，但是这个参数好像是无用的，怎么设置返回的都是十五条....
        'begin':str(begin_num),# 整个表单就这个参数有用了，而且是倒着数，真是奇葩...
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
    # 因为此网站每个页面都要登录，所以采用session开启一个会话
    r = s.post(req_url, headers =headers, data=data,cookies = cookies)
    r.encoding =None #解决编码混乱问题，禁止request自己判断，直接设置为无
    text = r.text
    return text
```
然后很简单地用我最熟悉的beautifulsoup解析出id.再下载出html这些都很简单。
## 增强爬虫的稳定性(robust)
虽然这次数据量没有昨天大，但是我还是开启了多进程。因为在跑的过程中我发现这个网站屡屡在中间就停止响应了（500错误），起初我以为是ip封锁了，然后换代理IP，不起作用，还是会爬取一段时间就挂掉...网上查原因，还有人说没有IP封锁就是单纯的他们服务器撑不住这一下子这么多的并发请求...（怪我用多进程了???）

真让人头大，多次调试我发现只有第一个请求ID的那个会崩溃，那么为了增加稳定性，我就设置了边读取边保存爬取到的变量，这样即使程序跑到一半挂掉了，前面得到的还可以接着用。这就是id.json的目的。


