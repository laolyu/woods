import json
import random
import re
import time
from datetime import date

import mysql.connector
import requests
from requests.adapters import HTTPAdapter
from requests_html import HTMLSession

# 基本配置
# ua = UserAgent(use_cache_server=False)
# ua = UserAgent(verify_ssl=False)
session = HTMLSession()
session.mount('http://', HTTPAdapter(max_retries=3))
session.mount('https://', HTTPAdapter(max_retries=3))
session.keep_alive = False


def parse_ymd(s):
    year_s, mon_s, day_s = re.split(r"[年月日]", s)[:-1]
    return date(int(year_s), int(mon_s), int(day_s))


def insert(value):
    db = mysql.connector.connect(
        host="localhost",  # 数据库主机地址
        user="root",  # 数据库用户名
        passwd="l0vezm",  # 数据库密码
        database="lvdb",
    )

    cursor = db.cursor()
    sql = """INSERT INTO law(flag,role,case_num,content,court,created)
         VALUES (%s,%s,%s,%s,%s,%s)"""
    try:
        cursor.execute(sql, value)
        db.commit()
        # print('sql insert success')
    except:
        db.rollback()
        print("sql insert fail")
    finally:
        db.close()


def job(page):
    url = 'http://gy.homolo.net:8080/app/service/rest/app.Fy12368/collection/acquireNoticeGGXX'
    proxies = {'http': 'http://localhost:8888', 'https': 'http://localhost:8888'}
    data = {'noticeType': 'sdgg', 'startNo': page * 20, 'courtCode': '211000', 'start': '2020年12月14日'}
    ii = 0
    while ii < 3:
        r = session.post(url=url, data=data, proxies=proxies, verify=False)
        versionInfoPython = json.loads(r.text)
        dataList = versionInfoPython.get('result')
        code_api = versionInfoPython.get('code')
        if code_api != 1:
            ii += 1
        else:
            print(time.strftime("%Y%m%d %H:%M:%S", time.localtime()), 'page%s,startNo%s' % (page, page * 20))
            for i in range(len(dataList)):
                # global bt
                bt = dataList[i]['bt']
                xwdz = dataList[i]['xwdz']
                try:
                    r2 = session.get(url=xwdz, proxies=proxies, verify=False)
                    bt_list = bt.split('——')
                    line_li = r2.html.text.split('\n')
                    line_list = list(filter(None, line_li))
                    flag = bt_list[0]
                    role = bt_list[1]
                    case = line_list[1]
                    content = line_list[-3]
                    court = line_list[-2]
                    created = parse_ymd(line_list[-1])
                    bank = (flag, role, case, content, court, created)
                    print(bank)
                    insert(bank)
                    time.sleep(random.uniform(2, 10))
                except Exception as e:
                    print(e)
            new_page = len(dataList) // 20 + page
            if new_page != page:
                job(new_page)
            else:
                print('当前页面数据不足20条,任务已完成')
            return


# def send_mail():
#     receiver = "laolyu@139.com"
#     yag = yagmail.SMTP("laolyu@foxmail.com", 'okpykwvdqeczhage', 'smtp.qq.com')
#     # global bt
#     body = bt
#     print(bt)

# yag.send(
#     to=receiver,
#     subject="fa signed in",
#     contents=body,
#     # attachments=filename,
# )
# print('2212-send mail')


if __name__ == '__main__':
    job(0)
