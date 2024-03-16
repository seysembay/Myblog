from os import getenv

from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from flask_migrate import Migrate
from werkzeug.exceptions import NotFound
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, Post, User

secret_key = getenv('SECRET_KEY', 'bc8e68da85e667ba4c8682e2bd7706a3')
database_uri = getenv('SQLALCHEMY_DATABASE_URI', 'postgresql+psycopg2://user:password@172.18.0.2:5432/myblog')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SECRET_KEY'] = secret_key

db.init_app(app)
login_manager = LoginManager(app)
migrate = Migrate(app, db)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.cli.command("create-db")
def create_user():
    db.create_all()


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not username or not email or not password:
            error = 'Имя пользователя, адрес электронной почты и пароль являются обязательными полями.'
            return render_template('register.html', error=error)
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            error = 'Пользователь с таким именем уже существует.'
            return render_template('register.html', error=error)

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return 'Неправильное имя пользователя или пароль'
        else:
            login_user(user)
            return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.get("/", endpoint="index")
@login_required
def index():
    posts = Post.query.all()
    return render_template("index.html", posts=posts)


@app.route('/post/create/', endpoint='create', methods=['GET', 'POST'])
@login_required
def product_create():
    if request.method == 'GET':
        return render_template('create.html')

    title = request.form.get('title')
    print(title)
    title = request.form.get('title')
    content = request.form.get('content')

    if not title or not content:
        error = 'Заголовок и содержание поста являются обязательными полями.'
        return render_template('create_post.html', error=error)
    post = Post(title=title, content=content, user_id=current_user.id)
    db.session.add(post)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/post/<int:post_id>/')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    if post is None:
        raise NotFound
    return render_template('post.html', post=post)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
