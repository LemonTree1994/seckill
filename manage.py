from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

# from normalapp import create_app as create_normalapp, db
from rediscacheapp import create_app as create_rediscacheapp, db
app = create_rediscacheapp()
manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command("db",MigrateCommand)
manager.add_command("runserver",Server(threaded=True,host="0.0.0.0",port=9999))

if __name__ == '__main__':
    manager.run(default_command="runserver")