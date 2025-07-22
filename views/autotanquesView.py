import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import simpledialog
from converter.autotanquesConverter import generar_reporte_mal_estado_general
from data.db_autotanquesRepo import *

class AutotanquesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Mantenimiento - Autotanques Tara")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f0f0")
        self.modo = "Consultar"
        self.adaptacion_actual = None
        
        self.crear_widgets()
    
    def crear_widgets(self):
        main_frame = tk.Frame(self.root, padx=20, pady=20, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título principal
        tk.Label(main_frame, text="Sistema de Mantenimiento", 
                font=("Arial", 18, "bold"), bg="#f0f0f0").grid(row=0, column=0, columnspan=4, pady=10)
        
        tk.Label(main_frame, text="Autotanques Tara", 
                font=("Arial", 14), bg="#f0f0f0").grid(row=1, column=0, columnspan=4, pady=5)
        
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).grid(row=2, column=0, columnspan=4, pady=10, sticky="ew")
        
        # Frame de controles superiores
        control_frame = tk.Frame(main_frame, bg="#f0f0f0")
        control_frame.grid(row=3, column=0, columnspan=4, pady=10, sticky="ew")
        
        # Botón para agregar nuevo mantenimiento
        agregar_btn = tk.Button(control_frame, text="+ Nuevo Mantenimiento", 
                              command=self.mostrar_formulario_agregar,
                              bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        agregar_btn.pack(side=tk.LEFT, padx=5)
        
        # Frame de búsqueda
        search_frame = tk.Frame(control_frame, bg="#f0f0f0")
        search_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(search_frame, text="Buscar por TR:", bg="#f0f0f0").pack(side=tk.LEFT)
        self.buscar_entry = tk.Entry(search_frame, width=15)
        self.buscar_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Buscar", command=self.buscar_por_tr).pack(side=tk.LEFT)
        
        # Botones para modo
        mode_frame = tk.Frame(control_frame, bg="#f0f0f0")
        mode_frame.pack(side=tk.RIGHT)
        
        self.consultar_btn = tk.Button(mode_frame, text="Modo Consulta", 
                                     command=lambda: self.cambiar_modo("Consultar"),
                                     bg="#2196F3", fg="white")
        self.consultar_btn.pack(side=tk.LEFT, padx=5)
        
        self.editar_btn = tk.Button(mode_frame, text="Modo Edición", 
                                  command=lambda: self.cambiar_modo("Editar"),
                                  bg="#FF9800", fg="white")
        self.editar_btn.pack(side=tk.LEFT, padx=5)
        
        # Botón para regresar al menú principal
        regresar_btn = tk.Button(control_frame, text="Regresar al Menú", 
                               command=self.regresar_al_menu,
                               bg="#9C27B0", fg="white", font=("Arial", 10, "bold"))
        regresar_btn.pack(side=tk.RIGHT, padx=5)
        
        # Botón para generar reporte general de mal estado
        report_frame = tk.Frame(main_frame, bg="#f0f0f0")
        report_frame.grid(row=4, column=0, columnspan=4, pady=10)
        
        pdf_btn = tk.Button(report_frame, text="Generar Reporte General de Mal Estado", 
                          command=lambda: self.generar_reporte_mal_estado(),
                          bg="#FF5252", fg="white", font=("Arial", 10, "bold"))
        pdf_btn.pack(side=tk.LEFT, padx=5)
        
        pdf_tr_btn = tk.Button(report_frame, text="Generar Reporte por TR", 
                             command=lambda: self.generar_reporte_mal_estado_por_tr(),
                             bg="#FF5252", fg="white", font=("Arial", 10, "bold"))
        pdf_tr_btn.pack(side=tk.LEFT, padx=5)
        
        # Notebook (pestañas)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=5, column=0, columnspan=4, pady=20, sticky="nsew")
        
        self.tabs = {}
        adaptaciones = ["Carrocería", "Motor", "TrenMotriz", "Tanque", "Doli"]
        for nombre in adaptaciones:
            tab = tk.Frame(self.notebook, bg="#f0f0f0")
            self.notebook.add(tab, text=nombre)
            self.tabs[nombre] = tab
        
        # Frame flotante para formulario de agregar
        self.formulario_agregar = tk.Toplevel(self.root)
        self.formulario_agregar.title("Agregar Nuevo Mantenimiento")
        self.formulario_agregar.geometry("600x500")
        self.formulario_agregar.withdraw()
        self.crear_formulario_agregar()
        
        # Mostrar la primera adaptación por defecto
        self.adaptacion_actual = adaptaciones[0]
        self.mostrar_adaptacion(self.adaptacion_actual)
        
        # Configurar evento para cambiar de pestaña
        self.notebook.bind("<<NotebookTabChanged>>", self.cambiar_pestana)
        
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)

    def regresar_al_menu(self):
        """Cierra la ventana actual y regresa al menú principal"""
        self.root.destroy()
        from views.menu import MenuView
        root = tk.Tk()
        MenuView(root)

    def cambiar_pestana(self, event):
        """Maneja el cambio de pestaña en el notebook"""
        tab_index = self.notebook.index(self.notebook.select())
        self.adaptacion_actual = self.notebook.tab(tab_index, "text")
        self.mostrar_adaptacion(self.adaptacion_actual)
        
    def crear_formulario_agregar(self):
        form_frame = tk.Frame(self.formulario_agregar, padx=20, pady=20, bg="#f0f0f0")
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(form_frame, text="Agregar Nuevo Mantenimiento", 
                font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)
        
        # Campos del formulario
        campos = [
            ("Tr:", "entry"),
            ("Tipo:", "combobox", ["Adaptación", "División"]),
            ("Adaptación/División:", "combobox", ["Carrocería", "Motor", "TrenMotriz", "Tanque", "Doli"]),
            ("Número (solo división):", "entry"),
            ("Mantenimiento:", "entry"),
            ("Fecha:", "entry"),
            ("KM Actual:", "entry"),
            ("KM Mantenimiento:", "entry"),
            ("Costo:", "entry"),
            ("Estado:", "combobox", ["Buen estado", "Mal estado"])
        ]
        
        self.campos_formulario = {}
        
        for i, (label, tipo, *opciones) in enumerate(campos):
            frame = tk.Frame(form_frame, bg="#f0f0f0")
            frame.pack(fill=tk.X, pady=5)
            
            tk.Label(frame, text=label, width=25, anchor="e", bg="#f0f0f0").pack(side=tk.LEFT)
            
            if tipo == "entry":
                entry = tk.Entry(frame, width=30)
                entry.pack(side=tk.LEFT)
                self.campos_formulario[label.replace(":", "").lower().replace(" ", "_")] = entry
            elif tipo == "combobox":
                combobox = ttk.Combobox(frame, values=opciones[0], width=27)
                combobox.pack(side=tk.LEFT)
                if label == "Estado:":
                    combobox.set("Buen estado")
                elif label == "Tipo:":
                    combobox.set("Adaptación")
                self.campos_formulario[label.replace(":", "").lower().replace(" ", "_")] = combobox
        
        # Configurar evento para cambiar tipo
        self.campos_formulario["tipo"].bind("<<ComboboxSelected>>", self.actualizar_campos_por_tipo)
        
        # Botones
        button_frame = tk.Frame(form_frame, bg="#f0f0f0")
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Guardar", 
                 command=self.guardar_nuevo_mantenimiento,
                 bg="#4CAF50", fg="white", width=15).pack(side=tk.LEFT, padx=10)
        
        tk.Button(button_frame, text="Cancelar", 
                 command=self.formulario_agregar.withdraw,
                 bg="#F44336", fg="white", width=15).pack(side=tk.LEFT, padx=10)

    def actualizar_campos_por_tipo(self, event=None):
        tipo = self.campos_formulario["tipo"].get()
        if tipo == "División":
            self.campos_formulario["adaptación/división"].config(values=["Tanque", "Doli"])
        else:
            self.campos_formulario["adaptación/división"].config(values=["Carrocería", "Motor", "TrenMotriz", "Tanque", "Doli"])
        
        # Establecer la adaptación actual si es modo adaptación
        if tipo == "Adaptación":
            self.campos_formulario["adaptación/división"].set(self.adaptacion_actual)

    def mostrar_formulario_agregar(self):
        for campo in self.campos_formulario.values():
            if isinstance(campo, tk.Entry):
                campo.delete(0, tk.END)
            elif isinstance(campo, ttk.Combobox):
                if campo['values'][0] == "Buen estado":
                    campo.set("Buen estado")
                elif campo['values'][0] == "Adaptación":
                    campo.set("Adaptación")
                else:
                    campo.set("")
        
        # Establecer la adaptación actual en el combobox
        self.campos_formulario["tipo"].set("Adaptación")
        self.actualizar_campos_por_tipo()
        
        self.formulario_agregar.deiconify()
        self.formulario_agregar.lift()

    def guardar_nuevo_mantenimiento(self):
        try:
            tr = self.campos_formulario["tr"].get()
            tipo = self.campos_formulario["tipo"].get()
            nombre = self.campos_formulario["adaptación/división"].get()
            numero = self.campos_formulario["número_(solo_división)"].get() if tipo == "División" else None
            mantenimiento = self.campos_formulario["mantenimiento"].get()
            fechaMant = self.campos_formulario["fecha"].get()
            kiloActu = self.campos_formulario["km_actual"].get()
            kiloMant = self.campos_formulario["km_mantenimiento"].get()
            costo = self.campos_formulario["costo"].get()
            estado = self.campos_formulario["estado"].get()
            
            if not all([tr, tipo, nombre, mantenimiento, fechaMant, kiloActu, kiloMant, costo, estado]):
                messagebox.showerror("Error", "Todos los campos obligatorios deben ser completados")
                return
                
            if tipo == "División" and not numero:
                messagebox.showerror("Error", "El número es obligatorio para divisiones")
                return
                
            try:
                tr = int(tr)
                kiloActu = int(kiloActu)
                kiloMant = int(kiloMant)
                costo = float(costo)
                if tipo == "División":
                    numero = int(numero)
            except ValueError:
                messagebox.showerror("Error", "Tr, Número, KM Actual, KM Mantenimiento y Costo deben ser números válidos")
                return
                
            if tipo == "Adaptación":
                insertar_mantenimiento_adaptacion(tr, nombre, mantenimiento, fechaMant, kiloActu, kiloMant, costo, estado)
            else:
                insertar_mantenimiento_division(tr, numero, nombre, mantenimiento, fechaMant, kiloActu, kiloMant, costo, estado)
            
            # Actualizar la vista actual
            if tipo == "Adaptación" and nombre == self.adaptacion_actual:
                self.crear_tabla(self.tabs[nombre], nombre)
            elif tipo == "División" and nombre in ["Tanque", "Doli"] and nombre == self.adaptacion_actual:
                self.crear_tabla(self.tabs[nombre], nombre)
            
            self.formulario_agregar.withdraw()
            messagebox.showinfo("Éxito", "Mantenimiento agregado correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al guardar: {str(e)}")

    def mostrar_adaptacion(self, nombreAdaptacion):
        self.crear_tabla(self.tabs[nombreAdaptacion], nombreAdaptacion)

    def generar_reporte_mal_estado(self):
        """Genera y muestra el PDF general de mal estado"""
        success, result = generar_reporte_mal_estado_general()
        if success:
            messagebox.showinfo("Éxito", f"Reporte de mal estado generado exitosamente:\n{result}")
        else:
            messagebox.showwarning("Información", result)

    def generar_reporte_mal_estado_por_tr(self):
        """Genera reporte de mal estado para un TR específico"""
        tr = simpledialog.askinteger("Reporte por TR", "Ingrese el TR para generar el reporte:")
        if tr is not None:
            success, result = generar_reporte_mal_estado_general(tr)
            if success:
                messagebox.showinfo("Éxito", f"Reporte de mal estado para TR {tr} generado exitosamente:\n{result}")
            else:
                messagebox.showwarning("Información", result)

    def crear_tabla(self, parent, nombre):
        for widget in parent.winfo_children():
            widget.destroy()

        main_tab_frame = tk.Frame(parent, bg="#f0f0f0")
        main_tab_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        table_frame = tk.Frame(main_tab_frame, bg="#f0f0f0")
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configurar columnas según si es adaptación o división
        if nombre in ["Tanque", "Doli"]:
            columns = ("tr", "numero", "mantenimiento", "fechaMant", "kiloActu", "kiloMant", "costo", "estado")
        else:
            columns = ("tr", "mantenimiento", "fechaMant", "kiloActu", "kiloMant", "costo", "estado")
        
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # Configurar encabezados según el tipo
        if nombre in ["Tanque", "Doli"]:
            self.tree.heading("tr", text="Tr")
            self.tree.heading("numero", text="Número")
            self.tree.heading("mantenimiento", text="Mantenimiento")
            self.tree.heading("fechaMant", text="Fecha")
            self.tree.heading("kiloActu", text="KM Actual")
            self.tree.heading("kiloMant", text="KM Mant.")
            self.tree.heading("costo", text="Costo")
            self.tree.heading("estado", text="Estado")
            
            self.tree.column("tr", width=80, anchor=tk.CENTER)
            self.tree.column("numero", width=80, anchor=tk.CENTER)
            self.tree.column("mantenimiento", width=180)
            self.tree.column("fechaMant", width=100, anchor=tk.CENTER)
            self.tree.column("kiloActu", width=90, anchor=tk.CENTER)
            self.tree.column("kiloMant", width=90, anchor=tk.CENTER)
            self.tree.column("costo", width=90, anchor=tk.CENTER)
            self.tree.column("estado", width=110, anchor=tk.CENTER)
        else:
            self.tree.heading("tr", text="Tr")
            self.tree.heading("mantenimiento", text="Mantenimiento")
            self.tree.heading("fechaMant", text="Fecha")
            self.tree.heading("kiloActu", text="KM Actual")
            self.tree.heading("kiloMant", text="KM Mant.")
            self.tree.heading("costo", text="Costo")
            self.tree.heading("estado", text="Estado")
            
            self.tree.column("tr", width=80, anchor=tk.CENTER)
            self.tree.column("mantenimiento", width=200)
            self.tree.column("fechaMant", width=120, anchor=tk.CENTER)
            self.tree.column("kiloActu", width=100, anchor=tk.CENTER)
            self.tree.column("kiloMant", width=100, anchor=tk.CENTER)
            self.tree.column("costo", width=100, anchor=tk.CENTER)
            self.tree.column("estado", width=120, anchor=tk.CENTER)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Obtener datos según el tipo
        if nombre in ["Tanque", "Doli"]:
            datos = obtener_mantenimientos_por_division(nombre)
            for dato in datos:
                self.tree.insert("", tk.END, values=dato)
        else:
            datos = obtener_mantenimientos_por_nombreAdaptacion(nombre)
            for dato in datos:
                self.tree.insert("", tk.END, values=dato)
        
        form_frame = tk.LabelFrame(main_tab_frame, text="Formulario de Mantenimiento", 
                                 padx=10, pady=10, bg="#f0f0f0")
        form_frame.pack(fill=tk.X, padx=10, pady=10)
        
        if self.modo == "Editar":
            if nombre in ["Tanque", "Doli"]:
                tk.Label(form_frame, text="Tr:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5, sticky="e")
                self.tr_entry = tk.Entry(form_frame, width=15)
                self.tr_entry.grid(row=0, column=1, padx=5, pady=5)
                
                tk.Label(form_frame, text="Número:", bg="#f0f0f0").grid(row=0, column=2, padx=5, pady=5, sticky="e")
                self.numero_entry = tk.Entry(form_frame, width=15)
                self.numero_entry.grid(row=0, column=3, padx=5, pady=5)
                
                tk.Label(form_frame, text="Mantenimiento:", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5, sticky="e")
                self.mantenimiento_entry = tk.Entry(form_frame, width=30)
                self.mantenimiento_entry.grid(row=1, column=1, padx=5, pady=5)
                
                tk.Label(form_frame, text="Fecha:", bg="#f0f0f0").grid(row=1, column=2, padx=5, pady=5, sticky="e")
                self.fecha_entry = tk.Entry(form_frame, width=30)
                self.fecha_entry.grid(row=1, column=3, padx=5, pady=5)
                
                tk.Label(form_frame, text="KM Actual:", bg="#f0f0f0").grid(row=2, column=0, padx=5, pady=5, sticky="e")
                self.km_actual_entry = tk.Entry(form_frame, width=15)
                self.km_actual_entry.grid(row=2, column=1, padx=5, pady=5)
                
                tk.Label(form_frame, text="KM Mantenimiento:", bg="#f0f0f0").grid(row=2, column=2, padx=5, pady=5, sticky="e")
                self.km_mantenimiento_entry = tk.Entry(form_frame, width=15)
                self.km_mantenimiento_entry.grid(row=2, column=3, padx=5, pady=5)
                
                tk.Label(form_frame, text="Costo:", bg="#f0f0f0").grid(row=3, column=0, padx=5, pady=5, sticky="e")
                self.costo_entry = tk.Entry(form_frame, width=15)
                self.costo_entry.grid(row=3, column=1, padx=5, pady=5)
                
                tk.Label(form_frame, text="Estado:", bg="#f0f0f0").grid(row=3, column=2, padx=5, pady=5, sticky="e")
                self.estado_combobox = ttk.Combobox(form_frame, values=["Buen estado", "Mal estado"], width=15)
                self.estado_combobox.grid(row=3, column=3, padx=5, pady=5)
                self.estado_combobox.set("Elige un estado")
                
                button_frame = tk.Frame(form_frame, bg="#f0f0f0")
                button_frame.grid(row=4, column=0, columnspan=4, pady=10)
                
                tk.Button(button_frame, text="Editar Seleccionado", 
                         command=lambda: self.editar_dato_division(nombre),
                         bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=5)
                
                tk.Button(button_frame, text="Eliminar Seleccionado", 
                                                 command=lambda: self.eliminar_dato_division(nombre),
                         bg="#F44336", fg="white").pack(side=tk.LEFT, padx=5)
                
                tk.Button(button_frame, text="Agregar Nuevo", 
                         command=lambda: self.mostrar_formulario_agregar_division(nombre),
                         bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
            else:
                tk.Label(form_frame, text="Tr:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5, sticky="e")
                self.tr_entry = tk.Entry(form_frame, width=15)
                self.tr_entry.grid(row=0, column=1, padx=5, pady=5)
                
                tk.Label(form_frame, text="Mantenimiento:", bg="#f0f0f0").grid(row=0, column=2, padx=5, pady=5, sticky="e")
                self.mantenimiento_entry = tk.Entry(form_frame, width=30)
                self.mantenimiento_entry.grid(row=0, column=3, padx=5, pady=5)
                
                tk.Label(form_frame, text="Fecha:", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5, sticky="e")
                self.fecha_entry = tk.Entry(form_frame, width=30)
                self.fecha_entry.grid(row=1, column=1, padx=5, pady=5)
                
                tk.Label(form_frame, text="KM Actual:", bg="#f0f0f0").grid(row=1, column=2, padx=5, pady=5, sticky="e")
                self.km_actual_entry = tk.Entry(form_frame, width=15)
                self.km_actual_entry.grid(row=1, column=3, padx=5, pady=5)
                
                tk.Label(form_frame, text="KM Mantenimiento:", bg="#f0f0f0").grid(row=2, column=0, padx=5, pady=5, sticky="e")
                self.km_mantenimiento_entry = tk.Entry(form_frame, width=15)
                self.km_mantenimiento_entry.grid(row=2, column=1, padx=5, pady=5)
                
                tk.Label(form_frame, text="Costo:", bg="#f0f0f0").grid(row=2, column=2, padx=5, pady=5, sticky="e")
                self.costo_entry = tk.Entry(form_frame, width=15)
                self.costo_entry.grid(row=2, column=3, padx=5, pady=5)
                
                tk.Label(form_frame, text="Estado:", bg="#f0f0f0").grid(row=3, column=0, padx=5, pady=5, sticky="e")
                self.estado_combobox = ttk.Combobox(form_frame, values=["Buen estado", "Mal estado"], width=15)
                self.estado_combobox.grid(row=3, column=1, padx=5, pady=5)
                self.estado_combobox.set("Elige un estado")
                
                button_frame = tk.Frame(form_frame, bg="#f0f0f0")
                button_frame.grid(row=4, column=0, columnspan=4, pady=10)
                
                tk.Button(button_frame, text="Editar Seleccionado", 
                         command=lambda: self.editar_dato_adaptacion(nombre),
                         bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=5)
                
                tk.Button(button_frame, text="Eliminar Seleccionado", 
                         command=lambda: self.eliminar_dato_adaptacion(nombre),
                         bg="#F44336", fg="white").pack(side=tk.LEFT, padx=5)
                
                tk.Button(button_frame, text="Agregar Nuevo", 
                         command=lambda: self.mostrar_formulario_agregar_adaptacion(nombre),
                         bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
        
        # Configurar evento de selección
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_dato)
    
    def mostrar_formulario_agregar_division(self, nombreDivision):
        """Muestra un formulario para agregar nueva división (Tanque o Doli)"""
        self.formulario_agregar_division = tk.Toplevel(self.root)
        self.formulario_agregar_division.title(f"Agregar Mantenimiento - {nombreDivision}")
        self.formulario_agregar_division.geometry("400x400")
        
        form_frame = tk.Frame(self.formulario_agregar_division, padx=20, pady=20, bg="#f0f0f0")
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(form_frame, text=f"Agregar Mantenimiento - {nombreDivision}", 
                font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=10)
        
        campos = [
            ("Tr:", "entry"),
            ("Número:", "entry"),
            ("Mantenimiento:", "entry"),
            ("Fecha:", "entry"),
            ("KM Actual:", "entry"),
            ("KM Mantenimiento:", "entry"),
            ("Costo:", "entry"),
            ("Estado:", "combobox", ["Buen estado", "Mal estado"])
        ]
        
        self.campos_division = {}
        
        for i, (label, tipo, *opciones) in enumerate(campos):
            frame = tk.Frame(form_frame, bg="#f0f0f0")
            frame.pack(fill=tk.X, pady=5)
            
            tk.Label(frame, text=label, width=20, anchor="e", bg="#f0f0f0").pack(side=tk.LEFT)
            
            if tipo == "entry":
                entry = tk.Entry(frame, width=25)
                entry.pack(side=tk.LEFT)
                self.campos_division[label.replace(":", "").lower().replace(" ", "_")] = entry
            elif tipo == "combobox":
                combobox = ttk.Combobox(frame, values=opciones[0], width=22)
                combobox.pack(side=tk.LEFT)
                combobox.set("Buen estado")
                self.campos_division[label.replace(":", "").lower().replace(" ", "_")] = combobox
        
        button_frame = tk.Frame(form_frame, bg="#f0f0f0")
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Guardar", 
                 command=lambda: self.guardar_nueva_division(nombreDivision),
                 bg="#4CAF50", fg="white", width=15).pack(side=tk.LEFT, padx=10)
        
        tk.Button(button_frame, text="Cancelar", 
                 command=self.formulario_agregar_division.destroy,
                 bg="#F44336", fg="white", width=15).pack(side=tk.LEFT, padx=10)
    
    def guardar_nueva_division(self, nombreDivision):
        try:
            tr = self.campos_division["tr"].get()
            numero = self.campos_division["número"].get()
            mantenimiento = self.campos_division["mantenimiento"].get()
            fecha = self.campos_division["fecha"].get()
            km_actual = self.campos_division["km_actual"].get()
            km_mantenimiento = self.campos_division["km_mantenimiento"].get()
            costo = self.campos_division["costo"].get()
            estado = self.campos_division["estado"].get()
            
            if not all([tr, numero, mantenimiento, fecha, km_actual, km_mantenimiento, costo, estado]):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
                
            try:
                tr = int(tr)
                numero = int(numero)
                km_actual = int(km_actual)
                km_mantenimiento = int(km_mantenimiento)
                costo = float(costo)
            except ValueError:
                messagebox.showerror("Error", "Tr, Número, KM Actual, KM Mantenimiento y Costo deben ser números válidos")
                return
                
            insertar_mantenimiento_division(tr, numero, nombreDivision, mantenimiento, fecha, 
                                          km_actual, km_mantenimiento, costo, estado)
            
            # Actualizar la tabla
            self.crear_tabla(self.tabs[nombreDivision], nombreDivision)
            self.formulario_agregar_division.destroy()
            messagebox.showinfo("Éxito", "Mantenimiento agregado correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al guardar: {str(e)}")
    
    def mostrar_formulario_agregar_adaptacion(self, nombreAdaptacion):
        """Muestra un formulario para agregar nueva adaptación"""
        self.formulario_agregar_adaptacion = tk.Toplevel(self.root)
        self.formulario_agregar_adaptacion.title(f"Agregar Mantenimiento - {nombreAdaptacion}")
        self.formulario_agregar_adaptacion.geometry("400x350")
        
        form_frame = tk.Frame(self.formulario_agregar_adaptacion, padx=20, pady=20, bg="#f0f0f0")
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(form_frame, text=f"Agregar Mantenimiento - {nombreAdaptacion}", 
                font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=10)
        
        campos = [
            ("Tr:", "entry"),
            ("Mantenimiento:", "entry"),
            ("Fecha:", "entry"),
            ("KM Actual:", "entry"),
            ("KM Mantenimiento:", "entry"),
            ("Costo:", "entry"),
            ("Estado:", "combobox", ["Buen estado", "Mal estado"])
        ]
        
        self.campos_adaptacion = {}
        
        for i, (label, tipo, *opciones) in enumerate(campos):
            frame = tk.Frame(form_frame, bg="#f0f0f0")
            frame.pack(fill=tk.X, pady=5)
            
            tk.Label(frame, text=label, width=20, anchor="e", bg="#f0f0f0").pack(side=tk.LEFT)
            
            if tipo == "entry":
                entry = tk.Entry(frame, width=25)
                entry.pack(side=tk.LEFT)
                self.campos_adaptacion[label.replace(":", "").lower().replace(" ", "_")] = entry
            elif tipo == "combobox":
                combobox = ttk.Combobox(frame, values=opciones[0], width=22)
                combobox.pack(side=tk.LEFT)
                combobox.set("Buen estado")
                self.campos_adaptacion[label.replace(":", "").lower().replace(" ", "_")] = combobox
        
        button_frame = tk.Frame(form_frame, bg="#f0f0f0")
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Guardar", 
                 command=lambda: self.guardar_nueva_adaptacion(nombreAdaptacion),
                 bg="#4CAF50", fg="white", width=15).pack(side=tk.LEFT, padx=10)
        
        tk.Button(button_frame, text="Cancelar", 
                 command=self.formulario_agregar_adaptacion.destroy,
                 bg="#F44336", fg="white", width=15).pack(side=tk.LEFT, padx=10)
    
    def guardar_nueva_adaptacion(self, nombreAdaptacion):
        try:
            tr = self.campos_adaptacion["tr"].get()
            mantenimiento = self.campos_adaptacion["mantenimiento"].get()
            fecha = self.campos_adaptacion["fecha"].get()
            km_actual = self.campos_adaptacion["km_actual"].get()
            km_mantenimiento = self.campos_adaptacion["km_mantenimiento"].get()
            costo = self.campos_adaptacion["costo"].get()
            estado = self.campos_adaptacion["estado"].get()
            
            if not all([tr, mantenimiento, fecha, km_actual, km_mantenimiento, costo, estado]):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
                
            try:
                tr = int(tr)
                km_actual = int(km_actual)
                km_mantenimiento = int(km_mantenimiento)
                costo = float(costo)
            except ValueError:
                messagebox.showerror("Error", "Tr, KM Actual, KM Mantenimiento y Costo deben ser números válidos")
                return
                
            insertar_mantenimiento_adaptacion(tr, nombreAdaptacion, mantenimiento, fecha, 
                                           km_actual, km_mantenimiento, costo, estado)
            
            # Actualizar la tabla
            self.crear_tabla(self.tabs[nombreAdaptacion], nombreAdaptacion)
            self.formulario_agregar_adaptacion.destroy()
            messagebox.showinfo("Éxito", "Mantenimiento agregado correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al guardar: {str(e)}")
    
    def seleccionar_dato(self, event):
        """Llena los campos del formulario con el dato seleccionado"""
        if self.modo != "Editar":
            return
            
        selected = self.tree.focus()
        if not selected:
            return
            
        values = self.tree.item(selected, "values")
        
        if self.adaptacion_actual in ["Tanque", "Doli"]:
            self.tr_entry.delete(0, tk.END)
            self.tr_entry.insert(0, values[0])
            
            self.numero_entry.delete(0, tk.END)
            self.numero_entry.insert(0, values[1])
            
            self.mantenimiento_entry.delete(0, tk.END)
            self.mantenimiento_entry.insert(0, values[2])
            
            self.fecha_entry.delete(0, tk.END)
            self.fecha_entry.insert(0, values[3])
            
            self.km_actual_entry.delete(0, tk.END)
            self.km_actual_entry.insert(0, values[4])
            
            self.km_mantenimiento_entry.delete(0, tk.END)
            self.km_mantenimiento_entry.insert(0, values[5])
            
            self.costo_entry.delete(0, tk.END)
            self.costo_entry.insert(0, values[6])
            
            self.estado_combobox.set(values[7])
        else:
            self.tr_entry.delete(0, tk.END)
            self.tr_entry.insert(0, values[0])
            
            self.mantenimiento_entry.delete(0, tk.END)
            self.mantenimiento_entry.insert(0, values[1])
            
            self.fecha_entry.delete(0, tk.END)
            self.fecha_entry.insert(0, values[2])
            
            self.km_actual_entry.delete(0, tk.END)
            self.km_actual_entry.insert(0, values[3])
            
            self.km_mantenimiento_entry.delete(0, tk.END)
            self.km_mantenimiento_entry.insert(0, values[4])
            
            self.costo_entry.delete(0, tk.END)
            self.costo_entry.insert(0, values[5])
            
            self.estado_combobox.set(values[6])
    
    def editar_dato_division(self, nombreDivision):
        """Edita un registro de división seleccionado"""
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione un registro para editar")
            return
            
        old_values = self.tree.item(selected, "values")
        
        try:
            tr = self.tr_entry.get()
            numero = self.numero_entry.get()
            mantenimiento = self.mantenimiento_entry.get()
            fecha = self.fecha_entry.get()
            km_actual = self.km_actual_entry.get()
            km_mantenimiento = self.km_mantenimiento_entry.get()
            costo = self.costo_entry.get()
            estado = self.estado_combobox.get()
            
            if not all([tr, numero, mantenimiento, fecha, km_actual, km_mantenimiento, costo, estado]):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
                
            try:
                tr = int(tr)
                numero = int(numero)
                km_actual = int(km_actual)
                km_mantenimiento = int(km_mantenimiento)
                costo = float(costo)
            except ValueError:
                messagebox.showerror("Error", "Tr, Número, KM Actual, KM Mantenimiento y Costo deben ser números válidos")
                return
                
            actualizar_mantenimiento_division(
                tr, numero, nombreDivision, old_values[2],  # mantenimiento original
                mantenimiento, fecha, km_actual, km_mantenimiento, costo, estado
            )
            
            # Actualizar la tabla
            self.crear_tabla(self.tabs[nombreDivision], nombreDivision)
            messagebox.showinfo("Éxito", "Registro actualizado correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al actualizar: {str(e)}")
    
    def editar_dato_adaptacion(self, nombreAdaptacion):
        """Edita un registro de adaptación seleccionado"""
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione un registro para editar")
            return
            
        old_values = self.tree.item(selected, "values")
        
        try:
            tr = self.tr_entry.get()
            mantenimiento = self.mantenimiento_entry.get()
            fecha = self.fecha_entry.get()
            km_actual = self.km_actual_entry.get()
            km_mantenimiento = self.km_mantenimiento_entry.get()
            costo = self.costo_entry.get()
            estado = self.estado_combobox.get()
            
            if not all([tr, mantenimiento, fecha, km_actual, km_mantenimiento, costo, estado]):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
                
            try:
                tr = int(tr)
                km_actual = int(km_actual)
                km_mantenimiento = int(km_mantenimiento)
                costo = float(costo)
            except ValueError:
                messagebox.showerror("Error", "Tr, KM Actual, KM Mantenimiento y Costo deben ser números válidos")
                return
                
            actualizar_mantenimiento_adaptacion(
                tr, nombreAdaptacion, old_values[1],  # mantenimiento original
                mantenimiento, fecha, km_actual, km_mantenimiento, costo, estado
            )
            
            # Actualizar la tabla
            self.crear_tabla(self.tabs[nombreAdaptacion], nombreAdaptacion)
            messagebox.showinfo("Éxito", "Registro actualizado correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al actualizar: {str(e)}")
    
    def eliminar_dato_division(self, nombreDivision):
        """Elimina un registro de división seleccionado"""
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione un registro para eliminar")
            return
            
        values = self.tree.item(selected, "values")
        
        if messagebox.askyesno("Confirmar", "¿Está seguro que desea eliminar este registro?"):
            try:
                eliminar_mantenimiento_division(
                    int(values[0]), int(values[1]), nombreDivision, values[2], 
                    values[3], int(values[4]), int(values[5]), float(values[6]), values[7]
                )
                
                # Actualizar la tabla
                self.crear_tabla(self.tabs[nombreDivision], nombreDivision)
                messagebox.showinfo("Éxito", "Registro eliminado correctamente")
                
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error al eliminar: {str(e)}")
    
    def eliminar_dato_adaptacion(self, nombreAdaptacion):
        """Elimina un registro de adaptación seleccionado"""
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Advertencia", "Por favor seleccione un registro para eliminar")
            return
            
        values = self.tree.item(selected, "values")
        
        if messagebox.askyesno("Confirmar", "¿Está seguro que desea eliminar este registro?"):
            try:
                eliminar_mantenimiento_adaptacion(
                    int(values[0]), nombreAdaptacion, values[1], values[2], 
                    int(values[3]), int(values[4]), float(values[5]), values[6]
                )
                
                # Actualizar la tabla
                self.crear_tabla(self.tabs[nombreAdaptacion], nombreAdaptacion)
                messagebox.showinfo("Éxito", "Registro eliminado correctamente")
                
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error al eliminar: {str(e)}")
    
    def cambiar_modo(self, modo):
        """Cambia entre modo consulta y edición"""
        self.modo = modo
        if modo == "Consultar":
            self.consultar_btn.config(bg="#2196F3", fg="white")
            self.editar_btn.config(bg="#f0f0f0", fg="black")
        else:
            self.consultar_btn.config(bg="#f0f0f0", fg="black")
            self.editar_btn.config(bg="#FF9800", fg="white")
        
        # Actualizar la vista actual
        self.mostrar_adaptacion(self.adaptacion_actual)
    
    def buscar_por_tr(self):
        """Busca registros por TR"""
        tr = self.buscar_entry.get()
        if not tr:
            messagebox.showwarning("Advertencia", "Por favor ingrese un TR para buscar")
            return
            
        try:
            tr = int(tr)
        except ValueError:
            messagebox.showerror("Error", "El TR debe ser un número válido")
            return
            
        # Buscar en adaptaciones
        datos_adaptacion = buscar_por_tr_adaptacion(tr)
        # Buscar en divisiones
        datos_division = buscar_por_tr_division(tr)
        
        if not datos_adaptacion and not datos_division:
            messagebox.showinfo("Información", f"No se encontraron registros para el TR {tr}")
            return
            
        # Mostrar resultados en una nueva ventana
        resultados_window = tk.Toplevel(self.root)
        resultados_window.title(f"Resultados de búsqueda para TR {tr}")
        resultados_window.geometry("900x600")
        
        main_frame = tk.Frame(resultados_window, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        if datos_adaptacion:
            # Crear pestaña para adaptaciones
            adaptacion_frame = tk.Frame(notebook)
            notebook.add(adaptacion_frame, text="Adaptaciones")
            
            tree = ttk.Treeview(adaptacion_frame, columns=("tr", "adaptacion", "mantenimiento", "fecha", "km_actual", "km_mantenimiento", "costo", "estado"), show="headings")
            
            tree.heading("tr", text="Tr")
            tree.heading("adaptacion", text="Adaptación")
            tree.heading("mantenimiento", text="Mantenimiento")
            tree.heading("fecha", text="Fecha")
            tree.heading("km_actual", text="KM Actual")
            tree.heading("km_mantenimiento", text="KM Mant.")
            tree.heading("costo", text="Costo")
            tree.heading("estado", text="Estado")
            
            tree.column("tr", width=50, anchor=tk.CENTER)
            tree.column("adaptacion", width=100)
            tree.column("mantenimiento", width=150)
            tree.column("fecha", width=100, anchor=tk.CENTER)
            tree.column("km_actual", width=80, anchor=tk.CENTER)
            tree.column("km_mantenimiento", width=80, anchor=tk.CENTER)
            tree.column("costo", width=80, anchor=tk.CENTER)
            tree.column("estado", width=100, anchor=tk.CENTER)
            
            scrollbar = ttk.Scrollbar(adaptacion_frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            for dato in datos_adaptacion:
                tree.insert("", tk.END, values=dato)
        
        if datos_division:
            # Crear pestaña para divisiones
            division_frame = tk.Frame(notebook)
            notebook.add(division_frame, text="Divisiones")
            
            tree = ttk.Treeview(division_frame, columns=("tr", "numero", "division", "mantenimiento", "fecha", "km_actual", "km_mantenimiento", "costo", "estado"), show="headings")
            
            tree.heading("tr", text="Tr")
            tree.heading("numero", text="Número")
            tree.heading("division", text="División")
            tree.heading("mantenimiento", text="Mantenimiento")
            tree.heading("fecha", text="Fecha")
            tree.heading("km_actual", text="KM Actual")
            tree.heading("km_mantenimiento", text="KM Mant.")
            tree.heading("costo", text="Costo")
            tree.heading("estado", text="Estado")
            
            tree.column("tr", width=50, anchor=tk.CENTER)
            tree.column("numero", width=50, anchor=tk.CENTER)
            tree.column("division", width=80)
            tree.column("mantenimiento", width=150)
            tree.column("fecha", width=100, anchor=tk.CENTER)
            tree.column("km_actual", width=80, anchor=tk.CENTER)
            tree.column("km_mantenimiento", width=80, anchor=tk.CENTER)
            tree.column("costo", width=80, anchor=tk.CENTER)
            tree.column("estado", width=100, anchor=tk.CENTER)
            
            scrollbar = ttk.Scrollbar(division_frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            for dato in datos_division:
                tree.insert("", tk.END, values=dato)

# ====================== EJECUCIÓN DE LA APLICACIÓN ======================
if __name__ == "__main__":
    crear_tabla_si_no_existe()
    root = tk.Tk()
    app = AutotanquesApp(root)
    root.mainloop()