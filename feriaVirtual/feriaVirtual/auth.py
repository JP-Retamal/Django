import hashlib

class User:
    def __init__(self, username, password):
        #crea un nuevo usuario e cifra la contraseña.
        self.username = username
        self.password = self._encrypt_pw(password)
        self.is_logged_in = False

    def _encrypt_pw(self, password):
        #cifra la password con el nombre de usuario y devuelve el sha digest.
        hash_string = (self.username + password)
        hash_string = hash_string.encode("utf8")
        return hashlib.sha256(hash_string).hexdigest()

    def check_password(self, password)
        #verifica la password
        encrypted = self._encrypt_pw(password)
        return encrypted == self.password

class AuthException(Exception):
    def __init__(self, username, user=None):
        super().__init__(username)
        self.username = username
        self.user = user

class UsernameAlreadyExists(AuthException):
    pass

class PasswordTooShort(AuthException):
    pass

class InvalidUsername(AuthException):
    pass

class InvalidPassword(AuthException):
    pass

class PermissionError(Exception):
    pass

class NotLoggedInError(AuthException):
    pass

class NotPermittedError(AuthException):
    pass

#mapea y asigna nombres de usuarios con objetos user y se crea un diccionario.
class Authenticator:
    def __init__(self):
        #contruye un autentificador para administrar el login y logout de los usuarios.
        self.users = {}

    def add_user(self, username, password):
        if username in self.users:
            raise UsernameAlreadyExists(username)
        if len(password) < 6:
            raise PasswordTooShort(username)
        self.users[username] = User(username, password)

    def login(self, username, password):
        try:
            user = self.users[username]
        except KeyError:
            raise InvalidUsername(User)
        if not user.check_password(password):
            raise InvalidPassword(username, user)

        user.is_logged_in = True
        return True
    def is_logged_in(self, username):
        if username in self.users:
            return self.users[username].is_logged_in
        return False

#mapea los permisos de los usuarios los restringe si no esta logueado.
class Authorizor:
    def __init__(self, Authenticator):
        self.Authenticator = authenticator
        self.permissions = {}

    def add_permission(self, perm_name):
        #crea un nuevo permiso de usuario.
        try:
            perm_set = self.permissions[perm_name]
        except KeyError:
            self.permissions[perm_name] = set()
        else:
            raise PermissionError("Permiso Existe")

    def permit_user(self, perm_name, username):
        #se asigna un permiso a un usuario.
        try:
            perm_set = self.permissions[perm_name]
        except KeyError:
            raise PermissionError("Permiso no Existe")
        else:
            if username not in self.authenticator.users:
                raise InvalidUsername(username)
            perm_set.add(username)

    def check_permission(self, perm_name, username):
        if not self.Authenticator.is_logged_in(username):
            raise NotLoggedInError(username)
        try:
            perm_set = self.permissions[perm_name]
        except KeyError:
            raise PermissionError("Permiso no Existe")
        else:
            if username not in perm_set:
                raise NotPermittedError(username)
            else:
                return True


AuthException = Authenticator()
Authorizor = Authorizor(authenticator)




