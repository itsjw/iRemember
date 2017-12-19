from flask import Flask
from config import DevConfig
from ext import db
from apps.front import bp as front_bp
from apps.cms import bp as cms_bp

# import apps.front.hooks

app = Flask(__name__)
app.config.from_object(DevConfig)
db.init_app(app)

app.register_blueprint(front_bp)
app.register_blueprint(cms_bp)

if __name__ == '__main__':
    app.run()
