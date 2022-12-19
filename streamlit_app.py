import requests
from lxml import etree
import urllib
from urllib.request import urlopen
import streamlit as st
import arrow as ar
import requests as req
import json

st.set_page_config(
    page_title="星河梦华",
    page_icon="🌌",
)


# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-


def get_web_now_time(time_format='YYYY-MM-DD HH:mm'):
    """
    获取网络时间，返回时间格式：2019-12-13 11:39:48.398
    :param time_format:控制返回字符串的格式，默认为：'YYYY-MM-DD HH:mm:ss.SSS'
    :return:
    """
    res = req.get('https://www.baidu.com/').headers['Date']
    # res = req.get('https://www.hao123.com/').headers['Date']
    time_diff = ar.get(res[4:-4], 'DD MMM YYYY HH:mm:ss') - ar.now().floor('second')
    web_now_time = (ar.now() + time_diff).format(time_format)

    return web_now_time


def english_word():
    url = 'http://dict.eudic.net/home/dailysentence'
    req = urllib.request.Request(url)
    html = urlopen(req).read()
    # 解析网页数据
    html = etree.HTML(html)
    # 获取想要的内容
    result = html.xpath('.//div[@id="senten_move"]/p/text()')
    # 英文句子
    english = result[0]
    # 翻译
    chinese = result[1]
    return english, chinese


english_day, chinese_day = english_word()


def meiriyiwen():
    url = 'https://meiriyiwen.com/'
    req = urllib.request.Request(url)
    html = urlopen(req).read()
    # 解析网页数据
    html = etree.HTML(html)
    # 获取想要的内容
    result = html.xpath('//*[@id="article_show"]/div[1]')
    return result


def music_get():
    music_json = requests.get('https://api.uomg.com/api/rand.music?sort=热歌榜&format=json')

    # 返回 json 数据
    # return music_json.json()
    json_str = json.dumps(music_json.json())
    data_music = json.loads(json_str)
    return data_music['data']['name'], data_music['data']['url'], data_music['data']['picurl']


st.markdown("""![今日诗词](https://v2.jinrishici.com/one.svg?font-size=40&spacing=4)""")

st.header(get_web_now_time())

st.write(english_day)
st.write(chinese_day)
music_name, music_url, music_pic = music_get()
st.image(music_pic, caption=music_name, width=300, use_column_width='True')
st.audio(music_url)
