from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from main import app
from ext import db
# from apps.front.models import User, Book
from apps.front.models_new import User
from apps.cms.models import CMSUser

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('server', Server())
manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
    return dict(app=app,
                db=db,
                User=User,
                # Book=Book,
                CMSUser=CMSUser)


@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
def create_cms_user(username, password):
    # 后台管理用户设置，因为后台只有登录没有注册，所以直接在本地通过命令行方式创建用户
    user = CMSUser(username=username, password=password)
    db.session.add(user)
    db.session.commit()


if __name__ == '__main__':
    manager.run()
