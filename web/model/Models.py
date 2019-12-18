from web import db


class Attack(db.Model):
    __tablename__ = 'attacktype'
    id = db.Column(db.Integer, primary_key=True)
    attackType = db.Column(db.String(25))
    ip = db.Column(db.String(15))
    source = db.Column(db.String(25))
    status = db.Column(db.String(10))
    time = db.Column(db.String(50))
    details = db.Column(db.String(10000))
    result = db.Column(db.String(10))
    executor = db.Column(db.String(10))
    # def __init__(self):
    #     self.time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def to_json(self):
        json_student = {
            'id': self.id,
            'attackType': self.attackType,
            'ip': self.ip,
            'source': self.source,
            'status': self.status,
            'time': self.time,
            'details': self.details
        }
        return json_student


# 这个是攻击种类对应的漏洞危害和解决方法
class AttackRe(db.Model):
    __tablename__ = 'attackRe'
    id = db.Column(db.Integer, primary_key=True)
    attackType = db.Column(db.String(25), unique=True)
    damage = db.Column(db.String(1000))
    protect = db.Column(db.String(1000))


# attackType 包括exception
class AttackCnt(db.Model):
    __tablename__ = 'attackCount'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    attackType = db.Column(db.String(25))
    count = db.Column(db.Integer)
