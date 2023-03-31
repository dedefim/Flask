from flask import Flask
from flask import render_template
from blog.views.users import users_app
from blog.views.articles import articles_app
from flask_migrate import Migrate
import os


app = Flask(__name__)
app.register_blueprint(users_app, url_prefix="/users")
app.register_blueprint(articles_app, url_prefix="/articles")
cfg_name = os.environ.get("CONFIG_NAME") or "ProductionConfig"
app.config.from_object(f"blog.configs.{cfg_name}")
migrate = Migrate(app, db)


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

