from saleapp import app
from saleapp.models import TuyenBay, ChuyenBay, SanBay


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