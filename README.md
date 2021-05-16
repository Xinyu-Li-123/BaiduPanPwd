# 暴力破解百度网盘密码的小工具
selenium自动化控制浏览器进行暴力破解，不用担心ip被封，缺点是速度慢，对设备性能要求比较高，目前代码报错率比较高

## Feature
* selenium自动化控制浏览器，ip不会被封
* 日志记录，断点续破
* 随机尝试密码
* 多线程破解
## 运行说明
### 运行环境
* python3环境
* python selenium库
* chrome浏览器
* chrome浏览器版本对应的chromedriver驱动，默认在当前文件夹
* 修改配置文件setting.py
```sh
python crack_by_sele.py
```
## 软件使用
### 参数说明
* URL地址：保证格式为https://pan.baidu.com/share/init?xxx即可，如果不是请在浏览器打开看看会不会自动跳转。
* 破解字典文件名：包含待尝试密码的文件名，文件格式一行一个密码，默认为目录下的allpwd.dic文件，可以使用superdic等软件生成
* 线程数：尝试线程数（8GB内存配置建议15）
### 日志文件
* 程序默认日志文件为log.dic，内容为尝试失败的密码，格式和破解字典相同，可以直接用于之后程序的忽略密码文件名参数。写入方式为追加写入，不会对已有数据造成影响。
* 找到的密码将会输出在屏幕上并且保存在yes.dic文件中，使用文本编辑器打开即可看到。
* 显示提取码错误网页元素id百度云经常会换，需要首先提取码试错一次，然后用浏览器开发者工具查找，后期会尽量解决这个问题
* 由于浏览器加载存在延迟，经常报错，这里采用二段方式，条件确认可行后再次确认，成功后追加到yes.dic
## 总结
欢迎大家提交issues和改良的见解，本人尽量在第一时间回复
### 优点
* ip不会被封
### 缺点
* 误报率比较高，yes.dic中的密码需要手动试错
* 速度比较慢，15-40个/min
* 占用系统资源比较高