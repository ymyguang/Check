import datetime
import os
import re
import sys
import urllib.parse
from datetime import datetime as da
import time
from math import ceil
import ddddocr
import requests
from bs4 import BeautifulSoup
from function import feedback, recall
import properties
from function import interactedSQL

targetQQ = properties.targetQQ
qq_dict = properties.qq_dict
condition = properties.condition
_name = []
# 键：学号； 值：姓名
_map = {}

maxPage = 99

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
    user = properties.user
    password = properties.password
    r = requests.get('http://xscfw.hebust.edu.cn/evaluate/verifyCode', stream=True)
    cookie = str(r.headers['Set-Cookie']).split(" ")[0]
    header['Cookie'] = cookie

    ocr = ddddocr.DdddOcr()
    res = ocr.classification(r.content)
    print("cookie:{}    verify:{}".format(cookie, res))
    r = requests.post("http://xscfw.hebust.edu.cn/evaluate/evaluate", headers=header,
                      data="username={}&password={}&verifyCode=".format(user, password) + urllib.parse.quote(res))


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
    now = da.now()
    if os.name == 'posix':
        print("Linux格式")
        current_time = now.strftime("%Y-%-m-%-d")  # Linux获取时间
    else:
        print("Windows格式")
        current_time = now.strftime("%Y-%#m-%#d")

    # current_time = '2022-3-30'
    c = requests.post("http://xscfw.hebust.edu.cn/evaluate/survey/surveyList", headers=header,
                      data="surveyCX=" + str(
                          current_time) + "%E5%81%A5%E5%BA%B7%E6%97%A5%E6%8A%A5&typeCX=-1&pageNo=1").text
    soup = BeautifulSoup(c, 'html.parser')
    current_time += "健康日报"
    for tr in soup.findAll('tbody')[0].findAll('tr'):
        res = tr.a
        try:
            if current_time in res['title']:
                Lid = res['href']
                print(res['title'], "->", Lid)
                return 'http://xscfw.hebust.edu.cn/evaluate/survey/' + Lid
        except Exception as e:
            print("提取数据时，产生异常")
            print(e)


# 登陆成功后（cookie生效）获取原始信息
def getInfo(page):
    # 初始化参数
    global maxPage
    # 构造请求
    params = {
        "typeCX": 0,  # 未完成0，已完成1
        "pageNo": page,
        # "classCX": "软件L194"  # 班级号
    }
    c = requests.post(url=getId(), params=params, headers=header).text
    # print(c)
    # 获取maxPage数据
    index = str(c).find("maxPage")
    if index == -1:  # 无信息
        print("全部填报完成")
        maxPage = 0
    else:
        maxPage = re.findall(r'var maxPage = (.*);', c)[0]
        # print(maxPage)
        # maxPage = 1
    return c


# 登陆验证
def isOk():
    params = {
        "typeCX": 0,  # 未完成0，已完成1
        "pageNo": 0,
        "classCX": "电信L201"  # 班级号
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

        for _ in tt:
            _ = _.split("\n")
            sin = _[-6]  # 姓名
            _name.append(sin)
            number = _[-7]  # 学号
            _grade = _[-5]
            _class = _[-2]
            # 没有条件直接加入字典
            if condition is None:
                if _class not in _map.keys():
                    _map[_class] = []
                _map[_class].append({'name': sin, 'number': number})
            # 有条件-> 判断班级类别
            else:
                if _grade == condition:
                    if _class not in _map.keys():
                        _map[_class] = []
                    _map[_class].append({'name': sin, 'number': number})
            # print(number,sin)
    except():
        pass


# 学号判断QQ
def getQQ(name, number):
    QQ = None
    if number in qq_dict:
        QQ = qq_dict[number]
    if QQ is not None:
        return " @at={}@ \n".format(QQ)
    else:
        return "(找不到对应QQ,请班委督导)\n"


def generateMess():
    if len(_map) == 0:
        return
    material = []
    material_len = 0
    pageNum = 80  # at的总个数
    for _ in _map:
        material.append(_ + "班")
        for i in _map.get(_):
            material.append(str(i['name'] + "|" + i['number']))
            material_len += 1

    # print(material)
    f = 0
    currentPage = 1
    message = '以下同学抓紧时间填报体温~'
    totalPage = str(ceil(material_len / pageNum))
    for elem in material:
        if '班' in elem:
            message += "\n■【" + elem + '】\n'
            flag = 0
        else:
            flag = 1
            f += 1
            t = elem.split("|")
            name = t[0]
            number = t[1]
            message += "➩" + name + getQQ(name, number)

        if f % pageNum == 0 and flag == 1:  # 满足一页的个数，就推送
            message += "\n【第{}页，共{}页】--共{}人".format(
                str(currentPage),
                totalPage,
                material_len)
            currentPage += 1
            feedback.feedback(message, "G", qq=targetQQ)
            time.sleep(10)
            # message = '以下同学抓紧时间填报体温~\n----------------------\n'
            message = ''

    if f % pageNum != 0:  # 不是pageNum倍数的情况
        message += "\n【第{}页，共{}页】--共{}人".format(
            str(currentPage),
            totalPage,
            material_len)
        feedback.feedback(message, "G", qq=targetQQ)
    # 生成最后10人

    date = datetime.date.today()
    lastPeople = interactedSQL.getNumberPeople(date)
    # 若找到就生成
    if lastPeople:
        message_pro = "\n\n============\n【昨日16:00后填报体温名单：】\n"
        for _ in lastPeople:
            _ = _.split("|")
            message_pro += "★" + _[0] + "班" + '-' * 2 + _[1] + "★\n"
    else:
        message_pro = "\n昨日没有16:00之后才填报的同学!!!\n大 家 继 续 保 持！"
    feedback.feedback("填写地址：http://xscfw.hebust.edu.cn/survey/index.action{}".format(message_pro),
                      "G", qq=targetQQ)


if __name__ == '__main__':
    print("\n")
    print(da.now())
    print("------------------------------------------------")
    login()
    for i in range(1, 100):
        print("################################################")
        process(i)
        print("第{}页，处理完成".format(i))
        if i == maxPage or maxPage == 0:
            break
    print("------------------------------------------------")
    print("未填报同学{}个".format(len(_name)))

    # exit()
    a = sys.argv[-1]
    print(a)
    if a == "check":
        if len(_map) == 0:
            day = datetime.datetime.now().date()
            day = str(day) + "\n"
            with open("./flag.txt", 'r') as reader:
                numbers = reader.readlines()
                flag = str(numbers[-1])
                reader.close()
            print("day:{}flag:{}".format(day, flag))
            if day != flag:
                print("进入通知")
                recall.action()
                feedback.feedback("全部填写完成(此消息自动发送，无需回复)   @at={}@".format(properties.teacher), "G", qq=targetQQ)
                # 通知完成后，写入标记。防止通知失败情况下，直接写入，导致的无消息提醒。
                with open("./flag.txt", 'w') as reader:
                    reader.write(str(day))
                    print("写入完毕：{}".format(day))
                    reader.close()
            else:
                print("今日已推送")
        else:
            print("未填报完成")
    else:
        recall.action()
        generateMess()
        # 插入数据
        for _class in _map:
            for _ in _map[_class]:
                interactedSQL.insert_people(_['number'], _class, _['name'])
        print("写入结束")
        interactedSQL.close_sql()
