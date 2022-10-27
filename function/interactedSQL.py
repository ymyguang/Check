import pymysql
import datetime

conn = pymysql.connect(host='49.233.159.179', user='vip_kuan', passwd='XPcd7tbFNc3HeDNy',
                       db='vip_kuan', charset='utf8')
cursor = conn.cursor()


def insert_people(id, _class, _name):
    sql = """INSERT INTO vip_kuan.liujia (`id`,`class`,`name`,`time`) 
    VALUE ('{}','{}','{}', NOW() )
    """.format(id, _class, _name)
    cursor.execute(sql)
    conn.commit()


def getPeopleByTime(start, end, num):
    sql = """SELECT `class` ,`name`,COUNT(`name`)
FROM liujia
WHERE `time` BETWEEN "{}" AND "{}"
GROUP BY `name`
ORDER BY COUNT(`name`) DESC
LIMIT 0,{}""".format(start, end, num)
    print(sql)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


# 获取按照时间倒序排列的人员
def getNumberPeople(date):
    # 前一天
    preDate = date - datetime.timedelta(days=1)
    preDate = preDate.strftime('%Y-%m-%d 15:59:00')
    sql = '''SELECT `class` ,`name`
FROM liujia
where `time` between "{}" and "{}"
    '''.format(preDate, date)
    print(sql)
    cursor.execute(sql)
    nameSet = set()
    result = cursor.fetchall()

    if result is not None:
        for i in result:
            nameSet.add(i[0] + "|" + i[1])
    nameSet = list(nameSet)
    nameSet.sort(reverse=True)
    return nameSet


def getOrderClass(start, end):
    sql = """SELECT `class` ,COUNT(`class`)
    FROM liujia
    WHERE `time` BETWEEN "{}" AND "{}"
    GROUP BY `class`
    ORDER BY COUNT(`class`) DESC""".format(start, end)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def truncateTable(data):
    sql = "delete from liujia where `time` < '{}'".format(data)
    cursor.execute(sql)
    conn.commit()


def close_sql():
    conn.close()
