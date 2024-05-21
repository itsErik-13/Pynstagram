import flask_login
import sirope
import werkzeug.security as safe


class User(flask_login.mixins.UserMixin):
    def __init__(self, name, username, email, pswd):
        self.__name = name
        self.__username = username
        self.__email = email
        self.set_password(pswd)
        self.__profile_picture = "/static/profile_pictures/default_pfp.png"
        self.__uploaded_photos = []
        self.__commented_photos = []
        
        
    @property
    def name(self):
        return self.__name
    ...
    @property
    def username(self):
        return self.__username
    ...
    @property
    def email(self):
        return self.__email
    ...
    @property
    def profile_picture(self):
        return self.__profile_picture
    ...
    
    @property
    def uploaded_photos(self):
        return self.__uploaded_photos
    ...
    
    @property
    def commented_photos(self):
        return self.__commented_photos
    ...
        
    def set_password(self, pswd):
        self.__pswd = safe.generate_password_hash(pswd)
        
    def set_name(self, name):
        self.__name = name
        
    def set_username(self, username):
        self.__username = username
    
    def set_email(self, email):
        self.__email = email
        
        
    def upload_photo(self, photo):
        self.__uploaded_photos = self.__uploaded_photos + [photo]
        
    def set_profile_picture(self, profile_picture):
        self.__profile_picture = f"/static/profile_pictures/{profile_picture}"
    
    def add_commented_photo(self, photo):
        self.__commented_photos = self.__commented_photos + [photo]
        print(self.__commented_photos)
        
    
        
    def remove_commented_photo(self, photo):
        try:
            self.__commented_photos.remove(photo)
        except ValueError:
            pass

    def get_id(self):
        return self.username
    ...
    
    def get_safe_id(self, srp):
        return srp.safe_from_oid(self.__oid__)
    ...

    def chk_pswd(self, other_pswd):
        return safe.check_password_hash(self.__pswd, other_pswd)
    ...
    
    def modify(self, name, username, email, pswd):
        self.__name = name
        self.__username = username
        self.__email = email
        self.set_password(pswd) if pswd is not None else None

    @staticmethod
    def current():
        usr = flask_login.current_user

        if usr.is_anonymous:
            flask_login.logout_user()
            usr = None
        ...

        return usr
    ...

    @staticmethod
    def find(srp: sirope.Sirope, username: str) -> "User":
        return srp.find_first(User, lambda u: u.username == username)
    ...
    
    @staticmethod
    def find(srp: sirope.Sirope, data: str) -> "User":
        return srp.find_first(User, lambda u: u.username == data or u.email == data)
    ...
...
