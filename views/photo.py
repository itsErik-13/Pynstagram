
import flask
import sirope
import flask_login
import time

from model.User import User
from model.Link import Link
from model.Photo import Photo


def get_blprint():
    photo_module = flask.blueprints.Blueprint("photo_blpr", __name__,
                                        url_prefix="/photo",
                                        template_folder="templates",
                                        static_folder="static")
    syrp = sirope.Sirope()
    return photo_module, syrp
...


photo_blpr, srp = get_blprint()


@flask_login.login_required
@photo_blpr.route("/add", methods=["POST"])
def photo_add():
    uploaded_photo = flask.request.files['uploadedPhoto']
    caption = flask.request.form.get("caption", "").strip()
    
    date_string = time.strftime("%Y-%m-%d-%H-%M")
    
    photo_filename = f"{date_string}{uploaded_photo.filename}"
    
    photo_url = f"static/uploaded_photos/{photo_filename}"
    
    print(photo_filename)
    

    if (not uploaded_photo or not caption):
        flask.flash("Faltan datos de la fotografía.")
        return flask.redirect("/")
    ...
    uploaded_photo.save(photo_url)
    ph = Photo(photo_url,caption)
    
    srp.save(ph)
    flask.flash("Fotografía añadida.")
    return flask.redirect("/")
...


@flask_login.login_required
@photo_blpr.route("/delete")
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
