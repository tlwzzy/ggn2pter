import requests
import re
from bs4 import BeautifulSoup
import os
import scatfunc
import json
import bencodepy
import configparser


headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'User-Agent': 'REDBetter crawler',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'}

release_type_dict = {
    'Full ISO': '1',
    'GGn Internal': '1',
    'P2P': '1',
    'Rip': '1',
    'Scrubbed': '1',
    'Home Rip': '1',
    'DRM Free': '1',
    'ROM': '1',
    'Other': '1',
    'Fix/Keygen': '3',
    'Update': '2',
    'DLC': '9',
    'GOG-Goodies': '5',
    'Trainer': '4',
    'Tool': '8',
    'Guide': '6',
    'Artwork': '5',
    'Audio': '7'
}

release_format_dict = {
    'Full ISO': '2',
    'GGn Internal': '4',
    'P2P': '4',
    'Rip': '3',
    'Scrubbed': '7',
    'Home Rip': '4',
    'DRM Free': '5',
    'ROM': '1',
}


class GGnApi:
    def __init__(self, dl_link, cookies=None):
        self.session = requests.Session()
        self.session_cookies = cookies
        self.session.headers = headers
        self.dl_link = dl_link
        self.torrent_id = re.search(r'id=(\d+)', dl_link).group(1)

    def _install_cookies(self):
        if not self.session_cookies:
            with open('cookies.json', 'r') as r:
                cookies = json.load(r)
            cookies = scatfunc.cookie2dict(cookies['ggn'])
            self.session.cookies = requests.utils.cookiejar_from_dict(cookies)
        else:
            return None

    def _find_store(self):
        url = 'https://gazellegames.net/torrents.php?torrentid={}'.format(self.torrent_id)
        url = self.session.get(url).url
        res = self.session.get(url)
        self.res_soup = BeautifulSoup(res.text, 'lxml')
        self.name = re.search(r'-\s(.+)\s\(\d{4}', self.res_soup.select_one('#display_name').text).group(1)
        try:
            self.steam = self.res_soup.select_one('a[href^="https://store.steampowered.com/app/"][title="Steam"]')[
                'href']
        except TypeError:
            self.steam = None
        try:
            self.epic = self.res_soup.select_one('a[href^="https://www.epicgames.com/store"][title="EpicGames"]')[
                'href']
        except TypeError:
            self.epic = None
        return {'steam': self.steam, 'epic': self.epic}

    def _copy_desc(self):
        url = 'https://gazellegames.net/torrents.php?action=edit&id={}'.format(self.torrent_id)
        # url = 'http://127.0.0.1:85/ggn5.html'
        desc = self.session.get(url)
        desc_soup = BeautifulSoup(desc.text, 'lxml')
        self.torrent_desc = desc_soup.select_one('#release_desc').text.replace('[align=center]','').replace('[/align]','')
        self.release_title = desc_soup.select_one('#release_title').get('value')
        if desc_soup.select_one('#remaster_title'):
            self.release_title += '-GOG' if 'GOG' in desc_soup.select_one('#remaster_title').get(
                'value').upper() else ''
        self.release_type = desc_soup.select_one('#miscellaneous option[selected="selected"]').text
        if self.release_type == 'GameDOX':
            self.release_type = desc_soup.select_one('#gamedox option[selected="selected"]').text
        self.scene = 'yes' if desc_soup.select_one('input#ripsrc_scene[checked="checked"]') else 'no'
        self.verified = 'yes' if self.release_type in 'P2P DRM Free' else 'no'
        return self.torrent_desc

    def _download_torrent(self):
        res = self.session.get(self.dl_link)
        torrent = bytes()
        for chunk in res.iter_content(100000):
            torrent += chunk
        torrent = bencodepy.decode(torrent)
        torrent[b'announce'] = b'https://tracker.pterclub.com/announce?passkey='+bytes(pter_key,encoding='utf-8')
        torrent[b'info'][b'source'] = bytes('[pterclub.com] ＰＴ之友俱乐部',encoding='utf-8')
        del torrent[b'comment']
        torrent = bencodepy.encode(torrent)
        if 'torrents' not in os.listdir():
            os.mkdir('torrents')
        with open(os.path.join('torrents', os.path.basename('{}.torrent'.format(self.release_title))), 'wb') as t:
            t.write(torrent)

    def _return_terms(self):
        attr = {}
        for name, value in vars(self).items():
            attr[name] = value
        del attr['res_soup']
        del attr['session']
        return attr

    def worker(self):
        self._install_cookies()
        print('正在获取游戏信息...')
        self._find_store()
        print('正在获取种子信息...')
        self._copy_desc()
        print('正在下载种子...')
        self._download_torrent()
        return self._return_terms()


class PTerApi:
    def __init__(self, ggn_info, cookies=None):
        self.session = requests.Session()
        self.session_cookies = cookies
        self.session.headers = headers
        self.name = ggn_info['name']
        self.steam = ggn_info['steam']
        self.epic = ggn_info['epic']
        self.release_title = ggn_info['release_title']
        self.release_type = ggn_info['release_type']
        self.torrent_desc = ggn_info['torrent_desc']
        self.scene = ggn_info['scene']
        self.verified = ggn_info['verified']
        self.gid = None

    def _install_cookies(self):
        if not self.session_cookies:
            with open('cookies.json', 'r') as r:
                cookies = json.load(r)
            cookies = scatfunc.cookie2dict(cookies['pter'])
            self.session.cookies = requests.utils.cookiejar_from_dict(cookies)
        else:
            return None

    def _find_game(self):
        url = 'https://pterclub.com/searchgameinfo.php'
        data = {'name': self.name}
        # data = {'name':'into'}
        res = self.session.post(url, data=data)
        res_soup = BeautifulSoup(res.text, 'lxml')
        user_class = res_soup.select_one('a[href^="userdetails.php?id="][class$="_Name"]')['class'][0].split('_')[0]
        uplev = 'ModeratorAdministratorUploaderSysOp'
        if user_class in uplev:
            self.uplver = 'yes'
        else:
            self.uplver = 'no'
        game_list = res_soup.select('a[title="点击发布这游戏设备的种子"]')
        platform_list = res_soup.select('img[src^="/pic/category/chd/scenetorrents/"]')
        if not game_list:
            return None
        game_dict = {}
        num = 1
        for game, platform in zip(game_list[::2], platform_list):
            print(platform)
            gid = re.search(r'detailsgameinfo.php\?id=(\d+)', game['href']).group(1)
            game_dict[str(num)] = '{}: {} GID:{}'.format(platform['title'], game.text, gid)
            num += 1
        print('我们在猫站找到以下游戏，请选择要上传的游戏分组（输入编号(并非gid)即可，如果没有请输入0）：')
        for num, game in game_dict.items():
            print('{}.{}'.format(num, game))
        gid = (input('编号： '))
        if gid == '0':
            return None
        print(game_dict[gid])
        gid = re.search(r'GID:(.+)', game_dict[gid]).group(1)
        print(gid)
        self.gid = gid
        return gid

    def _upload_game(self):
        url = 'https://pterclub.com/takeuploadgameinfo.php'
        if self.steam:
            game_info = scatfunc.steam_api(self.steam)
        else:
            game_info = scatfunc.epic_api(self.epic)
        data = {'uplver': self.uplver, 'detailsgameinfoid': '0', 'name': self.name, 'color': '0', 'font': '0',
                'size': '0', 'descr': game_info['about'], 'console': '16', 'year': game_info['year'],
                'has_allowed_offer': '0', 'small_descr': input('请输入游戏中文名')}
        game_url = self.session.post(url, data=data).url
        gid = re.search(r'detailsgameinfo.php\?id=(\d+)', game_url).group(1)
        self.gid = gid

    def _upload_torrent(self):
        url = 'https://pterclub.com/takeuploadgame.php'
        torrent_file = os.path.join(torrent_dir,'[PTer]{}.torrent'.format(self.release_title))
        file = ("file", (os.path.basename(torrent_file), open(torrent_file, 'rb'), 'application/x-bittorrent')),
        data = {'uplver': self.uplver, 'categories': release_type_dict[self.release_type],
                'format': release_format_dict[self.release_type] if self.release_type in release_format_dict else '7', 'has_allowed_offer': '0', 'gid': self.gid,
                'descr': self.torrent_desc}
        region = input('请选择种子地区（直接输入数字即可）：\n1.大陆\n2.香港\n3.台湾\n4.英美\n5.韩国\n6.日本\n7.其它\n')
        if self.scene == 'yes':
            data['sce'] = self.scene
        if self.verified == 'yes':
            data['vs'] = self.verified
        if input('该资源是否有中文？（yes/no）默认为no：') == 'yes':
            data['zhongzi'] = 'yes'
        if input('该资源是否有国语？(yes/no) 默认为no：') == 'yes':
            data['guoyu'] = 'yes'
        data['team'] = region
        short_name = scatfunc.back0day(self.name, self.release_title)
        user_title = input('智能检测到的种子标题为{}，若有错误，请输入正确的标题，没有请直接回车：'.format(short_name))
        user_title = short_name if user_title == '' else user_title
        data['name'] = user_title
        self.session.post(url, data=data, files=file)

    def worker(self):
        self._install_cookies()
        print('正在搜索猫站游戏列表...')
        self._find_game()
        if self.gid is None:
            print('未找到相关游戏，正在上传游戏资料...')
            self._upload_game()
        print('正在上传种子...')
        self._upload_torrent()


if __name__ == '__main__':
    ggn = GGnApi('none')
    ggn._download_torrent()
