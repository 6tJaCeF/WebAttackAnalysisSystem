from web.model import AttackCount
from web.model import Attack
import json
from flask import jsonify, Blueprint
from web.utils.mail import detectionWarning

Homepage = Blueprint('Homepage', __name__)


@Homepage.route('/latestAttack', methods=['GET', 'POST'])
def latestAttack():
    objects_list = Attack.selectLatestAttack()
    return jsonify(objects_list)


@Homepage.route('/radarchart', methods=['GET', 'POST'])
def radarchart():
    objects_list = AttackCount.selectTimeCount()
    detectionWarning()
    return jsonify(objects_list)


@Homepage.route('/visitcountchart', methods=['GET', 'POST'])
def visitcountchart():
    return jsonify(AttackCount.selectLatestThreeMonth())


@Homepage.route('/visitcount', methods=['GET', 'POST'])
def visitcount():
    list_cnt = AttackCount.selectOneDayCnt()
    list_cnt[0] = list_cnt[0]+list_cnt[1]+list_cnt[2]
    return jsonify(list_cnt)
