from datetime import datetime

from flask import Flask, request, session
from flask import render_template
import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)


class Admin(db.Model):
    __tablename__ = 'Admin'
    id = db.Column(db.Integer, primary_key=True)
    admin_login = db.Column(db.String(25), nullable=False)
    admin_password = db.Column(db.String(25), nullable=False)
    def __init__(self, login, password):
        self.admin_login = login
        self.admin_password = password


class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    post_name = db.Column(db.String(255), nullable=False)
    post_text = db.Column(db.Text(), nullable=False)
    post_image = db.Column(db.String(255), nullable=False)
    continent = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.Date(), default=datetime.utcnow)
    def __init__(self, name, text, url, continent):
        self.post_name = name
        self.post_text = text
        self.post_image = url
        self.continent = continent

row = Admin('admin', 'admin')
db.session.add(row)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<name>')
def user_index(name):
    return render_template('index.html', user_name = name)

@app.route('/Articles')
def Articles():
    new_articles = Posts.query.all()
    return render_template('articles.html', articles = new_articles)


@app.route('/Admin', methods=['GET'])
def Admin_enter():
    message = "Ведите свой логин и пароль."
    return render_template('login_admin.html', message=message)

@app.route('/Admin', methods=['POST'])
def Admin_login():
    login = request.form['login']
    password = request.form['password']
    if Admin.query.filter_by(admin_login=login).all() == []:
        message="Ведите правельный логин!"
        return render_template('login_admin.html',  message=message)
    else:
        if Admin.query.filter_by(admin_password=password).all() == []:
            message = "Ведите правельный пароль!"
            return render_template('login_admin.html', message=message)
        else:
            if 'link' in session:
                session['user'] = login

                return redirect(session['link'])
            else:
                return render_template('add_article.html')

@app.route('/add_post', methods=['POST'])
def add_post():
    title = request.form['title']
    text = request.form['text']
    URL = request.form['URL']
    continent = request.form['continent']
    row = Posts(title, text, URL, continent)
    db.session.add(row)
    db.session.commit()
    return render_template('add_article.html')

@app.route('/add_post', methods=['GET'])
def add_post_form():
    if 'user' in session:
        return render_template('add_article.html')
    else:
        session['link'] = '/add_post'
        message = "Ведите свой логин и пароль."
        return render_template('login_admin.html', message=message)

@app.route('/post_details/<number>')
def details(number):
    row = Posts.query.filter_by(id=number).first()
    return render_template('details.html', row=row)

@app.route('/delete_article', methods = ['GET'])
def delete_article_form():
    if 'user' in session:
        articles = Posts.query.all()
        return render_template('delete_article.html', articles=articles)
    else:
        session['link']='/delete_article'
        message = "Ведите свой логин и пароль."
        return render_template('login_admin.html', message=message)


@app.route('/delete_article', methods = ['POST'])
def delete_article():
    id_list = request.form.getlist('id')
    for id in id_list:
        row = Posts.query.filter_by(id=id).first()
        db.session.delete(row)
    db.session.commit()
    articles = Posts.query.all()
    return render_template('delete_article.html', articles=articles)




if __name__ == "__main__":
   app.run()
