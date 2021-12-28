import os
import sys
import requests
from function import properties

path = properties.filepath

def recall(id):
    id = str(id)
    url = properties.IP + "/delete_msg?message_id=" + id
    print(url)
    a = requests.get(url)
    print(a.text)
    print('撤回成功')


def action():
    with open(path, 'r') as reader:
        numbers = reader.readlines()
        for number in numbers:
            number = str(number).replace("\n", "")
            print(number)
            recall(number)

    with open(path, 'w') as file:
        file.write("")
