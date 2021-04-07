import requests, time
import re
from PIL import Image
import urllib3
from fateadm_api_lv import ocr_fateadm

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = 'https://www.bitcloud-home.com/home/login/index.html'
proxies = {'http': 'http://localhost:8888', 'https': 'http://localhost:8888'}
headers = {
    # 'Cache-Control': 'max-age=0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    # 'Cookie': '__cfduid=dcda8557973894b0e74718962658388a61590326594; PHPSESSID=8p2m94ac999qfk5043gls4kai5; cf_clearance=42b7cf3f81708d856111cf8de2b74b506dcc1a4a-1590329236-0-150'
}
# 定义一个session()的对象实体s来储存cookie
s0 = requests.session()
response0 = s0.get(url=url, headers=headers, proxies=proxies, verify=False, timeout=10)
# response1.encoding = 'utf-8'
time.sleep(10)
s = requests.session()
response1 = s0.get(url=url,
                   headers=headers,
                   proxies=proxies,
                   verify=False, timeout=10
                   )
# response1.encoding = 'utf-8'


# html1 = response1.text
# 利用正则表达式找到验证码的url，由于得到的是列表，用list[0]转成str
# cheakcode_url = re.findall(r'<img\s*src="(.*?)"\s*width="80px"\s*height="20px"', html1)[0]
cheakcode_url = 'https://www.bitcloud-home.com/Home/login/verify'
response2 = s.get(url=cheakcode_url, headers=headers, proxies=proxies, verify=False)
# 在当前文件夹保存为code.jpg，注意要用'b'的二进制写的方式，用content来获得bytes格式

if response2.status_code == 200:
    with open('code.jpg', 'wb') as fp:
        fp.write(response2.content)
        # time.sleep(5)
    try:
        # 打开并显示图片
        img = Image.open('code.jpg')
        img.show()
        img.close()
        # testbank = TestFunc('code.jpg')
    except:
        print('获取验证码失败')
else:
    print('验证码请求失败-----<>----')

    # with open('vercode.png', 'wb') as f:
    #     f.write(r.content)
    #     time.sleep(5)
    #
    # try:
    #     image = Image.open('vercode.png')
    #     im = image.point(lambda x: 0 if x < 143 else 255)  # 阈值处理
    #     im.save('wode.png')
    #     # im.show()
    #     # im.close()
    # except:
    #     print('获取验证码失败')

# 需要给服务端传送的数据，字典格式
# data = {}
# data['username'] = '你的帐号'
# data['password'] = '你的密码'
# data['checkCode'] = input('输入验证码：')
# response3 = s.post(url=url, data=data, headers=headers)
# print(response3.text)
# testbank = TestFunc('code.jpg')
data = {}
data['account'] = '15183684212'
data['password'] = 'l0vepp'
data['verCode'] = ocr_fateadm('code.jpg')
data['dlzt'] = ' 1'
data['submit'] = ' 登 ? ? 录'

response3 = s.post(url=url, data=data, headers=headers, proxies=proxies, verify=False)
