from wtforms.validators import InputRequired, NumberRange

from app import db, app, dao
from app.models import Category, Book, UserRole, RestockDetails, GoodsRestock, Order
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import redirect, request
from flask_login import logout_user, current_user
from wtforms import TextAreaField
from wtforms.widgets import TextArea


class AuthenticatedModeView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()



class OrderView(AuthenticatedModeView):
    column_filters = ['type', 'status']
    can_view_details = True
    column_searchable_list = ['user_id']
class BookView(AuthenticatedModeView):
    column_searchable_list = ['name', 'description']
    column_filters = ['name', 'price']
    can_view_details = True
    column_exclude_list = ['image']
    can_export = True
    column_export_list = ['id', 'name', 'description']
    column_labels = {
        'name': 'Tên sách',
        'description': 'Mô tả',
        'price': 'Giá'
    }
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'description': CKTextAreaField
    }


class RestockDetailsView(ModelView):
    column_list = ()
    # validator wtforms
    form_args = {
        "quantity": {"validators": [InputRequired(), NumberRange(min=150)]},
        "Book": {"query_factory": lambda: Book.query.filter(Book.quantity < 300)}
    }
    column_filters = ['restock_id', 'quantity', 'Book.name']
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.InventoryManagement



class GoodsRestockView(ModelView):
    can_view_details = True
    column_filters = ['isConfirm']

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.InventoryManagement


class StatsView(AuthenticatedView):
    @expose('/')
    def index(self):
        stats1 = dao.stats_revenue_by_cate(kw=request.args.get('kw1'),
                                           from_date=request.args.get('from_date1'),
                                           to_date=request.args.get('to_date1'))
        stats2 = dao.stats_frequency_by_book(kw=request.args.get('kw2'),
                                             from_date=request.args.get('from_date2'),
                                             to_date=request.args.get('to_date2'))
        return self.render('admin/stats.html', stats1=stats1, stats2=stats2)


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


class AdminView(AdminIndexView):
    @expose('/')
    def index(self):
        stats = dao.count_book_by_cate()
        return self.render('admin/index.html', stats=stats)


admin = Admin(app=app, name='Quản lý nhà sách', template_mode='bootstrap4', index_view=AdminView())
admin.add_view(AuthenticatedModeView(Category, db.session, name='Danh mục'))
admin.add_view(BookView(Book, db.session, name='Sách'))
admin.add_view(RestockDetailsView(RestockDetails, db.session, name='Sách nhập'))
admin.add_view(GoodsRestockView(GoodsRestock, db.session, name='phiếu nhập'))
admin.add_view(OrderView(Order, db.session, name='Quản lý đơn hàng'))
admin.add_view(StatsView(name='Thống kê - báo cáo'))
admin.add_view(LogoutView(name='Đăng xuất'))
