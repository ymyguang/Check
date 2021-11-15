import urllib.parse

import ddddocr
import requests
from bs4 import BeautifulSoup

res = None

header = {
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'http://xscfw.hebust.edu.cn/evaluate/verifyCode?d=1636955535211',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
}


# 获取cookie和验证码
def init():
    global res
    r = requests.get('http://xscfw.hebust.edu.cn/evaluate/verifyCode', stream=True)
    cookie = str(r.headers['Set-Cookie']).split(" ")[0]
    header['Cookie'] = cookie

    ocr = ddddocr.DdddOcr()
    res = ocr.classification(r.content)
    print("cookie:{}    verify:{}".format(cookie, res))


# 使cookie生效 (登陆)
def login():
    global res
    init()
    r = requests.post("http://xscfw.hebust.edu.cn/evaluate/evaluate", headers=header,
                      data="username=xxxyhaolei&password=Haolei2021l19.&verifyCode=" + urllib.parse.quote(res))
    soup = BeautifulSoup(r.text, 'html.parser')

    t = soup.get_text()
    t = str(t).replace("\n", "")
    print(t)
    print(type(t))


if __name__ == '__main__':
    while True:
        login()
        input()
