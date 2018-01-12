# coding=utf-8
from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from flask import abort, redirect, url_for
import Edu_administration
from exception.MyException import *

app = Flask(__name__)


@app.route('/detail')
def detial():
    study_id = request.cookies.get('study_id')
    courses = Edu_administration.query_course(study_id)
    return render_template('course_detail.html', courses=courses)


@app.route('/logout')
def logout():
    resp = make_response(render_template('login.html'))
    # 设置jid和学号存在cookie里
    resp.set_cookie('is_login', 'n')
    return redirect(url_for('index'))


@app.route('/login', methods=['post'])
def login():
    study_id = request.form['study_id']
    password = request.form['password']
    print(study_id, password)
    try:
        jid = Edu_administration.my_login(study_id, password)
        print(jid)
        c = {'study_id': study_id, 'JSESSIONID': jid}
        Edu_administration.ifEmptyLoad(study_id, c)
        result = Edu_administration.statistic(study_id)
        resp = make_response(render_template('index.html', result=result))
        # 设置jid和学号存在cookie里
        resp.set_cookie('JSESSIONID', jid)
        resp.set_cookie('study_id', study_id)
        return resp
    except PasswordNotCorrectException, e:
        return "password err"
    except UserNotExistException, e:
        return "user not exist"
    finally:
        pass


@app.route('/index')
def index():
    jid = request.cookies.get('JSESSIONID')
    study_id = request.cookies.get('study_id')
    isLogin = request.cookies.get('is_login')
    if jid is None or jid == '' or study_id is None or study_id == '' or \
            (not Edu_administration.test_connect(JSESSIONID=jid) or isLogin is None or isLogin == 'n'):
        return render_template('login.html')
    else:  # 已登录，显示成绩
        Edu_administration.ifEmptyLoad(study_id, request.cookies)
        result = Edu_administration.statistic(study_id)
        return render_template('index.html', result=result)


@app.route('/')
def hello_world():
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
