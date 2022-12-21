from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text, Enum, DateTime
from saleapp import db, app
from sqlalchemy.orm import relationship
from enum import Enum as UserEnum
from flask_login import UserMixin


class UserRole(UserEnum):
    USER = 1
    ADMIN = 2
    CUSTOMER = 3


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class SanBay(BaseModel):
    name = Column(String(100), nullable=False)
    note = Column(Text)
    active = Column(Boolean, default=True)
    ct_chuyen_bay = relationship('ChiTietChuyenBay', backref='san_bay', lazy=True)

    def __str__(self):
        return self.name


class MayBay(BaseModel):
    name = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)
    chuyen_bay = relationship('ChuyenBay', backref='may_bay', lazy=True)

    def __str__(self):
        return self.name


class TuyenBay(BaseModel):
    name = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)
    chuyen_bay = relationship('ChuyenBay', backref='tuyen_bay', lazy=True)
    san_bay_di_id = Column(Integer, ForeignKey("san_bay.id"), nullable=False)
    san_bay_den_id = Column(Integer, ForeignKey("san_bay.id"), nullable=False)

    san_bay_di = relationship('SanBay', foreign_keys=[san_bay_di_id], backref='san_bay_di', lazy=True)
    san_bay_den = relationship('SanBay', foreign_keys=[san_bay_den_id], backref='san_bay_den', lazy=True)

    def __str__(self):
        return self.name


class ChuyenBay(BaseModel):
    name = Column(String(100), nullable=False)
    ngay_bay = Column(DateTime, nullable=False)
    thoi_gian_bay = Column(String(100), nullable=False)
    so_ghe1 = Column(Integer)
    so_ghe2 = Column(Integer)
    active = Column(Boolean, default=True)
    image = Column(String(100), nullable=False)
    tuyen_bay_id = Column(Integer, ForeignKey(TuyenBay.id), nullable=False)
    may_bay_id = Column(Integer, ForeignKey(MayBay.id), nullable=False)
    ct_chuyen_bay = relationship('ChiTietChuyenBay', backref='chuyen_bay', lazy=True)
    hang_ghe = relationship('HangGhe', backref='chuyen_bay', lazy='subquery')
    ve = relationship('Ve', backref='chuyen_bay', lazy=True)

    def __str__(self):
        return self.name


class ChiTietChuyenBay(BaseModel):
    thoi_gian_dung = Column(String(100))
    san_bay_trung_gian = Column(Integer, ForeignKey(SanBay.id))
    chuyen_bay_id = Column(Integer, ForeignKey(ChuyenBay.id), nullable=False)


class HangGhe(BaseModel):
    name = Column(String(100), nullable=False)
    don_gia = Column(Float, nullable=False)
    chuyen_bay_id = Column(Integer, ForeignKey(ChuyenBay.id), nullable=False)
    ve = relationship('Ve', backref='hang_ghe', lazy=True)

    def __str__(self):
        return self.name


class User(BaseModel, UserMixin):
    name = Column(String(100), nullable=False)
    phone = Column(String(50), nullable=False)
    address = Column(String(100), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    image = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.CUSTOMER)
    ve = relationship('Ve', backref='user', lazy=True)

    def __str__(self):
        return self.name


class Ve(BaseModel):
    ten_kh = Column(String(100), nullable=False)
    cccd = Column(String(50), nullable=False)
    phone = Column(String(50))
    chuyen_bay_id = Column(Integer, ForeignKey(ChuyenBay.id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    hang_ghe_id = Column(Integer, ForeignKey(HangGhe.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        # import hashlib
        # password = str(hashlib.md5('D123456'.encode('utf-8')).hexdigest())
        # u = User(name='Hồ Duyên', phone='0812881212', address='TPHCM', username='adminD', password=password,
        #          image='https://res.cloudinary.com/dwhnp2hsa/image/upload/v1671206362/zlq0axh3exiqw8nggxgh.jpg',
        #          user_role=UserRole.ADMIN)
        #
        # password1 = str(hashlib.md5('N123456'.encode('utf-8')).hexdigest())
        # u1 = User(name='Lê Ngân', phone='0819613163', address='TPHCM', username='adminN', password=password1,
        #          image='https://res.cloudinary.com/dwhnp2hsa/image/upload/v1671206081/c6q0azltjwboqtv73pwq.jpg',
        #          user_role=UserRole.ADMIN)
        # db.session.add_all([u, u1])
        # db.session.commit()
        #
        # import hashlib
        # password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        # u2 = User(name='Văn An', phone='0812881234', address='TPHCM', username='an123', password=password,
        #          image='https://res.cloudinary.com/dwhnp2hsa/image/upload/v1671206362/zlq0axh3exiqw8nggxgh.jpg',
        #          user_role=UserRole.CUSTOMER)
        #
        # password1 = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        # u3 = User(name='Văn Bình', phone='0819613123', address='TPHCM', username='binh123', password=password1,
        #           image='https://res.cloudinary.com/dwhnp2hsa/image/upload/v1671206362/zlq0axh3exiqw8nggxgh.jpg',
        #           user_role=UserRole.CUSTOMER)
        # db.session.add_all([u2, u3])
        # db.session.commit()
        #
        # sb1 = SanBay(name='Tân Sơn Nhất', note='TPHCM')
        # sb2 = SanBay(name='Nội Bài', note='Hà Nội')
        # sb3 = SanBay(name='Liên Khương', note='Đà Lạt')
        # sb4 = SanBay(name='Cam Ranh', note='Nha Trang')
        # sb5 = SanBay(name='Vân Đồn', note='Quảng Ninh')
        # sb6 = SanBay(name='Cát Bi', note='Hải Phòng')
        # sb7 = SanBay(name='Vinh', note='Nghệ An')
        # sb8 = SanBay(name='Incheon', note='Hàn Quốc')
        # sb9 = SanBay(name='Narita', note='Nhật Bản')
        # sb10 = SanBay(name='Suvarnabhumi', note='Thái Lan')
        # sb11 = SanBay(name='Changi', note='Singapore')
        # sb12 = SanBay(name='Kuala Lumpur', note='Malaysia')
        # sb13 = SanBay(name='Bắc Kinh', note='Trung Quốc')
        # sb14 = SanBay(name='John F Kennedy', note='New York')
        # sb15 = SanBay(name='Los Angeles', note='Los Angeles')
        #
        # db.session.add_all([sb1, sb2, sb3, sb4, sb5, sb6, sb7, sb8, sb9, sb10, sb11, sb12, sb13, sb14, sb15])
        # db.session.commit()
        #
        # mb1 = MayBay(name='Boeing 777')
        # mb2 = MayBay(name='Boeing 787')
        # mb3 = MayBay(name='Airbus A321')
        # mb4 = MayBay(name='Airbus A330')
        # mb5 = MayBay(name='Airbus A350')
        # mb6 = MayBay(name='Airbus A380-900')
        # mb7 = MayBay(name='Boeing 747-400')
        # db.session.add_all([mb1,mb2,mb3, mb4, mb5, mb6, mb7])
        # db.session.commit()

        # tb1 = TuyenBay(name='TPHCM - Hà Nội', san_bay_di_id=1, san_bay_den_id=2)
        # tb2 = TuyenBay(name='TPHCM - Đà Lạt', san_bay_di_id=1, san_bay_den_id=3)
        # tb3 = TuyenBay(name='TPHCM - Nha Trang', san_bay_di_id=1, san_bay_den_id=4)
        # tb4 = TuyenBay(name='TPHCM - Quảng Ninh', san_bay_di_id=1, san_bay_den_id=5)
        # tb5 = TuyenBay(name='TPHCM - Hải Phòng', san_bay_di_id=1, san_bay_den_id=6)
        # tb6 = TuyenBay(name='TPHCM - Nghệ An', san_bay_di_id=1, san_bay_den_id=7)
        # tb7 = TuyenBay(name='TPHCM - Hàn Quốc', san_bay_di_id=1, san_bay_den_id=8)
        # tb8 = TuyenBay(name='TPHCM - Nhật Bản', san_bay_di_id=1, san_bay_den_id=9)
        # tb9 = TuyenBay(name='TPHCM - Thái Lan', san_bay_di_id=1, san_bay_den_id=10)
        # tb10 = TuyenBay(name='TPHCM - Singapore', san_bay_di_id=1, san_bay_den_id=11)
        # tb11 = TuyenBay(name='TPHCM - New York', san_bay_di_id=1, san_bay_den_id=14)
        # tb12 = TuyenBay(name='Hà Nội - TPHCM', san_bay_di_id=2, san_bay_den_id=1)
        # tb13 = TuyenBay(name='Hà Nội - Bắc Kinh', san_bay_di_id=2, san_bay_den_id=13)
        # tb14 = TuyenBay(name='Hà Nội - Los Angeles', san_bay_di_id=2, san_bay_den_id=15)
        # db.session.add_all([tb1, tb2,tb3, tb4, tb5, tb6, tb7, tb8, tb9, tb10, tb11, tb12, tb13, tb14])
        # db.session.commit()
        #
        # cb1 = ChuyenBay(name='HCM-HN-B0777', ngay_bay='2023-01-10 18:00:00', thoi_gian_bay='2 giờ 40 phút',
        #                 so_ghe1=50, so_ghe2=15, tuyen_bay_id=1, may_bay_id=1, image='https://res.cloudinary.com/dwhnp2hsa/image/upload/v1671525896/rlyyacqkepnxjuxcyaqc.jpg')
        # cb2 = ChuyenBay(name='HCM-DL-B0787', ngay_bay='2023-01-20 07:00:00', thoi_gian_bay='1 giờ 5 phút',
        #                 so_ghe1=55, so_ghe2=10, tuyen_bay_id=2, may_bay_id=2, image='https://res.cloudinary.com/dwhnp2hsa/image/upload/v1671525836/mn15izgqz7cy6uxykdga.jpg')
        # cb3 = ChuyenBay(name='HCM-NT-A321', ngay_bay='2023-01-11 21:00:00', thoi_gian_bay='1 giờ 10 phút',
        #                 so_ghe1=50, so_ghe2=170, tuyen_bay_id=5, may_bay_id=3, image='https://res.cloudinary.com/dwhnp2hsa/image/upload/v1671525774/fuvgxrrv5ocvwcl4etwo.jpg')
        # cb4 = ChuyenBay(name='HCM-QN-A330', ngay_bay='2023-03-24 08:00:00', thoi_gian_bay='2 giờ 15 phút',
        #                 so_ghe1=200, so_ghe2=220, tuyen_bay_id=4, may_bay_id=4, image='https://res.cloudinary.com/dwhnp2hsa/image/upload/v1671525740/yaapbljo06vq3gjj2gpf.jpg')
        # cb5 = ChuyenBay(name='HCM-HP-A330', ngay_bay='2023-03-25 17:00:00', thoi_gian_bay='2 giờ 5 phút',
        #                 so_ghe1=200, so_ghe2=220, tuyen_bay_id=5, may_bay_id=4, image='https://res.cloudinary.com/dwhnp2hsa/image/upload/v1671525786/ohl9bu4kbpoqbmdghwtb.jpg')
        # cb6 = ChuyenBay(name='HCM-NA-A321', ngay_bay='2023-04-22 12:00:00', thoi_gian_bay='1 giờ 55 phút',
        #                 so_ghe1=50, so_ghe2=170, tuyen_bay_id=6, may_bay_id=3, image='https://res.cloudinary.com/dwhnp2hsa/image/upload/v1671525200/krc7ub9bakgmqqg0oeqo.jpg')
        # cb7 = ChuyenBay(name='HCM-HQ-A350', ngay_bay='2023-05-15 06:00:00', thoi_gian_bay='4 giờ 55 phút',
        #                 so_ghe1=200, so_ghe2=220, tuyen_bay_id=7, may_bay_id=5, image='https://res.cloudinary.com/dwhnp2hsa/image/upload/v1671525825/gosju1dbiwmipzyhrma3.jpg')
        # cb8 = ChuyenBay(name='HCM-NB-A350', ngay_bay='2023-06-12 20:00:00', thoi_gian_bay='8 giờ 20 phút',
        #                 so_ghe1=200, so_ghe2=220, tuyen_bay_id=8, may_bay_id=5, image='https://res.cloudinary.com/dwhnp2hsa/image/upload/v1671525798/pxcaezltm89vz1yhhiob.jpg')
        # cb9 = ChuyenBay(name='HCM-TL-A330', ngay_bay='2023-06-21 09:00:00', thoi_gian_bay='1 giờ 30 phút',
        #                 so_ghe1=200, so_ghe2=220, tuyen_bay_id=9, may_bay_id=4, image='https://res.cloudinary.com/dwhnp2hsa/image/upload/v1671525850/nfag79dcppcak5zdicxs.jpg')
        # cb10 = ChuyenBay(name='HCM-Sing-A380-900', ngay_bay='2023-07-24 13:00:00', thoi_gian_bay='2 giờ 5 phút',
        #                  so_ghe1=400, so_ghe2=453, tuyen_bay_id=10, may_bay_id=6, image='https://res.cloudinary.com/dwhnp2hsa/image/upload/v1671525921/dd344657l5zwgi9qwarj.jpg')
        # cb11 = ChuyenBay(name='HCM-NY-B0747-400', ngay_bay='2023-08-03 15:00:00', thoi_gian_bay='20 giờ 20 phút',
        #                  so_ghe1=300, so_ghe2=324, tuyen_bay_id=11, may_bay_id=7, image='https://res.cloudinary.com/dwhnp2hsa/image/upload/v1671525811/jztn7xhropt2gg1gtof1.jpg')
        # cb12 = ChuyenBay(name='HN-HCM-B0777', ngay_bay='2023-08-15 21:00:00', thoi_gian_bay='2 giờ 40 phút',
        #                  so_ghe1=50, so_ghe2=15, tuyen_bay_id=12, may_bay_id=1, image='https://res.cloudinary.com/dwhnp2hsa/image/upload/v1671525718/czxfgrj8cc5m5kxfgcmw.jpg')
        # cb13 = ChuyenBay(name='HN-BK-A321', ngay_bay='2023-09-21 20:00:00', thoi_gian_bay='7 giờ 30 phút',
        #                  so_ghe1=50, so_ghe2=170, tuyen_bay_id=13, may_bay_id=3, image='https://res.cloudinary.com/dwhnp2hsa/image/upload/v1671525864/ti58mcuj5ttevvkhb9us.jpg')
        # cb14 = ChuyenBay(name='HN-LA-A380-900', ngay_bay='2023-10-29 10:00:00', thoi_gian_bay='15 giờ 55 phút',
        #                   so_ghe1=400, so_ghe2=453, tuyen_bay_id=14, may_bay_id=6, image='https://res.cloudinary.com/dwhnp2hsa/image/upload/v1671525879/ckgzu0edmfujfji3pl3f.jpg')
        # db.session.add_all([cb1, cb2, cb3, cb4, cb5, cb6, cb7, cb8, cb9, cb10, cb11, cb12, cb13, cb14])
        # db.session.commit()
        #
        hg1 = HangGhe(name="Hạng ghế 2", chuyen_bay_id=1, don_gia=1500000)
        hg2 = HangGhe(name="Hạng ghế 2", chuyen_bay_id=5, don_gia=1500000)
        hg3 = HangGhe(name="Hạng ghế 2", chuyen_bay_id=2, don_gia=1500000)
        hg4 = HangGhe(name="Hạng ghế 2", chuyen_bay_id=3, don_gia=1500000)
        hg5 = HangGhe(name="Hạng ghế 2", chuyen_bay_id=4, don_gia=1500000)
        hg6 = HangGhe(name="Hạng ghế 2", chuyen_bay_id=6, don_gia=1500000)
        hg7 = HangGhe(name="Hạng ghế 1", chuyen_bay_id=11, don_gia=3000000)
        hg8 = HangGhe(name="Hạng ghế 1", chuyen_bay_id=12, don_gia=3000000)
        hg9 = HangGhe(name="Hạng ghế 1", chuyen_bay_id=13, don_gia=3000000)
        hg10 = HangGhe(name="Hạng ghế 1", chuyen_bay_id=1, don_gia=3000000)
        hg11 = HangGhe(name="Hạng ghế 1", chuyen_bay_id=2, don_gia=3000000)
        hg12 = HangGhe(name="Hạng ghế 1", chuyen_bay_id=3, don_gia=3000000)
        hg13 = HangGhe(name="Hạng ghế 1", chuyen_bay_id=4, don_gia=3000000)
        hg14 = HangGhe(name="Hạng ghế 1", chuyen_bay_id=5, don_gia=3000000)
        hg15 = HangGhe(name="Hạng ghế 1", chuyen_bay_id=6, don_gia=3000000)
        hg16 = HangGhe(name="Hạng ghế 1", chuyen_bay_id=7, don_gia=3000000)
        hg17 = HangGhe(name="Hạng ghế 1", chuyen_bay_id=8, don_gia=3000000)
        hg18 = HangGhe(name="Hạng ghế 1", chuyen_bay_id=9, don_gia=3000000)
        hg19 = HangGhe(name="Hạng ghế 1", chuyen_bay_id=10, don_gia=3000000)
        db.session.add_all([hg1, hg2, hg3, hg4, hg5, hg6, hg7, hg8, hg9, hg10, hg11, hg12, hg13, hg14, hg15, hg16, hg17, hg18, hg19])
        db.session.commit()

        # db.create_all()