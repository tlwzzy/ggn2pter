import site_api
import json
import os
import configparser


def initial():
    if 'cookies.json' not in os.listdir():
        print('检测到cookies文件不存在，请手动输入cookies：')
        ggn_cookie = input('请输入GGn的cookie：')
        pter_cookie = input('请输入PTer的cookie：')
        cookies = {"ggn": ggn_cookie, "pter": pter_cookie}
        with open('cookies.json', 'w') as coo:
            json.dump(cookies, coo)

    if 'config.ini' not in os.listdir():
        print('检测到config文件不存在，接下来将引导生成配置文件')
        config = configparser.ConfigParser()
        passkey = input('请输入passkey：')
        anonymous = input('是否匿名发布(yes/no)：')
        torrent_dir = input('请输入种子下载路径，默认为当前目录下的torrents文件夹:')
        if torrent_dir == '':
            torrent_dir = 'torrents'
        config['PTER'] = {'pter_key': passkey, 'anonymous': anonymous}
        config['WORKDIR'] = {'torrent_dir': torrent_dir}
        config.write(open('config.ini', 'w'))


if __name__ == "__main__":
    initial()
    ggn_link = input('请输入一个GGn种子下载连接或者直接回车开始扫描\'ggn_links.txt\'文件：')
    if ggn_link == '':
        with open('ggn_links.txt') as games:
            ggn_links = games.read().splitlines()
    else:
        ggn_links = [ggn_link]
    for ggn_link in ggn_links.copy():
        ggn = site_api.GGnApi(ggn_link)
        ggn_info = ggn.worker()
        pter = site_api.PTerApi(ggn_info)
        pter.worker()
        ggn_links.remove(ggn_link)
    with open('ggn_links.txt', 'w') as gls:
        for link in ggn_links:
            gls.write(link + '\n')
    input('上传完毕，输入任意字符退出')
