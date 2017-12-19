#!usr/bin/env python  
# -*- coding:utf-8 -*-  
# @author: Johnathon Qiang
# @file  : views.py 
# @time  : 2017/12/18 10:51:41
# @description：
import logging
from flask import (
    Blueprint,
    views,
    render_template,
    request,
    session,
    redirect,
    url_for
)

from .hooks import login_required
from .forms import CMSLoginForm
from .models import CMSUser
from config import DevConfig

bp = Blueprint('cms', '__name__', url_prefix='/cms')


@bp.route('/index/')
@login_required
def index():
    return render_template('admin/index.html')


class CMSLogin(views.MethodView):
    def get(self):
        return render_template('admin/cms_login.html')

    def post(self):
        form = CMSLoginForm(request.form)
        logging.warning(form)
        if form.validate():
            username = form.username.data
            password = form.password.data
            # print(username)
            # print(password)
            logging.info('username:%s' % username)
            logging.info('password:%s' % password)
            user = CMSUser.query.filter_by(username=username).first()
            print(user)
            # print(user.username)
            # print(user.password)
            if user and user.check_password(password):
                session[DevConfig.CMS_USER_ID] = user.id
                return redirect(url_for('cms.index'))

            return '用户名或密码不正确'
        return '验证不通过'


bp.add_url_rule('/login/', view_func=CMSLogin.as_view('login'))


@bp.route('/logout/')
@login_required
def logout():
    del session[DevConfig.CMS_USER_ID]
    return redirect(url_for('cms.login'))
