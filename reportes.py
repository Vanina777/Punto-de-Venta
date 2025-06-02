import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk,messagebox
from PIL import Image, ImageTk
from tkcalendar import DateEntry
import sys
import os
import babel.numbers
    
class Reportes(tk.Frame):
    db_name = "database.db"
    0
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
        
        titulo = tk.Label(self, text="REPORTES 1", font="sans 30 bold", bg="#BEBEBE", anchor="center")
        titulo.pack()  
        titulo.place(x=5, y=0, width=1090, height=90)
        
#Frame izquierdo Reporte de ventas totales
        
        self.frame1 = tk.Frame(self, bg="#7A7A7A",highlightbackground="gray", highlightthickness=1)
        self.frame1.place(x=0, y=100, width=550, height=550)  # Ajuste de altura a 260
        
    #Agregar el label de Reporte de ventas totales
        label_reporte = tk.Label(self.frame1, text="Reporte de ventas totales", font="sans 22 bold", bg="#7A7A7A", fg="black")
        label_reporte.place(x=110, y=10, height=40)  

    #Crear los widgets para el filtro de fechas
        self.frame_filtro = tk.LabelFrame(self.frame1, bg="#BEBEBE")
        self.frame_filtro.place(x=10, y=60, width=530, height=120)

        label_desde = tk.Label(self.frame_filtro, text="Desde:", font="sans 14 bold", bg="#BEBEBE")
        label_desde.place(x=0, y=5, width=100, height=40)
        self.entry_desde = DateEntry(self.frame_filtro, font="sans 14 bold",date_pattern="yyyy-mm-dd")
        self.entry_desde.place(x=100, y=5, width=130, height=40)

        label_hasta = tk.Label(self.frame_filtro, text="Hasta:", font="sans 14 bold", bg="#BEBEBE")
        label_hasta.place(x=240, y=5, width=100, height=40)
        self.entry_hasta = DateEntry(self.frame_filtro, font="sans 14 bold",date_pattern="yyyy-mm-dd")
        self.entry_hasta.place(x=340, y=5, width=130, height=40)

        ruta=self.rutas(r"icono/filtrar.png")
        imagen_pil = Image.open(ruta)
        imagen_resize = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize)

        boton_filtrar = tk.Button(self.frame_filtro, text="Filtrar", font="sans 12 bold", bg="#FFFFFF", command=self.generar_reporte)
        boton_filtrar.config(image=imagen_tk, compound=LEFT, padx=10)
        boton_filtrar.image = imagen_tk
        boton_filtrar.place(x=100, y=60, width=140, height=40)

    #Crear la tabla para mostrar el reporte de ventas
        self.tabla_reporte = ttk.Treeview(self.frame1, columns=("Cantidad de Ventas", "Total de Ventas"), show="headings", height=5)  
        self.tabla_reporte.heading("Cantidad de Ventas", text="Cantidad de productos vendidos", anchor="center")
        self.tabla_reporte.heading("Total de Ventas", text="Total de Ventas", anchor="center")
        self.tabla_reporte.column("Cantidad de Ventas", width=200, anchor="center")
        self.tabla_reporte.column("Total de Ventas", width=200, anchor="center")
        self.tabla_reporte.place(x=10, y=200, width=530, height=200)  

        # Formatear la columna "Total de Ventas" 
        self.tabla_reporte.tag_configure("money", font="sans 10")
        self.tabla_reporte.tag_configure("money", foreground="black")
        self.tabla_reporte.tag_configure("money", background="#BEBEBE")
        self.tabla_reporte.tag_configure("money", anchor="center")
        
    #Nota
        label_nota = tk.Label(self.frame1, text="El reporte de ventas totales equivale al total de las ventas de los \nproductos incluyendo costo y ganancia", font="sans 10 bold", bg="#7A7A7A", fg="black")
        label_nota.place(x=50, y=420, height=80) 
        
#Frame derecha Reporte de ganancias
        
        self.frame2 = tk.Frame(self, bg="#7A7A7A",highlightbackground="gray", highlightthickness=1)
        self.frame2.place(x=550, y=100, width=550, height=550)

        # Agregar el label de Reporte de ventas totales
        label_reporte = tk.Label(self.frame2, text="Reporte de ganancias", font="sans 22 bold", bg="#7A7A7A", fg="black")
        label_reporte.place(x=110, y=10, height=40)  

        self.frame_filtro1 = tk.LabelFrame(self.frame2, bg="#BEBEBE")
        self.frame_filtro1.place(x=10, y=60, width=530, height=120)

        ruta=self.rutas(r"icono/filtrar.png")
        imagen_pil = Image.open(ruta)
        imagen_resize1 = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize1)

        boton_reporte = tk.Button(self.frame_filtro1, text="Reporte", font="sans 12 bold", bg="#FFFFFF",command=self.generar_reporte_ganancias_totales)
        boton_reporte .config(image=imagen_tk, compound=LEFT, padx=10)
        boton_reporte .image = imagen_tk
        boton_reporte .place(x=100, y=60, width=140, height=40)
        
        label_desde1 = tk.Label(self.frame_filtro1, text="Desde:", font="sans 14 bold", bg="#BEBEBE")
        label_desde1.place(x=0, y=5, width=100, height=40)
        self.entry_desde1 = DateEntry(self.frame_filtro1, font="sans 14 bold",date_pattern="yyyy-mm-dd")
        self.entry_desde1.place(x=100, y=5, width=130, height=40)

        label_hasta1 = tk.Label(self.frame_filtro1, text="Hasta:", font="sans 14 bold", bg="#BEBEBE")
        label_hasta1.place(x=240, y=5, width=100, height=40)
        self.entry_hasta1 = DateEntry(self.frame_filtro1, font="sans 14 bold",date_pattern="yyyy-mm-dd")
        self.entry_hasta1.place(x=340, y=5, width=130, height=40)
        
        # Crear el Treeview para mostrar el reporte de ganancias totales
        self.tabla_ganancias = ttk.Treeview(self.frame2, columns=("Ganancias Totales",), show="headings",height=5)
        self.tabla_ganancias.heading("Ganancias Totales", text="Ganancias Totales", anchor="center")
        self.tabla_ganancias.column("Ganancias Totales", width=200,anchor="center")
        self.tabla_ganancias.place(x=300, y=300, width=300, height=200, anchor="center")  
        
    #Nota
        label_nota = tk.Label(self.frame2, text="El reporte de ganancias equivale a las ventas totales menos el costo \nde los productos", font="sans 10 bold", bg="#7A7A7A", fg="black")
        label_nota.place(x=50, y=420, height=80) 
       
#funciones del Frame izquierdo ventas totales
    def format_currency(self, amount):
        # Convertir el número a una cadena con separadores de miles 
        return f' {amount:,.0f}'

    def generar_reporte(self):
        fecha_desde = self.entry_desde.get()
        fecha_hasta = self.entry_hasta.get()

        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()

            # Consulta para obtener la cantidad de ventas y el total de ventas para el intervalo de fechas
            c.execute("SELECT COUNT(*), SUM(total) FROM ventas WHERE fecha BETWEEN ? AND ?", (fecha_desde, fecha_hasta))
            resultado = c.fetchone()
            conn.close()

            cantidad_ventas = resultado[0]
            total_ventas = resultado[1]

            # Limpiar la tabla antes de actualizarla con nuevos datos
            for item in self.tabla_reporte.get_children():
                self.tabla_reporte.delete(item)

            # Formatear el total de ventas como moneda 
            formatted_total = self.format_currency(total_ventas)

            # Insertar los resultados en la tabla de reporte
            self.tabla_reporte.insert("", "end", values=(cantidad_ventas, formatted_total))

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al generar el reporte: {e}")
       
#Funciones del Frame derecha ganancias totales
    def generar_reporte_ganancias_totales(self):
        # Obtener las fechas desde los widgets de entrada
        fecha_desde = self.entry_desde1.get()
        fecha_hasta = self.entry_hasta1.get()

        try:
            # Conectar a la base de datos
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()

            # Obtener la sumatoria de los valores de la columna 'total' para el intervalo de fechas
            c.execute("SELECT SUM(total) FROM ventas WHERE fecha BETWEEN ? AND ?", (fecha_desde, fecha_hasta))
            total_ventas = c.fetchone()[0] or 0

            # Obtener la sumatoria de los valores de la columna 'costo' para el intervalo de fechas
            c.execute("SELECT SUM(costo) FROM ventas WHERE fecha BETWEEN ? AND ?", (fecha_desde, fecha_hasta))
            total_costos = c.fetchone()[0] or 0

            # Calcular las ganancias totales restando los costos totales de las ventas totales
            ganancias_totales = total_ventas - total_costos

            conn.close()

            # Borrar cualquier entrada anterior en la tabla de ganancias
            for item in self.tabla_ganancias.get_children():
                self.tabla_ganancias.delete(item)

            # Insertar una fila en la tabla con las ganancias totales
            self.tabla_ganancias.insert("", "end", values=(f" {ganancias_totales:,.0f}",))

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al generar el reporte de ganancias totales: {e}")