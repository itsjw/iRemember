from wtforms import Form, StringField
from wtforms.validators import InputRequired, Length


class CMSLoginForm(Form):
    username = StringField()
    password = StringField()
