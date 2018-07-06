# spider_Tourism
基于scrapy的分布式爬虫，爬取途牛旅游攻略

# 1.页面分析

[点击登录途牛旅游网](http://v.tuniu.com/)

途牛的网站模块比较多，在这个项目中我只爬取菜单栏中攻略中的东西。

![分析_网页1](img\fenxi_wangye1.PNG)

上图中的攻略，将在这个项目中爬取游记、视频两个板块, 点击进入游记。第一步我们需要分析的是游记板块的数据是怎样加载的。

经过页面分析，发现游记板块，除了第一次进去，源码中已经在script中将第一页的数据默认处理了，在点击第二页后，出现了ajax异步请求，顺利get到第二页的接口

	http://trips.tuniu.com/travels/index/ajax-list?sortType=1&page=1&limit=10&_=1530860823504

很明显中间的page代表的就是哪一页的数据了，在XHR中查看接口内容是最清晰最简便的方式，通过接口返回的数据，我们需要去了解，哪些数据是我们需要的。

![接口分析](img\jiekoufenxi.PNG)

游记这个板块的接口比较清晰，我们需要的数据是authorHeadImg（封面图片）, authorId(发布者的id)，authorName(发布者的名字), id(应该是游记的id), name(游记的名字), picUrl(发布者头像), summary(文章部分内容), 找到这，我们会发现，在接口中并没有直接展示进入文章内容的链接，通过审查元素发现，是通过文章的id加，游记的链接组合出现的页面，比如：[点击进入页面](http://www.tuniu.com/trips/12606533)

# 2.项目建立到环境配置
主要依赖库为scrapy， scrapy_redis, redis, pymongo。

	pip install scrapy

注意：在安装scrapy的时候，很有可能会有连带安装的包安装失败导致scrapy安装失败，这个时候解决的方法是，直接去官网符合自己python版本的源文件下载后进行安装，再重装scrapy即可

其中scrapy_redis就是要实现分布式最重要的库，这里面实现分布式的基本原理，不难理解，主程序负责爬取所有链接并存入redis当中，从程序，读取redis中存储的url，进行爬取并通过mongodb实现数据持久化。

