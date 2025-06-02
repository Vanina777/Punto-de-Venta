import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import datetime
import sys
import os

class Pedidos(tk.Frame):
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
                
        titulo = tk.Label(self, text="PEDIDOS", font="sans 30 bold", bg="#BEBEBE", anchor="center",)
        titulo.pack()  
        titulo.place(x=5, y=0, width=1090, height=90)
        
#Frame inferior
        frame2 = tk.Frame(self, bg="#545454", highlightbackground="gray", highlightthickness=1)
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
        self.numero_pedido = 1  # Variable para mantener el número de pedido actual
        
        labelframe = tk.LabelFrame(frame2, text="Registrar pedidos", font="sans 22 bold", bg="#BEBEBE")
        labelframe.place(x=20,y=30,width=400,height=500)

        lblpedido = Label(labelframe, text="N° Pedido: ", font="sans 14 bold", bg="#BEBEBE")
        lblpedido.place(x=10, y=20)
        self.pedido = Label(labelframe, text="", font="sans 14 bold", relief="groove")
        self.pedido.place(x=140,y=20,width=240,height=40)
        self.actualizar_numero_pedido()  # Actualizar el número de pedido inicial

        lblproveedor = Label(labelframe, text="Proveedor: ", font="sans 14 bold", bg="#BEBEBE")
        lblproveedor.place(x=10, y=80)
        self.proveedor = ttk.Combobox(labelframe, font="sans 14 bold",state="readonly")
        self.proveedor.place(x=140,y=80,width=240,height=40)

        self.cargar_proveedores()

        lblproducto = Label(labelframe, text="Producto: ", font="sans 14 bold", bg="#BEBEBE")
        lblproducto.place(x=10, y=140)
        self.producto = ttk.Combobox(labelframe, font="sans 14 bold",state="readonly")
        self.producto.place(x=140,y=140,width=240,height=40)

        self.cargar_productos()

        lblcantidad = Label(labelframe, text="Nueva Cant: ", font="sans 14 bold", bg="#BEBEBE")
        lblcantidad.place(x=10, y=200)
        self.cantidad = ttk.Entry(labelframe, font="sans 14 bold")
        self.cantidad.place(x=140,y=200,width=240,height=40)

        ruta=self.rutas(r"icono/pedido.png")
        imagen_pil = Image.open(ruta)
        imagen_resize = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize)

        btn1 = Button(labelframe, bg="#FFFFFF", fg="black", text="Agregar", font="roboto 16 bold",command=self.agregar_pedido)
        btn1.config(image=imagen_tk, compound=LEFT, padx=10)
        btn1.image = imagen_tk
        btn1.place(x=80, y=280, width=240, height=40)
        
        ruta=self.rutas(r"icono/rpedido.png")
        imagen_pil = Image.open(ruta)
        imagen_resize1 = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize1)

        btn2 = Button(labelframe, bg="#FFFFFF", fg="black", text="Registrar", font="roboto 16 bold",command=self.registrar_pedido)
        btn2.config(image=imagen_tk, compound=LEFT, padx=10)
        btn2.image = imagen_tk
        btn2.place(x=80, y=340, width=240, height=40)

        ruta=self.rutas(r"icono/verpedidos.png")
        imagen_pil = Image.open(ruta)
        imagen_resize1 = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize1)

        btn3 = Button(labelframe, bg="#FFFFFF", fg="black", text="Ver pedidos", font="roboto 16 bold",command=self.ver_pedidos)
        btn3.config(image=imagen_tk, compound=LEFT, padx=10)
        btn3.image = imagen_tk
        btn3.place(x=80, y=400, width=240, height=40)

    #TreeView Tabla
        treFrame=Frame(frame2,bg="#FFFFFF") 
        treFrame.place(x=440,y=50,width=620,height=450)
        
        # Barra de desplazamiento vertical
        scrol_y = ttk.Scrollbar(treFrame)
        scrol_y.pack(side=RIGHT, fill=Y)

        # Barra de desplazamiento horizontal
        scrol_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill=X)
        
        self.treeview = ttk.Treeview(treFrame, columns=("N° Pedido", "Proveedor", "Producto", "Cantidad", "Fecha", "Hora"), show="headings")
        self.treeview.pack(expand=True, fill=BOTH)

        scrol_y.config(command=self.treeview.yview)
        scrol_x.config(command=self.treeview.xview)

        # Configurar las columnas
        self.treeview.heading("N° Pedido", text="N° Pedido")
        self.treeview.heading("Proveedor", text="Proveedor")
        self.treeview.heading("Producto", text="Producto")
        self.treeview.heading("Cantidad", text="Cantidad")
        self.treeview.heading("Fecha", text="Fecha")
        self.treeview.heading("Hora", text="Hora")

        # Establecer el ancho de las columnas
        self.treeview.column("N° Pedido", width=80,anchor="center")
        self.treeview.column("Proveedor", width=100,anchor="center")
        self.treeview.column("Producto", width=100,anchor="center")
        self.treeview.column("Cantidad", width=100,anchor="center")
        self.treeview.column("Fecha", width=100,anchor="center")
        self.treeview.column("Hora", width=100,anchor="center")

#Funciones
    def cargar_proveedores(self):
            try:
                conn = sqlite3.connect(self.db_name)
                c = conn.cursor()
                c.execute("SELECT nombre FROM proveedores")
                proveedores = c.fetchall()
                nombres_proveedores = [proveedor[0] for proveedor in proveedores]
                self.proveedor["values"] = nombres_proveedores
                conn.close()
            except sqlite3.Error as e:
                print("Error cargando proveedores:", e)
                
    def cargar_productos(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT nombre FROM inventario")
            products = c.fetchall()
            self.producto["values"] = [product[0] for product in products]
            conn.close()
        except sqlite3.Error as e:
            print("Error cargando productos:", e)
            
    def actualizar_fecha_y_hora(self):
        # Obtener la fecha y hora actual
        fecha_actual = datetime.datetime.now().strftime("%d-%m-%Y")
        hora_actual = datetime.datetime.now().strftime("%H:%M:%S")

        # Actualizar las etiquetas de fecha y hora
        self.label_fecha.config(text=fecha_actual)
        self.label_hora.config(text=hora_actual)

        # Llamar a este método nuevamente 
        self.after(1000, self.actualizar_fecha_y_hora)
        
    def actualizar_numero_pedido(self):
        # Conexión a la base de datos
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Obtener el último número de pedido registrado en la base de datos
        cursor.execute("SELECT MAX(numero_pedido) FROM pedidos")
        ultimo_pedido = cursor.fetchone()[0]

        # Si no hay pedidos registrados, establecer el número de pedido como 1
        if ultimo_pedido is None:
            self.numero_pedido = 1
        else:
            # Aumentar el número de pedido en 1
            self.numero_pedido = ultimo_pedido + 1

        # Actualizar la visualización 
        self.pedido.config(text=str(self.numero_pedido))

        conn.close()

    def registrar_pedido(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Recorrer los elementos del Treeview y guardarlos en la base de datos
        for child in self.treeview.get_children():
            pedido = self.treeview.item(child)['values']
            numero_pedido, proveedor, producto, cantidad, fecha, hora = pedido
            
            # Insertar el pedido en la tabla 'pedidos'
            cursor.execute("INSERT INTO pedidos (numero_pedido, proveedor, producto, cantidad, fecha, hora) VALUES (?, ?, ?, ?, ?, ?)", pedido)
            
            # Actualizar el stock en la tabla 'inventario'
            cursor.execute("UPDATE inventario SET stock = stock + ? WHERE nombre = ?", (cantidad, producto))
        
        # Confirmar la transacción y cerrar la conexión
        conn.commit()
        conn.close()

        # Limpiar el Treeview
        self.treeview.delete(*self.treeview.get_children())

        # Mostrar un mensaje de confirmación
        messagebox.showinfo("Pedido registrado", "El pedido ha sido registrado exitosamente.")
        
        # Actualizar la visualización del número de pedido
        self.actualizar_numero_pedido()
        
    def agregar_pedido(self):
        proveedor = self.proveedor.get()  
        producto = self.producto.get() 
        cantidad = self.cantidad.get() 
        
        # Verificar si se han ingresado todos los datos necesarios
        if proveedor and producto and cantidad:
            # Llamar a la función para agregar el pedido al Treeview
            self.agregar_pedido_a_treeview(proveedor, producto, cantidad)
            
            # Limpiar los campos después de agregar el pedido
            self.proveedor.set("") 
            self.producto.set("")    
            self.cantidad.delete(0, "end")  
        else:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
               
    def agregar_pedido_a_treeview(self, proveedor, producto, cantidad):
        # Obtener el número de pedido actual
        n_pedido = self.numero_pedido
        
        # Obtener la fecha y hora actual
        fecha_actual = datetime.datetime.now().strftime("%d-%m-%Y")
        hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
        
        # Insertar los datos del pedido en el Treeview con el mismo número de pedido
        self.treeview.insert("", "end", values=(n_pedido, proveedor, producto, cantidad, fecha_actual, hora_actual))
        
    def ver_pedidos(self):
        # Crear el Toplevel
        top_pedidos = Toplevel(self)
        top_pedidos.title("Lista de Pedidos Registrados")
        top_pedidos.geometry("800x600")  
        top_pedidos.config(bg="#BEBEBE") 

        label_pedidos = tk.Label(top_pedidos, text="Pedidos Registrados", font="sans 22 bold", bg="#BEBEBE")
        label_pedidos.pack(pady=10) 

        # Crear el Treeview
        tree_pedidos = ttk.Treeview(top_pedidos, show="headings")
        tree_pedidos['columns'] = ('N° Pedido', 'Proveedor', 'Producto', 'Cantidad', 'Fecha', 'Hora')
        tree_pedidos.column("#0", anchor='center', width=100)
        tree_pedidos.column('#1', anchor='center', width=100)
        tree_pedidos.column('#2', anchor='center', width=100)
        tree_pedidos.column('#3', anchor='center', width=100)
        tree_pedidos.column('#4', anchor='center', width=100)
        tree_pedidos.column('#5', anchor='center', width=150)
        tree_pedidos.column('#6', anchor='center', width=150)

        tree_pedidos.heading('#1', text='N° Pedido')
        tree_pedidos.heading('#2', text='Proveedor')
        tree_pedidos.heading('#3', text='Producto')
        tree_pedidos.heading('#4', text='Cantidad')
        tree_pedidos.heading('#5', text='Fecha')
        tree_pedidos.heading('#6', text='Hora')

        # Obtener datos de la base de datos
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pedidos")
        rows = cursor.fetchall()
        for row in rows:
            tree_pedidos.insert('', 'end', text=row[0], values=row[1:])
        conn.close()

        # Ubicar el Treeview en el Toplevel 
        tree_pedidos.place(x=50, y=100, width=700, height=450) 

        # Asegurar que el Treeview tenga barras de desplazamiento vertical
        scroll_y_pedidos = ttk.Scrollbar(top_pedidos, orient='vertical', command=tree_pedidos.yview)
        scroll_y_pedidos.place(x=750, y=100, height=450)  # Ubicar la barra de desplazamiento vertical
        tree_pedidos.config(yscrollcommand=scroll_y_pedidos.set)