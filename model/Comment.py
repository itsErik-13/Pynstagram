from datetime import datetime
import sirope

class Comment:
    def __init__(self, usrname, msg, time):
        self.__usrname = usrname
        self.__msg = msg
        self.__time = time
    ...

    @property
    def usrname(self):
        return self.__usrname
    ...
    
    @property
    def msg(self):
        return self.__msg
    ...
    
    @property
    def time(self):
        return self.__time
    ...


    def get_safe_id(self, srp):
        return srp.safe_from_oid(self.__oid__)
    ...
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            usrname=data['_Comment__usrname'],
            msg=data['_Comment__msg'],
            time=data['_Comment__time']
        )
    
    @staticmethod
    def find(srp: sirope.Sirope, usrname, msg: str) -> "Comment":
        return srp.find_first(Comment, lambda u: u.usrname == usrname and u.msg == msg)
...
