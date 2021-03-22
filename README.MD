# ggn2pter GGn自动转种机器人![python](https://img.shields.io/badge/python-3.7-blue)![time](https://img.shields.io/github/last-commit/scatking/ggn2pter)

## 简介

该脚本能够在你输入GGn的下载链接后自动获取相关信息并下载种子，同时自动将种子上传至PTerClub

---
## 工具特点
* 自动转种并能够下载相关种子，方便配合BT客户端实现自动做种
* 支持有 `steam` `epic`或`indenova`条目的游戏
* 支持位列于 [platforms.txt](platforms.txt)目录下的平台
* 支持转载 `游戏本体` `更新补丁` `修改器` `DLC` `GAMEDOX`

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
如果你无法安装的话可能是你的用户权限不够，尝试使用`sudo`安装；对于某些同时装有`python2` 与 `python3` 的用户，可能需要指明`pip`的版本，如 `pip`
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

### 1.填写`config.ini`
```ini
[PASSKEY]
pter_key = passkey
;这里输入猫站的passkey
[WORKDIR]
torrent_dir = torrents
;这里输入种子下载目录
```

### 2.填写cookies
第一次运行程序时，程序会让你输入GGn与猫站的cookies，按照提示输入即可：
![cookies.png](https://img.pterclub.com/images/2021/03/15/2021-03-15-223914.png)
如果不知道如何获取cookies的，可以参考[常见问题](https://github.com/scatking/ggn2pter#%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98)

### 3.输入GGn的下载链接

### 4.等待程序运行

### 5.选择游戏信息
如果程序认为将要上传的种子的游戏信息可能已经存在于猫站，会返回一个列表让你选择游戏信息，如果不存在相关游戏的话，系统会自动上传到猫站。
```shell
我们在猫站找到以下游戏，请选择要上传的游戏分组（输入编号(并非gid)即可，如果没有请输入0）：
1.Windows: Cooking Simulator GID:3409
编号： <输入编号>
```
### 6. 选择indienova条目（仅主机）
对于没有`steam`和`epic`条目的主机游戏，脚本会自动搜索indienova网站并返回一个游戏列表，此时需要输入列表中的编号
```shell
未找到steam或epic链接，正在前往indenova查询
... ... ...
1.Cooking Simulator (2018)|g※|厨房模拟器|g※|
2.Cooking Simulator: Cakes and Cookies (2020)|g※|厨房模拟器：蛋糕和曲奇饼|g※|
请输入适配游戏的序号：<输入编号>
```
### 7.输入种子额外信息
由于无法从GGn稳定获取游戏地区，中文字幕与国语配音的相关信息，需要用户手动输入：
![moreinfo.png](https://img.pterclub.com/images/2021/03/15/2021-03-15-224809.png)

### 8.审查种子标题
脚本会自动将GGn的标题转换为符合猫站规则的标题，但是仍然需要用户进行检查。如果有错误请输入正确的标题，无误则直接回车。
~~~
智能检测到的种子标题为-TiNYiSO，若有错误，请输入正确的标题，没有请直接回车：
~~~

### 8.上传完成

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

