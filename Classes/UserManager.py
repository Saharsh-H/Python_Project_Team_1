class UserManager():
    def __init__(self, username, password):
        self._id = username
        self.password = password
        self.packages = []
