from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import unittest, time, re, os
import sys, requests, urllib3
import yagmail
from apscheduler.schedulers.background import BackgroundScheduler
from selenium.common.exceptions import UnexpectedAlertPresentException

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
# sys.path.append(rootPath)
# import bank
from bdocr import domain


class Py(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.bitcloud-home2.com"
        self.verificationErrors = []
        self.accept_next_alert = True
        self.scheduler = BackgroundScheduler()

    def test_158(self):
        # self.login('13628105564', 'l0vepp')
        # self.login('13796491944', 'l0vepp')

        self.login('15828211624', 'l0vepp')
        # self.login('18942752145', 'l0vepp')
        # self.login('15050566251', 'l0vepp')
        self.sign()
        # self.send_mail()
        # self.isOrderExist()

        # self.screenshot()  # 会员中心截图
        # driver.find_element_by_css_selector("i.iconfont.icon-wxbdingwei").click()
        # driver.find_element_by_link_text("买入CBT").click()
        # self.screenshot()  # 买单截图
        # self.isElem01Exist()
        # self.isElem02Exist()
        # driver.find_element_by_link_text("卖出CBT").click()
        # self.isElem01Exist()
        # self.screenshot()  # 卖出截图

    #     self.scheduler.add_job(self.job, 'cron', hour='7-18', minute='1-59/2', second=41)
    #
    # def job(self):
    #     time.sleep(randint(0, 10))
    #     self.driver.find_element_by_css_selector("i.iconfont.icon-wxbdingwei").click()
    #     self.is_element_present("name", "Submit")

    def login(self, account, password):
        driver = self.driver
        driver.set_window_position(0, 1360)
        driver.set_window_size(600, 800)
        driver.get(self.base_url + "/home/login/index.html")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img')))
        time.sleep(5)
        # driver.find_element_by_id('submit')
        driver.find_element_by_css_selector('img').screenshot('code_08.png')
        # try:
        #     # 打开并显示图片
        #     img = Image.open('code_08.png')
        #     img.show()
        #     img.close()
        # except:
        #     print('获取验证码失败')
        vercode = domain('code_08.png')
        time.sleep(1)
        driver.find_element_by_id("account").clear()
        driver.find_element_by_id("account").send_keys(account)
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(password)
        driver.find_element_by_id("verCode").clear()
        driver.find_element_by_id("verCode").send_keys(vercode)
        driver.find_element_by_id("submit").click()  # 确定登录
        self.close_alert_and_get_its_text()

    def sign(self):
        driver = self.driver
        driver.find_element_by_css_selector("i.iconfont.icon-shouye").click()
        driver.find_element_by_id("fwqsj").click()
        self.body = self.close_alert_and_get_its_text_02()
        if '成功' not in self.body:
            self.send_mail()

    def send_mail(self):
        receiver = "pytest@139.com"
        yag = yagmail.SMTP("laolyu@foxmail.com", 'okpykwvdqeczhage', 'smtp.qq.com')
        body = self.body

        yag.send(
            to=receiver,
            subject="158 signed in",
            contents=body,
            # attachments=filename,
        )
        print('158-send mail')

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to.alert
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            WebDriverWait(self.driver, 1).until(EC.alert_is_present(),
                                                'Timed out waiting for PA creation ' + 'confirmation popup to appear.')
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
                if '出售成功' in alert_text:
                    print('send mail')
                elif '错误' in alert_text:
                    print(alert_text)
                    self.login('15828211624', 'l0vepp')
                else:
                    print(alert_text)
            else:
                alert.dismiss()
            return alert_text
        except TimeoutException:
            return True
        finally:
            self.accept_next_alert = True

    def close_alert_and_get_its_text_02(self):
        try:
            WebDriverWait(self.driver, 2).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            print(alert_text)
            return alert_text
        except UnexpectedAlertPresentException:
            print('selenium.common.exceptions.UnexpectedAlertPresentException')
            # alert = self.driver.switch_to.alert
            # alert_text = alert.text
            # alert.accept()
            # print(alert_text)
        #     if '成功' in alert_text:
        #         self.send_mail()
        # except TimeoutException:
        #     pass

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
