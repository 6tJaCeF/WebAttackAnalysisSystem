from web.model.Models import Attack
from web.model import Attack
import json
from flask import request, Blueprint
from flask import jsonify
AttackDetection = Blueprint('AttackDetection', __name__)


@AttackDetection.route('/HistoricAttackStatistics', methods=['GET', 'POST'])
def HistoricAttackStatistics():
    objects_list = Attack.selectThreeDayAttack()
    return jsonify(objects_list)


@AttackDetection.route('/AttackDetails', methods=['GET', 'POST'])
def AttackDetails():
    id = request.form.get('id', None)
    if id is None:
        return jsonify([])
    else:
        objects_list = Attack.selectAllById(id)
        return jsonify(objects_list)


@AttackDetection.route('/AttackCount', methods=['GET', 'POST'])
def AttackCc():
    return str(Attack.selectAttackCount())


@AttackDetection.route('/AuditOfInspectionResult', methods=['GET', 'POST'])
def AuditOfInspectionResult():
    objects_list = Attack.selectLatestAttack()#打一个问号这个什么数据比较好
    return json.dumps(objects_list)


@AttackDetection.route('/SearchHistory', methods=['GET', 'POST'])
def SearchHistory():
    label = request.form.get("label")
    objects_list = Attack.selectSearchHistory(label)
    return json.dumps(objects_list)


@AttackDetection.route('/SearchResult', methods=['GET', 'POST'])
def SearchResult():
    label = request.form.get("label")
    objects_list = Attack.selectSearchResult(label)
    return json.dumps(objects_list)


@AttackDetection.route('/DetectionResultCheck', methods=['GET', 'POST'])
def DetectionResultCheck():
    return jsonify(Attack.detectResult())


@AttackDetection.route('/UpdateCheckResult', methods=['GET', 'POST'])
def UpdateCheckResult():
    id = request.form.get('id', None)
    result = request.form.get('result', None)
    if id is None or result is None:
        return jsonify([])
    else:
        return jsonify(Attack.updateAttackResult(id, result))
