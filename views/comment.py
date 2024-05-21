
from datetime import datetime
import flask
import sirope
import flask_login
import time
import os

from model.User import User
from model.Photo import Photo
from model.Comment import Comment


def get_blprint():
    comment_module = flask.blueprints.Blueprint("comment_blpr", __name__,
                                        url_prefix="/comment",
                                        template_folder="templates",
                                        static_folder="static")
    syrp = sirope.Sirope()
    return comment_module, syrp
...


comment_blpr, srp = get_blprint()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@flask_login.login_required
@comment_blpr.route("/add", methods=["POST"])
def comment_add():
    
    photo = Photo.find(srp, flask.request.form.get("hiddenUrl"))
    comment = flask.request.form.get("comment", "").strip()
    time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    

    if (not comment):
        flask.flash("Faltan datos del comentario.")
        return flask.redirect("/")
    ...
    
    cm = Comment(User.current().username, comment, time)
    photo.add_comment(cm)
    
    
    srp.save(cm)
    srp.save(photo)
    
    flask.flash("Comentario añadido.")
    return flask.redirect("/")
...

@comment_blpr.route("/modify", methods=["POST"])
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

@flask_login.login_required
@comment_blpr.route("/delete")
def photo_delete():
    comment_safe_id = flask.request.args.get("comment_id", "").strip()
    comment_oid = srp.oid_from_safe(comment_safe_id)

    if srp.exists(comment_oid):
        com = srp.load(comment_oid)
        photo = Photo.find(srp, com.url)
        path = '.' +srp.load(comment_oid).url
        srp.delete(comment_oid)
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
