from web.model.Models import Attack,AttackCnt
from web.model import Attack
from flask import jsonify
from web import app
from web.utils.mail import sendEmail
from web.utils.SensitiveWordMatching import matchSensitiveWord

@app.route('/test')
def all():
    att = 0
    ok = 0
    xss = 0
    attack = Attack.historyAttack()[1::2]
    print(len(attack))
    attacktype = Attack.historyAttack()[::2]
    li = list()
    for i in range(len(attack)):
        li.append(attacktype[i])
        li.append(matchSensitiveWord(attack[i]))
        if attacktype[i] != 'normal':
            att += 1
        if attacktype[i] == 'XSS':
            xss+=1
        if matchSensitiveWord(attack[i]) != [] and attacktype[i] != 'normal':
            ok +=1
    print('正确率', ok/att)
    print(xss)
    return jsonify(li)

@app.route('/mail')
def mail():
    sendEmail()