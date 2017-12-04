#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-11-24 15:27:06
# @Author  : Cyb (${email})
# @Link    : ${link}
# @Version : $Id$

import requests
from bs4 import BeautifulSoup
import json
import re
import logging
import sys

logging.basicConfig(level=logging.INFO)


def GetHeader():
    header = {
        'Cookie': 'appver=1.5.0.75771',
        'Referer': 'http://music.163.com/'
    }
    return header


def GetLyric(song_id):
    url = 'http://music.163.com/api/song/lyric?id=' + \
        str(song_id) + '&lv=1&kv=1&tv=-1'

    result = requests.get(url, headers=GetHeader())
    soup = BeautifulSoup(result.content, 'html.parser')
    json_obj = soup.text
    j = json.loads(json_obj)

    if 'lrc' in j:
        if 'lyric' in j['lrc']:
            lrc = j['lrc']['lyric']
            # logging.debug(lrc)
            pat = re.compile(r'\[.*\]')
            lrc = re.sub(pat, "", lrc)
            lrc = lrc.strip()
            logging.debug(lrc)
            return lrc
        else:
            logging.debug(str(song_id) + '暂无歌词收录')
    else:
        logging.debug(str(song_id) + '纯音乐无歌词')
    return None
    # except Exception as e:
    #     logging.debug(str(song_id) + '这首歌没有歌词')
    #     logging.exception(e)


def GetSongs(artist_id):
    url = 'http://music.163.com/artist?id=' + str(artist_id)
    result = requests.get(url, headers=GetHeader())
    soup = BeautifulSoup(result.content, 'html.parser')
    name = soup.title.string
    CM_tail = re.compile(' - 歌手 - 网易云音乐')
    name = re.sub(CM_tail, '', name)
    logging.info('歌手： ' + name)
    logging.info('歌手id： ' + str(artist_id))
    logging.info('-----------------------------------')
    a_obj = soup.find_all('a')
    song_list = []
    # logging.debug(songs.title)
    pat = re.compile(r'/song\?id=[\d*]')
    for song in a_obj:
        tmp_url = song.get('href')
        if re.match(pat, tmp_url):
            logging.info('歌名: ' + song.get_text())
            song_id = re.sub(r'/song\?id=', "", tmp_url)
            logging.debug(tmp_url)
            logging.debug(song_id)
            song_list.append(song_id)
            # GetLyric(song_id)
    return song_list
    # logging.debug(song)
    # return songs


def GetArtists(type_id):
    # class_=msk 大图歌手 class_=nm nm-icn f-thide s-fc0 歌手id class_=f-tdn 歌手个人主页
    # 华语歌手100x(1<=x<=3) 欧美200x 日本600x 韩国700x 其他400x
    url = 'http://music.163.com/discover/artist/cat?id=' + str(type_id)
    result = requests.get(url, headers=GetHeader())
    soup = BeautifulSoup(result.content, 'html.parser')
    soup = soup.find_all('a', class_='nm nm-icn f-thide s-fc0')
    artist_list = []
    pat = re.compile(r'/artist\?id=')
    for link in soup:
        artist_id = link.get('href')
        artist_id = re.sub(pat, "", artist_id)
        logging.debug(link.get('title'))
        logging.debug('his/her/their id is ' + artist_id)
        artist_list.append(artist_id)
    logging.info('歌手list： ' + str(artist_list))
    logging.info('list大小' + str(len(artist_list)))
    return artist_list


def CountLove(mode, lrc):
    if mode == 1:
        pat = re.compile(r'爱')
    elif mode == 2:
        pat = re.compile(r'love', re.I)

    return len(pat.findall(lrc))


logging.debug(sys.argv[0])
love = 0
for x in range(1001, 1002):
    ArtistList = GetArtists(x)
    count = 0
    for artist in ArtistList:
        ArtistsSongs = GetSongs(artist)
        for song in ArtistsSongs:
            lrc = GetLyric(song)
            if lrc:
                love += CountLove(x % 1000, lrc)
        count += 1
        logging.info('----------------------已爬取' + str(count) +
                     '/' + str(len(ArtistList)) + '位歌手-----------------')

print('一共出现了' + str(love) + '次“爱”')


# GetLyric(28866346)
# GetLyric(374590)
# GetSongs(12707)
