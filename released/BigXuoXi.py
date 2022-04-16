from datetime import datetime
import re
import requests
import ddddocr

# 在下方输入登陆账号密码
username = "2096304869@qq.com"
password = "beff06"


# -----------------下方代码非必要时，无需更改！-----------------
l = []
total = None
oid = None
name = None
orgname = None
token = None
header = {'Accept': 'application/json, text/plain, */*',
          'Accept-Encoding': 'gzip, deflate,br',
          'Accept-Language': 'zh-CN,zh;q=0.9',
          'Cache-Control': 'no-cache',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
          'token': token
          }


def getVerify(r):
    print("正在识别验证码")
    ocr = ddddocr.DdddOcr()
    res = ocr.classification(r.content)
    print("当前验证码:{}，尝试登陆".format(res))
    return res


def getToken():
    global name
    global orgname
    global token
    status = "FIRST"
    c = None
    # print("Try to get token")
    f = False
    while status != "success":
        if f:
            print(status, '正在重试')
        r = requests.get('https://bgapi.54heb.com/login/verify', stream=True)

        print(vars(r.request))
        exit()
        cookieSet = vars(r.request)["_cookies"]
        cookieSet = str(cookieSet).split(",")
        c = re.findall(r'\w*?=.*?\s', str(r.cookies))
        c = str(c[0]).replace(" ", ";")

        cookie = c
        for i in cookieSet:
            c = re.findall(r'\w*?=.*?\s', i)
            c = str(c[0]).replace(" ", ";")
            cookie += c

        _header = {
            "cookie": cookie
        }

        verify = getVerify(r)
        par = {"account": username, "pass": password, "verify": verify, "is_quick": 0}
        c = requests.post("https://bgapi.54heb.com/admin/login", headers=_header, params=par)
        status = c.json()['msg']
        f = True
    print("登陆成功\n------------------------")
    # print(c.json())
    req = c.json()['data'][0]
    name = req['username']
    orgname = req["orgname"]
    token = c.json()['data'][0]["token"]


def originInfo():
    global total
    global oid
    url = 'https://bgapi.54heb.com/regiment?page=1&rows=100&keyword=&oid=' + str(oid)

    soup = requests.get(url, headers=header)
    total = soup.json()['data']['total']

    # print(soup.json())
    print("管理员姓名：{}\n团组织：{}\n总人数：{}人\n------------------------".format(name, orgname, total))

    for sa in soup.json()['data']['data']:
        if sa['isStudy'] != "是":
            l.append(sa['realname'])


# def processInfo():
#     if len(l) == 0:
#         print("大学习已全部完成！")
#     else:
#         # 构造消息内容
#         content = []
#         for leader in Leader:
#             non_ok = 0
#             info = {'len': 0, 'leader': leader, 'index': str(Leader.get(str(leader))[-1]['number']), "member": []}
#             for people in l:
#                 if people in Leader.get(leader):
#                     info['member'].append(people)
#                     non_ok += 1
#             if len(info['member']) != 0:
#                 info['len'] = non_ok  # 没有完成的人数
#                 content.append(info)
#         print(content)
#
#         now = datetime.now()
#         current_time = now.strftime("%m月%d日 %H时%M分")
#         message = "截止至[{}]".format(current_time)
#         message += "\n大学习未完成（无记录）名单：\n-----------------------\n"
#         content.sort(key=compLen)
#         member = ""
#         # return
#
#         # 生成名单
#         for i in content:
#             member += "【" + str(i.get('index')) + "】宿舍长:" + i.get("leader") + "\n"
#             for r in i.get('member'):
#                 member += "->" + r + "\n"
#
#             member += " @at={}@ ".format(
#                 qq_dict[str(i.get('leader'))]) + "\n\n"
#         message += member
#         message += "共计{}个\n".format(len(l))
#         message += "-----------------------\n请宿舍长们及时督促！"
#         print(message)
#         # recall.action()
#         # feedback.feedback(message, "G", qq=targetQQ)


def setOrgInfo():
    global oid
    header['token'] = token
    r = requests.get("https://bgapi.54heb.com/organization/getOrganizeMess", headers=header)
    req = r.json()['data']
    # print(req)
    oid = req['id']
    # print(r.json())


if __name__ == '__main__':
    print("当前账号：{}\n当前密码:{}".format(username, password))
    getToken()
    setOrgInfo()
    originInfo()
    # processInfo()
    input("------------------------\n查询结束，按任意键退出")
