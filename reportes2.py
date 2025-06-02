import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk,messagebox
from PIL import Image, ImageTk
from tkcalendar import DateEntry
import sys
import os
import babel.numbers

class Reportes2(tk.Frame):
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
        
        titulo = tk.Label(self, text="REPORTES 2", font="sans 30 bold", bg="#BEBEBE", anchor="center")
        titulo.pack()  
        titulo.place(x=5, y=0, width=1090, height=90)
        
#Frame izquierdo Costo total de inventario
        
        self.frame3 = tk.Frame(self, bg="#7A7A7A",highlightbackground="gray", highlightthickness=1)
        self.frame3.place(x=0, y=100, width=550, height=550)

        label_reporte_costo = tk.Label(self.frame3, text="Costo Total de Inventario", font="sans 22 bold", bg="#7A7A7A", fg="black")
        label_reporte_costo.pack(pady=10)

        self.tabla_costo_inventario = ttk.Treeview(self.frame3, columns=("Costo Total",), show="headings", height=5)
        self.tabla_costo_inventario.heading("Costo Total", text="Costo Total", anchor="center")
        self.tabla_costo_inventario.column("Costo Total", width=200, anchor="center")
        self.tabla_costo_inventario.pack(pady=10)

        ruta=self.rutas(r"icono/reporte.png")
        imagen_pil = Image.open(ruta)
        imagen_resize2 = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize2)

        boton_generar_reporte_costo = tk.Button(self.frame3, text="Generar Reporte", font="sans 12 bold", bg="#FFFFFF", command=self.calcular_costo_total)
        boton_generar_reporte_costo.config(image=imagen_tk, compound=LEFT, padx=10)
        boton_generar_reporte_costo.image = imagen_tk
        boton_generar_reporte_costo.pack(pady=10)
        
    #Nota
        label_nota = tk.Label(self.frame3, text="El reporte de costo total de inventario muestra lo que costo adquirir \nlos productos", font="sans 10 bold", bg="#7A7A7A", fg="black")
        label_nota.place(x=50, y=420, height=80) 

#Frame derecha Costo total de inventario

        self.frame4 = tk.Frame(self, bg="#7A7A7A",highlightbackground="gray", highlightthickness=1)
        self.frame4.place(x=550, y=100, width=550, height=550)
     
        label_reporte_costo_ventas = tk.Label(self.frame4, text="Reporte de Costo Total de Ventas", font="sans 22 bold", bg="#7A7A7A", fg="black")
        label_reporte_costo_ventas.pack(pady=10)

    #Frame Entry fechas
        self.lblframe = tk.Frame(self.frame4,bg="#BEBEBE",highlightbackground="gray", highlightthickness=1)
        self.lblframe.place(x=20,y=80,width=250,height=200)

        label_desde_ventas = tk.Label(self.lblframe, text="Desde:", font="sans 14 bold", bg="#BEBEBE")
        label_desde_ventas.place(x=10, y=15)

        self.entry_desde_ventas = DateEntry(self.lblframe, font="sans 14 bold",date_pattern="yyyy-mm-dd")
        self.entry_desde_ventas.place(x=90, y=15, width=130, height=40)

        label_hasta_ventas = tk.Label(self.lblframe, text="Hasta:", font="sans 14 bold", bg="#BEBEBE")
        label_hasta_ventas.place(x=10, y=70)

        self.entry_hasta_ventas = DateEntry(self.lblframe, font="sans 14 bold",date_pattern="yyyy-mm-dd")
        self.entry_hasta_ventas.place(x=90, y=70, width=130, height=40)

    #TreeView Tabla
        self.tabla_costo_ventas = ttk.Treeview(self.frame4, columns=("Costo Total de Ventas",), show="headings", height=5)
        self.tabla_costo_ventas.heading("Costo Total de Ventas", text="Costo Total de Ventas", anchor="center")
        self.tabla_costo_ventas.column("Costo Total de Ventas", width=180, anchor="center")
        self.tabla_costo_ventas.place(x=300, y=80, width=180, height=200)

        ruta=self.rutas(r"icono/reporte.png")
        imagen_pil = Image.open(ruta)
        imagen_resize3 = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize3)

        boton_generar_reporte_costo_ventas = tk.Button(self.lblframe, text="Generar Reporte", font="sans 12 bold", bg="#FFFFFF", command=self.calcular_costo_total_ventas)
        boton_generar_reporte_costo_ventas.config(image=imagen_tk, compound=LEFT, padx=10)
        boton_generar_reporte_costo_ventas.image = imagen_tk
        boton_generar_reporte_costo_ventas.place(x=50, y=130, width=180, height=40)
        
    #Nota
        label_nota = tk.Label(self.frame4, text="El reporte de costo total de ventas muestra lo que costó \nunicamente los productos que ya se vendieron", font="sans 10 bold", bg="#7A7A7A", fg="black")
        label_nota.place(x=100, y=420, height=80) 
 
#funciones del Frame 3 ganancias totales
    def eje_consulta(self, consulta):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(consulta)
            return cursor
        except sqlite3.Error as e:
            messagebox.showerror("Error de Base de Datos", f"Error al ejecutar la consulta: {e}")
    
    def calcular_costo_total(self):
        try:
            consulta = "SELECT SUM(costo * stock) FROM inventario"
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(consulta)
            total_invertido = cursor.fetchone()[0] or 0
            conn.close()

            # Limpiar la tabla antes de actualizarla con nuevos datos
            for item in self.tabla_costo_inventario.get_children():
                self.tabla_costo_inventario.delete(item)

            # Insertar el total invertido en el Treeview
            self.tabla_costo_inventario.insert("", "end", values=(f" {total_invertido:,.0f}",))

        except sqlite3.Error as e:
            messagebox.showerror("Error de Base de Datos", f"Error al ejecutar la consulta: {e}")
            
#funciones del Frame 4 ganancias totales    
    def calcular_costo_total_ventas(self):
        fecha_desde = self.entry_desde_ventas.get()
        fecha_hasta = self.entry_hasta_ventas.get()

        try:
            consulta = "SELECT SUM(costo) FROM ventas WHERE fecha BETWEEN ? AND ?"
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(consulta, (fecha_desde, fecha_hasta))
            total_costo_ventas = cursor.fetchone()[0] or 0
            conn.close()

            # Limpiar la tabla antes de actualizarla con nuevos datos
            for item in self.tabla_costo_ventas.get_children():
                self.tabla_costo_ventas.delete(item)

            # Insertar el total de costo de ventas en el Treeview
            self.tabla_costo_ventas.insert("", "end", values=(f" {total_costo_ventas:,.0f}",))

        except sqlite3.Error as e:
            messagebox.showerror("Error de Base de Datos", f"Error al ejecutar la consulta: {e}")