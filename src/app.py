import json
import flask
import flask_login
import sirope
import os

from model.User import User
from model.Photo import Photo

from views.user import user_blpr
from views.photo import photo_blpr
from views.comment import comment_blpr

BASE_DIR = '.'  

if not os.path.exists(BASE_DIR + "/static/uploaded_photos"):
    os.makedirs(BASE_DIR + "/static/uploaded_photos")

def create_app():
    flapp = flask.Flask(__name__)
    sirop = sirope.Sirope()
    login = flask_login.login_manager.LoginManager()

    flapp.config.from_file("instance/config.json", json.load)
    login.init_app(flapp)
    flapp.register_blueprint(user_blpr)
    flapp.register_blueprint(photo_blpr)
    flapp.register_blueprint(comment_blpr)
    return flapp, sirop, login
...


app, srp, lm = create_app()


@lm.unauthorized_handler
def unauthorized_handler():
    flask.flash("unauthorized")
    return flask.redirect("/")
...


@lm.user_loader
def user_loader(email: str) -> User:
    return User.find(srp, email)
...


@app.route("/favicon.ico")
def get_fav_icon():
    return app.send_static_file("icons/favicon.ico")
...


@app.route("/login", methods=["POST"])
def login():
    if User.current():
        flask_login.logout_user()
        flask.flash("Ha pasado algo extraño. Por favor, entra de nuevo.")
        return flask.redirect("/")
    ...

    usr_username_email = flask.request.form.get("loginName", "").strip()
    usr_pswd = flask.request.form.get("loginPassword", "").strip()

    if (not usr_username_email
     or not usr_pswd):
        flask.flash("Faltan credenciales")
        return flask.redirect("/")
    ...

    usr = User.find(srp, usr_username_email)

    if (not usr
     or not usr.chk_pswd(usr_pswd)):
        flask.flash("Credenciales incorrectas: ¿has hecho el registro?")
        return flask.redirect("/")
    ...

    flask_login.login_user(usr)
    flask.flash("Login realizado.")
    return flask.redirect("/")
...


@flask_login.login_required
@app.route("/logout")
def logout():
    flask_login.logout_user()
    return flask.redirect("/")
...

@flask_login.login_required
@app.route("/account/<nombre_usuario>")
def account(nombre_usuario):
    acc_usr = User.find(srp, nombre_usuario)
    
    
    
    if acc_usr:
        sust = {
        "usr" : User.current(),
        "acc_usr": acc_usr,
        "srp": srp,
        "list_images" : srp.filter(Photo, lambda l: l.usrname == acc_usr.username)
        }
        return flask.render_template("account.html", **sust)
    else:
        flask.flash("El usuario buscado no existe.")
        return flask.redirect("/")
...




@app.route("/")
def main():
    usr = User.current()
    image_list = []
    image_list = srp.load_all(Photo)

    sust = {
        "usr": usr,
        "srp": srp,
        "image_list": image_list
    }

    return flask.render_template("index.html", **sust)
...


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
...
