from web.model import AttackCount
from flask import jsonify, request, Blueprint

SituationAssessment = Blueprint('SituationAssessment', __name__)


@SituationAssessment.route('/AttackSituationAssessmentStatistics', methods=['GET', 'POST'])
def AttackSituationAssessmentStatistics():
    startTime = request.form.get('startTime', None)
    endTime = request.form.get('endTime', None)
    print(startTime, endTime)
    if startTime is None or endTime is None:
        return jsonify([])
    else:
        return jsonify(AttackCount.AttackSituationAssessmentStatistics(startTime, endTime))


@SituationAssessment.route('/HistoricalAssessmentTrendStatistics', methods=['GET', 'POST'])
def HistoricalAssessmentTrendStatistics():
    return jsonify(AttackCount.HistoricalAssessmentTrendStatistics())
