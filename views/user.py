# Links (c) 2024 Baltasar MIT License <baltasarq@gmail.com>


import flask
import sirope


from model.User import User


def get_blprint():
    usr_module = flask.blueprints.Blueprint("user_blpr", __name__,
                                        url_prefix="/user",
                                        template_folder="templates",
                                        static_folder="static")
    syrp = sirope.Sirope()
    return usr_module, syrp
...


user_blpr, srp = get_blprint()


@user_blpr.route("/add", methods=["POST"])
def user_add():
    usr_name = flask.request.form.get("registerName")
    usr_email = flask.request.form.get("registerEmail")
    usr_username = flask.request.form.get("registerUsername")
    usr_passw = flask.request.form.get("registerPassword")
    usr_passw_repeat = flask.request.form.get("registerRepeatPassword")
    

    if (not usr_email
     or not usr_passw or not usr_username or not usr_name):
        flask.flash(f"Faltan credenciales... {usr_email=} , {usr_passw=} , {usr_username=} , {usr_name=}")
        return flask.redirect("/")
    ...

    if User.find(srp, usr_name) or User.find(srp, usr_email):
        flask.flash("Usuario ya registrado, haga el login.")
        return flask.redirect("/")
    ...
    
    if (usr_passw != usr_passw_repeat):
        flask.flash("Las contraseñas no coinciden.")
        return flask.redirect("/")

    usr = User(usr_name, usr_username, usr_email, usr_passw)
    srp.save(usr)
    flask.flash("Ahora ya puedes entrar con tus nuevas credenciales.")
    return flask.redirect("/")
...

@user_blpr.route("/modify", methods=["POST"])
def user_modify():
    usr_name = flask.request.form.get("modifyName")
    usr_email = flask.request.form.get("modifyEmail")
    usr_username = flask.request.form.get("modifyUsername")
    usr_passw = flask.request.form.get("modifyPassword")
    usr_passw_repeat = flask.request.form.get("modifyRepeatPassword")
    
    if (not usr_email and not usr_passw and not usr_username and not usr_name):
        flask.flash(f"No se ha modificado nada")
        return flask.redirect("/")
    
    if usr_name:
        User.current().set_name(usr_name)
        
    if usr_username and User.find(srp, usr_username):
        flask.flash("Usuario ya registrado, prueba con otro user.")
        return flask.redirect("/")
    elif not usr_username:
        usr_username = User.current().username
    else:
        User.current().set_username(usr_username)
    ...
    
    if usr_email and User.find(srp, usr_email):
        flask.flash(f"Usuario ya registrado, prueba con otro email. {usr_email=}")
        return flask.redirect("/")
    elif not usr_email:
        usr_email = User.current().email
    else:
        User.current().set_email(usr_email)
    ...
    
    if (usr_passw and usr_passw_repeat and usr_passw != usr_passw_repeat):
        flask.flash("Las contraseñas no coinciden.")
        return flask.redirect("/")
    elif usr_passw and usr_passw_repeat:
        User.current().set_password(usr_passw)
    ...
    
    srp.save(User.current())
    flask.flash("Ahora ya puedes entrar con tus nuevas credenciales.")
    return flask.redirect("/logout")
...
