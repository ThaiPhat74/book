from flask import session
from app import app, dao, admin, login, utils, controllers


app.add_url_rule('/', 'index', controllers.index)

app.add_url_rule('/books/<int:book_id>', 'details', controllers.details)

app.add_url_rule('/login-admin', 'login-admin', controllers.login_admin, methods=['post'])

app.add_url_rule('/login', 'login', controllers.login_my_user, methods=['get', 'post'])

app.add_url_rule('/logout', 'logout', controllers.logout_my_user)

app.add_url_rule('/register', 'register', controllers.register, methods=['get', 'post'])


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


app.add_url_rule('/cart', 'cart', controllers.cart)

app.add_url_rule('/api/cart', 'add-cart', controllers.add_to_cart, methods=['post'])

app.add_url_rule('/api/cart/<book_id>', 'update-cart', controllers.update_cart, methods=['put'])

app.add_url_rule('/api/cart/<book_id>', 'delete-cart', controllers.delete_cart, methods=['delete'])

app.add_url_rule('/pay', 'pay', controllers.pay)

app.add_url_rule('/preorder', 'preorder', controllers.preorder)

app.add_url_rule('/account', 'account', controllers.account)

app.add_url_rule('/edit', 'edit', controllers.edit, methods=['get', 'post'])

app.add_url_rule('/change-password', 'change-password', controllers.change_password, methods=['get', 'post'])

app.add_url_rule('/order-history', 'order-history', controllers.load_order)

app.add_url_rule('/order-history/<int:order_id>', 'order-details', controllers.order_details)


@app.context_processor
def common_attribute():
    categories = dao.load_categories()
    return {
        'categories': categories,
        'cart': utils.cart_stats(session.get(app.config['CART_KEY']))
    }


app.add_url_rule('/api/books/<int:book_id>/comments', 'comment-list', controllers.comments)
app.add_url_rule('/api/books/<int:book_id>/comments', 'comment-add', controllers.add_comment, methods=['post'])


if __name__ == '__main__':
    app.run(debug=True,port=8888)
