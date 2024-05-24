import sirope

class Comment:
    def __init__(self, usrname, msg, time):
        self.__usrname = usrname
        self.__msg = msg
        self.__time = time
    ...

    # Devuelve el usuario que ha escrito el comentario
    @property
    def usrname(self):
        return self.__usrname
    ...
    
    # Devuelve el contenido del comentario
    @property
    def msg(self):
        return self.__msg
    ...
    # Devuelve la hora en la que se ha escrito el comentario
    @property
    def time(self):
        return self.__time
    ...

    # Devuelve el id del comentario en la base de datos
    def get_safe_id(self, srp):
        return srp.safe_from_oid(self.__oid__)
    ...
    
    # Permite convertir un __dict__ en un Comment
    @classmethod
    def from_dict(cls, data):
        return cls(
            usrname=data['_Comment__usrname'],
            msg=data['_Comment__msg'],
            time=data['_Comment__time']
        )
    
    # Busca un comentario en la base de datos
    @staticmethod
    def find(srp: sirope.Sirope, usrname, msg: str) -> "Comment":
        return srp.find_first(Comment, lambda u: u.usrname == usrname and u.msg == msg)
...
