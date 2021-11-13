import datetime

import requests
from bs4 import BeautifulSoup

set_name = set()
maxPage = 99


def post(page=1):
    # 初始化参数
    global maxPage
    url = "http://xscfw.hebust.edu.cn/evaluate/survey/surveyStuList?id="
    a = datetime.datetime(2021, 11, 12)
    b = datetime.datetime.now()
    c = (b - a).days
    listName = 712 + c
    url += str(listName)

    # 构造请求
    params = {
        "typeCX": 0,
        "pageNo": page,
        "classCX": "软件L194"
    }
    header = {
        "Cookie": "JSESSIONID=DB7A2301B0FE253C24734FC2218CC770; JSESSIONID=FBBFF38A51E403C4A8396F5B65D9303D"
    }
    c = requests.post(url=url, params=params, headers=header).text

    # 检查cookie
    if str(c).find("重新") != -1:
        print("Cookie失效")
        exit()

    # 获取maxPage数据
    index = str(c).find("maxPage")
    if index == -1:  # 无信息
        print("全部填报完成")
        maxPage = 0
    else:
        maxPage = int(c[index + 10])
    return c


def process(index):
    target = post(index)
    try:
        soup = BeautifulSoup(target, 'html.parser')
        t = soup.tbody.get_text()
        tt = str(t).split("未完成")
        tt.pop()

        for i in tt:
            sin = i.split("\n")[-6]
            set_name.add(sin)
            print(sin)
    except():
        pass


if __name__ == '__main__':

    for i in range(1, 100):
        print("-------------------")
        process(i)
        if i == maxPage or maxPage == 0:
            break
