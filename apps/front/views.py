#!usr/bin/env python  
# -*- coding:utf-8 -*-  
# @author: Johnathon Qiang
# @file  : views.py
# @time  : 2017/11/24 19:57:14
# @description：

from flask import (
    Blueprint,
    views,
    render_template,
    redirect,
    url_for,
    request,
    session,
    make_response,
    flash,
    g)
from .forms import LoginForm, RegisterForm, BookForm
# from .models import User, Book
from .models_new import User, Book
from config import DevConfig
from ext import db
import random
from utils.captcha import Captcha
from io import BytesIO

bp = Blueprint('front', __name__)


@bp.route('/captcha/')
def graph_captcha():
    # 获取验证码
    text, image = Captcha.gene_graph_captcha()
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp


@bp.route('/')
def index():
    """前台主页面"""
    return render_template('front/index.html')


class SignUpView(views.MethodView):
    """前台用户注册"""

    def get(self):
        return render_template('front/signup.html')

    def post(self):
        form = RegisterForm(request.form)
        if form.validate():
            user = User()
            telephone = form.telephone.data
            username = form.username.data
            password = form.password.data
            confirm = form.confirm.data
            email = form.email.data

            if password == confirm:
                user.telephone = telephone
                user.username = username
                user.password = password
                user.email = email
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('front.signin'))
            else:
                return '两次密码不一致'
        return '验证不通过'


class SignInView(views.MethodView):
    """前台用户登录"""

    def get(self):
        return render_template('front/signin.html')

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            username = form.username.data
            password = form.password.data
            remember = form.remember.data

            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                session[DevConfig.USER_ID] = user.id
                if remember:
                    session.permanent = True
                return redirect(url_for('front.index'))
            else:
                print('用户名或密码错误')
                return self.get()
        else:
            print('验证不通过：%s' % form.errors)
            return self.get()


bp.add_url_rule('/signup/', view_func=SignUpView.as_view('signup'))
bp.add_url_rule('/signin/', view_func=SignInView.as_view('signin'))


@bp.route('/logout/')
def logout():
    del session[DevConfig.USER_ID]
    return redirect(url_for('front.signin'))


@bp.route('/list/')
def list():
    """图书展示页面"""

    books = None
    book_random = None
    # 已登录用，查看所有属于自己的记录
    if DevConfig.USER_ID in session:
        books = Book.query.filter(Book.user_id == session[DevConfig.USER_ID]).all()
    else:
        # 未登录用户随机查看十条记录
        books_random = Book.query.all()
        print(books_random)
        if len(books_random) > 5:
            book_random = random.sample(Book.query.all(), 5)
        else:
            book_random = books_random

    return render_template('front/list_books.html', books=books, book_random=book_random)


class BookView(views.MethodView):
    """图书编辑页面视图"""

    def get(self):
        return render_template('front/add_books.html')

    def post(self):
        form = BookForm(request.form)
        if form.validate():
            book = Book()
            book_name = form.book_name.data
            book_author = form.book_author.data
            book.book_name = book_name
            book.book_author = book_author
            book.user_id = g.user.id
            db.session.add(book)
            db.session.commit()
            print('%s添加成功！' % book_name)
            return redirect(url_for('front.list'))
        else:
            print(form.errors)
            return self.get()


bp.add_url_rule('/add/', view_func=BookView.as_view('add'))


class UserInfoView(views.MethodView):
    def get(self):
        return render_template('front/user_info.html')

    def post(self):
        pass

bp.add_url_rule('/user/', view_func=UserInfoView.as_view('user'))


@bp.before_request
def my_before_request():
    # user_id = session.get(DevConfig.USER_ID)
    # if user_id:
    #     user = User.query.filter(User.id == user_id).first()
    #     if user:
    #         g.user = user
    if DevConfig.USER_ID in session:
        user_id = session.get(DevConfig.USER_ID)
        user = User.query.get(user_id)
        if user:
            g.user = user


@bp.context_processor
def my_context_processor():
    if hasattr(g, 'user'):
        return {'user': g.user}
    return {}

#
# class LoginView(views.MethodView):
#     def get(self):
#         return render_template('front/login.html')
#
#     def post(self):
#         form = LoginForm(request.form)
#
#         if form.validate():
#             username = form.username.data
#             password = form.password.data
#             remember = form.remember.data
#
#             user = User.query.filter_by(username=username).first()
#             if user and user.check_password(password):
#                 session[DevConfig.USER_ID] = user.id
#                 if remember:
#                     session.permanent = True
#                 return redirect(url_for('front.index'))
#             else:
#                 flash('用户名或密码有误', 'errors')
#                 return self.get()
#         else:
#             # message = form.errors.popitem()[1][0]
#             return self.get()

# bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))

# @bp.route('/register/', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         user = User()
#         username = request.form.get('username')
#         password = request.form.get('password')
#         email = request.form.get('email')
#         phone = request.form.get('phone')
#         user.username = username
#         user.password = password
#         user.email = email
#         user.phone = phone
#         if user.username and user.password:
#             db.session.add(user)
#             db.session.commit()
#             return redirect(url_for('front.login'))
#         else:
#             flash('用户名和密码不能为空', 'error')
#             return render_template('front/register.html')
#     return render_template('front/register.html')
