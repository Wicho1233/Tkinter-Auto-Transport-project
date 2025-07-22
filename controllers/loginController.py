from data.db_userRepo import verificar_usuario

class LoginController:
    def verificar_login(self, username, password):
        return verificar_usuario(username, password) is not None
