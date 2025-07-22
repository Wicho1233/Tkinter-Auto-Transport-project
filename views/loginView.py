import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import BOLD
import util.generic as utl
from views.autotransportesView import AutotransportesApp


class LoginView:
    def __init__(self, root, controller, abrir_app):
        self.root = root
        self.controller = controller
        self.abrir_app = abrir_app

        self.root.title("Iniciar sesion")
        self.root.geometry("800x500")
        self.root.config(width=0, height=0)
        utl.centrar_ventana(self.root,800,500)

        img1 = utl.leer_imagen("./pictures/img1.jpg",(400,600))
        
        frame_logo = tk.Frame(self.root, bd=0, width=300, relief=tk.SOLID, padx=10, pady=10,bg='#f39c12')
        frame_logo.pack(side="left",expand=tk.YES,fill=tk.BOTH)
        label = tk.Label( frame_logo, image=img1,bg='#f39c12' )
        label.place(x=0,y=0,relwidth=1, relheight=1)
        
    
        #frame_form
        frame_form = tk.Frame(self.root, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form.pack(side="right",expand=tk.YES,fill=tk.BOTH)
        #frame_form
        
        #frame_form_top
        frame_form_top = tk.Frame(frame_form,height = 50, bd=0, relief=tk.SOLID,bg='black')
        frame_form_top.pack(side="top",fill=tk.X)
        title = tk.Label(frame_form_top, text="Inicio de sesion",font=('Arial', 30), fg="#f39c12",bg='#fcfcfc',pady=50)
        title.pack(expand=tk.YES,fill=tk.BOTH)
        #end frame_form_top

        #frame_form_fill
        frame_form_fill = tk.Frame(frame_form,height = 50,  bd=0, relief=tk.SOLID,bg='#fcfcfc')
        frame_form_fill.pack(side="bottom",expand=tk.YES,fill=tk.BOTH)

        etiqueta_usuario = tk.Label(frame_form_fill, text="Usuario", font=('Arial', 14) ,fg="#f39c12",bg='#fcfcfc', anchor="w")
        etiqueta_usuario.pack(fill=tk.X, padx=20,pady=5)
        self.usuario = ttk.Entry(frame_form_fill, font=('Arial', 14))
        self.usuario.pack(fill=tk.X, padx=20,pady=10)

        etiqueta_password = tk.Label(frame_form_fill, text="Contraseña", font=('Arial', 14),fg="#f39c12",bg='#fcfcfc' , anchor="w")
        etiqueta_password.pack(fill=tk.X, padx=20,pady=5)
        self.password = ttk.Entry(frame_form_fill, font=('Arial', 14))
        self.password.pack(fill=tk.X, padx=20,pady=10)
        self.password.config(show="*")

        tk.Button(frame_form_fill,text="Iniciar sesion",font=('Arial', 15,BOLD),bg='#f39c12', bd=0,fg="#fff",command=self.login).pack(fill=tk.X, padx=20,pady=20)        
        self.root.mainloop()
        
    def login(self):
        nombreUsuario = self.usuario.get()
        contraUsuario = self.password.get()
        if self.controller.verificar_login(nombreUsuario, contraUsuario):
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso.")
            self.root.destroy()
            self.abrir_app()

        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")


