import sqlite3
import tkinter as tk
from tkinter import ttk
import datetime
from PIL import Image, ImageTk
import sys
import os

class Informacion(tk.Frame):
    db_name = "database.db"

    def __init__(self, parent):
        super().__init__(parent)
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
        
        titulo = tk.Label(frame1, text="INFORMACION", font="sans 30 bold", bg="#BEBEBE", anchor="center")
        titulo.pack() 
        titulo.place(x=5, y=0, width=1090, height=90)
        
        #Frame inferior
        
        frame2 = tk.Frame(self, bg="#FFFFFF",highlightbackground="gray", highlightthickness=1)
        frame2.place(x=0, y=100, width=1100, height=550)

        # Texto de información sobre nosotros
        texto_informacion = """
            Esta aplicación de Punto de Venta fue desarrollada 
            para gestionar eficientemente las ventas en el bar de la facultad. 

            Permite registrar productos, realizar ventas 
            y administrar inventarios y proveedores. 
        
            

            Fue creada en Python con libreria en Tkinter y base de datos en SQLite.

            

            Desarrollado por Vanina Resquin
            Estudiante de Tenico Universitario en Programacion

            UTN Reconquista
        """
        label_info = tk.Label(frame2, text=texto_informacion, font="sans 16", bg="#FFFFFF", justify="center")
        label_info.place(x=150, y=50)
