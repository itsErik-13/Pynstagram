
import flask
import sirope
import flask_login
import time
import os

from model.User import User
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
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@flask_login.login_required
@photo_blpr.route("/add", methods=["POST"])
def photo_add():
    uploaded_photo = flask.request.files['uploadedPhoto']
    caption = flask.request.form.get("caption", "").strip()
    
    date_string = time.strftime("%Y-%m-%d-%H-%M-%S")
    
    photo_filename = f"{date_string}{uploaded_photo.filename}"
    
    photo_url = f"static/uploaded_photos/{photo_filename}"
    

    if (not uploaded_photo or not caption):
        flask.flash("Faltan datos de la fotografía.")
        return flask.redirect("/")
    ...
    uploaded_photo.save(photo_url)
    photo_url = '/' + photo_url
    ph = Photo(photo_url,caption, User.current().username)
    
    User.current().upload_photo(photo_url)
    
    srp.save(ph)
    srp.save(User.current())
    
    flask.flash("Fotografía añadida.")
    return flask.redirect("/")
...

@photo_blpr.route("/modify", methods=["POST"])
def photo_modify():
    
    photo = Photo.find(srp, flask.request.form.get("hiddenUrl"))
    caption = flask.request.form.get("modifyCaption")
    if not caption:
        flask.flash(f"No se ha modificado nada")
        return flask.redirect("/")
    
    photo.caption = caption
    srp.save(photo)
    return flask.redirect("/")
...

@photo_blpr.route("/like", methods=["POST"])
def photo_like():
    
    username = User.current().username
    photo = Photo.find(srp, flask.request.form.get("hiddenUrl"))
    photo.like(username)
    srp.save(photo)
    return flask.redirect("/")
...


@flask_login.login_required
@photo_blpr.route("/delete")
def photo_delete():
    photo_safe_id = flask.request.args.get("photo_id", "").strip()
    photo_oid = srp.oid_from_safe(photo_safe_id)

    if srp.exists(photo_oid):
        path = '.' +srp.load(photo_oid).url
        srp.delete(photo_oid)
        User.current().uploaded_photos.remove(path[1:])
        print(User.current().uploaded_photos)
        srp.save(User.current())
        if os.path.exists(path):
            # Elimina el archivo del sistema de archivos
            os.remove(path)
        flask.flash("Fotografía borrada.")
    else:
        flask.flash("Fotografía no encontrada.")
    ...

    return flask.redirect("/")
...
