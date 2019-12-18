from web.model import AttackCount
from web.model import Attack
from flask import jsonify, request, Blueprint

AttackAnalysis = Blueprint('AttackAnalysis', __name__)


@AttackAnalysis.route('/AttackCnt', methods=['GET', 'POST'])
def attackCountAna():
    objects_list = AttackCount.selectAllAttackCount()
    return jsonify(objects_list)


@AttackAnalysis.route('/attackTypeTable', methods=['GET', 'POST'])
def attackCountTable():
    objects_list = AttackCount.selectSevenDayAttackType()
    return jsonify(objects_list)


@AttackAnalysis.route('/ipTopTable', methods=['GET', 'POST'])
def ipTopTable():
    object_list = Attack.selectSevenDayIpCount()
    return jsonify(object_list)


@AttackAnalysis.route('/ipStatistics', methods=['GET', 'POST'])
def ipStatistics():
    object_list = Attack.attackSourceIp()
    return jsonify(object_list)


@AttackAnalysis.route('/sourceIpTop', methods=['GET', 'POST'])
def sourceIpTop():
    object_list = Attack.selectSourceAndCount()
    return jsonify(object_list)


@AttackAnalysis.route('/attacksourceip', methods=['GET', 'POST'])
def attacksourceip():
    startTime = request.form.get('startTime', None)
    endTime = request.form.get('endTime', None)
    if startTime is None or endTime is None:
        return jsonify(Attack.attackSourceIp())
    else:
        return jsonify(Attack.attackSourceIpTime(startTime, endTime))


@AttackAnalysis.route('/attackSource', methods=['GET', 'POST'])
def attackSource():
    startTime = request.form.get('startTime', None)
    endTime = request.form.get('endTime', None)
    if startTime is None or endTime is None:
        return jsonify([])
    else:
        return jsonify(Attack.attackSource(startTime, endTime))


@AttackAnalysis.route('/AttackCountTime', methods=['GET', 'POST'])
def attackCountTime():
    startTime = request.form.get('startTime', None)
    endTime = request.form.get('endTime', None)
    if startTime is None or endTime is None:
        return jsonify(AttackCount.selectAllAttackCount())
    else:
        return jsonify(AttackCount.selectAllAttackCountTime(startTime, endTime))


@AttackAnalysis.route('/VisitCountTime', methods=['GET', 'POST'])
def VisitCountTime():
    startTime = request.form.get('startTime', None)
    endTime = request.form.get('endTime', None)
    if startTime is None or endTime is None:
        return jsonify([])
    else:
        return jsonify(AttackCount.selectAllCountTime(startTime, endTime))
