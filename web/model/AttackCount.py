from web.model.Models import AttackCnt
from sqlalchemy import func, and_, desc
import datetime
from web.utils import SituationAssessmentAlgorithms


# 查询所有数量
def selectAllAttackCount():
    attackCnt = AttackCnt.query.with_entities(AttackCnt.attackType, func.sum(AttackCnt.count).label("count"))\
        .group_by(AttackCnt.attackType).all()
    objects_list = []
    for i in attackCnt:
        json = {
            "value": int(i.count),
            "name": i.attackType
        }
        objects_list.append(json)
    return objects_list


# 查询给定时间攻击数量
def selectAllAttackCountTime(beginDate, endDate):
    attackCnt = AttackCnt.query.with_entities(AttackCnt.attackType, func.sum(AttackCnt.count).label("count")) \
        .filter(and_(AttackCnt.time > beginDate, AttackCnt.time < endDate)).group_by(AttackCnt.attackType).all()
    objects_list = []
    for i in attackCnt:
        json = {
            "value": int(i.count),
            "name": i.attackType
        }
        objects_list.append(json)
    return objects_list


# 查询给定时间数量
def selectAllCountTime(beginDate, endDate):
    end_date = datetime.datetime.strptime(endDate, "%Y-%m-%dT%H:%M").strftime("%Y-%m-%d %H:%M:%S")
    begin_date = datetime.datetime.strptime(beginDate, "%Y-%m-%dT%H:%M").strftime("%Y-%m-%d %H:%M:%S")
    attack = AttackCnt.query.with_entities(func.sum(AttackCnt.count).label("count")). \
        filter(and_(AttackCnt.attackType.notin_(['normal', 'anomalous']),
               AttackCnt.time >= begin_date,
               AttackCnt.time <= end_date)).first()
    if attack == (None,):
        attackCount = 0
    else:
        attackCount = int(attack.count)

    normal = AttackCnt.query.with_entities(func.sum(AttackCnt.count).label("count")). \
        filter(AttackCnt.attackType == 'normal', AttackCnt.time >= begin_date,
               AttackCnt.time <= end_date).group_by(AttackCnt.attackType).first()
    if normal is None:
        normalCount = 0
    else:
        normalCount = int(normal.count)

    anomalous = AttackCnt.query.with_entities(func.sum(AttackCnt.count).label("count")). \
        filter(AttackCnt.attackType == 'anomalous',
               AttackCnt.time >= begin_date,
               AttackCnt.time <= end_date).group_by(AttackCnt.attackType).first()
    if anomalous is None:
        anomalousCount = 0
    else:
        anomalousCount = int(anomalous.count)
    seize = [normalCount+anomalousCount+attackCount, anomalousCount, attackCount]
    return seize


# 查询五天的态势情况
def selectTimeCount():
    objects_list = []
    list_All = []
    end_date = datetime.datetime.now()
    for i in range(5):
        begin_date = end_date-datetime.timedelta(days=1)
        attackCnt = AttackCnt.query.with_entities(AttackCnt.attackType, func.sum(AttackCnt.count).label("count"))\
            .filter(and_(AttackCnt.time >= begin_date, AttackCnt.time <= end_date)).\
            group_by(AttackCnt.attackType).all()
        li = dict()
        for j in attackCnt:
            li[j.attackType] = int(j.count)
        objects_list.append(SituationAssessmentAlgorithms.calculate_Three(li))
        end_date = begin_date

    endDate = datetime.datetime.now().strftime("%Y-%m-%d %H")
    begindate = (datetime.datetime.strptime(endDate, "%Y-%m-%d %H") - datetime.timedelta(days=3)).strftime(
        "%Y-%m-%d %H")
    attackCnt = AttackCnt.query.with_entities(AttackCnt.attackType, func.sum(AttackCnt.count).label("count")).filter(
        and_(AttackCnt.time >= datetime.datetime.strptime(begindate, "%Y-%m-%d %H"),
             AttackCnt.time <= datetime.datetime.strptime(endDate, "%Y-%m-%d %H"))). \
        group_by(AttackCnt.attackType).all()
    li = dict()
    for i in attackCnt:
        li[i.attackType] = int(i.count)
    list_All.append(SituationAssessmentAlgorithms.calculate_All(li))
    list_All.append(objects_list)
    return list_All


# beginDateHour='2018-01-01 23', endDateHour='2018-01-03 00'
def selectLatestThreeMonth():
    beginDateHour = (datetime.datetime.now()-datetime.timedelta(days=7)).strftime("%Y-%m-%d %H")
    endDateHour = datetime.datetime.now().strftime("%Y-%m-%d %H")
    dhour = datetime.datetime.strptime(beginDateHour, "%Y-%m-%d %H")
    date = beginDateHour[:]
    time = []
    attackCount = []
    normalCount = []
    anomalousCount = []
    while date <= endDateHour:
        time.append(date)
        attack = AttackCnt.query.with_entities(AttackCnt.time, func.sum(AttackCnt.count).label("count")).\
            filter(AttackCnt.attackType.notin_(['normal', 'anomalous']),
                   AttackCnt.time == datetime.datetime.strptime(date, "%Y-%m-%d %H"))\
            .group_by(AttackCnt.attackType).first()
        if attack is None:
            attackCount.append(0)
        else:
            attackCount.append(int(attack.count))

        normal = AttackCnt.query.with_entities(AttackCnt.time, func.sum(AttackCnt.count).label("count")).\
            filter(AttackCnt.attackType == 'normal', AttackCnt.time == datetime.datetime.strptime(date, "%Y-%m-%d %H"))\
            .group_by(AttackCnt.attackType).first()
        if normal is None:
            normalCount.append(0)
        else:
            normalCount.append(int(normal.count))

        anomalous = AttackCnt.query.with_entities(AttackCnt.time, func.sum(AttackCnt.count).label("count")).\
            filter(AttackCnt.attackType == 'anomalous',
                   AttackCnt.time == datetime.datetime.strptime(date, "%Y-%m-%d %H")).\
            group_by(AttackCnt.attackType).first()
        if anomalous is None:
            anomalousCount.append(0)
        else:
            anomalousCount.append(int(anomalous.count))

        dhour = dhour + datetime.timedelta(hours=1)
        date = dhour.strftime("%Y-%m-%d %H")
    serize = list()
    serize.append(time)
    serize.append(normalCount)
    serize.append(anomalousCount)
    serize.append(attackCount)
    return serize


def selectOneDayCnt():
    beginDateHour = datetime.datetime.now()-datetime.timedelta(days=1)
    endDateHour = datetime.datetime.now()
    attack = AttackCnt.query.with_entities(func.sum(AttackCnt.count).label("count")). \
        filter(AttackCnt.attackType.notin_(['normal', 'anomalous']),
               AttackCnt.time >= beginDateHour,
               AttackCnt.time <= endDateHour).first()
    if attack == (None,):
        attackCount = 0
    else:
        attackCount = int(attack.count)

    normal = AttackCnt.query.with_entities(func.sum(AttackCnt.count).label("count")). \
        filter(AttackCnt.attackType == 'normal', AttackCnt.time >= beginDateHour,
               AttackCnt.time <= endDateHour).group_by(AttackCnt.attackType).first()
    if normal is None:
        normalCount = 0
    else:
        normalCount = int(normal.count)

    anomalous = AttackCnt.query.with_entities(func.sum(AttackCnt.count).label("count")). \
        filter(AttackCnt.attackType == 'anomalous',
               AttackCnt.time >= beginDateHour,
               AttackCnt.time <= endDateHour).group_by(AttackCnt.attackType).first()
    if anomalous is None:
        anomalousCount = 0
    else:
        anomalousCount = int(anomalous.count)
    seize = [normalCount, anomalousCount, attackCount]
    return seize


def selectSevenDayAttackCnt():
    beginDateHour = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d %H")
    endDateHour = datetime.datetime.now().strftime("%Y-%m-%d %H")
    attack = AttackCnt.query.with_entities(func.sum(AttackCnt.count).label("count")). \
        filter(AttackCnt.attackType.notin_(['normal', 'anomalous']),
               AttackCnt.time >= datetime.datetime.strptime(beginDateHour, "%Y-%m-%d %H"),
               AttackCnt.time <= datetime.datetime.strptime(endDateHour, "%Y-%m-%d %H")).first()
    if attack == (None,):
        attackCount = 0
    else:
        attackCount = int(attack.count)
    return attackCount


# 30天的测试数据，实际上是7天
def selectSevenDayCnt():
    beginDateHour = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d %H")
    endDateHour = datetime.datetime.now().strftime("%Y-%m-%d %H")
    attack = AttackCnt.query.with_entities(func.sum(AttackCnt.count).label("count")). \
        filter(AttackCnt.attackType.notin_(['normal', 'anomalous']),
               AttackCnt.time >= datetime.datetime.strptime(beginDateHour, "%Y-%m-%d %H"),
               AttackCnt.time <= datetime.datetime.strptime(endDateHour, "%Y-%m-%d %H")).first()
    if attack == (None,):
        attackCount = 0
    else:
        attackCount = int(attack.count)

    normal = AttackCnt.query.with_entities(func.sum(AttackCnt.count).label("count")). \
        filter(AttackCnt.attackType == 'normal',
               AttackCnt.time >= datetime.datetime.strptime(beginDateHour, "%Y-%m-%d %H"),
               AttackCnt.time <= datetime.datetime.strptime(endDateHour, "%Y-%m-%d %H")).group_by(
        AttackCnt.attackType).first()
    if normal is None:
        normalCount = 0
    else:
        normalCount = int(normal.count)

    anomalous = AttackCnt.query.with_entities(func.sum(AttackCnt.count).label("count")). \
        filter(AttackCnt.attackType == 'anomalous',
               AttackCnt.time >= datetime.datetime.strptime(beginDateHour, "%Y-%m-%d %H"),
               AttackCnt.time <= datetime.datetime.strptime(endDateHour, "%Y-%m-%d %H")).group_by(
        AttackCnt.attackType).first()
    if anomalous is None:
        anomalousCount = 0
    else:
        anomalousCount = int(anomalous.count)
    allCnt = attackCount+normalCount+anomalousCount
    return allCnt


def AttackSituationAssessmentStatistics(beginDate, endDate):
    endDate = datetime.datetime.strptime(endDate, "%Y-%m-%dT%H:%M").strftime("%Y-%m-%d %H")
    beginDate = datetime.datetime.strptime(beginDate, "%Y-%m-%dT%H:%M").strftime("%Y-%m-%d %H")
    attackCnt = AttackCnt.query.with_entities(AttackCnt.attackType, func.sum(AttackCnt.count).label("count")).filter(
        and_(AttackCnt.time >= beginDate, AttackCnt.time <= endDate)).group_by(AttackCnt.attackType).all()
    li = {}
    for i in attackCnt:
        li[i.attackType] = int(i.count)
    return SituationAssessmentAlgorithms.calculate_One(li)


def HistoricalAssessmentTrendStatistics():
    time = []
    Jurisdiction = []
    Completeness = []
    Controllability = []
    endDate = datetime.datetime.now()
    for i in range(10):
        begindate = endDate - datetime.timedelta(days=1)
        attackCnt = AttackCnt.query.with_entities(AttackCnt.attackType,
                                                  func.sum(AttackCnt.count).label("count")).filter(
            and_(AttackCnt.time >= begindate,
                 AttackCnt.time <= endDate)). \
            group_by(AttackCnt.attackType).all()
        li = {}
        for j in attackCnt:
            li[j.attackType] = int(j.count)
        list_calculate = SituationAssessmentAlgorithms.calculate_Three(li)
        time.append(endDate)
        Jurisdiction.append(list_calculate[0])
        Completeness.append(list_calculate[1])
        Controllability.append(list_calculate[2])
        endDate = begindate
    objects_list = [time, Jurisdiction, Completeness, Controllability]
    return objects_list


def weekdayCount():
    endDate = datetime.datetime.now()
    time = []
    attack_list = []
    normal_list = []
    anomalous_list = []
    for i in range(7):
        beginDate = endDate - datetime.timedelta(days=1)
        attack = AttackCnt.query.with_entities(func.sum(AttackCnt.count).label("count")). \
            filter(AttackCnt.attackType.notin_(['normal', 'anomalous']),
                   AttackCnt.time >= beginDate,
                   AttackCnt.time <= endDate).first()
        if attack == (None,):
            attack_list.append(0)
        else:
            attack_list.append(int(attack.count))

        normal = AttackCnt.query.with_entities(func.sum(AttackCnt.count).label("count")). \
            filter(AttackCnt.attackType == 'normal',
                   AttackCnt.time >= beginDate,
                   AttackCnt.time <= endDate).group_by(
            AttackCnt.attackType).first()
        if normal is None:
            normal_list.append(0)
        else:
            normal_list.append(int(normal.count))

        anomalous = AttackCnt.query.with_entities(func.sum(AttackCnt.count).label("count")). \
            filter(AttackCnt.attackType == 'anomalous',
                   AttackCnt.time >= beginDate,
                   AttackCnt.time <= endDate).group_by(
            AttackCnt.attackType).first()
        if anomalous is None:
            anomalous_list.append(0)
        else:
            anomalous_list.append(int(anomalous.count))
        endDate = beginDate
        time.append(endDate.weekday())
    return [time, normal_list, anomalous_list, attack_list]


def selectSevenDayAttackType():
    beginDateHour = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d %H")
    endDateHour = datetime.datetime.now().strftime("%Y-%m-%d %H")
    attackcnt = AttackCnt.query.with_entities(func.sum(AttackCnt.count).label("count"), AttackCnt.attackType). \
        filter(AttackCnt.attackType.notin_(['normal', 'anomalous']),
               AttackCnt.time >= datetime.datetime.strptime(beginDateHour, "%Y-%m-%d %H"),
               AttackCnt.time <= datetime.datetime.strptime(endDateHour, "%Y-%m-%d %H")).\
        group_by(AttackCnt.attackType).order_by(desc('count')).limit(5)
    li = []
    for i in attackcnt:
        li.append(i.attackType)
    return li
