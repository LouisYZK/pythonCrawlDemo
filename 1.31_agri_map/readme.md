# 爬取渲染地图数据
> 时间过得很快，这是实习的倒数第三天了，按照自己的安排，这是最后一周，下一周准备一下建模比赛，然后就到农历春节了。 这四周的实习很不舍，很艰辛，也学到了很多。第一次出来上班，感受到了外面的世界对技术的要求，绝不是自己在学校里面随便玩玩就能达到要求的。最后一周扫尾工作，我所写的js代码因为公司隐私的问题不能上传，只能上传py的代码。
> 爬虫也是一样，出来后才知道要想精通这门技术是不可能的，他涉及很多领域，在实习中也深感我的计算机网络知识不扎实，js功底不牢固（*以前感觉不做前端干嘛要把js掌握的很好，出来后师父告诉我js是每个IT人必备的知识*）,还有数据库知识的匮乏（*数据库的东西，学校里学的那一套根本用不上，换句话说，太老套了*）。总之要学习的东西还有很多，要追赶的人也有很多，感谢在武汉最寒冷的冬天，自己创造的这一段经历。

今天爬取的是地图数据，地图前端js框架有很多，百度API、googleMAP、highmap等等，爬取的关键是分析到地图“点数据”的生成模式。 今天的网站[农业市场空间分布情况](http://jgsb.agri.cn/controller?ifnew=false&type=2&province=&SERVICE_ID=REGISTRY_MARKET_MAP_SEARCH_SERVICE&login_result_sign=nologin)是用一个没听说过的js框架搞的，本以为不好办，但是经分析很简单。

![](https://ws1.sinaimg.cn/large/6af92b9fly1fnzs2xy7d8j20iw0e5q7r.jpg)

## 请求
请求参数就在地址中，两个关键字段，type表示市场类型，province表示查询的省份。经过测试这个网站爬取门槛很低，不需要做任何修饰，直接请求即可。
## 解析分析
抓包查找需要的关键数据:
```javascript
var coordinate='116.044933,29.747925';
var arr=coordinate.split(",");
var x=arr[0];
var y=arr[1];
var marketName='赣九江琵琶湖';
var marketWeb='http://';
var pfscCount='6';
var marker = new TMarker(new TLngLat(x,y)); 
marker.name=marketName;
marker.cnName=marketCnName;
marker.count=count;
marker.marketWeb=marketWeb;
marker.setTitle(marker.name);
TEvent.addListener(marker,"click",onClick); 
map.addOverLay(marker); 
```
直接写在js中的字段，很简单，正则的写法也不难，倒是我图省事儿写了一行简便但稍微复杂一些的代码惹来了吐槽：
```python
coordinate = list(map(lambda s : s.split('=')[1],re.findall(pattern1,html)))
```
我耐心地解释，仅仅是解析的处理我把几行简写为一行，避免了for循环，至少我没犯功能耦合的错误嘛。。。
## 存储
这次存储我尝试用mongodb，算是一种开始补习数据库的信号了吧。

python对数据库的支持都很不错，我在多次课设中使用到了pymysql。可以直接写sql语句控制。如果对sql掌握的不好，也可以用ORM的sqlalchemy. python对mongodb的支持包pymongo保留了mongodb原生语句的风格，学习门槛很低。

###启动mongodb(win)
```shell
mongod --dbpath D:\mongodb\db
```
###pymongo
将数据封装成字典，调用pymongo实现插入：
```python
dic = {
            '地理坐标':coordinate[i],
            '市场名称':marketName[i],
            '市场全名':marketCnName[i],
            '数量':count[i],
            '网站':marketWeb[i]
        }
# 链接数据库
client = pymongo.MongoClient(host = 'localhost',port =27017)
# 选择数据库
db = client.python_map
# 选择集合
collection = db.map_info1
for item in res:
    collection.insert(item) #插入文档
    client.close()
```
###查看检验
![](https://ws1.sinaimg.cn/large/6af92b9fly1fnzu19ibdyj20pi09fgn6.jpg)
mongodb的可视化版本也很多，随便挑选一款使用即可。