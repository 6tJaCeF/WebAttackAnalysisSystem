from flask_mail import Message
from web import mail, app
import datetime
from web.model.Models import AttackCnt
from sqlalchemy import func, and_
from web.utils.SituationAssessmentAlgorithms import calculate_All


def sendEmail(message):
    with app.app_context():
        msg = Message('Attention Please!', sender='3022489608@qq.com',
                      recipients=['15858294046@163.com'])
        msg.body = message
        mail.send(msg)


def detectionWarning():
    endDate = datetime.datetime.now().strftime("%Y-%m-%d %H")
    beginDate = (datetime.datetime.strptime(endDate, "%Y-%m-%d %H") - datetime.timedelta(days=3)).strftime(
        "%Y-%m-%d %H")
    attackCnt = AttackCnt.query.with_entities(AttackCnt.attackType, func.sum(AttackCnt.count).label("count")).filter(
        and_(AttackCnt.time >= datetime.datetime.strptime(beginDate, "%Y-%m-%d %H"),
             AttackCnt.time <= datetime.datetime.strptime(endDate, "%Y-%m-%d %H"))). \
        group_by(AttackCnt.attackType).all()
    li = dict()
    for i in attackCnt:
        li[i.attackType] = int(i.count)
    situation = calculate_All(li)
    if situation < 60:
        message = '当前的系统的态势值为'+str('%.2f' %situation)+'\n在 '+beginDate+'点'+'--'+endDate +'点'+ '发生了\n'
        for i in attackCnt:
            message += str(int(i.count))+'次  '+i.attackType+'\n'
        message += '请登录系统进行查看'
        sendEmail(message)
    else:
        print('----')


# def executeDetection():
#     job = {
#         'id': 'job01',  # 任务的唯一ID，不要冲突
#         'func': 'detectionWarning',  # 执行任务的function名称
#         'args': '',  # 如果function需要参数，就在这里添加
#     }
#     result = scheduler.add_job(func=__name__+':'+job['func'], id=job['id'], trigger='interval', seconds=5, replace_existing=True)
#     print(result)
