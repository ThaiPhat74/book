from datetime import datetime
from flask_login import current_user
from app.models import Category, Book, User, Order, OrderDetails, \
    TypeofCreator, OrderType, OrderStatus, Comment
from app import db, app
from sqlalchemy import func
import hashlib


def load_categories():
    return Category.query.all()


def load_type():
    return TypeofCreator.query.all()


def load_books(category_id=None, kw=None, page=1):
    query = Book.query

    if category_id:
        query = query.filter(Book.category_id.__eq__(category_id))

    if kw:
        query = query.filter(Book.name.contains(kw))

    return query.paginate(page=page, per_page=8)


def count_books():
    return Book.query.count()


def get_book_by_id(book_id):
    return Book.query.get(book_id)


def get_quantity(book_id):
    b = Book.query.get(book_id)
    return b.quantity


def load_book_has_same_cate(book_id):
    b = Book.query.get(book_id)
    # return Book.query.join(Category, Book.category_id==Category.id)\
    #     .filter(Category.id.__eq__(b.category_id)).limit(2).all()
    # return Book.query.join(Category, Book.category_id == Category.id) \
    #     .filter(Category.id.__eq__(b.category_id)).count()
    return Book.query.join(Category, Book.category_id == Category.id) \
        .filter(Category.id.__eq__(b.category_id)).order_by(func.random()).limit(4)


def auth_user(username, password):
    password = password

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def register(name, username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    if not bool(User.query.filter_by(username=username).first()):
        u = User(name=name, username=username.strip(), password=password)
        db.session.add(u)
        db.session.commit()
        return True
    else:
        return False


def update_profile(user_id, name, address, phone):
    user = User.query.get(user_id)
    user.name = name
    user.address = address
    user.phone = phone
    db.session.commit()


def change_pw(user_id, old, new):
    user = User.query.get(user_id)
    oldpw = str(hashlib.md5(old.encode('utf-8')).hexdigest())
    if oldpw.__eq__(user.password):
        user.password = str(hashlib.md5(new.encode('utf-8')).hexdigest())
        db.session.commit()
        return True
    return False


def get_user_by_id(user_id):
    return User.query.get(user_id)


def add_order(cart):
    if cart:
        r = Order(user=current_user, type=OrderType.DatHang, date=datetime.now(), status=OrderStatus.Waiting)
        db.session.add(r)
        for c in cart.values():
            b = Book.query.get(c['id'])
            if b.quantity >= c['quantity']:
                b.quantity -= c['quantity']
                d = OrderDetails(quantity=c['quantity'], price=c['price'], order=r, book_id=c['id'])
                db.session.add(d)
            else:
                return False
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return False
        else:
            return True


def make_payment(cart):
    if cart:
        r = Order(user=current_user, type=OrderType.ThanhToan, date=datetime.now(), status=OrderStatus.Success)
        db.session.add(r)
        for c in cart.values():
            b = Book.query.get(c['id'])
            if b.quantity >= c['quantity']:
                b.quantity -= c['quantity']
                d = OrderDetails(quantity=c['quantity'], price=c['price'], order=r, book_id=c['id'])
                db.session.add(d)
            else:
                return False
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return False
        else:
            return True


def count_book_by_cate():
    return db.session.query(Category.id, Category.name, func.count(Book.id)) \
        .join(Book, Book.category_id.__eq__(Category.id), isouter=True) \
        .group_by(Category.id).order_by(Category.name).all()


def stats_frequency_by_book(kw=None, from_date=None, to_date=None):
    query = db.session.query(Book.id, Book.name, Category.name, func.count(Order.id)) \
        .join(OrderDetails, OrderDetails.book_id.__eq__(Book.id)) \
        .join(Order, OrderDetails.order_id.__eq__(Order.id)) \
        .join(Category, Book.category_id.__eq__(Category.id), isouter=True)
    if kw:
        query = query.filter(Book.name.contains(kw))
    if from_date:
        query = query.filter(Order.date.__ge__(from_date))
    if to_date:
        query = query.filter(Order.date.__le__(to_date))
    return query.group_by(Book.id).order_by(Book.id).all()


def stats_revenue_by_cate(kw=None, from_date=None, to_date=None):
    query = db.session.query(Category.id, Category.name,
                             func.sum(OrderDetails.quantity * OrderDetails.price), func.count(Book.id)) \
        .join(OrderDetails, OrderDetails.book_id.__eq__(Book.id)) \
        .join(Category, Book.category_id.__eq__(Category.id))
    if kw:
        query = query.filter(Category.name.contains(kw))
    if from_date:
        query = query.filter(Order.date.__ge__(from_date))
    if to_date:
        query = query.filter(Order.date.__le__(to_date))
    return query.group_by(Category.id).all()


def load_order_history(user_id):
    u = User.query.get(user_id)
    my_order = Order.query.join(User, User.id == Order.user_id).filter(Order.user_id == user_id).all()
    for i in my_order:
        if i.type == OrderType.DatHang and i.status == OrderStatus.Waiting:
            rs = (datetime.now() - i.date)
            rs = rs.days * 24 + rs.seconds / 3600
            if rs > 48:
                i.status = OrderStatus.Failure
                db.session.commit()
    return my_order


def isEnoughBook(id, quantity):
    book = Book.query.get(id)
    if quantity > book.quantity:
        return False
    return True


def load_order_details(od_id):
    return Order.query.get(od_id)


def load_comments(book_id):
    return Comment.query.filter(Comment.book_id.__eq__(book_id)).order_by(-Comment.id).all()


def save_comment(book_id, content):
    c = Comment(content=content, book_id=book_id, created_date=datetime.now(), user=current_user)
    db.session.add(c)
    db.session.commit()
    return c


if __name__ == '__main__':
    from app import app

    with app.app_context():
        print(stats_revenue_by_cate())
        print(stats_frequency_by_book())
        # print(count_book_by_cate())
