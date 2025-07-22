import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import BOLD
import util.generic as utl
from views.autotransportesView import AutotransportesApp
from views.autotanquesView import AutotanquesApp


class MenuView:
    def __init__(self, root):
        self.root = root
      
        self.root.title("Selecionar compañia")
        self.root.geometry("800x500")
        self.root.config(width=0, height=0)
        utl.centrar_ventana(self.root,800,500)

        img2 = utl.leer_imagen("./pictures/img2.jpg",(400,600))
        
        frame_logo = tk.Frame(self.root, bd=0, width=300, relief=tk.SOLID, padx=10, pady=10,bg='')
        frame_logo.pack(side="left",expand=tk.YES,fill=tk.BOTH)
        label = tk.Label( frame_logo, image=img2,bg='#f39c12' )
        label.place(x=0,y=0,relwidth=1, relheight=1)
        
    
        #frame_form
        frame_form = tk.Frame(self.root, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form.pack(side="right",expand=tk.YES,fill=tk.BOTH)
        #frame_form
        
        #frame_form_top
        frame_form_top = tk.Frame(frame_form,height = 50, bd=0, relief=tk.SOLID,bg='black')
        frame_form_top.pack(side="top",fill=tk.X)
        title = tk.Label(frame_form_top, text="Seleccionar Compañia",font=('Arial', 30), fg="#f39c12",bg='#fcfcfc',pady=50)
        title.pack(expand=tk.YES,fill=tk.BOTH)
        #end frame_form_top

        #frame_form_fill
        frame_form_fill = tk.Frame(frame_form,height = 50,  bd=0, relief=tk.SOLID,bg='#fcfcfc')
        frame_form_fill.pack(side="bottom",expand=tk.YES,fill=tk.BOTH)

        #Botones 

        etiqueta_tanque = tk.Label(frame_form_fill, text="Autotransportes Cardenas", font=('Arial', 14) ,fg="#f39c12",bg='#fcfcfc', anchor="w")
        etiqueta_tanque.pack(fill=tk.X, padx=20,pady=5)
        tk.Button(frame_form_fill,text="Cardenas",font=('Arial', 15,BOLD),bg='#f39c12', bd=0,fg="#fff",command=self.empresaCardenas).pack(fill=tk.X, padx=20,pady=10)        
        
        etiqueta_partes = tk.Label(frame_form_fill, text="Autotanques Tara del centro", font=('Arial', 14),fg="#f39c12",bg='#fcfcfc' , anchor="w")
        etiqueta_partes.pack(fill=tk.X, padx=20,pady=5)
        tk.Button(frame_form_fill,text="Tara",font=('Arial', 15,BOLD),bg='#f39c12', bd=0,fg="#fff",command=self.empresaTara).pack(fill=tk.X, padx=20,pady=10) 
       
        self.root.mainloop()
    
    def empresaCardenas(self):
         self.root.destroy()  
         root = tk.Tk()
         app = AutotransportesApp(root)
         root.mainloop()
        
    def empresaTara(self):
         self.root.destroy()  
         root = tk.Tk()
         app = AutotanquesApp(root)
         root.mainloop()