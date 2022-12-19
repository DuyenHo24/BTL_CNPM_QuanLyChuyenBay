from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babelex import Babel
import cloudinary

app = Flask(__name__)
app.secret_key = 'ihdvjkbgkjeb@$^*(#*NDUUFVNEU***' #chuỗi gì cũng đc (ngoằn ngoèo, khó nhớ) => thêm, sửa, xoá trong trang admin
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/saledb?charset=utf8mb4' % quote('12345678')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

cloudinary.config(cloud_name='dwhnp2hsa', api_key='422672812142572', api_secret='IvSWkIQDax32lByzdZOD09HLUSA')

db = SQLAlchemy(app=app)

login = LoginManager(app=app)

babel = Babel(app=app)


@babel.localeselector
def load_locale():
    return 'vi'
