import site_api
import json
import os

if __name__ == "__main__":
    if 'cookies.json' not in os.listdir():
        print('检测到cookies文件不存在，请手动输入cookies：')
        ggn_cookie = input('请输入GGn的cookie：')
        pter_cookie = input('请输入PTer的cookie：')
        cookies = {"ggn":ggn_cookie,"pter":pter_cookie}
        with open('cookies.json','w') as coo:
            json.dump(cookies,coo)
    while True:
        ggn_link = input('请输入一个GGn种子下载连接：')
        ggn = site_api.GGnApi(ggn_link)
        ggn_info = ggn.worker()
        pter = site_api.PTerApi(ggn_info)
        pter.worker()
