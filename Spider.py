# -*- coding: utf-8 -*-
import requests
from lxml import etree
from lib import IP
import random
import os
from tqdm import tqdm



proxies = {
    "http": random.choice(IP.ip)
}
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'cookie': 'Hm_lvt_985c57aa6304c183e46daae6878b243b=1725587403; HMACCOUNT=E02DBA47ED4636D0; Hm_lpvt_985c57aa6304c183e46daae6878b243b=1725587418'
}
'''
笔趣阁网站地址
https://www.bbtxt8.com
https://www.bqgbe.com
https://www.bqgbi.com

https://www.bqgbi.com/book/496/
'''

print("=============================================================================\n\n")

'''
模式一  每个章节为一个txt文件
模式二  所有章节为一个txt文件
'''

def get_data():
    # 获取用户输入参数
    #url_name = input("请输入笔趣阁最新网址：")
    url_name = 'https://www.bqgai.cc'
    #novel_url = input("请输入要下载小说的网址：")
    novel_url = 'https://www.bqgai.cc/book/181741/'
    download_mode = input("请选择下载模式：\n (1)每章节一个文本文件\n (2)所有章节一个文本文件 \n 请输入数字选择：")

    response = requests.get(novel_url, headers=headers).content.decode("utf-8")
    novel_info_html = etree.HTML(response)
    print("--------------------------------")
    print(novel_info_html)
    # 获取小说名称
    novel_title = "".join(novel_info_html.xpath("//h1/text()"))
    print("--------------------------------")
    print(novel_title)
    # 获取每一章节名称
    novel_chapters_title = novel_info_html.xpath("//dd/a/text()")
    print("--------------------------------")
    print(novel_chapters_title)
    # 获取每一章节的地址
    novel_charters_url = novel_info_html.xpath("//dd/a/@href")
    novel_charters_url = [link for link in novel_charters_url if link.endswith('.html')]
    print("--------------------------------")
    print(novel_charters_url)
    # 如果没有就创建一个存放所有小说的目录
    if not os.path.exists('./Novel'):
        os.mkdir("./Novel")
    # 判断下载模式
    if download_mode == '1':
        # 判断小说目录是否已存在
        if not os.path.exists('./Novel/' + novel_title):
            # 根据小说名称创建目录
            os.mkdir("./Novel/" + novel_title)
        for novel_charter_url, novel_charter_title in zip(novel_charters_url, novel_chapters_title):
            # print(novel_charter_title)
            # 拼接每一章小说地址
            novel_charter_url = url_name + novel_charter_url
            print('章节名称：', novel_charter_title, '\n地址：', novel_charter_url,)
            try:
                charter_info = requests.get(novel_charter_url, headers=headers, proxies=proxies).content.decode("utf-8")
                charter_info_html = etree.HTML(charter_info)
                charter_content = charter_info_html.xpath("//div[@id='chaptercontent']/text()")
                # print(charter_content)
                for item in charter_content:
                    with open('./Novel/' + novel_title + "/" + novel_charter_title + ".txt", "a+", encoding="utf-8") as file:
                        file.write('\n' + item.replace('\xa0', '\n\n'))
            except:
                pass
            print(novel_charter_title + "--下载完成")
    elif download_mode == '2':
        with open('./Novel/' + novel_title + '.txt', 'a+', encoding='utf-8') as file:
            for novel_url, novel_chapter_title in tqdm(list(zip(novel_charters_url, novel_chapters_title)), desc='下载中', ncols=100, colour='#3271ae'):
                # 拼接每一章小说地址
                novel_charter_url = url_name + novel_url
                try:
                    charter_info = requests.get(novel_charter_url, headers=headers, proxies=proxies).content.decode("utf-8")
                    charter_info_html = etree.HTML(charter_info)
                    charter_content = charter_info_html.xpath("//div[@id='chaptercontent']/text()")
                    file.write(novel_chapter_title + '\n')
                    for item in charter_content:
                        file.write('\n' + item.replace('\xa0', '\n\n'))
                except Exception as e:
                    pass
    print("《%s》下载完成！" % novel_title)