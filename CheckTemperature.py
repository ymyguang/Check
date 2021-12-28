import datetime
import urllib.parse
from datetime import datetime as da
import time
from math import ceil
import feedback
import ddddocr
import requests
from bs4 import BeautifulSoup


targetQQ = 708227196
targetQQ = str(targetQQ)

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
    "宇文可豪": 1625290298,
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


def getId():
    c = requests.get("http://xscfw.hebust.edu.cn/evaluate/survey/surveyList", headers=header).text
    soup = BeautifulSoup(c, 'html.parser')
    now = da.now()
    current_time = now.strftime("%Y年%m月%d日健康日报")
    for tr in soup.findAll('tbody')[0].findAll('tr'):
        res = tr.a
        if current_time == res['title']:
            Lid = res['href']
            print(res['title'], "->", Lid)
            return 'http://xscfw.hebust.edu.cn/evaluate/survey/' + Lid


# 登陆成功后（cookie生效）获取原始信息
def getInfo(page):
    # 初始化参数
    global maxPage
    # 构造请求
    params = {
        "typeCX": 0,  # 未完成0，已完成1
        "pageNo": page,
        "classCX": "软件L194"  # 班级号
    }
    c = requests.post(url=getId(), params=params, headers=header).text

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
        if soup.tbody is None:
            return
        t = soup.tbody.get_text()
        tt = str(t).split("未完成")
        tt.pop()

        for i in tt:
            sin = i.split("\n")[-6]
            set_name.add(sin)
            print(sin)
    except():
        pass


def generateMess():
    pageNum = 8  # at的总个数
    f = 0
    if len(set_name) == pageNum:
        return
    message = "叮叮叮，赶紧填体温📣📣📣 \n"
    totalPage = str(ceil(len(set_name) / pageNum))
    currentPage = 1
    for e in set_name:
        f += 1  # 记录本次推送at的个数
        message += e + " "
        message += " @at={}@ \n".format(qq_dict[e])
        if f % pageNum == 0:  # 满足一页的个数，就推送
            message += "\n🌻🌻【第{}页，共{}页】🌻🌻".format(str(currentPage), totalPage)
            currentPage += 1
            feedback.feedback(message, "G", qq=targetQQ)
            message = '叮叮叮，赶紧填体温📣📣📣 \n'
            time.sleep(6)  # 5秒内不能连续推送
    if f % pageNum != 0:  # 不是pageNum倍数的情况
        message += "\n🌻🌻【第{}页，共{}页】🌻🌻".format(str(currentPage), totalPage)
        feedback.feedback(message, "G", qq=targetQQ)


if __name__ == '__main__':
    print("\n")
    print(da.now())
    print("------------------------------------------------")
    login()
    for i in range(1, 100):
        print("################################################")
        process(i)
        if i == maxPage or maxPage == 0:
            break
    generateMess()
    print("------------------------------------------------")

    # i = 0
    # for e in qq_dict:
    #     i += 1
    #     if i > 13:
    #         break
    #     else:
    #         set_name.add(e)
    # print(len(set_name))
    # print(set_name)
    # generateMess()
