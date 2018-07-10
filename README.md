# spider_Tourism
基于scrapy的分布式爬虫，爬取途牛旅游攻略

# day01

## 1.页面分析

[点击登录途牛旅游网](http://v.tuniu.com/)

途牛的网站模块比较多，在这个项目中我只爬取菜单栏中攻略中的东西。

![分析_网页1](img\fenxi_wangye1.PNG)

上图中的攻略，将在这个项目中爬取游记、视频两个板块, 点击进入游记。第一步我们需要分析的是游记板块的数据是怎样加载的。

经过页面分析，发现游记板块，除了第一次进去，源码中已经在script中将第一页的数据默认处理了，在点击第二页后，出现了ajax异步请求，顺利get到第二页的接口

	http://trips.tuniu.com/travels/index/ajax-list?sortType=1&page=1&limit=10&_=1530860823504

很明显中间的page代表的就是哪一页的数据了，在XHR中查看接口内容是最清晰最简便的方式，通过接口返回的数据，我们需要去了解，哪些数据是我们需要的。

![接口分析](img\jiekoufenxi.PNG)

游记这个板块的接口比较清晰，我们需要的数据是authorHeadImg（封面图片）, authorId(发布者的id)，authorName(发布者的名字), id(应该是游记的id), name(游记的名字), picUrl(发布者头像), summary(文章部分内容), 找到这，我们会发现，在接口中并没有直接展示进入文章内容的链接，通过审查元素发现，是通过文章的id加，游记的链接组合出现的页面，比如：[点击进入页面](http://www.tuniu.com/trips/12606533)

## 2.项目建立到环境配置
主要依赖库为scrapy， scrapy_redis, redis, pymongo。

	pip install scrapy

注意：在安装scrapy的时候，很有可能会有连带安装的包安装失败导致scrapy安装失败，这个时候解决的方法是，直接去官网符合自己python版本的源文件下载后进行安装，再重装scrapy即可

其中scrapy_redis就是要实现分布式最重要的库，这里面实现分布式的基本原理，不难理解，主程序负责爬取所有链接并存入redis当中，从程序，读取redis中存储的url，进行爬取并通过mongodb实现数据持久化。

# day02
在头一天进行了页面分析之后并创建了项目，不过在实际操作中，发现可以通过，直接修改接口limit的方式，获取所有的url，所以我进行的第一次爬取，是直接爬取数据的总数，然后将limit限制条件修改为这个总数结果不理想，可能途牛在设置这个接口的时候，限制了limit的最大个数，所有我上面的方法获得的data数据只是个空列表

之后就是老老实实的写上了主从程序， 主程序只负责把所有数据的id爬取到并转化成url并存储到redis当中， 从程序可以像下图中，同时开多个程序

![多个从程序同时进行](img\congjispider.png)

从程序中的配置：

	# scrapy-redis
	REDIS_URL = 'redis://:yzd@127.0.0.1:6379'  # for master
	# REDIS_URL = 'redis://:yzd@10.140.0.2:6379'  # for slave (master's ip)
	
	# SCHEDULER 是任务分发与调度，把所有的爬虫开始的请求都放在redis里面，所有爬虫都去redis里面读取请求。
	SCHEDULER = "scrapy_redis.scheduler.Scheduler"
	
	# 如果这一项设为True，那么在Redis中的URL队列不会被清理掉，但是在分布式爬虫共享URL时，要防止重复爬取。如果设为False，那么每一次读取URL后都会将其删掉，但弊端是爬虫暂停后重新启动，他会重新开始爬取。 
	SCHEDULER_PERSIST = True
	
	# REDIS_START_URLS_AS_SET指的是使用redis里面的set类型（简单完成去重），如果你没有设置，默认会选用list。
	REDIS_START_URLS_AS_SET = True
	
	# DUPEFILTER_CLASS 是去重队列，负责所有请求的去重
	DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
	
	# 爬虫的请求调度算法，有三种可供选择
	# scrapy_redis.queue.SpiderQueue：队列。先入先出队列，先放入Redis的请求优先爬取；
	# scrapy_redis.queue.SpiderStack：栈。后放入Redis的请求会优先爬取；
	# scrapy_redis.queue.SpiderPriorityQueue：优先级队列。根据优先级算法计算哪个先爬哪个后爬
	SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
	
	# 设置链接redis的配置，或者如下分别设置端口和IP地址
	REDIS_URL = 'redis://127.0.0.1:6379'
	
	# 分布式爬虫设置Ip端口
	REDIS_HOST = '127.0.0.1'
	REDIS_PORT = 6379

