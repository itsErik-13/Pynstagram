class Photo:
    def __init__(self, url, caption):
        self.__url = url
        self.__caption = caption
        self.__likes = 0
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
    def likes(self):
        return self.__likes
    ...
    
    def like(self):
        self.__likes += 1
    
    def dislike(self):
        self.__likes -= 1

    def get_safe_id(self, srp):
        return srp.safe_from_oid(self.__oid__)
    ...
...
