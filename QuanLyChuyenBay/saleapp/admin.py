from saleapp.models import TuyenBay, ChuyenBay
from saleapp import db, app
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class ChuyenBayView(ModelView):
    column_searchable_list = ['name', 'ngay_bay']
    column_filters = ['name', 'ngay_bay']
    column_labels = {
        'name': 'Tên Chuyến Bay',
        'ngay_bay': 'Ngày Bay',
        'thoi_gian_bay': 'Thời gian bay',
        'so_ghe1': 'Số ghế hạng 1',
        'so_ghe2': 'Số ghế hạng 2',
        'active': 'Tình Trạng',
        'tuyen_bay': 'Tuyến Bay',
        'may_bay': 'Máy Bay'
    }  # đổi tên cột
    can_view_details = True

    def is_accessible(self):
        return current_user.is_authenticated


class TuyenBayView(ModelView):
    column_searchable_list = ['name']
    column_filters = ['name']
    column_labels = {
        'name': 'Tên Tuyến Bay',
        'active': 'Tình Trạng',
        'san_bay_di': 'Sân bay đi',
        'san_bay_den': 'Sân bay đến'
    }  # đổi tên cột

    def is_accessible(self):
        return current_user.is_authenticated


class StatsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')

    def is_accessible(self):
        return current_user.is_authenticated


admin = Admin(app=app, name='QUẢN TRỊ BÁN VÉ MÁY BAY', template_mode='bootstrap4') #venv/lib/site-package/flask_admin/templates/bootstrap4
admin.add_view(TuyenBayView(TuyenBay, db.session, name='Tuyến Bay'))
admin.add_view(ChuyenBayView(ChuyenBay, db.session, name='Chuyến Bay'))
admin.add_view(StatsView(name='Thống kê'))

