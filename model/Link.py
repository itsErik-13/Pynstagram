class Link:
    def __init__(self, email, name, url):
        self.__email = email
        self.__name = name
        self.__url = url
    ...

    @property
    def usr_email(self):
        return self.__email
    ...

    @property
    def name(self):
        return self.__name
    ...

    @property
    def url(self):
        return self.__url
    ...

    def get_safe_id(self, srp):
        return srp.safe_from_oid(self.__oid__)
    ...

    def __str__(self):
        return f"{self.name}: '{self.url}' (de {self.usr_email})"
    ...
...
