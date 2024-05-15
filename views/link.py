
import flask
import sirope
import flask_login

from model.User import User
from model.Link import Link


def get_blprint():
    link_module = flask.blueprints.Blueprint("link_blpr", __name__,
                                        url_prefix="/link",
                                        template_folder="templates/link",
                                        static_folder="static/link")
    syrp = sirope.Sirope()
    return link_module, syrp
...


link_blpr, srp = get_blprint()


@flask_login.login_required
@link_blpr.route("add", methods=["GET", "POST"])
def link_add():
    if flask.request.method == "GET":
        sust = {
            "usr": User.current()
        }

        return flask.render_template("add_link.html", **sust)
    else:
        usr = User.current()
        link_name = flask.request.form.get("edName", "").strip()
        link_url = flask.request.form.get("edURL", "").strip()

        if (not link_name
         or not link_url):
            flask.flash("Faltan datos del enlace.")
            return flask.redirect(flask.url_for("add"))
        ...

        srp.save(Link(usr.email, link_name, link_url))
        flask.flash("Enlace '" + link_name + "' añadido.")
        return flask.redirect("/")
    ...
...


@flask_login.login_required
@link_blpr.route("/delete")
def link_delete():
    link_safe_id = flask.request.args.get("link_id", "").strip()
    link_oid = srp.oid_from_safe(link_safe_id)

    if srp.exists(link_oid):
        srp.delete(link_oid)
        flask.flash("Enlace borrado.")
    else:
        flask.flash("Enlace no encontrado.")
    ...

    return flask.redirect("/")
...
