import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk,messagebox
from PIL import Image, ImageTk
from container import Container
from tkinter import messagebox
import sys
import os

class Login(tk.Frame):
    image = None
    db_name = "database.db"

    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.pack()
        self.place(x=0, y=0, width=1100, height=650)
        self.controlador = controlador
        self.widgets()
        
    def rutas(self,ruta):
        try:
            rutabase=sys.__MEIPASS
        except Exception:
            rutabase=os.path.abspath(".")
        return os.path.join(rutabase,ruta)

    def validacion(self, user, pas):
        return len(user) > 0 and len(pas) > 0

    def login(self):
        user = self.username.get()
        pas = self.password.get()

        if self.validacion(user, pas):
            consulta = "SELECT rol FROM usuarios WHERE username=? AND password=?"
            parametros = (user, pas)

            try:
                with sqlite3.connect(self.db_name) as conn:
                    cursor = conn.cursor()
                    cursor.execute(consulta, parametros)
                    result = cursor.fetchone()

                    if result:
                        rol = result[0]
                        self.controlador.set_rol_actual(rol)  # Utiliza un setter para claridad
                        self.controlador.show_frame(Container)
                    else:
                        self.username.delete(0, 'end')
                        self.password.delete(0, 'end')
                        messagebox.showerror(title="Error", message="Usuario y/o contraseña incorrecta")
            except sqlite3.Error as e:
                messagebox.showerror(title="Error", message="No se conectó a la base de datos: {}".format(e))
        else:
            messagebox.showerror(title="Error", message="Llene todas las casillas")

    def password_command(self):
        if self.password.cget('show') == "*":
            self.password.config(show="")
        else:
            self.password.config(show="*")

    def control1(self):
        self.controlador.show_frame(Container)

    def control2(self):
        self.controlador.show_frame(Registro)

    def widgets(self):
        
#Frame izquierdo
        fondo = tk.Frame(self, bg="#FFFFFF",highlightbackground="gray", highlightthickness=1)
        fondo.pack()
        fondo.place(x=0, y=0, width=550, height=650)
        
        ruta=self.rutas(r"imagenes/logo1.png")
        self.logo_image = Image.open(ruta)
        self.logo_image = self.logo_image.resize((250, 250))
        self.logo_image = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = ttk.Label(fondo, image=self.logo_image, background="#FFFFFF")
        self.logo_label.place(x=140, y=60)
        
        lblubicacion=tk.Label(fondo, text="BAR UNIVERSITARIO", font="sans 30 bold", bg="#FFFFFF", fg="black", anchor="center")
        lblubicacion.place(x=0, y=360, width=545)
        
        lblcorreo=tk.Label(fondo, text="Email: bar@comunidad.frrq.utn.edu.ar", font="sans 20 bold", bg="#FFFFFF", fg="black", anchor="center")
        lblcorreo.place(x=0, y=420, width=545)
        
        
#Frame derecho
        fondo2 = tk.Frame(self, bg="#BEBEBE",highlightbackground="gray", highlightthickness=1)
        fondo2.pack()
        fondo2.place(x=550, y=0, width=550, height=650)

        label = ttk.Label(fondo2, text="Inicio de sesión", font="sans 36 bold", background="#BEBEBE")
        label.place(x=100, y=80)

        user = ttk.Label(fondo2, text="Nombre de usuario", font="sans 22 bold", background="#BEBEBE")
        user.place(x=150, y=180)

        self.username = ttk.Entry(fondo2, font="sans 16 bold")
        self.username.place(x=150, y=220, width=240, height=40)

        pas = ttk.Label(fondo2, text="Contraseña", font="sans 22 bold", background="#BEBEBE")
        pas.place(x=150, y=280)

        self.password = ttk.Entry(fondo2, show="*", font="sans 16 bold")
        self.password.place(x=150, y=320, width=240, height=40)

        ruta=self.rutas(r"icono/iniciar.png")
        imagen_pil = Image.open(ruta)
        imagen_resize = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize)

        btn1 = tk.Button(fondo2, text="Iniciar", background="#FFFFFF", image=imagen_tk, compound=tk.LEFT, command=self.login,font=("sans", 16, "bold"))
        btn1.image = imagen_tk
        btn1.place(x=150, y=400, width=240, height=40)

        ruta=self.rutas(r"icono/registrar.png")
        imagen_pil1 = Image.open(ruta)
        imagen_resize1 = imagen_pil1.resize((30, 30))
        imagen_tk1 = ImageTk.PhotoImage(imagen_resize1)

        btn2 = tk.Button(fondo2, text="Registrar", background="#FFFFFF", image=imagen_tk1, compound=tk.LEFT, command=self.control2,font=("sans", 16, "bold"))
        btn2.image = imagen_tk1
        btn2.place(x=150, y=460, width=240, height=40)
        
        # Check Button mostrar contraseña
        show_password = Checkbutton(fondo2, text="Mostrar contraseña", bg="#BEBEBE", font=("sans", 10, "bold"), command=self.password_command)
        show_password.place(x=150, y=370)

#Funciones    
class Registro(tk.Frame):
    image = None
    db_name = "database.db"

    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.pack()
        self.place(x=0, y=0, width=1100, height=650)
        self.controlador = controlador
        self.widgets()
        
    def rutas(self,ruta):
        try:
            rutabase=sys.__MEIPASS
        except Exception:
            rutabase=os.path.abspath(".")
        return os.path.join(rutabase,ruta)

    def validacion(self, user, pas):
        return len(user) > 0 and len(pas) > 0

    def create_table(self):
        consulta = '''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY,
            name TEXT,
            password TEXT
        )
        '''
        self.eje_consulta(consulta)

    def eje_consulta(self, consulta, parametros=()):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(consulta, parametros)
                conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror(title="Error", message="Error al ejecutar la consulta: {}".format(e))

    def registro(self):
        user = self.username.get()
        pas = self.password.get()
        key = self.key.get()
        if self.validacion(user, pas):
            if len(pas) < 6:
                messagebox.showinfo(title="Error", message="Contraseña demasiado corta")
                self.username.delete(0, 'end')
                self.password.delete(0, 'end')
            else:
                if key=="1234":
                    self.create_table()  # Asegurarse de que la tabla existe
                    # Insertar el usuario con rol predeterminado 'empleado'
                    consulta = "INSERT INTO usuarios (username, password, rol) VALUES (?, ?, ?)"
                    parametros = (user, pas, "Empleado")
                    self.eje_consulta(consulta, parametros)
                    self.control1()
                    # Mostrar mensaje de confirmación
                    messagebox.showinfo(title="Éxito", message="Usuario creado correctamente")
                else:
                    messagebox.showerror(title="Registro",message="Error al ingresar el código de registro")
            consulta = "SELECT rol FROM usuarios WHERE username=? AND password=?"
            parametros = (user, pas)

            try:
                with sqlite3.connect(self.db_name) as conn:
                    cursor = conn.cursor()
                    cursor.execute(consulta, parametros)
                    result = cursor.fetchone()

                    if result:
                        rol = result[0]
                        self.controlador.set_rol_actual(rol)  # Utiliza un setter para claridad
                        self.controlador.show_frame(Container)
                    else:
                        self.username.delete(0, 'end')
                        self.password.delete(0, 'end')
                        messagebox.showerror(title="Error", message="Usuario y/o contraseña incorrecta")
            except sqlite3.Error as e:
                messagebox.showerror(title="Error", message="No se conectó a la base de datos: {}".format(e))
        else:
            messagebox.showerror(title="Error", message="Llene sus datos")

    def control1(self):
        self.controlador.show_frame(Container)

    def control2(self):
        self.controlador.show_frame(Login)

    def widgets(self):
        
#Frame izquierdo 
        fondo = Frame(self, bg="#FFFFFF",highlightbackground="gray", highlightthickness=1)
        fondo.pack()
        fondo.place(x=0, y=0, width=550, height=650)

        ruta=self.rutas(r"imagenes/logo1.png")
        self.logo_image = Image.open(ruta)
        self.logo_image = self.logo_image.resize((250, 250))
        self.logo_image = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = ttk.Label(fondo, image=self.logo_image, background="#FFFFFF")
        self.logo_label.place(x=140, y=60)
        
        lblubicacion=tk.Label(fondo, text="BAR UNIVERSITARIO", font="sans 30 bold", bg="#FFFFFF", fg="black", anchor="center")
        lblubicacion.place(x=0, y=360, width=545)
            
        lblcorreo=tk.Label(fondo, text="Email: bar@comunidad.frrq.utn.edu.ar", font="sans 20 bold", bg="#FFFFFF", fg="black", anchor="center")
        lblcorreo.place(x=0, y=420, width=545)

#Frame derecho         
        fondo2 = Frame(self, bg="#BEBEBE",highlightbackground="gray", highlightthickness=1)
        fondo2.pack()
        fondo2.place(x=550, y=0, width=550, height=650)
        
        label = ttk.Label(fondo2, text="Registrarse", font="sans 36 bold", background="#BEBEBE")
        label.place(x=145, y=80)
        
        user = Label(fondo2, text="Nombre de usuario", font="sans 22 bold", bg="#BEBEBE")
        user.place(x=150, y=180)
        self.username = ttk.Entry(fondo2, font="sans 16 bold")
        self.username.place(x=150, y=220, width=240, height=40)
        
        pas = Label(fondo2, text="Contraseña", font="sans 22 bold", bg="#BEBEBE")
        pas.place(x=150, y=260)
        self.password = ttk.Entry(fondo2, show="*", font="16")
        self.password.place(x=150, y=300, width=240, height=40)
        
        key = Label(fondo2, text="Código de registro", font="sans 22 bold", bg="#BEBEBE")
        key.place(x=150, y=340)
        self.key = ttk.Entry(fondo2, show="*", font="16")
        self.key.place(x=150, y=380, width=240, height=40)

        ruta=self.rutas(r"icono/registrar.png")
        imagen_pil = Image.open(ruta)
        imagen_resize3 = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize3)
        
        btn3 = Button(fondo2, bg="#FFFFFF", fg="black", text="Registrarse", font="sans 16 bold", command=self.registro)
        btn3.config(image=imagen_tk, compound=LEFT, padx=10)
        btn3.image = imagen_tk
        btn3.place(x=150, y=440, width=240, height=40)

        ruta=self.rutas(r"icono/regresar.png")
        imagen_pil = Image.open(ruta)
        imagen_resize4 = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize4)

        btn4 = Button(fondo2, bg="#FFFFFF", fg="black", text="Regresar", font="sans 16 bold", command=self.control2)
        btn4.config(image=imagen_tk, compound=LEFT, padx=10)
        btn4.image = imagen_tk
        btn4.place(x=150, y=500, width=240, height=40)