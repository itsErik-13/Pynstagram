import flask_login
import sirope
import werkzeug.security as safe


class User(flask_login.mixins.UserMixin):
    def __init__(self, name, username, email, pswd):
        self.__name = name
        self.__username = username
        self.__email = email
        self.set_password(pswd)
        self.set_image()
        
        
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
        
    def set_password(self, pswd):
        self.__pswd = safe.generate_password_hash(pswd)

    def get_id(self):
        return self.username
    ...

    def chk_pswd(self, other_pswd):
        return safe.check_password_hash(self.__pswd, other_pswd)
    ...

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
