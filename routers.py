from flask import Flask, render_template, url_for, request, redirect, url_for, flash
from datetime import datetime, timedelta, date
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from function import raspTodaySotr, raspTodayGroup, Days, Month, pars_number, whatPlatform
from __init__ import app, db
from models import opk_spec, opk_aud, opk_sotr, opk_group, admins_sait, time, bot_user
import bd


@app.route('/')
def index():
    links = whatPlatform(request)
    spec = opk_spec.query.all()
    today = int(datetime.now().strftime("%w"))
    if today == 1:
        today = ', понедельник'
    elif today == 2:
        today = ', вторник'
    elif today == 3:
        today = ', среда'
    elif today == 4:
        today = ', четверг'
    elif today == 5:
        today = ', пятница'
    elif today == 6:
        today = ', суббота'
    elif today == 0:
        today = ', воскресенье'
    date_now = int(datetime.now().strftime('%H'))
    date_min = int(datetime.now().strftime('%M'))
    para = str()
    date_end = str()
    timerasp = time.query.all()
    for a in timerasp:
        if ((date_now >= int(a.hourUP_b) and date_now < int(a.hourEND_b)) or (date_now == int(a.hourEND_b) and date_min <= int(a.minutEND_b))) and today!=', воскресенье' and today!=', суббота':
            para = a.title_column
            date_end = f"завершится в {a.hourEND_b}:{a.minutEND_b}"
            break
        elif a.hourUP_s != '-1' and ((date_now >= int(a.hourUP_s) and date_now < int(a.hourEND_s)) or (date_now == int(a.hourEND_s) and date_min <= int(a.minutEND_s))) and today!=', воскресенье':
            para = a.title_column
            date_end = f"завершится в {a.hourEND_s}:{a.minutEND_s}"
            break
        elif today==', воскресенье':
            para = ''
            date_end = 'занятия будут в понедельник'
            break
        elif date_now <= 9 and today!=', воскресенье' and today!=', суббота':
            para = ''
            date_end = f'занятия начнутся в {a.hourUP_b}:{a.minutUP_b}'
            break
    return render_template('index.html', day=Days(0), month=Month(0), today=today, para = para, date_end=date_end, spec=spec, timerasp = timerasp, links=links)


@app.route('/group/<int:id>')
def groupa(id):
    links = whatPlatform(request)
    groupa = opk_group.query.filter_by(id_spec=id).all()
    return render_template('group.html', group = groupa, links=links)


@app.route('/WhoDidThat')
def loginPrikol():
    links = whatPlatform(request)
    return render_template('tipaAdmin.html', links=links)

@app.route('/prep')
def prep():
    links = whatPlatform(request)
    sotr = opk_sotr.query.order_by(opk_sotr.name).all()
    return render_template('prep.html', sotr=sotr, links=links)

@app.route('/Admins_login', methods=['POST', 'GET'])
def adminsLoginRout():
    links = whatPlatform(request)
    if not current_user.is_authenticated:
        login = request.form.get('login')
        password = request.form.get('password')
        if request.method == 'POST':
            if login and password:
                user = admins_sait.query.filter_by(login=login).first()
                if user and check_password_hash(user.password, password):
                    login_user(user)
                    return redirect(url_for('adminsMenuRout'))
                else:
                    flash('Логин/пароль не верны')
            else:
                flash('Заполните все поля')

        return render_template('login.html', links=links)
    else:
        return redirect(url_for('index'))



@app.route('/AdminMenuPanel', methods=['POST', 'GET'])
@login_required
def adminsMenuRout():
    links = whatPlatform(request)
    timerasp = time.query.all()

    if request.method == 'POST':
        i = 1
        while i<9:
            t1 = request.form.get(f"title_{i}")
            t2 = request.form.get(f"hourUP_b_{i}")
            t3 = request.form.get(f"hourUP_s_{i}")
            t4 = request.form.get(f"hourEND_b_{i}")
            t5 = request.form.get(f"hourEND_s_{i}")
            t6 = request.form.get(f"minutUP_b_{i}")
            t7 = request.form.get(f"minutUP_s_{i}")
            t8 = request.form.get(f"minutEND_b_{i}")
            t9 = request.form.get(f"minutEND_s_{i}")
            bd.sql(f"delete from time where id = {i}")
            bd.sql(f"insert into time values ({i}, '{t1}', '{t2}', '{t6}', '{t4}', '{t8}', '{t3}', '{t7}', '{t5}', '{t9}');")

            i += 1
        return redirect(url_for('adminsMenuRout'))
    else:
        return render_template('menu.html', timerasp = timerasp, bot_user = bot_user.query.count(), links=links)

@app.errorhandler(500)
def server_error(e):
    links = whatPlatform(request)
    return render_template('500.html', links=links), 500


@app.errorhandler(404)
def url_error(e):
    links = whatPlatform(request)
    return render_template('404.html', links=links), 404


@app.route('/rasp/<int:id>')
def rasp(id):
    links = whatPlatform(request)
    raspgroup = raspTodayGroup(id)
    raspgroup1 = []
    raspgroup2 = []
    raspgroup3 = []
    raspgroup4 = []
    for a in raspgroup:
        if a[0] == (date.today()+timedelta(days=0)).strftime("%d-%m-%Y"):
            if a[1] in pars_number:
                raspgroup1.append({'para' : a[1], 'disc' : a[2], 'aud' : a[4], 'sotr' : a[3]})
        elif a[0] == (date.today()+timedelta(days=1)).strftime("%d-%m-%Y"):
            if a[1] in pars_number:
                raspgroup2.append({'para' : a[1], 'disc' : a[2], 'aud' : a[4], 'sotr' : a[3]})
        elif a[0] == (date.today()+timedelta(days=2)).strftime("%d-%m-%Y"):
            if a[1] in pars_number:
                raspgroup3.append({'para' : a[1], 'disc' : a[2], 'aud' : a[4], 'sotr' : a[3]})
        elif a[0] == (date.today()+timedelta(days=3)).strftime("%d-%m-%Y"):
            if a[1] in pars_number:
                raspgroup4.append({'para' : a[1], 'disc' : a[2], 'aud' : a[4], 'sotr' : a[3]})
        else:
            return render_template('404.html'), 404
    group_name = opk_group.query.filter_by(id=id).first()
    return render_template('rasp.html', links=links, raspgroup1=raspgroup1, raspgroup2=raspgroup2, raspgroup3=raspgroup3, raspgroup4=raspgroup4, day1=Days(0), day2=Days(1), day3=Days(2), day4=Days(3), month1=Month(0), month2=Month(1), month3=Month(2), month4=Month(3), group_name=group_name)

@app.route('/raspprep/<int:id>')
def raspprep(id):
    links = whatPlatform(request)
    raspsotr = raspTodaySotr(id)
    raspsotr1 = []
    raspsotr2 = []
    raspsotr3 = []
    raspsotr4 = []
    for a in raspsotr:
        if a[0] == (date.today()+timedelta(days=0)).strftime("%d-%m-%Y"):
            if a[1] in pars_number:
                raspsotr1.append({'para' : a[1], 'disc' : a[3], 'aud' : a[4], 'name_group' : a[2]})
        elif a[0] == (date.today()+timedelta(days=1)).strftime("%d-%m-%Y"):
            if a[1] in pars_number:
                raspsotr2.append({'para' : a[1], 'disc' : a[3], 'aud' : a[4], 'name_group' : a[2]})
        elif a[0] == (date.today()+timedelta(days=2)).strftime("%d-%m-%Y"):
            if a[1] in pars_number:
                raspsotr3.append({'para' : a[1], 'disc' : a[3], 'aud' : a[4], 'name_group' : a[2]})
        elif a[0] == (date.today()+timedelta(days=3)).strftime("%d-%m-%Y"):
            if a[1] in pars_number:
                raspsotr4.append({'para' : a[1], 'disc' : a[3], 'aud' : a[4], 'name_group' : a[2]})
        else:
            return render_template('404.html'), 404
    sotr_name = opk_sotr.query.filter_by(id=id).first()
    return render_template('raspprep.html', links=links, raspsotr1=raspsotr1, raspsotr2=raspsotr2, raspsotr3=raspsotr3, raspsotr4=raspsotr4, day1=Days(0), day2=Days(1), day3=Days(2), day4=Days(3), month1=Month(0), month2=Month(1), month3=Month(2), month4=Month(3), sotr_name=sotr_name)


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('adminsLoginRout'))

    return response
