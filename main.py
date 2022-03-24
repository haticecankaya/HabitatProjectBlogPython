from flask import Flask, render_template, request, session, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import math

app = Flask(__name__)
app.secret_key = "super-secret-key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////HabitatProject/blog.db'
db = SQLAlchemy(app)


class Contacts(db.Model):
    num = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    mail = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(12), nullable=True)


class Posts(db.Model):
    num = db.Column(db.Integer, primary_key=True)
    baslik = db.Column(db.String(30), nullable=False)
    alt_bas = db.Column(db.String(30), nullable=False)
    url_yap = db.Column(db.String(30), nullable=False)
    icerik = db.Column(db.String(120), nullable=False)


"""@app.route('/addpost', methods=["GET", "POST"])
def add():
    if request.method == "POST":
        postname = request.form.get("postname")
        altpostname = request.form.get("altpostname")
        urlyapisi = request.form.get("url_yapisi")
        posticerik = request.form.get("icerik")
        entry = Posts(baslik=postname, alt_bas=altpostname, url_yap=urlyapisi, icerik=posticerik)
        db.session.add(entry)
        db.session.commit()
        return render_template("add.html")
    return render_template("add.html")"""


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        return render_template("contact.html")
    elif request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")

        entry = Contacts(name=name, phone_num=phone, msg=message, date=datetime.now(), mail=email)
        db.session.add(entry)
        db.session.commit()
        return render_template("contact2.html")


@app.route("/post/<string:url_yap>", methods=["GET", "POST"])
def post(url_yap):
    if request.method == "GET":
        posto = Posts.query.filter_by(url_yap=url_yap).first()
        return render_template("post2.html", posto=posto)
    return render_template("post2.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
    kullanici_adi = "hatice"
    kullanici_pass = "habitat"

    if "user" in session and session["user"] == kullanici_adi:
        posts = Posts.query.all()
        return render_template("dashboard.html", posts=posts)

    if request.method == "POST":
        username = request.form.get("uname")
        userpass = request.form.get("pass")
        if username == kullanici_adi and userpass == kullanici_pass:
            session["user"] = username
            posts = Posts.query.all()
            return render_template("dashboard.html", posts=posts)
        else:
            return render_template("login2.html")
    else:
        return render_template("login.html")


@app.route('/')
def index():
    sayi = 3
    posts = Posts.query.filter_by().all()
    last = math.ceil(len(posts)/(sayi))
    page = request.args.get("page")
    if not str(page).isnumeric():
        page = 1
    page = int(page)
    posts = posts[(page-1)*(sayi): (page-1)*(sayi)+(sayi)]
    if page == 1:
        geri = "#"
        next = "/?page="+str(page+1)
    elif page == last:
        geri = "/?page="+str(page-1)
        next = "#"
    else:
        next = "/?page=" + str(page + 1)
        geri = "/?page=" + str(page - 1)
    return render_template("index.html", posts=posts, geri=geri, next=next)


@app.route("/edit/<string:num>", methods=["GET", "POST"])
def edit(num):
    kullanici_adi = "hatice"
    kullanici_pass = "habitat"
    if "user" in session and session["user"] == kullanici_adi:
        if(request.method == "POST"):
            box_title = request.form.get("baslik")
            box_altbas = request.form.get("altbaslik")
            box_icerik = request.form.get("icerik")
            box_url_yap = request.form.get("url_yap")
            if num == "0":
                entry = Posts(baslik=box_title, alt_bas=box_altbas, url_yap=box_url_yap, icerik=box_icerik)
                db.session.add(entry)
                db.session.commit()

            else:
                post = Posts.query.filter_by(num=num).first()
                post.baslik = box_title
                post.alt_bas = box_altbas
                post.icerik = box_icerik
                post.url_yap = box_url_yap
                db.session.commit()
                return redirect("/edit/"+num)
        post = Posts.query.filter_by(num=num).first()
        return render_template("edit.html", post=post, num=num)


@app.route("/logout")
def logout():
    session.pop("user")
    return redirect("/dashboard")


@app.route("/delete/<string:num>")
def delete(num):
    kullanici_adi = "hatice"
    kullanici_pass = "habitat"
    if "user" in session and session["user"] == kullanici_adi:
        Posts.query.filter_by(num=num).delete()
        db.session.commit()
    return redirect("dashboard")


@app.route("/delete/dashboard")
def deletedashboard():
    return render_template(("deletedashboard.html"))


if __name__ == '__main__':
    app.run(debug=True)
