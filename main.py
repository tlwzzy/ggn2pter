import site_api

if __name__ == "__main__":

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
