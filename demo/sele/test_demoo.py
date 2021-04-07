import json

import yagmail
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import datetime as d

import unittest, time, re, os
import random
import urllib3, requests_html
from requests_html import HTMLSession
from apscheduler.schedulers.background import BackgroundScheduler
from requests.adapters import HTTPAdapter
from requests.cookies import RequestsCookieJar

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
session = HTMLSession()
session.mount('http://', HTTPAdapter(max_retries=3))
session.mount('https://', HTTPAdapter(max_retries=3))
session.keep_alive = False
requests_html.user_agent()


class Pydemo(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://jssdkstore.lytoufang.com/demo/index"
        self.verificationErrors = []
        self.accept_next_alert = True
        self.scheduler = BackgroundScheduler()

    def tet_demo(self):
        driver = self.driver
        driver.set_window_position(0, 900)
        driver.set_window_size(1400, 400)

        js1 = self.base_url + '.html'
        js2 = self.base_url + '2.html'
        js3 = self.base_url + '3.html'
        js4 = self.base_url + '4.html'
        js5 = self.base_url + '5.html'
        js = [js1, js2, js3, js4, js5]
        for i in range(1000):
            url = random.choice(js)
            # print(i, url)
            try:
                driver.get(url)
                time.sleep(1)
                self.click_demo()
            except Exception as e:
                print(e)
        time.sleep(300)

    def click_demo(self):
        driver = self.driver
        forest = random.randint(0, 8)
        if forest == 0:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a > img:nth-child(1)")))
            driver.find_element(By.CSS_SELECTOR, "a > img:nth-child(1)").click()
            # print('点击落地页')
            time.sleep(1)
            windows = driver.window_handles  # 获取当前页句柄
            driver.switch_to.window(windows[-1])  # 跳转到新标签页
            driver.close()
            driver.switch_to.window(windows[0])  # 跳转到新标签页

    def send_mail(self):
        receiver = "pytest@139.com"
        yag = yagmail.SMTP("laolyu@foxmail.com", 'okpykwvdqeczhage', 'smtp.qq.com')
        body = self.ssp

        yag.send(
            to=receiver,
            subject='ssp success',
            contents=body
            # attachments=filename,
        )
        print('ssp-send mail')

    def tet_get_cookie(self):
        self.driver.get("http://test.ssp.shzhanmeng.com/user/login")
        self.driver.set_window_size(800, 1000)
        time.sleep(1.1)
        self.driver.find_element(By.ID, "userName").send_keys("laolyu@foxmail.com")
        self.driver.find_element(By.ID, "password").send_keys('l0vezm')
        self.driver.find_element_by_css_selector('.ant-btn > span').click()
        time.sleep(2)
        cookies = self.driver.get_cookies()
        with open("../cookies_ssp.txt", "w") as fp:
            json.dump(cookies, fp)
        time.sleep(2)

    def test_req_api(self):
        url = 'http://test.ssp.shzhanmeng.com/api/app/slot/report'
        millis = int(round(time.time() * 1000))
        date_now = d.datetime.now().strftime("%Y%m%d")
        proxies = {'http': None, 'https': None}
        # proxies = {'http': 'http://localhost:8888', 'https': 'http://localhost:8888'}
        data = {"current": 1, "pageSize": 30, "_timestamp": millis, "time_slot": [date_now, date_now]}

        cookie_jar = RequestsCookieJar()
        with open("../cookies_ssp.txt", "r") as fp:
            cookies = json.load(fp)
            for cookie in cookies:
                cookie_jar.set(cookie['name'], cookie['value'].encode("utf-8").decode("latin1"))
            # cookie_jar = RequestsCookieJar()
            # cookie_jar.set('token',
            #                'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC90ZXN0LXNzcC1iYWNrZW5kLnNoemhhbm1lbmcuY29tXC9hcGlcL2F1dGhcL2xvZ2luIiwiaWF0IjoxNjAzNDUyNTM4LCJleHAiOjE2MDM0NTYxMzgsIm5iZiI6MTYwMzQ1MjUzOCwianRpIjoiNmxiU24yeUJmYVBJTlVGRCIsInN1YiI6MjIsInBydiI6Ijg3ZTBhZjFlZjlmZDE1ODEyZmRlYzk3MTUzYTE0ZTBiMDQ3NTQ2YWEifQ.BlQPI09hoEOaSguuEktJsT-mMeD-DOeVlMYb29i4g2w')
        try:
            r = session.post(url=url, json=data, cookies=cookie_jar, proxies=proxies, verify=False)
            result = r.json()['data']['result']
            sum = 0
            err = ''
            for i in result:
                show = i['show']
                income = float(i['income'])
                sum += income
                if show < 100 or income < 10:
                    erro = i['app_slot_name'] + '>show:%s,income:%s￥' % (show, income)
                else:
                    erro = ''
                err += erro
            self.ssp = '￥%s.' % sum + err
            self.send_mail()
        except Exception as e:
            print(e)

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
