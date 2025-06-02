import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import datetime
from tkcalendar import DateEntry
import sys
import os
import babel.numbers

class Gastos(tk.Frame):
    db_name = "database.db"
    
    def __init__(self, padre):
        super().__init__(padre)
        self.widgets()
        self.cargar_registros()
        
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
        
        titulo = tk.Label(self, text="CONTROL DE GASTOS", font="sans 30 bold", bg="#BEBEBE", anchor="center")
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
        
#LabelFrame con entrys para ingresar datos
        self.labelframe = tk.LabelFrame(frame2, text="Registrar gasto", font="sans 22 bold", bg="#BEBEBE")
        self.labelframe.place(x=20,y=30,width=400,height=500)
        
        lblconcepto = tk.Label(self.labelframe, text="Concepto: ", font="sans 14 bold", bg="#BEBEBE")
        lblconcepto.place(x=10, y=20)
        self.concepto = ttk.Entry(self.labelframe, font="sans 14 bold")
        self.concepto.place(x=140,y=20,width=240,height=40)
        
        lblvalor = tk.Label(self.labelframe, text="Valor: ", font="sans 14 bold", bg="#BEBEBE")
        lblvalor.place(x=10, y=80)
        self.valor = ttk.Entry(self.labelframe, font="sans 14 bold")
        self.valor.place(x=140,y=80,width=240,height=40)

        lblentidad = Label(self.labelframe, text="Entidad: ", font="sans 14 bold", bg="#BEBEBE")
        lblentidad.place(x=10, y=140)
        self.entidad = ttk.Entry(self.labelframe, font="sans 14 bold")
        self.entidad.place(x=140,y=140,width=240,height=40)
        
        lblfecha = tk.Label(self.labelframe, text="Fecha: ", font="sans 14 bold", bg="#BEBEBE")
        lblfecha.place(x=10, y=200)
        self.fecha = DateEntry(self.labelframe, font="sans 14 bold",date_pattern='dd-mm-yyyy')
        self.fecha.place(x=140,y=200,width=240,height=40)
        
        ruta=self.rutas(r"icono/ingresarc.png")
        imagen_pil = Image.open(ruta)
        imagen_resize = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize)
        
        btn1 = Button(self.labelframe, bg="#FFFFFF", fg="black", text="Ingresar", font="roboto 16 bold",command=self.registrar)
        btn1.config(image=imagen_tk, compound=LEFT, padx=10)
        btn1.image = imagen_tk
        btn1.place(x=140, y=280,width=150, height=40)

        ruta=self.rutas(r"icono/modificar.png")
        imagen_pil = Image.open(ruta)
        imagen_resize2 = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize2)

        btn_modificar = Button(self.labelframe, bg="#FFFFFF", fg="black", text="Modificar", font="roboto 16 bold", command=self.abrir_ventana_modificar)
        btn_modificar.config(image=imagen_tk, compound=LEFT, padx=10)
        btn_modificar.image = imagen_tk
        btn_modificar.place(x=140, y=340,width=150, height=40)

#Treeview Tabla
        treFrame=Frame(frame2,bg="white") 
        treFrame.place(x=440,y=50,width=620,height=450)
        
        # Barra de desplazamiento vertical
        scrol_y = ttk.Scrollbar(treFrame)
        scrol_y.pack(side=RIGHT, fill=Y)

        # Barra de desplazamiento horizontal
        scrol_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill=X)

        # Widget Treeview
        self.tre = ttk.Treeview(treFrame, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set, height=40, 
                                columns=("ID", "Concepto", "Valor", "Entidad", "Fecha"),show="headings")
        self.tre.pack(expand=True, fill=BOTH)

        scrol_y.config(command=self.tre.yview)
        scrol_x.config(command=self.tre.xview)

        # Configurar columnas
        self.tre.heading("ID", text="ID")
        self.tre.heading("Concepto", text="Concepto")
        self.tre.heading("Valor", text="Valor")
        self.tre.heading("Entidad", text="Entidad")
        self.tre.heading("Fecha", text="Fecha")

        self.tre.column("ID", width=50, anchor="center")
        self.tre.column("Concepto", width=200, anchor="center")
        self.tre.column("Valor", width=120, anchor="center")
        self.tre.column("Entidad", width=130, anchor="center")
        self.tre.column("Fecha", width=100, anchor="center")

#Funciones
    def cargar_registros(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM gastos ORDER BY id DESC")
            rows = cursor.fetchall()

            # Limpiar el Treeview antes de cargar los registros
            for item in self.tre.get_children():
                self.tre.delete(item)

            for row in rows:
                valor = row[2]
                valor_formateado = "{:,.0f} ".format(valor)
                self.tre.insert("", "end", values=(row[0], row[1], valor_formateado, row[3], row[4]))
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo cargar los registros: {e}")

    def validar_campos(self):
        if not self.concepto.get() or not self.valor.get() or not self.entidad.get() or not self.fecha.get():
            messagebox.showerror("Error", "Todos los campos son requeridos.")
            return False
        return True

    def registrar(self):
        if not self.validar_campos():
            return

        concepto = self.concepto.get()
        valor = self.valor.get()
        entidad = self.entidad.get()
        fecha = self.fecha.get()

        # Guardar en la base de datos
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # Obtener el último ID registrado
            cursor.execute("SELECT MAX(id) FROM gastos")
            last_id = cursor.fetchone()[0]
            new_id = last_id + 1 if last_id else 1  # Si last_id es None, iniciar en 1

            cursor.execute("INSERT INTO gastos (id, concepto, valor, entidad, fecha) VALUES (?, ?, ?, ?, ?)",
                        (new_id, concepto, valor, entidad, fecha))
            conn.commit()
            conn.close()

            valor_float = float(valor)
            valor_formateado = "{:,.0f} ".format(valor_float)
            messagebox.showinfo("Éxito", f"Gasto registrado correctamente. Valor: {valor_formateado}")

            self.limpiar_campos()
            self.cargar_registros()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar el gasto: {e}")

    def limpiar_campos(self):
        self.concepto.delete(0, END)
        self.valor.delete(0, END)
        self.entidad.delete(0, END)
        self.fecha.delete(0, END)

    def abrir_ventana_modificar(self):
        # Obtener el ID del registro seleccionado
        item = self.tre.selection()
        if not item:
            messagebox.showerror("Error", "Por favor selecciona un registro para modificar.")
            return
        id_seleccionado = self.tre.item(item, "values")[0]

        # Obtener los datos del registro seleccionado
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM gastos WHERE id=?", (id_seleccionado,))
        registro = cursor.fetchone()
        conn.close()

        if not registro:
            messagebox.showerror("Error", "No se pudo encontrar el registro seleccionado.")
            return

        #Toplevel para modificar el registro
        self.ventana_modificar = Toplevel(self)
        self.ventana_modificar.title("Modificar Registro")
        self.ventana_modificar.geometry("400x400")
        self.ventana_modificar.config(bg="#BEBEBE")

        # Crear campos para modificar los datos
        lblconcepto = Label(self.ventana_modificar, text="Concepto:", font="sans 14 bold",bg="#BEBEBE")
        lblconcepto.grid(row=0, column=0, padx=10, pady=5)
        self.entry_concepto_modificar = Entry(self.ventana_modificar, font="sans 14 bold")
        self.entry_concepto_modificar.grid(row=0, column=1, padx=10, pady=5)
        self.entry_concepto_modificar.insert(0, registro[1])  # Concepto

        lblvalor = Label(self.ventana_modificar, text="Valor (COP):", font="sans 14 bold",bg="#BEBEBE")
        lblvalor.grid(row=1, column=0, padx=10, pady=5)
        self.entry_valor_modificar = Entry(self.ventana_modificar, font="sans 14 bold")
        self.entry_valor_modificar.grid(row=1, column=1, padx=10, pady=5)
        self.entry_valor_modificar.insert(0, registro[2])  # Valor

        lblentidad = Label(self.ventana_modificar, text="Entidad:", font="sans 14 bold",bg="#BEBEBE")
        lblentidad.grid(row=2, column=0, padx=10, pady=5)
        self.entry_entidad_modificar = Entry(self.ventana_modificar, font="sans 14 bold")
        self.entry_entidad_modificar.grid(row=2, column=1, padx=10, pady=5)
        self.entry_entidad_modificar.insert(0, registro[3])  # Entidad

        lblfecha = Label(self.ventana_modificar, text="Fecha:", font="sans 14 bold",bg="#BEBEBE")
        lblfecha.grid(row=3, column=0, padx=10, pady=5)
        self.entry_fecha_modificar = DateEntry(self.ventana_modificar, font="sans 14 bold")
        self.entry_fecha_modificar.grid(row=3, column=1, padx=10, pady=5)
        self.entry_fecha_modificar.set_date(registro[4])  # Fecha

        # Botón para guardar los cambios
        ruta=self.rutas(r"icono/guardar.png")
        imagen_pil = Image.open(ruta)
        imagen_resize4 = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize4)
        
        btn_guardar_cambios = Button(self.ventana_modificar, text="Guardar Cambios", bg="#FFFFFF", fg="black", font="sans 14 bold", command=lambda: self.guardar_cambios(id_seleccionado))
        btn_guardar_cambios.config(image=imagen_tk, compound=LEFT, padx=10)
        btn_guardar_cambios.image = imagen_tk
        btn_guardar_cambios.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

    def guardar_cambios(self, id_registro):
        concepto = self.entry_concepto_modificar.get()
        valor = self.entry_valor_modificar.get()
        entidad = self.entry_entidad_modificar.get()
        fecha = self.entry_fecha_modificar.get()

        # Actualizar el registro en la base de datos
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("UPDATE gastos SET concepto=?, valor=?, entidad=?, fecha=? WHERE id=?",
                        (concepto, valor, entidad, fecha, id_registro))
            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", "Cambios guardados correctamente.")

            # Actualizar el Treeview
            self.cargar_registros()

            # Cerrar la ventana Toplevel
            self.ventana_modificar.destroy()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo guardar los cambios: {e}")

    def actualizar_fecha_y_hora(self): 
        # Obtener la fecha y hora actual
        fecha_actual = datetime.datetime.now().strftime("%d-%m-%Y")
        hora_actual = datetime.datetime.now().strftime("%H:%M:%S")

        # Actualizar las etiquetas de fecha y hora
        self.label_fecha.config(text=fecha_actual)
        self.label_hora.config(text=hora_actual)

        # Llamar a este método nuevamente después de 1000 ms (1 segundo)
        self.after(1000, self.actualizar_fecha_y_hora)