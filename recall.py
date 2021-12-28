import requests
import feedback

def recall(id):
    id = str(id)
    url = feedback.IP + "/delete_msg?message_id=" + id
    print(url)
    a = requests.get(url)
    print(a.text)


if __name__ == '__main__':
    with open("message_id.ini", 'r') as reader:
        numbers = reader.readlines()
        for number in numbers:
            number = str(number).replace("\n", "")
            print(number)
            recall(number)

    with open('message_id.ini', 'w') as file:
        file.write("")