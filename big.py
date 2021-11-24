from datetime import datetime
import datetime as da
import re

import requests
import ddddocr

l = []

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
    # print(printLog.get_time("feedback"), "推送目标QQ:{}".format(str(qq[case])))
    status = c.json()['success']
    # print(printLog.get_time("feedback"), "QQ推送状态：{},详情：{}".format(c.json()['success'], c.json()['reason']))
    print(status, c.json()['reason'])

    # QQ推送失败
    if status is False:
        # coolPush推送
        print("QQ推送失败，进入coolPush推送")
        t = requests.post("https://push.xuthus.cc/ww/ce4e2dfe9a211ca36f718441f089a88c", data=text.encode("utf-8"))
        status = t.json()['message']
        flag = str(status).find("等待执行")

        # coolPush推送失败
        if flag == -1:

            # server酱推送
            print("coolPush推送失败 -> 当前已进入Server酱推送")
            params = {
                "title": text,
            }
            s = requests.get(url="https://sctapi.ftqq.com/SCT33679Td3sATvBjES3VjKQeZgcsbxeB.send", params=params)
            print(s.json()['message'])

            # Server酱推送失败
            if str(s.json()['message']).find("超过当天的发") != -1:
                # 最后推送
                print("Server酱推送失败，执行最后coolPush推送")
                t = requests.post("https://push.xuthus.cc/ww/ce4e2dfe9a211ca36f718441f089a88c",
                                  data=text.encode("utf-8"))
                status = t.json()['message']
                print("coolPush推送状态（最终状态）:", status)
        else:
            print("coolPush通道推送成功")
    else:
        print("QQ通道推送成功")


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
        for ii in l:
            message += " @at={}@ ".format(qq_dict[ii])
        feedback(message, "G")


if __name__ == '__main__':
    print("\n")
    print(datetime.now())
    print("------------------------------------------------")
    originInfo()
    processInfo()
    print("------------------------------------------------")
