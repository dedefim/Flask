from flask import Flask
from flask import render_template
from blog.views.users import users_app
from blog.views.articles import articles_app
from flask_migrate import Migrate
import os
from blog.security import flask_bcrypt
from blog.views.authors import authors_app


app = Flask(__name__)
app.register_blueprint(users_app, url_prefix="/users")
app.register_blueprint(articles_app, url_prefix="/articles")
cfg_name = os.environ.get("CONFIG_NAME") or "ProductionConfig"
app.config.from_object(f"blog.configs.{cfg_name}")
migrate = Migrate(app, db)
flask_bcrypt.init_app(app)
app.register_blueprint(authors_app, url_prefix="/authors")


@app.route("/")
def index():
    return "Hello world!"


@app.route("/greet/<name>/")
def greet_name(name: str):
    return f"Hello {name}!"


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route("/")
def index():
    return render_template("index.html")


@app.cli.command("create-admin")
def create_admin():
    """
    Run in your terminal:
    ➜ flask create-admin
    > created admin: <User #1 'admin'>
    """
    from blog.models import User

    admin = User(username="admin", is_staff=True)
    admin.password = os.environ.get("ADMIN_PASSWORD") or "adminpass"

    db.session.add(admin)
    db.session.commit()
    print("created admin:", admin)