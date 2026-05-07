class User:
    __slots__ = ['name', '__role', '_initialized']

    def __init__(self, name, role):
        self.name = name
        self.__role = role
        self._initialized = True

    def __str__(self):
        return f"User(name={self.name}, role={self.role})"

    @property
    def role(self):
        return self.__role

    def __setattr__(self, name, value):
        if hasattr(self, '_initialized') and name.startswith('_User__'):
            raise AttributeError("Cannot modify role directly")
        super().__setattr__(name, value)

    def __delattr__(self, name):
        if name == '_initialized':
            raise AttributeError("Cannot delete _initialized attribute")
        super().__delattr__(name)


if __name__ == "__main__":
    u = User("Alice", "admin")
    
    #delattr(u, "_initialized")
    #setattr(u, '_User__role', "hacker")
    u.name = "Bob"

    print(u)