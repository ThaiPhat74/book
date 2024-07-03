import enum
from sqlalchemy import Text, Column, Integer, String, Float, ForeignKey, Enum, DateTime, Boolean
from sqlalchemy.orm import relationship, backref
from app import db, app
from flask_login import UserMixin
from datetime import datetime
import hashlib


class OrderType(enum.Enum):
    ThanhToan = 'Thanh toán'
    DatHang = 'Đặt Hàng'


class OrderStatus(enum.Enum):
    Waiting = 'Chờ lấy hàng'
    Success = 'Thành công'
    Failure = 'Thất bại'


class UserRole(enum.Enum):
    Customer = 1
    ADMIN = 2
    InventoryManagement = 3


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)



class Category(BaseModel):
    __tablename__ = 'Category'

    name = Column(String(50), nullable=False, unique=True)
    Books = relationship('Book', backref='category', lazy=True)

    def __str__(self):
        return self.name


class TypeofCreator(BaseModel):
    __tablename__ = 'TypeOfCreator'

    name = Column(String(50), nullable=False, unique=True)
    Creators = relationship('Creator', backref='typeofcreator', lazy=True)

    def __str__(self):
        return self.name


book_creator = db.Table('book_creator',
                        Column('book_id', ForeignKey('book.id'), nullable=False, primary_key=True),
                        Column('creator_id', ForeignKey('creator.id'), nullable=False, primary_key=True))


class Book(BaseModel):
    __tablename__ = 'book'

    name = Column(String(100), nullable=False)
    price = Column(Float, default=0)
    description = Column(Text)
    image = Column(String(130))
    quantity = Column(Integer)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    creators = relationship('Creator', secondary='book_creator', lazy='subquery', backref=backref('book', lazy=True))
    order_details = relationship('OrderDetails', backref='Book', lazy=True)
    restock_details = relationship('RestockDetails', backref='Book', lazy=True)
    comments = relationship('Comment', backref='Book', lazy=True)

    def __str__(self):
        return self.name


class Creator(BaseModel):
    __tablename__ = 'creator'

    name = Column(String(50), nullable=False)
    type_id = Column(Integer, ForeignKey(TypeofCreator.id), nullable=False)

    def __str__(self):
        return self.name


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    user_role = Column(Enum(UserRole), default=UserRole.Customer)
    phone = Column(String(15), nullable=True)
    address = Column(String(100), nullable=True)
    order = relationship('Order', backref='user', lazy=True)
    comments = relationship('Comment', backref='user', lazy=True)

    def __str__(self):
        return self.name


class Order(BaseModel):
    __tablename__ = 'Order'

    date = Column(DateTime, default=datetime.now())
    type = Column(Enum(OrderType), default=OrderType.ThanhToan)
    status = Column(Enum(OrderStatus), default=OrderStatus.Waiting)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    OrderDetails = relationship('OrderDetails', backref='order', lazy=True)


class OrderDetails(BaseModel):
    __tablename__ = 'OrderDetails'

    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)
    order_id = Column(Integer, ForeignKey(Order.id), nullable=False)


class GoodsRestock(BaseModel):
    __tablename__ = 'GoodsRestock'

    created_date = Column(DateTime, nullable=False, default=datetime.now())
    isConfirm = Column(Boolean, default=False)
    RestockDetails = relationship('RestockDetails', backref='restock', lazy=True)


class RestockDetails(BaseModel):
    __tablename__ = 'RestockDetails'

    quantity = Column(Integer, default=150, nullable=False)
    price = Column(Float, default=0)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)
    restock_id = Column(Integer, ForeignKey(GoodsRestock.id))


class Comment(BaseModel):
    content = Column(String(255), nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        c1 = Category(name='Sách giáo khoa')
        c2 = Category(name='Ngoại ngữ')
        c3 = Category(name='Khoa học')
        c4 = Category(name='Văn học - tiểu thuyết')

        db.session.add_all([c1, c2, c3, c4])
        db.session.commit()

        password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        u1 = User(name='Duong', username='admin1', password=password, user_role=UserRole.ADMIN)
        u2 = User(name='Kiệt', username='admin2', password=password, user_role=UserRole.InventoryManagement)
        u3 = User(name='User', username='user', password=password, user_role=UserRole.Customer)
        db.session.add_all([u1, u2, u3])
        db.session.commit()

        d1 = TypeofCreator(name='Tác giả')
        d2 = TypeofCreator(name='Minh họa')
        d3 = TypeofCreator(name='Dịch giả')

        a1 = Creator(name='Robert Cecil Martin', type_id=1)
        a2 = Creator(name='Alice Schroeder', type_id=1)
        a3 = Creator(name='Marry Buffet', type_id=1)
        a4 = Creator(name='Sean Seah', type_id=1)
        a5 = Creator(name='Mai Lan Hương', type_id=1)
        a6 = Creator(name='Hà Thanh Uyên', type_id=1)
        a7 = Creator(name='Bộ Giáo Dục Và Đào Tạo', type_id=1)
        a8 = Creator(name='Mishima Yomu', type_id=1)
        a9 = Creator(name='Monda', type_id=2)
        db.session.add_all([d1, d2, d3])
        db.session.commit()

        db.session.add_all([a1, a2, a3, a4, a5, a6, a7, a8, a9])
        db.session.commit()

        b1 = Book(name='Clean Code', price=299000, image='https://cdn0.fahasa.com/media/catalog/product/3/9/393129.jpg',
                  quantity=200, category_id=3)

        b2 = Book(name='Cuộc Đời Và Sự Nghiệp Của Warren Buffett', price=529000,
                  image='https://cdn0.fahasa.com/media/catalog/product/z/2/z2347757265330_74b3b3541a95b12454cbde947ccc635e.jpg',
                  quantity=300, category_id=4)

        b3 = Book(name='7 Phương Pháp Đầu Tư Warren Buffet', price=143000,
                  image='https://cdn0.fahasa.com/media/catalog/product/8/9/8936066694131.jpg',
                  quantity=300, category_id=4)

        b4 = Book(name='Giải Thích Ngữ Pháp Tiếng Anh ', price=139000,
                  image='https://cdn0.fahasa.com/media/catalog/product/z/3/z3097453775918_7ea22457f168a4de92d0ba8178a2257b.jpg'
                  , quantity=300, category_id=2)

        b5 = Book(name='Sách Giáo Khoa Bộ Lớp 12', price=180000,
                  image='https://cdn0.fahasa.com/media/catalog/product/3/3/3300000015422-1.jpg'
                  , quantity=300, category_id=1)

        b6 = Book(name='Thế Giới Otome Game Thật Khắc Nghiệt Với Nhân Vật Quần Chúng', price=120000,
                  image='https://cdn0.fahasa.com/media/catalog/product/6/0/600_nh-s_ch-th_-gi_i-otome-game...-5_2.jpg',
                  quantity=0, category_id=4)
        b1.creators.append(a1)
        b2.creators.append(a2)
        b3.creators.append(a3)
        b3.creators.append(a4)
        b4.creators.append(a5)
        b4.creators.append(a6)
        b5.creators.append(a7)
        b6.creators.append(a8)
        b6.creators.append(a9)
        db.session.add_all([b1, b2, b3, b4, b5, b6])
        db.session.commit()
        b1 = Book(name='Clean Code', price=299000, image='https://cdn0.fahasa.com/media/catalog/product/3/9/393129.jpg',
                  quantity=200, category_id=3)

        b2 = Book(name='Cuộc Đời Và Sự Nghiệp Của Warren Buffett', price=529000,
                  image='https://cdn0.fahasa.com/media/catalog/product/z/2/z2347757265330_74b3b3541a95b12454cbde947ccc635e.jpg',
                  quantity=300, category_id=4)

        b3 = Book(name='7 Phương Pháp Đầu Tư Warren Buffet', price=143000,
                  image='https://cdn0.fahasa.com/media/catalog/product/8/9/8936066694131.jpg',
                  quantity=300, category_id=4)

        b4 = Book(name='Giải Thích Ngữ Pháp Tiếng Anh ', price=139000,
                  image='https://cdn0.fahasa.com/media/catalog/product/z/3/z3097453775918_7ea22457f168a4de92d0ba8178a2257b.jpg'
                  , quantity=300, category_id=2)

        b5 = Book(name='Sách Giáo Khoa Bộ Lớp 12', price=180000,
                  image='https://cdn0.fahasa.com/media/catalog/product/3/3/3300000015422-1.jpg'
                  , quantity=300, category_id=1)

        b6 = Book(name='Thế Giới Otome Game Thật Khắc Nghiệt Với Nhân Vật Quần Chúng', price=120000,
                  image='https://cdn0.fahasa.com/media/catalog/product/6/0/600_nh-s_ch-th_-gi_i-otome-game...-5_2.jpg',
                  quantity=0, category_id=4)
        b1.creators.append(a1)
        b2.creators.append(a2)
        b3.creators.append(a3)
        b3.creators.append(a4)
        b4.creators.append(a5)
        b4.creators.append(a6)
        b5.creators.append(a7)
        b6.creators.append(a8)
        b6.creators.append(a9)
        db.session.add_all([b1, b2, b3, b4, b5, b6])
        db.session.commit()

        b1 = Book(name='Clean Code', price=299000, image='https://cdn0.fahasa.com/media/catalog/product/3/9/393129.jpg',
                  quantity=200, category_id=3)

        b2 = Book(name='Cuộc Đời Và Sự Nghiệp Của Warren Buffett', price=529000,
                  image='https://cdn0.fahasa.com/media/catalog/product/z/2/z2347757265330_74b3b3541a95b12454cbde947ccc635e.jpg',
                  quantity=300, category_id=4)

        b3 = Book(name='7 Phương Pháp Đầu Tư Warren Buffet', price=143000,
                  image='https://cdn0.fahasa.com/media/catalog/product/8/9/8936066694131.jpg',
                  quantity=300, category_id=4)

        b4 = Book(name='Giải Thích Ngữ Pháp Tiếng Anh ', price=139000,
                  image='https://cdn0.fahasa.com/media/catalog/product/z/3/z3097453775918_7ea22457f168a4de92d0ba8178a2257b.jpg'
                  , quantity=300, category_id=2)

        b5 = Book(name='Sách Giáo Khoa Bộ Lớp 12', price=180000,
                  image='https://cdn0.fahasa.com/media/catalog/product/3/3/3300000015422-1.jpg'
                  , quantity=300, category_id=1)

        b6 = Book(name='Thế Giới Otome Game Thật Khắc Nghiệt Với Nhân Vật Quần Chúng', price=120000,
                  image='https://cdn0.fahasa.com/media/catalog/product/6/0/600_nh-s_ch-th_-gi_i-otome-game...-5_2.jpg',
                  quantity=0, category_id=4)
        b1.creators.append(a1)
        b2.creators.append(a2)
        b3.creators.append(a3)
        b3.creators.append(a4)
        b4.creators.append(a5)
        b4.creators.append(a6)
        b5.creators.append(a7)
        b6.creators.append(a8)
        b6.creators.append(a9)
        db.session.add_all([b1, b2, b3, b4, b5, b6])
        db.session.commit()


