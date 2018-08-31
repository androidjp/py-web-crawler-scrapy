## 调试时
* 注释掉`settings.py` 最后的5行<br>
  答：这几行注释的作用是，Scrapy会缓存你有的Requests!当你再次请求时，如果存在缓存文档则返回缓存文档，而不是去网站请求，这样既加快了本地调试速度，也减轻了 网站的压力。一举多得【但最好在第一次成功call通的情况下，再enable 这个选项】

## 整个scrapy框架

## 编写流程
1. 在`items.py` 中定义类，你要爬取什么数据，就定义相应的字段。
2. 在`spiders` 文件夹中定义自己的爬虫
3. 在`pipelines.py` 中存储自己的数据
4. (可选) 改 `settings.py`


## 跑scrapy 之前，需要保证你的venv或者全局Python环境存在两个环境库：
1. pypiwin32 (`pip install pypiwin32` ，或者去[这里](https://sourceforge.net/projects/pywin32/files/pywin32/Build%20221/pywin32-221.win-amd64-py3.6.exe/download) for 全局安装)
2. Twisted (去[这里](https://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted)下载，然后pip 安装它)
