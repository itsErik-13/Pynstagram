import flask_login
import sirope
import werkzeug.security as safe
from model.Photo import Photo


class User(flask_login.mixins.UserMixin):
    def __init__(self, name, username, email, pswd):
        self.__name = name
        self.__username = username
        self.__email = email
        self.set_password(pswd)
        self.__profile_picture = "/static/profile_pictures/default_pfp.png"
        self.__uploaded_photos = []
        self.__commented_photos = []
        self.__liked_photos = []
        
    # Devuelve el nombre del usuario
    @property
    def name(self):
        return self.__name
    ...
    
    # Devuelve el nombre de usuario
    @property
    def username(self):
        return self.__username
    ...
    
    # Devuelve el email
    @property
    def email(self):
        return self.__email
    ...
    
    # Devuelve la url de la imagen de perfil
    @property
    def profile_picture(self):
        return self.__profile_picture
    ...
    
    # Devuelve la lista de url de fotos subidas
    @property
    def uploaded_photos(self):
        return self.__uploaded_photos
    ...
    
    # Devuelve la lista de url de fotos comentadas
    @property
    def commented_photos(self):
        for photo in self.__commented_photos:
            if sirope.Sirope().find_first(Photo, lambda p: p.url == photo) == None:
                self.__commented_photos.remove(photo)
        sirope.Sirope().save(self)
        return self.__commented_photos
    ...
    
    # Devuelve la lista de url de fotos likeadas
    @property
    def liked_photos(self):
        for photo in self.__liked_photos:
            if sirope.Sirope().find_first(Photo, lambda p: p.url == photo) == None:
                self.__liked_photos.remove(photo)
        sirope.Sirope().save(self)
        return self.__liked_photos
    ...
        
    # Permite setear la contraseña
    def set_password(self, pswd):
        self.__pswd = safe.generate_password_hash(pswd)
        
    # Permite setear el nombre     
    def set_name(self, name):
        self.__name = name
        
    # Permite setear el nombre de usuario
    def set_username(self, username):
        self.__username = username
    
    # Permite setear el email
    def set_email(self, email):
        self.__email = email
        
        
    # Añade una url de foto a la lista de fotos subidas
    def upload_photo(self, photo):
        self.__uploaded_photos.append(photo)
        
    # Permite cambiar la url de la imagen de perfil
    def set_profile_picture(self, profile_picture):
        self.__profile_picture = f"/static/profile_pictures/{profile_picture}"
        
    # Añade una url de foto a la lista de fotos comentadas
    def add_commented_photo(self, photo):
        self.__commented_photos.append(photo)
        
    # Añade una url de foto a la lista de fotos likeadas
    def add_liked_photo(self, photo):
        if photo not in self.__liked_photos:
            self.__liked_photos.append(photo)
        else:
            self.__liked_photos.remove(photo)
        
    
    # Elimina una url de foto de la lista de fotos comentadas
    def remove_commented_photo(self, photo):
        try:
            self.__commented_photos.remove(photo)
        except ValueError:
            print("Error")

    # Devuelve el id
    def get_id(self):
        return self.username
    ...
    
    # Devuelve el id encriptado para sirope
    def get_safe_id(self, srp):
        return srp.safe_from_oid(self.__oid__)
    ...


    # Comprueba la contraseña
    def chk_pswd(self, other_pswd):
        return safe.check_password_hash(self.__pswd, other_pswd)
    ...
    
    
    # Modifica el usuario
    def modify(self, name, username, email, pswd):
        self.__name = name
        self.__username = username
        self.__email = email
        self.set_password(pswd) if pswd is not None else None

    # Devuelve el usuario actual
    @staticmethod
    def current():
        usr = flask_login.current_user

        if usr.is_anonymous:
            flask_login.logout_user()
            usr = None
        ...

        return usr
    ...
  
    # Busca un usuario por su nombre de usuario o email
    @staticmethod
    def find(srp: sirope.Sirope, data: str) -> "User":
        return srp.find_first(User, lambda u: u.username == data or u.email == data)
    ...
...
