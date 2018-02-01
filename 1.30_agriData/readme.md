# 再次爬取基于Flex技术的某农产品每日价格历史数据
> 这个是实习期间耽搁时间最长的项目了，通过这个对pyamf这个包算是很熟悉了。不得不说他的请求伪造真的好复杂。。。

顺便吐槽一下，**像flash这种当今在网页上见得很少了，但是众多政府网站依然使用，接受html5就那么难吗？？？还是说懒得换架构和模式？？**

网上对pyamf包的使用案例几乎没有，只能从国外找，1.23那天项目已经实践过一次，但是奈何这次的头比较复杂很多东西我并不知道如何伪造，不过花了两个下午，总算顺利解决了。
## 网络分析
### 前端分析
先看看这个flash张啥样吧：
![](https://ws1.sinaimg.cn/large/6af92b9fly1fo117nwef9j20mz0cndhg.jpg)

数据项我已经用红框给圈了出来，基本的请求模式就是，先选择市场名，然后会发送一个请求，返回所有的品种大类和品种小类，选择品种小类和时间段，点击查询，发送给后端返回平均价格。 剩下的图表由前端负责渲染。

可以看出一共请求了后端两次，但是我们的需求仅仅是**输入市场、品种名称和截止日期，输出该时间段内每天的价格**
所以并不需要模拟第一次请求。
### 请求分析
chales抓包如图（目前只有chales能使amf数据明文显示，fiddler还做不到）
![](https://ws1.sinaimg.cn/large/6af92b9fly1fo11g3pzmyj20ev0aemy8.jpg)

可以看到请求的东西包含了选择的品种小类和市场名称，最后一个BreedINfo是第一次请求返回的所有品类信息，后来经过测试这部分在第二次请求并不需要，所以我就全填了None。 

从请求的架构上看这与我的预想是一致的
### 响应分析
![](https://ws1.sinaimg.cn/large/6af92b9fly1fo11ipscknj20ef02wglr.jpg)

相应的body也很简洁明了，顺便返回了时间区间，解析的方法按照pyamf的层级选择语法写就行

## 构造请求(pyamf用法记录)
> 这是此次项目的最难的地方，也是考验耐心的地方。也算是pyamf的核心吧。
### message体
首先，我们看到包含了body的整个请求体在pyamf是用 messaging 类来创建的，基本的流程为:
```python
# 创建messsaging对象，填入基本字段，可以从抓包中看出
msg = messaging.RemotingMessage(messageId=str(uuid.uuid1()).upper(),clientId=str(uuid.uuid1()).upper(),operation='getDyscDpzData',destination='reportStatService',timeToLive=0,timestamp=0)
# 注册body，填入body所需字段
msg.body = [DyscdpzPara(startDate,endDate,select,market,breedInfoPo)]
# 构造header
msg.headers['DSEndpoint'] = None  
msg.headers['DSId'] = str(uuid.uuid1()).upper()
req = remoting.Request('null',body = (msg,))
```
### body
body的字段类型有几种: 字符串,日期对象等，在包中都很明显地标出了:
![](https://ws1.sinaimg.cn/large/6af92b9fly1fo11qftihqj20gu0aldh4.jpg)

红框为基本对象类型，蓝色框对应的具体的类名称，我们可以看到，body整个是一个array,里面只有一个元素。这个元素是一个大类。所以他的构造方式很简单：
```python
msg.body = [Para()] 
# Para是实例化的对象
```
而 startDate和endDate是两个Date类型，对应的是python中的datetime.datetime对象。（这并非是主观臆测，而是通过1.23项目中返回的日期字段是这个对象而得出的结论）

除了object类型之外的其他类型都可以直接创建变量表示。body里只有一个Dypzdqpara()类，首先就需要创建这个类：
```python
class DyscdpzPara():
    def __init__(self,StartDate,EndDate,SelectedBreeds,PMarketInfo,breedInfo):
        self.startDate = StartDate#2008-1-1 0:00:00 date类型
        self.endDate = EndDate #2008-1-2 0:00:00 date类型
        self.selectedBreeds	=SelectedBreeds #对象
        self.theDateType = '1'
        self.theSorting = '0'
        self.marketInfo	= PMarketInfo #对象
        self.theCycle = '7'
        self.breedInfo = breedInfo # 对象
```
初始化方法传入了必要的参数，可以看到除了传入普通变量类型之外还有三个对象：分别是：
- Selected，ArrayCollection对象，里面含一个BreedInfo对象...
- MarkeInfo, PMarketInfo对象，里面两个普通字段
- BreedInfoPo 对象，本需要填入第一次请求返回的所有breedInfo,但后经过测试此对象里面的属性可以全部设置为None（**但不能不填！！！，不实例化对象的话请求不出来，amf要求属性值可以没有，但是必要传入属性！**）

后俩的构建都没问题，复杂的是第一个：
![](https://ws1.sinaimg.cn/large/6af92b9fly1fo122qc63fj20ei03dq34.jpg)

尼玛啊，我当时就懵逼了，尝试了好多写法，比如
selectedBreed = [breed()] ，那么selectedBreed就不是对象，是一个Array了。。。
如果不把SelectedBreed 创建为对象，然后用
```python
pyamf.register_class(SelectedBreeds, alias='flex.messaging.io.ArrayCollection')
```
注册成为类，那么类里面怎么写？？？
我甚至尝试了self = [breed] ...

> 这个问题让我想到了数组与类的关系问题，在java语言中数组本身就是个类，数组也是类的实例化对象，对象数组本身当然是对象了。 可是到python中,[对象1，对象2，...]这是对象吗？？ 网上有人说是，我也坚信OOP语言应该是一切为对象的，但是在今天这个问题上依然不好使...

那么list()究竟是不是类，需要追溯源文档探索了...

无奈之下，只好求教我师父了，唉，厉害的人果然十分钟给我解决了问题:
github上在这个项目底下搜索ArrayCollection，看看与他相关的东西是怎么用的。
![](https://ws1.sinaimg.cn/large/6af92b9fly1fo12ay24l2j20cg07emxa.jpg)

我都要哭了，原来自己定义的有专门的类... 传入对象即可...（再次证明了这个东西有多么冷门...）
```python
breedInfoPo = BreedInfoPo(None,None,None,None)
    select_breed = BreedInfoPo(item_code,item_name,None,None)
    select = ArrayCollection([select_breed])
    market = PMarketInfo(market_code,market_name)
    msg = messaging.RemotingMessage(messageId=str(uuid.uuid1()).upper(),clientId=str(uuid.uuid1()).upper(),operation='getDyscDpzData',destination='reportStatService',timeToLive=0,timestamp=0)
    msg.body = [DyscdpzPara(startDate,endDate,select,market,breedInfoPo)]
    msg.headers['DSEndpoint'] = None  
    msg.headers['DSId'] = str(uuid.uuid1()).upper()
    req = remoting.Request('null',body = (msg,))
    env = remoting.Envelope(amfVersion=pyamf.AMF3)
    env.bodies = [('/1',req)]
    data = bytes(remoting.encode(env).read())
```
改写、注册，事情就算完了，至于日期上的错误，一个UTC时间上的转换也很容易。
![运行效果](https://ws1.sinaimg.cn/large/6af92b9fly1fo11e7q4mtj20q50ajn0o.jpg)

## 总结
虽说这个东西冷门，但是也收获了不少解决问题的办法，查看包的原文档是一种不错的途径，尤其是解决一些冷门问题。


