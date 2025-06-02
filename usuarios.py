import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import datetime
import sys
import os

class Usuarios(tk.Frame):
    db_name = "database.db"
    
    def __init__(self, padre):
        super().__init__(padre)
        self.widgets()
        
    def rutas(self,ruta):
        try:
            rutabase=sys.__MEIPASS
        except Exception:
            rutabase=os.path.abspath(".")
        return os.path.join(rutabase,ruta)
        
    def widgets(self):
        
#Frame superior
        frame1 = tk.Frame(self, bg="#BEBEBE",highlightbackground="gray", highlightthickness=1)
        frame1.pack()
        frame1.place(x=0, y=0, width=1100, height=100)
        
        titulo = tk.Label(frame1, text="ADMINISTRAR USUARIOS", font="sans 30 bold", bg="#BEBEBE", anchor="center")
        titulo.pack() 
        titulo.place(x=5, y=0, width=1090, height=90)
        
#Frame inferior
        
        frame2 = tk.Frame(self, bg="#545454",highlightbackground="gray", highlightthickness=1)
        frame2.place(x=0, y=100, width=1100, height=550)
        
        # Crear etiqueta para mostrar la fecha actual
        ruta=self.rutas(r"icono/calendario.png")
        imagen_pil = Image.open(ruta)
        imagen_resize11 = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize11)
        
        self.label_fecha = tk.Label(frame2, text="", font="sans 14 bold", bg="#545454", fg="#FFFFFF")
        self.label_fecha.config(image=imagen_tk, compound="left", padx=10)
        self.label_fecha.image = imagen_tk
        self.label_fecha.place(x=780, y=3)

        # Crear etiqueta para mostrar la hora actualizada
        ruta=self.rutas(r"icono/hora.png")
        imagen_pil = Image.open(ruta)
        imagen_resize12 = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize12)
        
        self.label_hora = tk.Label(frame2, text="", font="sans 14 bold", bg="#545454", fg="#FFFFFF")
        self.label_hora.config(image=imagen_tk, compound="left", padx=10)
        self.label_hora.image = imagen_tk
        self.label_hora.place(x=930, y=3)

        # Actualizar la fecha y la hora cada segundo
        self.actualizar_fecha_y_hora()

        treFrame=Frame(frame2) #frame recuadro dentro de la ventana ventas
        treFrame.place(x=50,y=50,width=620,height=450)
        
        # Barra de desplazamiento vertical
        scrol_y = ttk.Scrollbar(treFrame)
        scrol_y.pack(side=RIGHT, fill=Y)

        # Barra de desplazamiento horizontal
        scrol_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill=X)
        
        self.lista_usuarios = ttk.Treeview(treFrame, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set, height=40)
        self.lista_usuarios["columns"] = ("Username", "Password", "Rol")
        
        self.lista_usuarios.pack(expand=True, fill=BOTH)
        
        self.lista_usuarios.heading("#0", text="ID")
        self.lista_usuarios.heading("Username", text="Nombre")
        self.lista_usuarios.heading("Password", text="Contraseña")
        self.lista_usuarios.heading("Rol", text="Rol")
        
        self.lista_usuarios.column("#0", width=50, anchor="center")
        self.lista_usuarios.column("Username", width=150, anchor="center")
        self.lista_usuarios.column("Password", width=150, anchor="center")
        self.lista_usuarios.column("Rol", width=100, anchor="center")

        ruta=self.rutas(r"icono/guardar.png")
        imagen_pil = Image.open(ruta)
        imagen_resize = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize)

        btn_actualizar = Button(frame2, bg="#FFFFFF", fg="black", text="Actualizar Usuario", 
                                font="roboto 16 bold", command=self.actualizar_usuario_seleccionado)
        btn_actualizar.config(image=imagen_tk, compound=LEFT, padx=10)
        btn_actualizar.image = imagen_tk
        btn_actualizar.place(x=700, y=150, width=250,height=40)

        # Cargar datos de usuarios en el Treeview
        self.cargar_usuarios()

#Funciones        
    def leer_usuarios(self):
        try:
            conexion = sqlite3.connect(self.db_name)
            cursor = conexion.cursor()
            cursor.execute("SELECT id, username, password, rol FROM usuarios")

            usuarios = cursor.fetchall()
            return usuarios
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudieron leer los usuarios: {e}")
            return []

    def actualizar_usuario(self, id_usuario, username, password, rol):
        try:
            conexion = sqlite3.connect(self.db_name)
            cursor = conexion.cursor()
            cursor.execute("UPDATE usuarios SET username=?, password=?, rol=? WHERE id=?", (username, password, rol, id_usuario))
            conexion.commit()
            messagebox.showinfo("Éxito", "Usuario actualizado exitosamente")
            self.cargar_usuarios()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo actualizar el usuario: {e}")
        finally:
            if conexion:
                conexion.close()
                
    def cargar_usuarios(self):
        # Limpiar Treeview antes de cargar nuevos datos
        for row in self.lista_usuarios.get_children():
            self.lista_usuarios.delete(row)
            
        # Obtener datos de usuarios de la base de datos
        usuarios = self.leer_usuarios()

        # Insertar datos de usuarios en el Treeview
        for usuario in usuarios:
            # Insertar cada usuario como una nueva fila en el Treeview, con el ID como identificador único de la fila
            self.lista_usuarios.insert("", "end", text=usuario[0], values=(usuario[1],usuario[2], usuario[3]))  
            
    def actualizar_usuario_seleccionado(self):
        # Obtener el item seleccionado en el Treeview
        item_seleccionado = self.lista_usuarios.selection()

        # Verificar si se seleccionó un item
        if item_seleccionado:
            # Obtener los datos del usuario seleccionado
            id_usuario = self.lista_usuarios.item(item_seleccionado, "text")
            username = self.lista_usuarios.item(item_seleccionado, "values")[0]
            password = self.lista_usuarios.item(item_seleccionado, "values")[1]
            rol = self.lista_usuarios.item(item_seleccionado, "values")[2]

            # Crear la ventana para modificar el usuario
            ventana_modificar = Toplevel(self)
            ventana_modificar.title("Modificar Usuario")
            ventana_modificar.geometry("400x500")  
            ventana_modificar.config(bg="#BEBEBE")

            label_username = Label(ventana_modificar, text="Nuevo nombre de usuario:",font="sans 14 bold",bg="#BEBEBE")
            label_username.place(x=70, y=20)
            entry_username = Entry(ventana_modificar,font="sans 14 bold")
            entry_username.insert(0, username)
            entry_username.place(x=75, y=50, width=240,height=40)

            label_password = Label(ventana_modificar, text="Nueva contraseña:",font="sans 14 bold",bg="#BEBEBE")
            label_password.place(x=70, y=110)
            entry_password = Entry(ventana_modificar,font="sans 14 bold")
            entry_password.insert(0, password)
            entry_password.place(x=75, y=150, width=240,height=40)

            Label(ventana_modificar, text="Rol:", font="sans 14 bold", bg="#BEBEBE").place(x=70, y=200)
            combobox_rol = ttk.Combobox(ventana_modificar, font="sans 14 bold", state="readonly")
            combobox_rol["values"] = ["Empleado", "Encargado"]
            combobox_rol.set(rol)
            combobox_rol.place(x=75, y=230, width=240, height=40)

            ruta=self.rutas(r"icono/guardar.png")
            imagen_pil = Image.open(ruta)
            imagen_resize1 = imagen_pil.resize((30, 30))
            imagen_tk = ImageTk.PhotoImage(imagen_resize1)

            btn_actualizar = Button(ventana_modificar, bg="#FFFFFF", fg="black", text="Actualizar", font="roboto 16 bold", command=lambda: self.actualizar_usuario(id_usuario, entry_username.get(), entry_password.get(), combobox_rol.get()))
            btn_actualizar.config(image=imagen_tk, compound=LEFT, padx=10)
            btn_actualizar.image = imagen_tk
            btn_actualizar.place(x=110, y=350,width=170,height=40)
        else:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un usuario para actualizar.")
        
    def actualizar_fecha_y_hora(self): 
        # Obtener la fecha y hora actual
        fecha_actual = datetime.datetime.now().strftime("%d-%m-%Y")
        hora_actual = datetime.datetime.now().strftime("%H:%M:%S")

        # Actualizar las etiquetas de fecha y hora
        self.label_fecha.config(text=fecha_actual)
        self.label_hora.config(text=hora_actual)

        # Llamar a este método nuevamente
        self.after(1000, self.actualizar_fecha_y_hora)