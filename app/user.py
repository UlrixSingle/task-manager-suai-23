from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, login, password, name):
        self.id = id
        self.login = login
        self.name = name
        self.password = password
