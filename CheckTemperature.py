import datetime
import time
import urllib.parse

import ddddocr
import requests
from bs4 import BeautifulSoup

set_name = set()
maxPage = 99
qq_dict = {
    "曹骏": 3137136096,
    "郭楠": 2690681751,
    "李昂": 1340170910,
    "李晨": 591487622,
    "李樊": 3029198839,
    "刘彪": 2096304869,
    "罗琦": 2502013244,
    "王鑫": 2248278179,
    "吴卫": 1473908028,
    "张稳": 1548720908,
    "赵伟": 2392965199,
    "蔡思琦": 1656909554,
    "揣星宇": 2086798102,
    "高世豪": 498661819,
    "郝梦畅": 1208067561,
    "康兴旺": 2315143636,
    "李佳林": 1306791767,
    "李江楠": 1009740561,
    "李可欣": 1092896132,
    "李尚恒": 1332250851,
    "李兆林": 2697951507,
    "刘明一": 1351244826,
    "刘善宝": 1395896975,
    "刘旭辉": 775373008,
    "吕天乐": 747920501,
    "苏世超": 292301843,
    "王湜裕": 835017638,
    "辛宇航": 953725247,
    "邢梓阳": 2209906415,
    "徐晓杰": 2817605916,
    "徐雪彬": 2417933635,
    "杨翔宇": 1950381153,
    "杨宇哲": 2212607441,
    "宇文可": 1625290298,
    "章传喜": 2811165455,
    "周超": 1000000000
}

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


def feedback(text, case='M'):
    qq = {
        'M': 2096304869,
        "G": 1042333099
        # 以下是宿舍
        # "G": 708227196

    }

    way = {
        "M": "send",
        "G": "group"
    }

    text = str(text)
    print("->【", text + ' 】')
    # return
    params1 = {
        "msg": text,
        "qq": qq[case],
    }

    # QQ推送
    url = "https://qmsg.zendee.cn/" + way[case] + "/d105a92ecd34dab1427db4dc4936e339"
    c = requests.get(url=url, params=params1)
    status = c.json()['success']
    print(status)

    if status is False:
        # coolPush推送
        # print(printLog.get_time("feedback"), "QQ推送失败，进入coolPush推送")
        text += "\nQQ推送失败！"
        t = requests.post("https://push.xuthus.cc/ww/ce4e2dfe9a211ca36f718441f089a88c", data=text.encode("utf-8"))
        status = t.json()['message']
        print(status)


# 获取cookie和验证码
def tryLogin():
    r = requests.get('http://xscfw.hebust.edu.cn/evaluate/verifyCode', stream=True)
    cookie = str(r.headers['Set-Cookie']).split(" ")[0]
    header['Cookie'] = cookie

    ocr = ddddocr.DdddOcr()
    res = ocr.classification(r.content)
    print("cookie:{}    verify:{}".format(cookie, res))
    r = requests.post("http://xscfw.hebust.edu.cn/evaluate/evaluate", headers=header,
                      data="username=xxxyhaolei&password=Haolei2021l19.&verifyCode=" + urllib.parse.quote(res))


# 使cookie生效 (登陆)
def login():
    tryLogin()
    # 登陆失败，一直重复
    while not isOk():
        tryLogin()


def getUrl():
    url = "http://xscfw.hebust.edu.cn/evaluate/survey/surveyStuList?id="
    a = datetime.datetime(2021, 11, 12)
    b = datetime.datetime.now()
    cc = (b - a).days
    listName = 712 + cc
    url += str(listName)
    return url


# 登陆成功后（cookie生效）获取原始信息
def getInfo(page):
    # 初始化参数
    global maxPage
    # 构造请求
    params = {
        "typeCX": 0,
        "pageNo": page,
        "classCX": "软件L194"
    }
    c = requests.post(url=getUrl(), params=params, headers=header).text

    # 获取maxPage数据
    index = str(c).find("maxPage")
    if index == -1:  # 无信息
        print("全部填报完成")
        maxPage = 0
    else:
        maxPage = int(c[index + 10])
    return c


def isOk():
    params = {
        "typeCX": 0,
        "pageNo": 1,
        "classCX": "软件L194"
    }
    c = requests.post(url=getUrl(), params=params, headers=header).text
    # 检查cookie
    if str(c).find("重新") != -1 or str(c).find("正确的用户名") != -1:
        print("登陆失败")
        return False
    print("登陆成功")
    return True


# 处理信息
def process(index):
    target = getInfo(index)
    try:
        soup = BeautifulSoup(target, 'html.parser')
        t = soup.tbody.get_text()
        # if t is None:
        #     return
        tt = str(t).split("未完成")
        tt.pop()

        for i in tt:
            sin = i.split("\n")[-6]
            set_name.add(sin)
            print(sin)
    except():
        pass


def generateMess():
    message = "以下同学赶紧填体温！！！\n"
    for e in set_name:
        message += e + "\n"

    for ee in set_name:
        message += " @at={}@ ".format(qq_dict[ee])
    feedback(message, "G")
    # print(message)


if __name__ == '__main__':
    login()
    for i in range(1, 100):
        print("-------------------")
        process(i)
        if i == maxPage or maxPage == 0:
            break
    generateMess()
