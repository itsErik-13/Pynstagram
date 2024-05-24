import sirope
from model.Comment import Comment

class Photo:
    def __init__(self, url, caption, usrname):
        self.__url = url
        self.__caption = caption
        self.__usrname = usrname
        self.__likes = 0
        self.__liked_by = []
        self.__comments = []
    ...

    # Devuelve la url de la fotografía
    @property
    def url(self):
        return self.__url
    ...
    # Devuelve lel pie de foto de la fotografía
    @property
    def caption(self):
        return self.__caption
    ...
    
    # Devuelve el nombre del usuario que ha posteado la fotografía
    @property
    def usrname(self):
        return self.__usrname
    ...
    
    # Devuelve el numero de likes de la fotografía
    @property
    def likes(self):
        return self.__likes
    ...
    
    # Devuelve los usuarios que han dado like a la fotografía
    @property
    def liked_by(self):
        return self.__liked_by
    ...
    # Devuelve los comentarios de la fotografía
    @property
    def comments(self):
        return self.__comments
    ...
    
    # Setea el pie de foto
    @caption.setter
    def caption(self, caption):
        self.__caption = caption
        
    # Da/quita like a la fotografía
    def like(self, user):
        if user not in self.liked_by:
            self.__likes += 1
            self.liked_by.append(user)
        else:
            self.__likes -= 1
            self.liked_by.remove(user)
            
    # Anade un nuevo comentario a la lista de comentarios
    def add_comment(self, comment):
        self.__comments.insert(0,comment.__dict__)
        
    # Elimina un comentario de la lista de comentarios
    def remove_comment(self, comment):
        self.__comments.remove(comment.__dict__)
    
    # Devuelve los comentarios de la fotografía, ordenados por tiempo
    def get_comments(self, srp):
        toret = []
        for comment in srp.filter(Comment, lambda u: u.__dict__ in self.__comments):
            toret.append(comment)
        
        toret.sort(key=lambda x: x.time, reverse=True)
        return toret

    # Devuelve el id de la fotografía
    def get_safe_id(self, srp):
        return srp.safe_from_oid(self.__oid__)
    ...
    
    # Busca una fotografía por su url
    @staticmethod
    def find(srp: sirope.Sirope, url: str) -> "Photo":
        return srp.find_first(Photo, lambda u: u.url == url)
...
