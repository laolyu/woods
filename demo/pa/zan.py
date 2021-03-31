# -*- coding:utf-8 -*-

import requests_html
from requests_html import HTMLSession
import urllib3
import json, random
import os
import time, datetime
import pandas as pd
import numpy as np
# from bs4 import BeautifulSoup
# # from decimal import *
# import mysql.connector
# import multiprocessing
# from multiprocessing import Pool
from requests.cookies import RequestsCookieJar
from requests.adapters import HTTPAdapter

# from apscheduler.schedulers.background import BackgroundScheduler

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
np.set_printoptions(suppress=True)
session = HTMLSession()
session.mount('http://', HTTPAdapter(max_retries=3))
session.mount('https://', HTTPAdapter(max_retries=3))
session.keep_alive = False
requests_html.user_agent()


def cookie_on():
    url = 'http://thweb.weixinzsb.net:8000/CmOrg/CmOrgMap?moduleid=88&mid=-1&pid=88'
    proxies = {'http': 'http://localhost:8888', 'https': 'http://localhost:8888'}

    # 这里我们使用cookie对象进行处理
    global jar
    jar = RequestsCookieJar()
    with open("../jiucai/cookies_zan.txt", "r") as fp:
        cookies = json.load(fp)
        for cookie in cookies:
            jar.set(cookie['name'], cookie['value'].encode("utf-8").decode("latin1"))

    r = session.get(url=url, proxies=proxies, verify=False, cookies=jar)
    if '请输入用户名' in r.html.text:
        print('cookie expired')


def cc():
    rel = {'户主': '01', '配偶': 10, '妻': 12, '妻子': 12, '子': 20, '儿子': 20, '女婿': 28, '女': 30, '女儿': 30, '儿媳': 38, '孙子': 41,
           '孙女': 42, '外孙': 43, '外孙子': 43, '外孙女': 44, '父亲': 51, '父': 51, '母': 52, '母亲': 52, '奶': 62, '爷': 61, '妹': 70,
           '弟': 73, '姐': 75, '伯': 81, '侄子': 93, '侄女': 94}
    path = r"C:\Users\Administrator\Desktop\g\\"
    filenames = os.listdir(path)
    for file in filenames:
        print(file)
        excel_path = path + file
        f = open(excel_path, 'rb')
        # df = pd.read_excel(f, header=3, keep_default_na=False)
        df = pd.read_excel(f, header=3, dtype=str)
        # df = df.dropna(how='all')
        df.dropna(axis=0, subset=['身份证号'], inplace=True)
        df = df[~df.身份证号.str.contains('\.')]
        df = df.fillna("")
        for i in df.index:
            global IDCard, Name, SexCode, RelCode, HdTel, HouseCode, BirthDate, MsCode
            try:
                IDCard = df.loc[i, ['身份证号']].values[0]
                num = int(IDCard[16:17])
                if num % 2 == 0:
                    SexCode = 2
                else:
                    SexCode = 1
                Name = df.loc[i, ['姓名']].values[0]
                HdTel = df.loc[i, ['联系方式']].values[0]
                HouseCode = df.loc[i, ['户号']].values[0]
                BirthDate = "{0}/{1}/{2}".format(IDCard[6:10], IDCard[10:12], IDCard[12:14])
                cc = df.loc[i, ['与户主关系']].values[0]
                RelCode_0 = ''.join(cc.split())
                RelCode = rel[RelCode_0]
                if RelCode_0 in ['户主', '配偶', '妻', '妻子', '女婿', '儿媳', '母', '母亲', '奶', '爷', '姐', '妹', '弟', '父', '父亲']:
                    MsCode = 20
                elif RelCode_0 in ['孙子', '孙女', '外孙', '外孙子', '外孙女']:
                    MsCode = 10
                else:
                    MsCode = 90
                # print("读取excel数据:{0}".format(data))  # 格式化输出
                print(IDCard, Name, SexCode, RelCode, HdTel, HouseCode, BirthDate, MsCode)
            except KeyError as e:
                print(e)
                RelCode = '00'
                MsCode = 90
            url = 'http://thweb.weixinzsb.net:8000/OperateActualRegistryPopuInfo/InsertActualRegistryPopuInfo'
            proxies = {'http': 'http://localhost:8888', 'https': 'http://localhost:8888'}

            data = {'ID': '', 'saveType': '0', 'PlaceCode': '', 'Domicile': '', 'CurrentResidence': '', 'HdId': '',
                    'RegionName': '昝岗村', 'RegionCode': '411328306200', 'BeforeName': '', 'NationCode': 1,
                    'AdProvince': '41', 'AdCity': '4113', 'AdCounty': '411328', 'MsCode': MsCode, 'PartyCode': '13',
                    'EduCode': '90', 'RfCode': '00', 'OcCode': '05100', 'Occupation': '', 'UnitOfService': '',
                    'Tel': '', 'Dom_AdProvince': '41', 'Dom_AdCity': '4113', 'Dom_AdCounty': '411328',
                    'DomicileAddr': '', 'LongBanId': '', 'Curr_AdProvince': '41', 'Curr_AdCity': '4113',
                    'Curr_AdCounty': '411328', 'CurrentResidenceAddr': '', 'IsAgreement': '01', 'HdIDCard': '',
                    'HdName': '', 'IDCard': IDCard, 'Name': Name, 'SexCode': SexCode, 'RelCode': RelCode,
                    'HdTel': HdTel, 'HouseCode': HouseCode, 'BirthDate': BirthDate}

            try:
                r = session.post(url=url, data=data, proxies=proxies, verify=False, cookies=jar)
                # print(r.text)
                if '重复' not in r.text:
                    print(r.text)
            except Exception as e:
                print(e)
            finally:
                time.sleep(random.uniform(0.2, 1.2))


if __name__ == '__main__':
    cookie_on()
    cc()
