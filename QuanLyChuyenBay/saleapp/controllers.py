from flask import render_template, request, redirect, session
from saleapp import app, dao, admin, login
from flask_login import login_user, logout_user
from saleapp.decorators import annonymous_user
import cloudinary.uploader


def index():
    tb_id = request.args.get('tuyen_bay_id')
    kw = request.args.get('keyword')
    chuyenbay = dao.load_chuyenbay(tb_id, kw)
    return render_template('index.html', chuyen_bay=chuyenbay)


def details(chuyen_bay_id):
    cb = dao.get_chuyenbay_by_id(chuyen_bay_id)

    return render_template('details.html', chuyenbay=cb) #chuyenbay sd bên details.html


def thongtindatve(chuyen_bay_id):
    cb = dao.get_chuyenbay_by_id(chuyen_bay_id)
    # hg = ['hang_ghe']
    # giave = dao.get_giave_by_hg_id(hg)
    return render_template('thongtindatve.html', chuyenbay=cb)


def login_admin():
    username = request.form['username']
    password = request.form['password']

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


def register_customer():
    err_msg = ''
    if request.method.__eq__('POST'):
        password = request.form['password']
        confirm = request.form['confirm']
        if password.__eq__(confirm):
            avatar = ''
            if request.files:
                res = cloudinary.uploader.upload(request.files['avatar'])
                avatar = res['secure_url']
            try:
                dao.register_customer(name=request.form['name'],
                                  address=request.form['address'],
                                  phone=request.form['phone'],
                                  username=request.form['username'], #'username' là thuộc tính name trong register.html
                                  password=password,
                                  avatar=avatar)
                return redirect('/logincustomer')
            except:
                err_msg = 'Hệ thống đang có lỗi, vui lòng quay lại sau'
        else:
            err_msg = 'Mật khẩu KHÔNG khớp'

    return render_template('registercustomer.html', err_msg=err_msg)


@annonymous_user
def login_customer():
    if request.method.__eq__('POST'):
        username = request.form['username']
        password = request.form['password']

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)
            return redirect('/')

    return render_template('logincustomer.html')


def logout_my_user():
    logout_user()
    return redirect('/logincustomer')


def datve():
    return render_template('datve.html')

