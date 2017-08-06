#!/usr/bin/env python

from blog.app import create_app, db
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)


manager.add_command('db', MigrateCommand)
manager.add_command('server', Server(
    host='0.0.0.0', port='4000', use_reloader=True, threaded=True))


@manager.command
def test():
    """Run the unit tests."""
    import subprocess
    code = subprocess.call(['py.test', 'tests', '--verbose'])
    return code


@manager.command
def profile(length=25, profile_dir=None):
    """Start the application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    app.run()


if __name__ == '__main__':
    manager.run()
