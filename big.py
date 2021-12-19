from datetime import datetime
import datetime as da
import re

import requests
import ddddocr

l = []
s = set()
total = 35
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

Leader = {
    '李晨': [
        "康兴旺",
        "刘彪",
        "李晨",
        "李樊",
        "刘明一",
        "杨翔宇"
    ],
    "张稳": [
        "张稳",
        "赵伟",
        "章传喜",
        "曹骏",
        "郭楠",
    ],
    '苏世超': [
        "苏世超",
        "刘旭辉",
        "李佳林",
    ],
    "揣星宇": [
        "揣星宇",
        "郝梦畅",
        "李可欣",
    ],
    "邢梓阳": [
        "邢梓阳",
        "王鑫",
        "徐晓杰",
        "徐雪彬",
        "王湜裕",
        "杨宇哲",

    ],
    "罗琦": [
        "罗琦",
        "李兆林",
        "李昂",
        "刘善宝",
        "吕天乐",
        "李江楠",
    ],
    "蔡思琦": [
        "辛宇航",
        "蔡思琦",
        "吴卫",
        "高世豪",
        "宇文可豪"
    ],
    "李尚恒": [
        "李尚恒",
    ]
}


def getVerify(r):
    ocr = ddddocr.DdddOcr()
    res = ocr.classification(r.content)
    return res


def getToken():
    status = "aa"
    c = None
    print("Try to get token")
    f = False
    while status != "success":
        if f:
            print(status, '正在重试')
        r = requests.get('https://bgapi.54heb.com/login/verify', stream=True)
        cookieSet = vars(r.request)["_cookies"]
        cookieSet = str(cookieSet).split(",")
        c = re.findall(r'\w*?=.*?\s', str(r.cookies))
        c = str(c[0]).replace(" ", ";")

        cookie = c
        for i in cookieSet:
            c = re.findall(r'\w*?=.*?\s', i)
            c = str(c[0]).replace(" ", ";")
            cookie += c

        header = {
            "cookie": cookie
        }
        verify = getVerify(r)
        par = {"account": "2096304869@qq.com", "pass": "beff06", "verify": verify, "is_quick": 0}
        c = requests.post("https://bgapi.54heb.com/admin/login", headers=header, params=par)
        status = c.json()['msg']
        f = True

    return c.json()['data'][0]["token"]


def push_QQ(text, case):
    # -1是请求异常
    # false是推送异常
    print("-- 进入QmsgPUSH --")

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
    params1 = {
        "msg": text,
        "qq": qq[case],
    }
    url = "https://qmsg.zendee.cn/" + way[case] + "/d105a92ecd34dab1427db4dc4936e339"

    try:
        c = requests.get(url=url, params=params1)
        status = c.json()['success']
        print(status)
        return status, c.text
    except Exception as e:
        print(e)
        return -1, e


def weChatPush(text, e):
    print("-- 进入WeCharPUSH --")
    text = "QQ推送失败\n" + "异常信息：" + str(e) + "\n" + text
    text = str(text)
    t = requests.post("https://push.xuthus.cc/ww/ce4e2dfe9a211ca36f718441f089a88c", data=text.encode("utf-8"))
    status = t.json()['message']
    print(status)


def feedback(text, case='M'):
    print("->【", text + ' 】')
    flag = False
    # return
    # text = "[测试]\n" + text
    qq_status, e = push_QQ(text, case)
    if qq_status == -1:
        print("请求失败---Qmsg服务器异常")
        flag = True
    elif qq_status is False:
        print("推送失败，进入coolPush推送")
        flag = True
    else:
        print("QQ推送成功")

    if flag:
        weChatPush(text, e)


def originInfo():
    url = 'https://bgapi.54heb.com/regiment?page=1&rows=100&keyword=&oid=100475653&leagueStatus=&goHomeStatus=&memberCardStatus=&isPartyMember=&age_type=&ageOption=&isAll='
    header = {'Accept': 'application/json, text/plain, */*',
              'Accept-Encoding': 'gzip, deflate,br',
              'Accept-Language': 'zh-CN,zh;q=0.9',
              'Cache-Control': 'no-cache',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
              'token': getToken(),
              }

    soup = requests.get(url, headers=header)
    # print(soup.json())
    if soup.json()['msg'] != 'success':
        print(soup.json()['msg'])
        feedback(soup.json()['msg'])
        exit()

    for sa in soup.json()['data']['data']:
        if sa['isStudy'] != "是":
            # print(sa['realname'])
            if sa['realname'] != '周超':
                l.append(sa['realname'])


def processInfo():
    if len(l) == 0:
        print("大学习已全部完成！")
    else:
        now = datetime.now()
        # now = now - da.timedelta(hours=2)
        current_time = now.strftime("%m月%d日 %H时%M分")
        message = "截止至[{}]".format(current_time)
        message += "\n大学习未完成（无记录）名单：\n"
        conut = 0
        for i in l:
            conut += 1
            message += str(conut) + "." + i + "\n"

        message += "\n请以上{}位同学抓紧（重新）学习！\n".format(
            str(conut))

        # At people
        for people in l:
            for leader in Leader:
                if people in leader:
                    s.add(leader)
                    print(leader)

        for ii in s:
            message += " @at={}@ ".format(qq_dict[ii])
        message += "\n请宿舍长们及时督促！"
        feedback(message, "G")


if __name__ == '__main__':
    print("\n")
    print(datetime.now())
    print("------------------------------------------------")
    originInfo()
    processInfo()
    print("------------------------------------------------")
