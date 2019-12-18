from web.model.Models import Attack
from web.model import AttackCount
from sqlalchemy import func, or_, and_, desc
import datetime
from web.utils.SituationAssessmentAlgorithms import *
from urllib.parse import unquote
from web.utils.SensitiveWordMatching import matchSensitiveWord
from web import db


# 根据攻击种类查找所有数据
def selectByAttackType(attackType):
    attack = Attack.query.filter(attackType=attackType).all()
    objects_list = []
    for i in attack:
        objects_list.append(i.to_json())
    return objects_list


# 查找来源地方最多的5个以及对应数量（所有）
def selectSourceAndCount():
    attack = Attack.query.with_entities(Attack.source, func.count(Attack.id).label('count')).group_by(Attack.source)\
        .order_by(desc('count')).limit(5)
    source = []
    count = []
    if AttackCount.selectSevenDayCnt() == 0:
        return []
    else:
        for i in attack:
            source.append(i.source)
            count.append(int(i.count)/AttackCount.selectSevenDayCnt())
        return [source, count]


# 查询出现最多的几个ip以及数量
def selectIpAndCount():
    attack = Attack.query.with_entities(Attack.ip, func.count(Attack.id).label('count')).group_by(Attack.ip).\
        order_by(desc('count')).limit(5)
    ip = []
    count = []
    for i in attack:
        ip.append(i.ip)
        count.append(int(i.count))
    return [ip, count]


# 查询最新的攻击orderby需要修改
def selectLatestAttack():
    attack = Attack.query.with_entities(Attack.time, Attack.ip, Attack.source, Attack.attackType, Attack.status)\
        .filter(Attack.attackType != 'normal').order_by(desc(Attack.time)).limit(3)
    objects_list = []
    for i in attack:
        json = [i.attackType, i.ip, i.time]
        objects_list.append(json)
    return objects_list


# 查询三天的攻击
def selectThreeDayAttack():
    endDate = datetime.datetime.now()
    beginDate = endDate-datetime.timedelta(days=1)
    attack = Attack.query.filter(and_(Attack.time >= beginDate, Attack.time <= endDate,
                                      Attack.attackType != "normal")).order_by(desc(Attack.time)).all()
    objects_list = []
    for i in attack:
        json = [i.id, i.time, i.attackType, i.ip, i.status, i.result]
        objects_list.append(json)
    return objects_list


# 根据id搜寻详细信息
def selectAttackDetailsById(attack_id):
    attack = Attack.query.filter_by(id=attack_id).first()
    json = {
        'id': attack.id,
        'attackType': attack.attackType,
        'ip': attack.ip,
        'source': attack.source,
        'status': attack.status,
        'time': attack.time,
        'details': attack.details
    }
    return json

# 多维关联


# 搜索
def selectSearchHistory(label):
    attack = Attack.query.filter(
        or_(Attack.attackType.like("%"+label+"%"),
            Attack.source.like("%"+label+"%"),
            Attack.ip.like("%"+label+"%"))
    ).all()
    objects_list = []
    for i in attack:
        json = {
            'id': i.id,
            'attackType': i.attackType,
            'ip': i.ip,
            'source': i.source,
            'status': i.status,
            'time': i.time,
            'details': i.details
        }
        objects_list.append(json)
    return objects_list


# 搜索所有
def selectSearchResult(label):
    attack = Attack.query.filter(or_(
        Attack.attackType.like("%"+label+"%"),
        Attack.result.like("%"+label+"%"),
        Attack.executor.like("%"+label+"%"),
        Attack.status.like("%"+label+"%")
    ))
    objects_list = []
    for i in attack:
        json = {
            'attackType': i.attackType,
            'result': i.source,
            'status': i.status,
            'executor': i.executor
        }
        objects_list.append(json)
    return objects_list


# 30天 最多的20条ip以及数量
def attackSourceIp():
    end_date = datetime.datetime.now()
    begin_date = end_date - datetime.timedelta(days=30)
    attack = Attack.query.with_entities(func.count(Attack.id).label('count'), Attack.ip).filter\
        (and_(Attack.time >= begin_date, Attack.time <= end_date, Attack.attackType.notin_(['normal', 'anomalous']))).\
        group_by(Attack.ip).order_by(desc("count")).limit(20)
    ip = []
    count = []
    for i in attack:
        ip.append(i.ip)
        count.append(int(i.count))
    objects_list = list()
    objects_list.append(ip)
    objects_list.append(count)
    return objects_list


# 30天内攻击的数量
def selectSevenDayIpCount():
    end_date = datetime.datetime.now()
    begin_date = end_date - datetime.timedelta(days=7)
    attack = Attack.query.with_entities(Attack.ip, func.count(Attack.id).label("count")).filter(
        and_(Attack.time >= begin_date, Attack.time <= end_date, Attack.attackType.notin_(['normal', 'anomalous'])))\
        .group_by(Attack.ip).order_by(desc("count")).limit(5)

    if attack.count is None:
        return []
    else:
        ip = list()
        count = list()
        for i in attack:
            ip.append(i.ip)
            if AttackCount.selectSevenDayAttackCnt() != 0:
                count.append(int(i.count)/AttackCount.selectSevenDayAttackCnt())
            else:
                count.append(0)
        return [ip, count]


def attackSourceIpTime(beginDate, endDate):
    endDate = datetime.datetime.strptime(endDate, "%Y-%m-%dT%H:%M").strftime("%Y-%m-%d %H:%M:%S")
    beginDate = datetime.datetime.strptime(beginDate, "%Y-%m-%dT%H:%M").strftime("%Y-%m-%d %H:%M:%S")
    attack = Attack.query.with_entities(func.count(Attack.id).label('count'), Attack.ip)\
        .filter(and_(Attack.time >= beginDate, Attack.time <= endDate, Attack.attackType.notin_(['normal', 'anomalous'])
                     )).group_by(Attack.ip).order_by(desc("count")).limit(20)
    ip = []
    count = []
    for i in attack:
        ip.append(i.ip)
        count.append(int(i.count))
    objects_list = list()
    objects_list.append(ip)
    objects_list.append(count)
    return objects_list


def attackSource(beginDate, endDate):
    end_date = datetime.datetime.strptime(endDate, "%Y-%m-%dT%H:%M").strftime("%Y-%m-%d %H:%M:%S")
    begin_date = datetime.datetime.strptime(beginDate, "%Y-%m-%dT%H:%M").strftime("%Y-%m-%d %H:%M:%S")
    attack = Attack.query.with_entities(func.count(Attack.id).label('count'), Attack.source) \
        .filter(and_(Attack.time >= begin_date, Attack.time <= end_date)).group_by(Attack.source).order_by(
        desc("count")).limit(5)
    objects_list = []
    for i in attack:
        json = {
            'name': i.source,
            'value': int(i.count)
        }
        objects_list.append(json)
    return objects_list


def selectLatestAttackInfo():
    attack = Attack.query.with_entities(Attack.time, Attack.ip, Attack.source, Attack.attackType, Attack.status)\
        .order_by(desc(Attack.time)).limit(5)
    objects_list = []
    for i in attack:
        list_one = [i.time, i.ip, i.attackType, w[i.attackType]]
        objects_list.append(list_one)
    return objects_list


def historyAttack():
    attack = Attack.query.with_entities(Attack.attackType, Attack.details).order_by(desc(Attack.time)).limit(100)
    objects_list = []
    for i in attack:
        attacktype = i.attackType
        detail = i.details.split('?')
        if len(detail) == 1:
            continue
        else:
            objects_list.append(attacktype)
            objects_list.append(detail[1])
    return objects_list


# 用户行为分析
def selectAllById(id):
    end_date = datetime.datetime.now()
    begin_date = end_date - datetime.timedelta(days=1)
    attack = Attack.query.with_entities(Attack.attackType, Attack.ip, Attack.time, Attack.details).\
        filter(Attack.id == id).first()
    json = [attack.attackType, attack.ip, attack.time]
    if len(attack.details.split('?')) == 1:
        json.append([])
    else:
        json.append(matchSensitiveWord(attack.details.split('?')[1]))
    json.append(unquote(attack.details))
    att = Attack.query.with_entities(Attack.attackType, Attack.time, Attack.details).filter(and_(
       Attack.ip == attack.ip, Attack.time < end_date, Attack.time > begin_date)).all()
    for i in att:
        js = [i.attackType, i.time, unquote(i.details)]
        json.append(js)
    # 一句话的分析
    
    return json


def selectAttackCount():
    end_date = datetime.datetime.now()
    begin_date = end_date - datetime.timedelta(minutes=2)
    attack = Attack.query.with_entities(func.count(Attack.id).label('count')).filter(and_(
        Attack.attackType != 'normal', Attack.time < end_date, Attack.time > begin_date)).first()
    return attack.count


# 修改审核结果
def updateAttackResult(id, result):
    attack = Attack.query.filter(Attack.id == id).first()
    attack.status = '已审核'
    attack.result = result
    db.session.commit()
    return "successfully"


# 输出所有异常请求
def detectResult():
    endDate = datetime.datetime.now()
    beginDate = endDate - datetime.timedelta(days=1)
    attack = Attack.query.filter(and_(Attack.attackType == 'anomalous',
                                      Attack.time >= beginDate, Attack.time <= endDate)).all()
    object_list = []
    for i in attack:
        json = {
            'id': i.id,
            'result': i.result
        }
        object_list.append(json)
    return object_list
