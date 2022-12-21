from saleapp.models import TuyenBay, ChuyenBay, Ve
from saleapp import db, app, dao
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import request


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
    column_exclude_list = ['image']  # ẩn cột

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


class TicketView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated


class StatsView(BaseView):
    @expose('/')
    def index(self):
        stats = dao.sum_doanhthu_by_chuyenbay(kw=request.args.get('kw'),
                                              from_date=request.args.get('from_date'),
                                              to_date=request.args.get('to_date'))
        return self.render('admin/stats.html', stats=stats)

    def is_accessible(self):
        return current_user.is_authenticated


class MyAdminView(AdminIndexView):
    @expose('/')
    def index(self):
        stats = dao.count_chuyenbay_by_tuyenbay()
        return self.render('admin/index.html', stats=stats)


admin = Admin(app=app, name='QUẢN TRỊ BÁN VÉ MÁY BAY', template_mode='bootstrap4', index_view=MyAdminView()) #venv/lib/site-package/flask_admin/templates/bootstrap4
admin.add_view(TuyenBayView(TuyenBay, db.session, name='Tuyến Bay'))
admin.add_view(ChuyenBayView(ChuyenBay, db.session, name='Chuyến Bay'))
admin.add_view(TicketView(Ve, db.session, name='Vé'))
admin.add_view(StatsView(name='Thống kê'))

