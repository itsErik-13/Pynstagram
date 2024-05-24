
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

# Permite añadir un comentario
@flask_login.login_required
@comment_blpr.route("/add", methods=["POST"])
def comment_add():
    
    comment = flask.request.form.get("comment", "").strip()

    if (not comment):
        flask.flash("Faltan datos del comentario.")
        return flask.redirect("/")
    ...
    photo = Photo.find(srp, flask.request.form.get("hiddenUrl"))
    time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    
    cm = Comment(User.current().username, comment, time)
    photo.add_comment(cm)
    User.current().add_commented_photo(photo.url)
    
    srp.save(cm)
    srp.save(photo)
    srp.save(User.current())
    
    flask.flash("Comentario añadido.")
    return flask.redirect("/")
...

# Permite borrar un comentario
@flask_login.login_required
@comment_blpr.route("/delete")
def photo_delete():
    comment_safe_id = flask.request.args.get("comment_id", "").strip()
    comment_oid = srp.oid_from_safe(comment_safe_id)
    
    photo_safe_id = flask.request.args.get("photo_id", "").strip()
    photo_oid = srp.oid_from_safe(photo_safe_id)
    

    if srp.exists(comment_oid) and srp.exists(photo_oid):
        com = srp.load(comment_oid)
        photo = srp.load(photo_oid)
        photo.remove_comment(com)
        User.current().remove_commented_photo(photo.url)
        srp.save(photo)
        srp.delete(comment_oid)
        srp.save(User.current())
        flask.flash("Comentario borrado.")
    else:
        flask.flash("Error, comentario no borrado.")
    ...
    return flask.redirect("/")
...
