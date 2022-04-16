import datetime
from function import interactedSQL
from function import feedback
import properties

if __name__ == '__main__':
    targetQQ = properties.targetQQ
    now = datetime.date.today() + datetime.timedelta(days=1)
    pre_date = now - datetime.timedelta(days=7)

    result = interactedSQL.getPeopleByTime(pre_date, now, 10)
    message = "★本周被提醒数排行榜★\n==================\n"
    for _ in result:
        message += _[0] + "" + "-" + _[1] + "-----" + str(_[2]) + "次\n"

    feedback.feedback(message, "G", qq=targetQQ)
