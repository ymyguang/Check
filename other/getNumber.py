import requests

url = "https://qun.qq.com/cgi-bin/qun_mgr/search_group_members"

_str = ""


def get_number(st, end):
    global _str
    payload = "gc=648341697&st={}&end={}&sort=0&bkn=453683140".format(st, end)
    headers = {
        'authority': 'qun.qq.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'dnt': '1',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://qun.qq.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://qun.qq.com/member.html',
        'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'cookie': 'RK=L7eZ/GhBdz; ptcz=681493a35d38a930654dc71ba68c570a58f0aff7d71246480b6c60d50db4be96; pgv_pvid=2213971315; o_cookie=2096304869; pac_uid=1_2096304869; _qpsvr_localtk=0.9164633277508019; uin=o1668558792; skey=@F0OiUWTDM; p_uin=o1668558792; pt4_token=elbP2dmaOY6Mk2QfmLM7bvazpNhG6gmdTGYl7lVpGWc_; p_skey=yl1ky2U5gpjnHTpwhVdCL-v8rJm1ZJDE3G7agIEudDw_; traceid=4c1969c4f9'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    user_dict = eval(str(response.text).replace("null", "None"))
    men = user_dict['mems']
    for element in men:
        # print(element)
        print(element['card'], element['uin'])


if __name__ == '__main__':
    for i in range(0, 515, 21):
        st = i
        end = i + 20
        if end > 515:
            end = 515
        get_number(st, end)
