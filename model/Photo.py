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

    @property
    def url(self):
        return self.__url
    ...
    
    @property
    def caption(self):
        return self.__caption
    ...
    
    @property
    def usrname(self):
        return self.__usrname
    ...
    
    @property
    def likes(self):
        return self.__likes
    ...
    
    @property
    def liked_by(self):
        return self.__liked_by
    ...
    
    @property
    def comments(self):
        return self.__comments
    ...
    
    @caption.setter
    def caption(self, caption):
        self.__caption = caption
        
    def like(self, user):
        if user not in self.liked_by:
            self.__likes += 1
            self.liked_by.append(user)
        else:
            self.__likes -= 1
            self.liked_by.remove(user)
            
    def add_comment(self, comment):
        self.__comments.insert(0,comment.__dict__)
        
    def remove_comment(self, comment):
        self.__comments.remove(comment.__dict__)
        
    def get_comments(self, srp):
        toret = []
        for comment in srp.filter(Comment, lambda u: u.__dict__ in self.__comments):
            toret.append(comment)
        
        toret.sort(key=lambda x: x.time, reverse=True)
        return toret

    def get_safe_id(self, srp):
        return srp.safe_from_oid(self.__oid__)
    ...
    
    @staticmethod
    def find(srp: sirope.Sirope, url: str) -> "Photo":
        return srp.find_first(Photo, lambda u: u.url == url)
...
