from wtforms import Form, StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, DataRequired, EqualTo


class LoginForm(Form):
    """
    登录验证表单
    """
    username = StringField(validators=[InputRequired(message='请输入用户名')])
    password = StringField(validators=[InputRequired(message='请输入密码'), Length(6, 24, message='密码长度不对')])
    remember = StringField()


class RegisterForm(Form):
    """
    注册验证表单
    """
    telephone = StringField('telephone', validators=[DataRequired(), Length(min=11, max=11, message='手机号码只能是11位')])
    # sms = StringField('sms_captcha', validators=[DataRequired(), Length(min=4, max=4, message='验证码不对或已过期')])
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), Length(min=6, max=24, message='密码长度必须在6-24位之间')])
    confirm = PasswordField('confirm', validators=[DataRequired(), EqualTo('password', message='两次输入密码必须保持一致')])
    email = StringField('email', validators=[DataRequired(), Email()])


class BookForm(Form):
    """
    添加书籍表单
    """
    book_name = StringField('book_name', validators=[DataRequired(message='请输入书名')])
    book_author = StringField('book_Author', validators=[DataRequired(message='请输入作者姓名')])
