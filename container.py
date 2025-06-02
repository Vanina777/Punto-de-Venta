from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
from ventas import Ventas
from inventario import Inventario
from clientes import Clientes
from reportes import Reportes
from proveedor import Proveedor
from reportes2 import Reportes2
from pedidos import Pedidos
from gastos import Gastos
from usuarios import Usuarios
from informacion import Informacion
import sys
import os

class Container(tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        self.pack()
        self.place(x=0, y=0, width=1100, height=650)
        self.config(bg="#545454")
        self.widgets()
        
    def rutas(self,ruta):
        try:
            rutabase=sys.__MEIPASS
        except Exception:
            rutabase=os.path.abspath(".")
        return os.path.join(rutabase,ruta)

    def show_frames(self, container):
        top_level = tk.Toplevel(self)
        frame = container(top_level)
        frame.config(bg="#BEBEBE")
        frame.pack(fill="both", expand=True)
        top_level.geometry("1100x650+120+20")
        top_level.resizable(False, False)
        
        top_level.transient(self.master)
        top_level.grab_set()
        top_level.focus_set()
        top_level.lift()

    def ventas(self):
        self.show_frames(Ventas)

    def inventario(self):
        if self.controlador.rol_actual == "Empleado":
            tk.messagebox.showwarning("Acceso Denegado", "No tienes permiso para acceder al Inventario.")
            return
        self.show_frames(Inventario)
        
    def clientes(self):
        self.show_frames(Clientes)

    def reportes(self):
        if self.controlador.rol_actual == "Empleado":
            tk.messagebox.showwarning("Acceso Denegado", "No tienes permiso para acceder al Reporte.")
            return
        self.show_frames(Reportes)

    def proveedor(self):
        if self.controlador.rol_actual == "Empleado":
            tk.messagebox.showwarning("Acceso Denegado", "No tienes permiso para acceder al Proveedor.")
            return
        self.show_frames(Proveedor)
        
    def reportes2(self):
        if self.controlador.rol_actual == "Empleado":
            tk.messagebox.showwarning("Acceso Denegado", "No tienes permiso para acceder al Reporte.")
            return
        self.show_frames(Reportes2)
        
    def pedidos(self):
        if self.controlador.rol_actual == "Empleado":
            tk.messagebox.showwarning("Acceso Denegado", "No tienes permiso para acceder a Pedidos.")
            return
        self.show_frames(Pedidos)
    
    def gastos(self):
        if self.controlador.rol_actual == "Empleado":
            tk.messagebox.showwarning("Acceso Denegado", "No tienes permiso para acceder a Gastos.")
            return
        self.show_frames(Gastos)
        
    def usuarios(self):
        if self.controlador.rol_actual == "Empleado":
            tk.messagebox.showwarning("Acceso Denegado", "No tienes permiso para acceder a Usuarios.")
            return
        self.show_frames(Usuarios)
        
    def informacion(self):
        self.show_frames(Informacion)

    def controlar_acceso(self):
       
        if self.controlador.rol_actual == "Empleado":
            # Solo habilitar botones permitidos para empleados
            self.btnventas.config(state="normal")
            self.btngraficos.config(state="normal")
            self.btninformacion.config(state="normal")
        
            # Deshabilitar otros botones
            self.btninventario.config(state="disabled")
            self.btnproveedor.config(state="disabled")
            self.btnpedidos.config(state="disabled")
            self.btnreportes.config(state="disabled")
            self.btnreportes2.config(state="disabled")
            self.btngastos.config(state="disabled")
            self.btnusuarios.config(state="disabled")
        elif self.controlador.rol_actual == "encargado":
            # Habilitar todos los botones
            self.btnventas.config(state="normal")
            self.btngraficos.config(state="normal")
            self.btninformacion.config(state="normal")
            self.btninventario.config(state="normal")
            self.btnproveedor.config(state="normal")
            self.btnpedidos.config(state="normal")
            self.btnreportes.config(state="normal")
            self.btnreportes2.config(state="normal")
            self.btngastos.config(state="normal")
            self.btnusuarios.config(state="normal")

    def widgets(self):  
        
#Frame superior
        frame1 = tk.Frame(self, bg="#BEBEBE",highlightbackground="gray")
        frame1.pack()
        frame1.place(x=0, y=0, width=1100, height=100)
        
        lblframe1=tk.Label(frame1, text="Inicio", font="sans 30 bold", bg="#BEBEBE", anchor="center")
        lblframe1.place(x=3, y=5, width=1095, height=90)
        
#Frame izquierdo
        frame2=tk.Frame(self, bg="#BEBEBE", highlightbackground="gray", highlightthickness=1)
        frame2.place(x=20, y=120, width=260, height=495)
        
        #Boton VENTAS
        ruta=self.rutas(r"icono/btnventas.png")
        imagen_pil = Image.open(ruta)
        imagen_resize = imagen_pil.resize((40, 40))
        imagen_tk = ImageTk.PhotoImage(imagen_resize)
        
        self.btnventas = Button(frame2, bg="#FFFFFF", fg="black", text="Ventas", font="sans 18 bold", command=self.ventas)
        self.btnventas.config(image=imagen_tk, compound="left", padx=10)
        self.btnventas.image = imagen_tk
        self.btnventas.place(x=10, y=30, width=240, height=60)
        
        #Boton INVENTARIO
        ruta=self.rutas(r"icono/btninventario.png")
        imagen_pil = Image.open(ruta)
        imagen_resize1 = imagen_pil.resize((40, 40))
        imagen_tk = ImageTk.PhotoImage(imagen_resize1)
        
        self.btninventario = Button(frame2, bg="#FFFFFF", fg="black", text="Inventario", font="sans 18 bold",command=self.inventario)
        self.btninventario.config(image=imagen_tk, compound="left", padx=10)
        self.btninventario.image = imagen_tk
        self.btninventario.place(x=10, y=120, width=240, height=60)
        
        #Boton CLIENTES
        ruta=self.rutas(r"icono/btnclientes.png")
        imagen_pil = Image.open(ruta)
        imagen_resize2 = imagen_pil.resize((40, 40))
        imagen_tk = ImageTk.PhotoImage(imagen_resize2)
        
        self.btngraficos = Button(frame2, bg="#FFFFFF", fg="black", text="Clientes", font="sans 18 bold", command=self.clientes)
        self.btngraficos.config(image=imagen_tk, compound="left", padx=10)
        self.btngraficos.image = imagen_tk
        self.btngraficos.place(x=10, y=210, width=240, height=60)
        
        #Boton PROVEEDOR
        ruta=self.rutas(r"icono/btnproveedor.png")
        imagen_pil = Image.open(ruta)
        imagen_resize4 = imagen_pil.resize((40, 40))
        imagen_tk = ImageTk.PhotoImage(imagen_resize4)
        
        self.btnproveedor = Button(frame2, bg="#FFFFFF", fg="black", text="Proveedor", font="sans 18 bold", command=self.proveedor)
        self.btnproveedor.config(image=imagen_tk, compound="left", padx=10)
        self.btnproveedor.image = imagen_tk
        self.btnproveedor.place(x=10, y=300, width=240, height=60)
        
        #Boton PEDIDOS
        ruta=self.rutas(r"icono/btnpedidos.png")
        imagen_pil = Image.open(ruta)
        imagen_resize5 = imagen_pil.resize((40, 40))
        imagen_tk = ImageTk.PhotoImage(imagen_resize5)
        
        self.btnpedidos = Button(frame2, bg="#FFFFFF", fg="black", text="Pedidos", font="sans 18 bold",command=self.pedidos)
        self.btnpedidos.config(image=imagen_tk, compound="left", padx=10)
        self.btnpedidos.image = imagen_tk
        self.btnpedidos.place(x=10, y=390, width=240, height=60)
        
#Frame centro
        lblframe3=tk.Frame(self, bg="#FFFFFF", highlightbackground="gray", highlightthickness=1)
        lblframe3.place(x=300, y=120, width=500, height=495)
        
         #Logo 
        ruta=self.rutas(r"imagenes/logo1.png")
        self.logo_image = Image.open(ruta)
        self.logo_image = self.logo_image.resize((250, 250))
        self.logo_image = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(lblframe3,image=self.logo_image, bg="#FFFFFF")
        self.logo_label.place(x=120, y=13)
        
        lblubicacion=tk.Label(lblframe3, text="BAR UNIVERSITARIO", font="sans 18 bold", bg="#FFFFFF", fg="black", anchor="center")
        lblubicacion.place(x=0, y=270, width=490, height=50)
        
        lblcorreo=tk.Label(lblframe3, text="Email: bar@comunidad.frrq.utn.edu.ar", font="sans 18 bold", bg="#FFFFFF", fg="black", anchor="center")
        lblcorreo.place(x=0, y=370, width=490, height=50)
        
#Frame derecho
        frame4=tk.Frame(self, bg="#BEBEBE", highlightbackground="gray", highlightthickness=1)
        frame4.place(x=820, y=120, width=260, height=495)
        
        #Boton REPORTES 1
        ruta=self.rutas(r"icono/btnreportes.png")
        imagen_pil = Image.open(ruta)
        imagen_resize3 = imagen_pil.resize((40, 40))
        imagen_tk = ImageTk.PhotoImage(imagen_resize3)
        
        self.btnreportes = Button(frame4, bg="#FFFFFF", fg="black", text="Reportes 1", font="sans 18 bold",command=self.reportes)
        self.btnreportes.config(image=imagen_tk, compound="left", padx=10)
        self.btnreportes.image = imagen_tk
        self.btnreportes.place(x=10, y=30, width=240, height=60)
        
        #Boton REPORTES 2
        ruta=self.rutas(r"icono/btnreportes2.png")
        imagen_pil = Image.open(ruta)
        imagen_resize6 = imagen_pil.resize((40, 40))
        imagen_tk = ImageTk.PhotoImage(imagen_resize6)
        
        self.btnreportes2 = Button(frame4, bg="#FFFFFF", fg="black", text="Reportes 2", font="sans 18 bold",command=self.reportes2)
        self.btnreportes2.config(image=imagen_tk, compound="left", padx=10)
        self.btnreportes2.image = imagen_tk
        self.btnreportes2.place(x=10, y=120, width=240, height=60)
        
        #Boton GASTOS
        ruta=self.rutas(r"icono/btngastos.png")
        imagen_pil = Image.open(ruta)
        imagen_resize8 = imagen_pil.resize((40, 40))
        imagen_tk = ImageTk.PhotoImage(imagen_resize8)
        
        self.btngastos = Button(frame4, bg="#FFFFFF", fg="black", text="Gastos", font="sans 18 bold",command=self.gastos)
        self.btngastos.config(image=imagen_tk, compound="left", padx=10)
        self.btngastos.image = imagen_tk
        self.btngastos.place(x=10, y=210, width=240, height=60)
        
        #Boton USUARIOS
        ruta=self.rutas(r"icono/btnusuarios.png")
        imagen_pil = Image.open(ruta)
        imagen_resize9 = imagen_pil.resize((40, 40))
        imagen_tk = ImageTk.PhotoImage(imagen_resize9)
        
        self.btnusuarios = Button(frame4, bg="#FFFFFF", fg="black", text="Usuarios", font="sans 18 bold",command=self.usuarios)
        self.btnusuarios.config(image=imagen_tk, compound="left", padx=10)
        self.btnusuarios.image = imagen_tk
        self.btnusuarios.place(x=10, y=300, width=240, height=60)
        
        #Boton ACERCA DE
        ruta=self.rutas(r"icono/btninformacion.png")
        imagen_pil = Image.open(ruta)
        imagen_resize10 = imagen_pil.resize((40, 40))
        imagen_tk = ImageTk.PhotoImage(imagen_resize10)
        
        self.btninformacion = Button(frame4, bg="#FFFFFF", fg="black", text="Acerca de", font="sans 18 bold",command=self.informacion)
        self.btninformacion.config(image=imagen_tk, compound="left", padx=10)
        self.btninformacion.image = imagen_tk
        self.btninformacion.place(x=10, y=390, width=240, height=60)

        self.controlar_acceso()       