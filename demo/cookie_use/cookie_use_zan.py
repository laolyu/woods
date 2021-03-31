# -*- coding:utf-8 -*-

import requests_html
from requests_html import HTMLSession
import urllib3
import json
import re, os
import time, datetime
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
# from decimal import *
import mysql.connector
import multiprocessing
from multiprocessing import Pool
from requests.cookies import RequestsCookieJar
from requests.adapters import HTTPAdapter
from apscheduler.schedulers.background import BackgroundScheduler

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
np.set_printoptions(suppress=True)
session = HTMLSession()
session.mount('http://', HTTPAdapter(max_retries=3))
session.mount('https://', HTTPAdapter(max_retries=3))
session.keep_alive = False

user_agent = requests_html.user_agent()
url = 'https://www.bitcloud-home.com/Home/Index/jy/'
proxies = {'http': 'http://localhost:8888', 'https': 'http://localhost:8888'}
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'}
# session.get(url=url, headers=headers, proxies=proxies, verify=False)

# 也可以使用字典设置
# cookies_dict = dict()
# with open("cookies.txt", "r") as fp:
#     cookies = json.load(fp)
#     for cookie in cookies:
#         cookies_dict[cookie['name']] = cookie['value']
# r = session.get("https://www.baidu.com/p/setting/profile/basic", cookies=cookies_dict)

# 这里我们使用cookie对象进行处理
jar = RequestsCookieJar()
with open("cookies_06.txt", "r") as fp:
    cookies = json.load(fp)
    for cookie in cookies:
        jar.set(cookie['name'], cookie['value'])


def api_cbt():
    r = session.get(url=url, proxies=proxies, verify=False, cookies=jar)
    if 'login' in r.url:
        print('cookie expired')
    else:
        return r


def insert(value):
    db = mysql.connector.connect(
        host="localhost",  # 数据库主机地址
        user="root",  # 数据库用户名
        passwd="l0vezm",  # 数据库密码
        database="lvdb",
    )

    cursor = db.cursor()
    sql = """INSERT INTO cbt(number,cash,id,price)
                VALUES(%s,%s,%s,%s)"""
    #      VALUES ('%.1f','%.1f',%d,'%.1f')"""

    try:
        cursor.execute(sql, value)
        db.commit()
        # print('sql insert success')
    except Exception as e:
        db.rollback()
        print("sql insert fail:", e)
    finally:
        db.close()


def insert_data():
    r = session.get(url=url, proxies=proxies, verify=False, cookies=jar)
    # 方法一
    # soup = BeautifulSoup(r.content, 'html.parser', from_encoding='utf-8')
    # tags = soup.find_all(class_="button button-fill button-warning")
    # if tags:
    #     regex = r'((\-|\+)?\d+(\.\d+)?)'
    #     for tag in tags[:4]:
    #         order_line = tag['onclick']
    #         print(order_line)
    #         onclick = []
    #         for m in re.finditer(regex, order_line):
    #             onclick.append(m.group())
    #         # print(onclick)
    #         num = float(onclick[0])
    #         jine = float(onclick[1])
    #         xuhao = int(onclick[5])
    #         danjia = round(jine / num, 2)
    #         # danjia = Decimal(jine) / Decimal(num)
    #         onclick.append(danjia)
    #         bank = (num, jine, xuhao, danjia)
    #         print(bank)
    #         # bb = int(16462.1)
    #         insert(bank)
    # else:
    #     print('failed to get data needed')
    #     return

    # 方法二
    tags = r.html.search_all("('本次出售{}个钱包余额,可收{}美元,需要{}手续费出售100扣{},确认出售吗?'))cs_cl('{}')")[0:4]
    if tags:
        for tag in range(len(tags)):
            num = float(tags[tag][0])
            jine = float(tags[tag][1])
            xuhao = int(tags[tag][-1])
            danjia = round(jine / num, 2)
            bank = (num, jine, xuhao, danjia)
            print(bank, tags[tag][2])
            insert(bank)
            time.sleep(10)
    else:
        print('failed to get data needed')
        return


def read_database(sql):
    db = mysql.connector.connect(
        host="localhost",  # 数据库主机地址
        user="root",  # 数据库用户名
        passwd="l0vezm",  # 数据库密码
        database="lvdb",
    )

    # 利用pandas模块导入mysql数据
    try:
        df = pd.read_sql(sql, db)
        id_ndarray = df.to_numpy()[0]
        # print(id_ndarray)
        return int(id_ndarray[2]), id_ndarray[3]
    except Exception as e:
        print('Reading Error:', e)
        return
    finally:
        db.close()


def sale():
    # 查询交易0.1的出价最高的用户中id最新的
    sql_01 = """select a.* from cbt a where price=(select MAX(price) from cbt where number = a.number) 
                                AND to_days(created) = to_days(now()) AND a.number=0.1 order by a.id DESC LIMIT 1 """
    # 查询交易0.1的出价最高的用户中id第2新的
    sql_02 = """select a.* from cbt a where price=(select MAX(price) from cbt where number = a.number)
                            AND to_days(created) = to_days(now()) AND a.number=0.1  order by a.id DESC LIMIT 1,1 """

    tuple_01 = read_database(sql_01)
    tuple_02 = read_database(sql_02)
    url_jy = 'https://www.bitcloud-home.com/Home/Index/cs_cl/id/{}/'
    try:
        url_sale = url_jy.format(tuple_01[0])
        if tuple_01[1] == tuple_02[1]:
            r = session.get(url=url_sale, proxies=proxies, verify=False, cookies=jar)
            print(tuple_01[0])
            print(r.html.search('alert({})')[0])
    except Exception as e:
        print(e)


def job():
    p = Pool(17)
    for i in range(16):
        p.apply_async(insert_data)
        p.apply_async(sale)
    p.close()
    print(datetime.datetime.now().time(), 'Exiting')
    p.join()


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(job, 'cron', hour='6-22', minute='1-59/2', second='52')
    # scheduler.add_job(job(), 'cron', hour='9-22', minute='0-59/2', second='0-5', args=[0])
    scheduler.start()
    try:
        api_cbt()
        while True:
            time.sleep(80)
            # time.sleep(0.01)  # 调试
    except (KeyboardInterrupt, SystemExit):
        print('exit')
        scheduler.shutdown()
