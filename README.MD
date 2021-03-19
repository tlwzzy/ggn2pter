# ggn2pter GGn自动转种机器人

## 简介

该脚本能够在你输入GGn的下载链接后自动获取相关信息并下载种子，同时自动将种子上传至PTerClub；使用过程中仅需要使用者确认是否存在中文字幕与国语配音

---

## 依赖环境 

###  python模式

* Python 3
*  Mac, Linux, Windows

### 可执行文件模式

* Windows, Linux

## 安装指南

### Python 模式

#### 1.克隆我的仓库
~~~~shell
git clone https://github.com/scatking/ggn2pter.git
~~~~
当然你也可以直接下载源码包后解压使用：
~~~~
https://github.com/scatking/ggn2pter/archive/master.zip
~~~~
#### 2.安装相关依赖
~~~~shell
pip install -r requirements.txt
~~~~
如果你无法安装的话可能是你的用户权限不够，尝试使用sudo安装
~~~~shell
sudo -H pip install -r requirements.txt
~~~~
#### 3.运行使用
~~~~shell
python main.py
~~~~
### 可执行文件模式

#### 稳定发布版

##### 1. 下载发布文件

前往 [发布页面](https://github.com/scatking/ggn2pter/releases ) 下载最新的发布文件

##### 2. 解压后双击`ggn2pter.py`运行使用

#### 最新版

#### 1. 下载发布文件
前往[Github Action](https://github.com/scatking/ggn2pter/actions)对应平台下载最新构建的发布包

##### 2. 解压后运行使用

## 使用指南

### 1.填写cookies
第一次运行程序时，程序会让你输入GGn与猫站的cookies，按照提示输入即可：
![cookies.png](https://img.pterclub.com/images/2021/03/15/2021-03-15-223914.png)
如果不知道如何获取cookies的，可以参考[常见问题](https://github.com/scatking/ggn2pter#%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98)

### 2.输入GGn的下载链接

### 3.等待程序运行

### 4.选择游戏信息
如果程序认为将要上传的种子的游戏信息可能已经存在于猫站，会返回一个列表让你选择游戏信息：

### 5.输入种子额外信息
由于无法从GGn稳定获取游戏地区，中文字幕与国语配音的相关信息，需要用户手动输入：
![moreinfo.png](https://img.pterclub.com/images/2021/03/15/2021-03-15-224809.png)

### 6.审查种子标题
脚本会自动将GGn的标题转换为符合猫站规则的标题，但是仍然需要用户进行检查。如果有错误请输入正确的标题，无误则直接回车。
~~~
智能检测到的种子标题为-TiNYiSO，若有错误，请输入正确的标题，没有请直接回车：
~~~

### 7.上传完成

## 常见问题
* Q. cookies 是个什么东西呀?怎么获取呀？
* A. cookie 是来存储你登陆信息的一串字符，下面我以chrome为例演示一下怎么获取。
* * 按下F12进入开发者工具，并切换至`NETWORK`栏目：
* * ![Network.png](https://img.pterclub.com/images/2020/02/28/1a74dee2a1e62fd48.png)
* * 单击你右上角的用户名，载入你的用户界面
* * 找到`NEWWORK`栏目里加载出来的user.php之类文件，并单击它：
* * ![user.php.png](https://img.pterclub.com/images/2020/02/28/2976315bd1515d7b2.png)
* * 找到request header 中cookie项目中的字段并复制下来（不用管演示里用红圈画起来的部分，实际上全部复制即可）：
* * ![cookies.png](https://img.pterclub.com/images/2020/02/28/33f121e11bf1e1639.png)

