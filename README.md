# tickets_tool
### 12306火车票查询工具

## 查询格式
"""Train tickets query via command-line.  
  
Usage:  
　　tickets [-GCDTKZYO] \<from> \<to> \<date>
  
Options:  
　　-h,--help   显示帮助菜单  
　　-G          高铁  
　　-C          城际  
　　-D          动车  
　　-T          特快  
　　-K          快速  
　　-Z          直达  
　　-Y          旅游  
　　-O          其他  
  
Example:  
　　tickets beijing shanghai 2016-08-25  
"""  
  
## 更新
* 2016.10.07 初版 实现基本功能， 分析发送的请求， 提取查询信息  
* 2016.10.10 更新 添加到站日期显示， 添加硬座、商务座查询列
* 2016.10.11 更新 日期已支持YYYYMMDD格式， 添加彩色车站信息标识
* 2017.03.13 更新 对于12306查询重新进行解析， 添加virtualenv， 添加包依赖信息requirement.txt  
* 2017.03.14 更新 利用docopt进行命令行参数自动解析，并按参数筛选符合条件的结果进行显示；修复一个历时显示错误的bug  

## 参考资料
[实验楼文档](https://www.shiyanlou.com/courses/623/labs/2072/document)  
[prettytable文档](https://code.google.com/archive/p/prettytable/wikis/Tutorial.wiki)  
[virtualenv参考资料](http://www.nowamagic.net/academy/detail/1330228)  
[docopt参考资料](http://www.tuicool.com/articles/36zyQnu)  
  
## ToDoList
- [x] 添加参数解析功能与对应结果筛选  
- [ ] 添加输入中文车站查询功能
- [ ] 添加可视化界面 暂计划使用wxpython
