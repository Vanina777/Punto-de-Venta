import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import datetime
import sys
import os

class Proveedor(tk.Frame):
    db_name = "database.db"

    def __init__(self, padre):
        super().__init__(padre)
        self.widgets()
        
    def rutas(self, ruta):
        try:
            rutabase = sys.__MEIPASS
        except Exception:
            rutabase = os.path.abspath(".")
        return os.path.join(rutabase, ruta)

    def widgets(self):
        
#Frame superior
        frame1 = tk.Frame(self, bg="#BEBEBE", highlightbackground="gray", highlightthickness=1)
        frame1.pack()
        frame1.place(x=0, y=0, width=1100, height=100)
                
        titulo = tk.Label(self, text="PROVEEDORES", font="sans 30 bold", bg="#BEBEBE", anchor="center")
        titulo.pack()  
        titulo.place(x=5, y=0, width=1090, height=90)

#Frame inferior
        frame2 = tk.Frame(self, bg="#545454", highlightbackground="gray", highlightthickness=1)
        frame2.place(x=0, y=100, width=1100, height=550)
        
        # Crear etiqueta para mostrar la fecha actual
        ruta = self.rutas(r"icono/calendario.png")
        imagen_pil = Image.open(ruta)
        imagen_resize11 = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize11)
        
        self.label_fecha = tk.Label(frame2, text="", font="sans 14 bold", bg="#545454", fg="#FFFFFF")
        self.label_fecha.config(image=imagen_tk, compound="left", padx=10)
        self.label_fecha.image = imagen_tk
        self.label_fecha.place(x=780, y=3)

        # Crear etiqueta para mostrar la hora actualizada
        ruta = self.rutas(r"icono/hora.png")
        imagen_pil = Image.open(ruta)
        imagen_resize12 = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize12)
        
        self.label_hora = tk.Label(frame2, text="", font="sans 14 bold", bg="#545454", fg="#FFFFFF")
        self.label_hora.config(image=imagen_tk, compound="left", padx=10)
        self.label_hora.image = imagen_tk
        self.label_hora.place(x=930, y=3)

        # Actualizar la fecha y la hora cada segundo
        self.actualizar_fecha_y_hora()

    #LabelFrame con entrys para ingresar datos
        labelframe = tk.LabelFrame(frame2, text="Registrar proveedor", font="sans 22 bold", bg="#BEBEBE")
        labelframe.place(x=20, y=30, width=400, height=500)

        lblnombre = Label(labelframe, text="Nombre: ", font="sans 14 bold", bg="#BEBEBE")
        lblnombre.place(x=10, y=20)
        self.nombre = ttk.Entry(labelframe, font="sans 14 bold")
        self.nombre.place(x=140, y=20, width=240, height=40)

        lblidentificacion = Label(labelframe, text="Identificación: ", font="sans 14 bold", bg="#BEBEBE")
        lblidentificacion.place(x=10, y=80)
        self.identificacion = ttk.Entry(labelframe, font="sans 14 bold")
        self.identificacion.place(x=140, y=80, width=240, height=40)

        lblcelular = Label(labelframe, text="Celular: ", font="sans 14 bold", bg="#BEBEBE")
        lblcelular.place(x=10, y=140)
        self.celular = ttk.Entry(labelframe, font="sans 14 bold")
        self.celular.place(x=140, y=140, width=240, height=40)

        lbldireccion = Label(labelframe, text="Dirección: ", font="sans 14 bold", bg="#BEBEBE")
        lbldireccion.place(x=10, y=200)
        self.direccion = ttk.Entry(labelframe, font="sans 14 bold")
        self.direccion.place(x=140, y=200, width=240, height=40)

        lblcorreo = Label(labelframe, text="Correo: ", font="sans 14 bold", bg="#BEBEBE")
        lblcorreo.place(x=10, y=260)
        self.correo = ttk.Entry(labelframe, font="sans 14 bold")
        self.correo.place(x=140, y=260, width=240, height=40)

        ruta = self.rutas(r"icono/ingresarc.png")
        imagen_pil = Image.open(ruta)
        imagen_resize = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize)

        btn1 = Button(labelframe, bg="#FFFFFF", fg="black", text="Registrar", font="roboto 16 bold", command=self.registrar_proveedor)
        btn1.config(image=imagen_tk, compound=LEFT, padx=10)
        btn1.image = imagen_tk
        btn1.place(x=80, y=330, width=240, height=40)
        
        ruta = self.rutas(r"icono/modificar.png")
        imagen_pil = Image.open(ruta)
        imagen_resize2 = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize2)
        
        btn2 = Button(labelframe, bg="#FFFFFF", fg="black", text="Editar", font="roboto 16 bold", command=self.editar_proveedor)
        btn2.config(image=imagen_tk, compound=LEFT, padx=10)
        btn2.image = imagen_tk
        btn2.place(x=80, y=400, width=240, height=40)

#TreeView Tabla
        treFrame = Frame(frame2, bg="#FFFFFF")  
        treFrame.place(x=440, y=50, width=620, height=450)
        
        # Barra de desplazamiento vertical
        scrol_y = ttk.Scrollbar(treFrame)
        scrol_y.pack(side=RIGHT, fill=Y)

        # Barra de desplazamiento horizontal
        scrol_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill=X)
        
        self.tre = ttk.Treeview(treFrame, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set, height=40, 
                                columns=("Nombre", "Identificación", "Celular", "Dirección", "Correo"), show="headings")
        self.tre.pack(expand=True, fill=BOTH)

        scrol_y.config(command=self.tre.yview)
        scrol_x.config(command=self.tre.xview)
        
        self.tre.heading("Nombre", text="Nombre")
        self.tre.heading("Identificación", text="Identificación")
        self.tre.heading("Celular", text="Celular")
        self.tre.heading("Dirección", text="Dirección")
        self.tre.heading("Correo", text="Correo")
        
        self.tre.column("Nombre", width=150, anchor="center")
        self.tre.column("Identificación", width=120, anchor="center")
        self.tre.column("Celular", width=120, anchor="center")
        self.tre.column("Dirección", width=200, anchor="center")
        self.tre.column("Correo", width=200, anchor="center")

        # Obtener datos de la base de datos
        self.cargar_proveedores()

#Funciones
    def cargar_proveedores(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM proveedores")
        rows = cursor.fetchall()
        for row in rows:
            self.tre.insert('', 'end', text=row[0], values=row[1:])
        conn.close()

    def registrar_proveedor(self):
        nombre = self.nombre.get()
        identificacion = self.identificacion.get()
        celular = self.celular.get()
        direccion = self.direccion.get()
        correo = self.correo.get()

        # Conexión a la base de datos
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Insertar los datos en la tabla proveedores, excepto en la columna id
        cursor.execute("INSERT INTO proveedores (nombre, identificacion, celular, direccion, correo) VALUES (?, ?, ?, ?, ?)",
                    (nombre, identificacion, celular, direccion, correo))

        # Confirmar la transacción y cerrar la conexión
        conn.commit()
        conn.close()

        # Insertar el nuevo proveedor en el TreeView
        self.tre.insert('', 'end', values=(nombre, identificacion, celular, direccion, correo))

        # Limpiar los campos después de la inserción
        self.nombre.delete(0, END)
        self.identificacion.delete(0, END)
        self.celular.delete(0, END)
        self.direccion.delete(0, END)
        self.correo.delete(0, END)
        
    def actualizar_fecha_y_hora(self):
        # Obtener la fecha y hora actual
        fecha_actual = datetime.datetime.now().strftime("%d-%m-%Y")
        hora_actual = datetime.datetime.now().strftime("%H:%M:%S")

        # Actualizar las etiquetas de fecha y hora
        self.label_fecha.config(text=fecha_actual)
        self.label_hora.config(text=hora_actual)

        # Llamar a este método nuevamente 
        self.after(1000, self.actualizar_fecha_y_hora)
        
    def editar_proveedor(self):
        # Obtener el item seleccionado 
        seleccionado = self.tre.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Por favor, seleccione un proveedor para editar.")
            return

        # Obtener los detalles del proveedor seleccionado
        item = seleccionado[0]
        detalles = self.tre.item(item, 'values')

        # Crear una ventana Toplevel para editar los detalles del proveedor
        ventana_editar = tk.Toplevel(self)
        ventana_editar.title("Editar Proveedor")
        ventana_editar.geometry("400x400")
        ventana_editar.config(bg="#BEBEBE")

        # Etiquetas y campos de entrada para editar los detalles
        lblnombre = Label(ventana_editar, text="Nombre:", font="sans 14 bold", bg="#BEBEBE")
        lblnombre.grid(row=0, column=0, padx=10, pady=5)
        nombre_editar = ttk.Entry(ventana_editar, font="sans 14 bold")
        nombre_editar.grid(row=0, column=1, padx=10, pady=5)
        nombre_editar.insert(0, detalles[0])

        lblidentificacion = Label(ventana_editar, text="Identificación:", font="sans 14 bold", bg="#BEBEBE")
        lblidentificacion.grid(row=1, column=0, padx=10, pady=5)
        identificacion_editar = ttk.Entry(ventana_editar, font="sans 14 bold")
        identificacion_editar.grid(row=1, column=1, padx=10, pady=5)
        identificacion_editar.insert(0, detalles[1])

        lblcelular = Label(ventana_editar, text="Celular:", font="sans 14 bold", bg="#BEBEBE")
        lblcelular.grid(row=2, column=0, padx=10, pady=5)
        celular_editar = ttk.Entry(ventana_editar, font="sans 14 bold")
        celular_editar.grid(row=2, column=1, padx=10, pady=5)
        celular_editar.insert(0, detalles[2])

        lbldireccion = Label(ventana_editar, text="Dirección:", font="sans 14 bold", bg="#BEBEBE")
        lbldireccion.grid(row=3, column=0, padx=10, pady=5)
        direccion_editar = ttk.Entry(ventana_editar, font="sans 14 bold")
        direccion_editar.grid(row=3, column=1, padx=10, pady=5)
        direccion_editar.insert(0, detalles[3])

        lblcorreo = Label(ventana_editar, text="Correo:", font="sans 14 bold", bg="#BEBEBE")
        lblcorreo.grid(row=4, column=0, padx=10, pady=5)
        correo_editar = ttk.Entry(ventana_editar, font="sans 14 bold")
        correo_editar.grid(row=4, column=1, padx=10, pady=5)
        correo_editar.insert(0, detalles[4])

        # Función para guardar los cambios
        def guardar_cambios():
            # Obtener el ID del proveedor seleccionado
            proveedor_id = self.tre.item(item, 'text')

            # Obtener los nuevos valores
            nuevo_nombre = nombre_editar.get()
            nueva_identificacion = identificacion_editar.get()
            nuevo_celular = celular_editar.get()
            nueva_direccion = direccion_editar.get()
            nuevo_correo = correo_editar.get()

            # Actualizar los valores en el Treeview
            self.tre.item(item, values=(nuevo_nombre, nueva_identificacion, nuevo_celular, nueva_direccion, nuevo_correo))

            # Actualizar los valores en la base de datos
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute("UPDATE proveedores SET nombre=?, identificacion=?, celular=?, direccion=?, correo=? WHERE id=?",
                            (nuevo_nombre, nueva_identificacion, nuevo_celular, nueva_direccion, nuevo_correo, proveedor_id))

            conn.commit()
            conn.close()

            # Cerrar la ventana de edición
            ventana_editar.destroy()
            
        # Botón para guardar los cambios
        ruta = self.rutas(r"icono/guardar.png")
        imagen_pil = Image.open(ruta)
        imagen_resize4 = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize4)
        
        btn_guardar = Button(ventana_editar, text="Guardar Cambios", bg="#FFFFFF", fg="black", font="roboto 16 bold", command=guardar_cambios)
        btn_guardar.config(image=imagen_tk, compound=LEFT, padx=10)
        btn_guardar.image = imagen_tk
        btn_guardar.grid(row=5, column=0, columnspan=2, pady=10)