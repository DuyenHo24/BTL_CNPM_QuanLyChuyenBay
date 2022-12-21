from flask import render_template, request, redirect, session
from saleapp import app, dao, admin, login, controllers
from flask_login import login_user, logout_user
from saleapp.decorators import annonymous_user
import cloudinary.uploader


app.add_url_rule("/", 'index', controllers.index)
app.add_url_rule("/chuyen_bay/<int:chuyen_bay_id>", 'chuyen-bay-details', controllers.details)
app.add_url_rule("/thongtindatve/<int:chuyen_bay_id>", 'thong-tin-dat-ve', controllers.thongtindatve)
app.add_url_rule("/login-admin", 'login-admin', controllers.login_admin, methods=['post'])
app.add_url_rule("/registercustomer", 'register', controllers.register_customer, methods=['get', 'post'])
app.add_url_rule("/logincustomer", 'login', controllers.login_customer, methods=['get', 'post'])
app.add_url_rule("/logout", 'logout', controllers.logout_my_user)
app.add_url_rule("/datve", 'dat-ve', controllers.datve)


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