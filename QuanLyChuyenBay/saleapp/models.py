from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text, Enum, DateTime
from saleapp import db, app
from sqlalchemy.orm import relationship
from enum import Enum as UserEnum


class UserRole(UserEnum):
    USER = 1
    ADMIN = 2


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
    tuyen_bay_id = Column(Integer, ForeignKey(TuyenBay.id), nullable=False)
    may_bay_id = Column(Integer, ForeignKey(MayBay.id), nullable=False)
    ct_chuyen_bay = relationship('ChiTietChuyenBay', backref='chuyen_bay', lazy=True)
    hang_ghe = relationship('HangGhe', backref='chuyen_bay', lazy=True)

    def __str__(self):
        return self.name


class ChiTietChuyenBay(BaseModel):
    thoi_gian_dung = Column(String(100))
    san_bay_trung_gian = Column(Integer, ForeignKey(SanBay.id))
    chuyen_bay_id = Column(Integer, ForeignKey(ChuyenBay.id), nullable=False)


class HangGhe(BaseModel):
    name = Column(String(100), nullable=False)
    chuyen_bay_id = Column(Integer, ForeignKey(ChuyenBay.id), nullable=False)
    gia_ve = relationship('GiaVe', backref='hang_ghe', lazy=True)

    def __str__(self):
        return self.name


class GiaVe(BaseModel):
    don_gia = Column(Float, default=0)
    hang_ghe_id = Column(Integer, ForeignKey(HangGhe.id), nullable=False)


class User(BaseModel):
    name = Column(String(50), nullable=False)
    sdt = Column(String(50), nullable=False)
    address = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    image = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)


if __name__ == '__main__':
    with app.app_context():
        # sb1 = SanBay(name='Tân Sơn Nhất', note='TPHCM')
        # sb2 = SanBay(name='Nội Bài', note='Hà Nội')
        # sb3 = SanBay(name='Liên Khương', note='Đà Lạt')
        #
        # db.session.add_all([sb1, sb2, sb3])
        # db.session.commit()
        #
        # mb1 = MayBay(name='Boeing 777')
        # mb2 = MayBay(name='Boeing 787')
        # db.session.add_all([mb1,mb2])
        # db.session.commit()

        # tb1 = TuyenBay(name='TPHCM - Hà Nội', san_bay_di_id=1, san_bay_den_id=2)
        # tb2 = TuyenBay(name='TPHCM - Đà Lạt', san_bay_di_id=1, san_bay_den_id=3)
        # db.session.add_all([tb1, tb2])
        # db.session.commit()

        # cb1 = ChuyenBay(name='HCM-HN-B0777', ngay_bay='2023-01-10 17:00:00', thoi_gian_bay='2 giờ 40 phút',
        #                 so_ghe1=50, so_ghe2=15, tuyen_bay_id=1, may_bay_id=1)
        # cb2 = ChuyenBay(name='HCM-DL-B0787', ngay_bay='2023-01-20 06:00:00', thoi_gian_bay='1 giờ 5 phút',
        #                 so_ghe1=55, so_ghe2=10, tuyen_bay_id=2, may_bay_id=2)
        # db.session.add_all([cb1, cb2])
        # db.session.commit()

        db.create_all()