from saleapp.models import TuyenBay, ChuyenBay, User
from saleapp import db
import hashlib


def load_tuyenbay():
    return TuyenBay.query.all()


def load_chuyenbay(tb_id=None, kw=None):
    query = ChuyenBay.query

    if tb_id:
        query = query.filter(ChuyenBay.tuyen_bay_id.__eq__(tb_id))

    #tìm chuyến bay theo tên hoặc theo ngày
    if kw:
        query = query.filter((ChuyenBay.name.contains(kw)) | (ChuyenBay.ngay_bay.contains(kw)))

    return query.all()


def get_chuyenbay_by_id(chuyen_bay_id):
    return ChuyenBay.query.get(chuyen_bay_id) #Select * From ChuyenBay Where id = chuyen_bay_id


#hàm đăng nhập
def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())  # strip()là cắt khoảng trắng 2 đầu
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()  # .first() xc thực lấy thằng đầu tiên


def get_user_by_id(user_id):
    return User.query.get(user_id)


# def register_customer(name, address, phone, username, password, avatar):
#     password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
#     c = Customer(name=name, address=address, phone=phone, username=username.strip(), password=password, image=avatar) #a=b thì a là tên trường trong lớp models
#     db.session.add(c)
#     db.session.commit()

