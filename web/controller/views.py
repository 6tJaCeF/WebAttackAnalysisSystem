from web import app
from .AttackAnalysis.AttackAnalysis import AttackAnalysis
from .AttackDetection.AttackDetection import AttackDetection
from .HomePage.Homepage import Homepage
from .HomePage.Home import Home
from .SituationAssessment.SituationAssessment import SituationAssessment

app.register_blueprint(AttackAnalysis, url_prefix='/AttackAnalysis')
app.register_blueprint(AttackDetection, url_prefix='/AttackDetection')
app.register_blueprint(Home, url_prefix='/Home')
app.register_blueprint(Homepage, url_prefix='/Homepage')
app.register_blueprint(SituationAssessment, url_prefix='/SituationAssessment')
