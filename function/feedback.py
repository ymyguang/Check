import requests
import properties

IP = properties.IP
path = properties.filepath


def myPush(text, qq, case, is_record):
    s = text.replace(" @at=", "[CQ:at,qq=").replace("@", "]")
    url = IP + "/send_group_msg?group_id=" + str(qq) + "&message=" + str(s)
    try:
        a = requests.post(url=url)
        result = a.json()
        print(result)
        status = result['status']
        message_id = result['data']['message_id']
        message_id = str(message_id)
        if case == "G" and is_record:
            print("record")
            with open(path, 'a') as file:
                file.write(message_id + "\n")
        print("message_id:" + message_id)
        return status

    except Exception as e:
        print(e)
        return -1, e


def push_QQ(text, case, qq_o):
    # -1是请求异常
    # false是推送异常
    print("-- 进入QmsgPUSH --")
    if case == "M":
        qq = 2096304869
    else:
        qq = qq_o

    way = {
        "M": "send",
        "G": "group"
    }
    params1 = {
        "msg": text,
        "qq": qq,
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


def feedback(text, case='M', qq=0, is_record=True):
    text = str(text)
    print("->【", text + ' 】')
    flag = False

    # return
    if qq != 0:
        status = myPush(text, qq, case, is_record)
        if status == -1:
            print("请求失败---MyPush服务器异常")
            flag = True
        elif status != 'ok':
            print("推送失败，进入Qmsg推送")
            flag = True
        else:
            flag = False
            print("QQ推送成功")
    # return

    if flag or qq == 0:
        qq_status, e = push_QQ(text, case, qq)
        if qq_status == -1:
            print("请求失败---Qmsg服务器异常")
            flag = True
        elif qq_status is False:
            print("推送失败，进入coolPush推送")
            flag = True
        else:
            flag = False
            print("QQ推送成功")

        if flag:
            weChatPush(text, e)
    print("退出推送函数")