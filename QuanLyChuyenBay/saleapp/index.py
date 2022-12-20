from flask import render_template, request, redirect, session
from saleapp import app, dao, admin, login
from flask_login import login_user, logout_user
from saleapp.decorators import annonymous_user
import cloudinary.uploader


@app.route("/")
def index():

    tb_id = request.args.get('tuyen_bay_id')
    kw = request.args.get('keyword')
    chuyenbay = dao.load_chuyenbay(tb_id, kw)
    return render_template('index.html', chuyen_bay=chuyenbay)


@app.route("/chuyen_bay/<int:chuyen_bay_id>")
def details(chuyen_bay_id):
    cb = dao.get_chuyenbay_by_id(chuyen_bay_id)

    return render_template('details.html', chuyenbay=cb) #chuyenbay sd bên details.html


@app.route('/thongtindatve/<int:chuyen_bay_id>')
def thongtindatve(chuyen_bay_id):
    cb = dao.get_chuyenbay_by_id(chuyen_bay_id)
    # hg = ['hang_ghe']
    # giave = dao.get_giave_by_hg_id(hg)
    return render_template('thongtindatve.html', chuyenbay=cb)

@app.route('/login-admin', methods=['post'])
def login_admin():
    username = request.form['username']
    password = request.form['password']

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


@app.route('/registercustomer', methods=['get', 'post']) #get để load trang regisister lên, còn post để tạo 1 tk mới
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


@app.route('/logincustomer', methods=['get','post'])
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


@app.route('/logout')
def logout_my_user():
    logout_user()
    return redirect('/logincustomer')


@app.route('/datve')
def datve():
    return render_template('datve.html')


@app.context_processor
def common_attr():
    tuyenbay = dao.load_tuyenbay()

    return {
        'tuyenbay': tuyenbay,
    }


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == "__main__":
    app.run(debug=True)