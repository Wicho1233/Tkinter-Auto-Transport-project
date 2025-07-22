import tkinter as tk
from views.loginView import LoginView
from controllers.loginController import LoginController
from views.menu import MenuView


def abrir_app_principal():
    root = tk.Tk()
    app = MenuView(root)
    root.mainloop()

def main():
   # insertar_usuario("Heriberto", "Hq12#6")
    #insertar_usuario("Admin", "pql28c")
    #insertar_usuario("Yareymi", "asd12ysd5")
    login_root = tk.Tk()
    controller = LoginController()
    LoginView(login_root, controller, abrir_app_principal)
    login_root.mainloop()

if __name__ == "__main__":
    main()
