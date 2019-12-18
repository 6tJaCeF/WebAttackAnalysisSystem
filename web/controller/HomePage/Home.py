from web import app
from web.model import AttackCount
from web.model import Attack
from flask import jsonify, Blueprint

Home = Blueprint('Home', __name__)


@Home.route('/ipCount', methods=['GET', 'POST'])
def ipCount():
    return jsonify(Attack.selectIpAndCount())


@Home.route('/weekdayCount', methods=['GET', 'POST'])
def weekdayCount():
    return jsonify(AttackCount.weekdayCount())


@Home.route('/latestAttack', methods=['GET', 'POST'])
def latestAttackInfo():
    return jsonify(Attack.selectLatestAttackInfo())


@Home.route('/visitCount', methods=['GET', 'POST'])
def visitCount():
    return jsonify(AttackCount.selectOneDayCnt())
