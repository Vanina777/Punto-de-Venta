import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from PIL import Image, ImageTk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import sys
import os

class Ventas(tk.Frame):
    db_name = "database.db"

    def __init__(self, parent):
        super().__init__(parent)
        self.numero_factura = self.obtener_numero_factura_actual()
        self.productos_seleccionados = []
        self.widgets()
        self.buscar_producto_por_codigo()
        self.cargar_clientes()
        
    def rutas(self,ruta):
        try:
            rutabase=sys.__MEIPASS
        except Exception:
            rutabase=os.path.abspath(".")
        return os.path.join(rutabase,ruta)

    def obtener_numero_factura_actual(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT MAX(factura) FROM ventas")
            last_invoice_number = c.fetchone()[0]
            conn.close()
            return last_invoice_number + 1 if last_invoice_number is not None else 1
        except sqlite3.Error as e:
            print("Error obteniendo el número de factura actual:", e)
            return 1
    
    def cargar_clientes(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT nombre FROM clientes")
            clientes = c.fetchall()
            nombres_clientes = [cliente[0] for cliente in clientes]
            self.entry_cliente["values"] = nombres_clientes
            conn.close()
        except sqlite3.Error as e:
            print("Error cargando clientes:", e)

    def buscar_producto_por_codigo(self, event=None):
        codigo_barra = self.entry_codigo_barra.get()

        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()

            # Buscar el producto por su código de barras
            c.execute("SELECT nombre, precio, stock FROM inventario WHERE codigo_barra=?", (codigo_barra,))
            producto = c.fetchone()
            conn.close()

            if producto:
                nombre_producto, precio, stock = producto
                self.entry_nombre.set(nombre_producto) 
                self.label_stock.config(text=f"Stock: {stock}")
                self.precio_producto = precio  # Guardar el precio del producto seleccionado
           
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al buscar el producto: {e}")

    def agregar_articulo(self):
        cliente = self.entry_cliente.get()
        producto = self.entry_codigo_barra.get()
        cantidad = self.entry_cantidad.get()
        nombre = self.entry_nombre.get()


        if not cliente:
            messagebox.showerror("Error", "Por favor seleccione un cliente.")
            return
       
        if not producto:
            messagebox.showerror("Error", "Por favor seleccione un producto.")
            return


        if not cantidad.isdigit() or int(cantidad) <= 0:
            messagebox.showerror("Error", "Por favor ingrese una cantidad válida.")
            return


        cantidad = int(cantidad)
        cliente = self.entry_cliente.get()


        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT precio, costo, stock FROM inventario WHERE codigo_barra=?", (producto,))
            resultado = c.fetchone()
           
            if resultado is None:
                messagebox.showerror("Error", "Producto no encontrado.")
                return


            precio, costo, stock = resultado
           
            if cantidad > stock:
                messagebox.showerror("Error", f"Stock insuficiente. Solo hay {stock} unidades disponibles.")
                return


            total = precio * cantidad
            total_cop = "{:,.0f} ".format(total)


            # Insertar el artículo en el Treeview con el número de factura actual
            self.tree.insert("", "end", values=(self.numero_factura, cliente, nombre, "{:,.0f} ".format(precio), cantidad, total_cop))
            self.productos_seleccionados.append((self.numero_factura, cliente, nombre, precio, cantidad, total_cop, costo))


            conn.close()


            # Limpiar Entry de cantidad y deseleccionar Combobox
            self.entry_cantidad.delete(0, 'end')
            self.entry_codigo_barra.delete(0, 'end')
        except sqlite3.Error as e:
            print("Error al agregar artículo:", e)
        self.calcular_precio_total()


    def realizar_pago(self):
        if not self.tree.get_children():
            messagebox.showerror("Error", "No hay productos seleccionados para realizar el pago.")
            return
        
        total_venta = sum(float(item[5].replace("", "").replace(",", "")) for item in self.productos_seleccionados)
        
        # Formatear el total para agregar puntos en los miles
        total_formateado = "{:,.0f}".format(total_venta)

        # Crear una nueva ventana TopLevel para que el usuario ingrese el monto pagado
        ventana_pago = tk.Toplevel(self)
        ventana_pago.title("Realizar pago")
        ventana_pago.geometry("400x400")
        ventana_pago.config(bg="#BEBEBE")
        ventana_pago.resizable(False, False)

        label_titulo = tk.Label(ventana_pago, text="Realizar pago", font="sans 30 bold", bg="#BEBEBE")
        label_titulo.place(x=70, y=10)

        label_total = tk.Label(ventana_pago, text=f"Total a pagar: {total_formateado} ", font="sans 14 bold", bg="#BEBEBE")
        label_total.place(x=80, y=100)

        label_monto = tk.Label(ventana_pago, text="Ingrese el monto pagado:", font="sans 14 bold", bg="#BEBEBE")
        label_monto.place(x=80, y=160)

        entry_monto = ttk.Entry(ventana_pago, font="sans 14 bold")
        entry_monto.place(x=80, y=210, width=240, height=40)

        ruta=self.rutas(r"icono/pago.png")
        imagen_pil = Image.open(ruta)
        imagen_resize10 = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize10)
        
        button_confirmar_pago = tk.Button(ventana_pago, text="Confirmar Pago", font="sans 14 bold", bg="#FFFFFF", fg="black", command=lambda: self.procesar_pago(entry_monto.get(), ventana_pago, total_venta))
        button_confirmar_pago.config(image=imagen_tk, compound="left", padx=10)
        button_confirmar_pago.image = imagen_tk
        button_confirmar_pago.place(x=80, y=270, width=240, height=40)

    def procesar_pago(self, cantidad_pagada, ventana_pago, total_venta):
        cantidad_pagada = float(cantidad_pagada)
        cliente = self.entry_cliente.get()  # Obtener el cliente seleccionado

        if cantidad_pagada < total_venta:
            messagebox.showerror("Error", "La cantidad pagada es insuficiente.")
            return

        cambio = cantidad_pagada - total_venta

        # Formatear el total para agregar puntos en los miles
        total_formateado = "{:,.0f}".format(total_venta)

        mensaje = f"Total: {total_formateado} \nCantidad pagada: {cantidad_pagada:,.0f} \nCambio: {cambio:,.0f} "
        messagebox.showinfo("Pago Realizado", mensaje)

        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()

            # Obtener la fecha y hora actual
            fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
            hora_actual = datetime.datetime.now().strftime("%H:%M:%S")

            # Insertar las ventas en la tabla 'ventas' usando el número de factura actual
            for item in self.productos_seleccionados:
                factura, cliente, nombre, precio, cantidad, total, costo = item
                c.execute("INSERT INTO ventas (factura, cliente, producto, precio, cantidad, total, costo, fecha, hora) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (factura, cliente, nombre, precio, cantidad, total.replace(" ", "").replace(",", ""), costo * cantidad, fecha_actual, hora_actual))

                # Restar la cantidad de productos vendidos del stock en la tabla 'inventario'
                c.execute("UPDATE inventario SET stock = stock - ? WHERE nombre = ?", (cantidad, nombre))

            conn.commit()

            # Generar factura en PDF
            self.generar_factura_pdf(total_venta, cliente)

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al registrar la venta: {e}")

        self.numero_factura += 1
        self.label_numero_factura.config(text=str(self.numero_factura))

        self.productos_seleccionados = []
        self.limpiar_campos()
        
        # Cerrar la ventana de pago después de procesar el pago
        ventana_pago.destroy()

    def limpiar_campos(self):
        # Limpiar TreeView y Label de precio total
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.label_precio_total.config(text="Precio a Pagar: 0 ")
        self.label_stock.config(text="Stock: ")

        self.entry_codigo_barra.delete(0, 'end')
        self.entry_cantidad.delete(0, 'end')

    def calcular_precio_total(self):
        total_pagar = sum(float(self.tree.item(item)["values"][-1].replace(" ", "").replace(",", "")) for item in self.tree.get_children())
        total_pagar_cop = "{:,.0f} ".format(total_pagar)
        self.label_precio_total.config(text=f"Precio a Pagar: {total_pagar_cop}")

    def generar_factura_pdf(self, total_venta, cliente):
        try:
            # Crear el PDF
            factura_path = f"facturas/Factura_{self.numero_factura}.pdf"
            c = canvas.Canvas(factura_path, pagesize=letter)

            # Información 
            empresa_nombre = "Bar Universitario UTN"
            empresa_logo_path = self.rutas(r"imagenes/Logoblanco.jpg")

            # Agregar logo 
            c.drawImage(empresa_logo_path, 50, 700, width=80, height=80)

            # Agregar contenido a la factura
            c.setFont("Helvetica-Bold", 18)
            c.drawString(250, 750, "FACTURA DE VENTA")

            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, 680, f"{empresa_nombre}")
            c.setFont("Helvetica", 12)
            c.drawString(50, 620, "----------------------------------------------------------------------------------------------------------------------------------")
            c.drawString(50, 600, f"Número de Factura: {self.numero_factura}")
            c.drawString(50, 580, f"Fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            c.drawString(50, 560, "----------------------------------------------------------------------------------------------------------------------------------")
            c.drawString(50, 540, f"Cliente: {cliente}")
            c.drawString(50, 520, "Descripción de Productos:")

            # Crear una tabla para los productos
            y_offset = 500
            c.setFont("Helvetica-Bold", 12)
            c.drawString(70, y_offset, "Producto")
            c.drawString(270, y_offset, "Cantidad")
            c.drawString(370, y_offset, "Precio")
            c.drawString(470, y_offset, "Total")

            y_offset -= 20
            c.setFont("Helvetica", 12)
            for item in self.productos_seleccionados:
                factura, cliente, producto, precio, cantidad, total, costo = item
                c.drawString(70, y_offset, producto)
                c.drawString(270, y_offset, str(cantidad))
                c.drawString(370, y_offset, "{:,.0f} ".format(precio))
                c.drawString(470, y_offset, total)
                y_offset -= 20

            c.drawString(50, y_offset, "----------------------------------------------------------------------------------------------------------------------------------")
            y_offset -= 20
            c.drawString(50, y_offset, f"Total a Pagar: {total_venta:,.0f} ")
            c.drawString(50, y_offset - 40, "----------------------------------------------------------------------------------------------------------------------------------")

            # Mensaje de agradecimiento
            c.setFont("Helvetica-Bold", 16)
            c.drawString(150, y_offset - 100, "¡Gracias por tu compra, vuelve pronto!")

            # Términos y condiciones
            y_offset -= 140
            c.setFont("Helvetica", 10)
            c.drawString(50, y_offset, "Términos y Condiciones:")
            c.drawString(50, y_offset - 20, "1. Los productos comprados no tienen devolución.")
            c.drawString(50, y_offset - 40, "2. Conserve esta factura como comprobante de su compra.")
            c.drawString(50, y_offset - 60, "3. Para más información,contacte a servicio al cliente.")

            # Pie de página con información de contacto y redes sociales
            c.setFont("Helvetica", 10)
            c.drawString(100, 50, "Para más información, síganos en nuestras redes sociales:")
            c.drawString(100, 40, "Instagram: @baruniversitario.utnfrrq")

            c.save()

            messagebox.showinfo("Factura Generada", f"Se ha generado la factura en: {factura_path}")
            
            # Abrir el archivo PDF
            os.startfile(os.path.abspath(factura_path))

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar la factura: {e}")

    def widgets(self):
        
#Frame superior
        frame1 = tk.Frame(self, bg="#BEBEBE",highlightbackground="gray", highlightthickness=1)
        frame1.pack()
        frame1.place(x=0, y=0, width=1100, height=100)
        
        titulo = tk.Label(frame1, text="VENTA DE PRODUCTOS", font="sans 30 bold", bg="#BEBEBE", anchor="center")
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
        labelframe = tk.LabelFrame(frame2, font="sans 14 bold", bg="#BEBEBE")  
        labelframe.place(x=20, y=40, width=1060, height=120)

        label_cliente = tk.Label(labelframe, text="Cliente:", font="sans 14 bold", bg="#BEBEBE")
        label_cliente.place(x=10, y=11)
        self.entry_cliente = ttk.Combobox(labelframe, font="sans 14 bold", state="readonly")
        self.entry_cliente.place(x=120, y=8, width=240, height=40)

        self.cargar_clientes()

        label_nombre = tk.Label(labelframe, text="Producto:", font="sans 14 bold", bg="#BEBEBE")
        label_nombre.place(x=10, y=70)
        self.entry_nombre = ttk.Combobox(labelframe, font="sans 14 bold", state="readonly")
        self.entry_nombre.place(x=120, y=66, width=240, height=40)

        label_codigo_barra = tk.Label(labelframe, text="Producto:", font="sans 14 bold", bg="#BEBEBE")
        label_codigo_barra.place(x=10, y=70)

        self.entry_codigo_barra = ttk.Entry(labelframe, font="sans 14 bold")
        self.entry_codigo_barra.place(x=120, y=66, width=240, height=40)
        self.entry_codigo_barra.bind("<Return>", self.buscar_producto_por_codigo)  # Vincula la tecla Enter para buscar


        label_cantidad = tk.Label(labelframe, text="Cantidad:", font="sans 14 bold", bg="#BEBEBE")
        label_cantidad.place(x=400, y=11)
        self.entry_cantidad = ttk.Entry(labelframe, font="sans 14 bold")
        self.entry_cantidad.place(x=500, y=8, width=80, height=40)
        
        #Label para mostrar el stock del producto seleccionado
        self.label_stock = tk.Label(labelframe, text="Stock:", font="sans 14 bold", bg="#BEBEBE")
        self.label_stock.place(x=400, y=70)

        self.entry_codigo_barra.bind("<<ComboboxSelected>>", self.actualizar_stock)  # Llamar a actualizar_stock cuando se seleccione un producto

        label_factura = tk.Label(labelframe, text="Número de Factura:", font="sans 14 bold", bg="#BEBEBE")
        label_factura.place(x=800, y=70)

        self.label_numero_factura = tk.Label(labelframe, text=f"{self.numero_factura}", font="sans 14 bold", bg="#BEBEBE")
        self.label_numero_factura.place(x=1010, y=70)

        ruta=self.rutas(r"icono/agregar.png")
        imagen_pil = Image.open(ruta)
        imagen_resize = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize)

        boton_agregar = tk.Button(labelframe, text="Agregar Artículo", font="sans 14 bold", bg="#FFFFFF", command=self.agregar_articulo)
        boton_agregar.config(image=imagen_tk, compound="left", padx=10)
        boton_agregar.image = imagen_tk
        boton_agregar.place(x=650, y=8,width=220, height=40)
        
    #TreeView Tabla
        treeFrame = tk.Frame(frame2, bg="#FFFFFF") 
        treeFrame.place(x=20, y=160, width=1060, height=300)  

        self.tree = ttk.Treeview(treeFrame, columns=("Factura", "Cliente", "Producto", "Precio", "Cantidad", "Total"), show="headings")
        self.tree.heading("Factura", text="Factura")
        self.tree.heading("Cliente", text="Cliente")
        self.tree.heading("Producto", text="Producto")
        self.tree.heading("Precio", text="Precio")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("Total", text="Total")

        self.tree.column("Factura", width=70, anchor="center")
        self.tree.column("Cliente", width=300, anchor="center")
        self.tree.column("Producto", width=300, anchor="center")
        self.tree.column("Precio", width=120, anchor="center")
        self.tree.column("Cantidad", width=120, anchor="center")
        self.tree.column("Total", width=150, anchor="center")

        self.tree.config(height=25) 

        scrollbar = ttk.Scrollbar(treeFrame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")

        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack() 

#Botones y total a pagar
        self.label_precio_total = tk.Label(frame2, text="Precio a Pagar: 0 ", font="sans 18 bold", bg="#545454", fg="#FFFFFF")
        self.label_precio_total.place(x=700, y=480)
        
        ruta=self.rutas(r"icono/pago.png")
        imagen_pil = Image.open(ruta)
        imagen_resize1 = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize1)
        
        boton_pagar = tk.Button(frame2, text="Pagar", font="sans 14 bold", bg="#FFFFFF", command=self.realizar_pago)
        boton_pagar.config(image=imagen_tk, compound="left", padx=10)
        boton_pagar.image = imagen_tk
        boton_pagar.place(x=20, y=480,width=180, height=40)

        ruta=self.rutas(r"icono/ver.png")
        imagen_pil = Image.open(ruta)
        imagen_resize2 = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize2)

        boton_ver_ventas = tk.Button(frame2, text="Ver Ventas Realizadas", font="sans 14 bold", bg="#FFFFFF", command=self.ver_ventas_realizadas)
        boton_ver_ventas.config(image=imagen_tk, compound="left", padx=10)
        boton_ver_ventas.image = imagen_tk
        boton_ver_ventas.place(x=240, y=480,width=300, height=40)

#Top level boton ver ventas realizadas
    def ver_ventas_realizadas(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT * FROM ventas")
            ventas = c.fetchall()
            conn.close()

            ventana_ventas = tk.Toplevel(self)
            ventana_ventas.title("Ventas Realizadas")
            ventana_ventas.geometry("1100x450")  
            ventana_ventas.configure(bg="#BEBEBE")  

            # Función para filtrar las ventas por factura
            def filtrar_ventas():
                factura_a_buscar = entry_factura.get()
                if factura_a_buscar:
                    ventas_filtradas = [venta for venta in ventas if str(venta[0]) == factura_a_buscar]
                else:
                    ventas_filtradas = ventas

                # Limpiar el Treeview antes de insertar los nuevos datos
                for item in tree.get_children():
                    tree.delete(item)

                # Insertar las ventas filtradas en el Treeview
                for venta in ventas_filtradas:
                    venta = list(venta)
                    venta[3] = "{:,.0f} ".format(venta[3])  # Precio
                    venta[5] = "{:,.0f} ".format(venta[5])  # Total
                    venta[6] = datetime.datetime.strptime(venta[6], "%Y-%m-%d").strftime("%d-%m-%Y")  # Fecha
                    tree.insert("", "end", values=venta)

            # Agregar el Label "Ventas Realizadas"
            label_ventas_realizadas = tk.Label(ventana_ventas, text="Ventas Realizadas", font="sans 26 bold", bg="#BEBEBE")
            label_ventas_realizadas.pack(pady=10)

            # Frame para el filtro por factura
            filtro_frame = tk.Frame(ventana_ventas, bg="#BEBEBE")
            filtro_frame.pack(pady=5)

            # Entry para ingresar el número de factura a filtrar
            label_factura = tk.Label(filtro_frame, text="Número de Factura:", bg="#BEBEBE", font="sans 14 bold")
            label_factura.grid(row=0, column=0)

            entry_factura = ttk.Entry(filtro_frame, font="sans 14 bold")
            entry_factura.grid(row=0, column=1, pady=5, ipady=5)  

            ruta=self.rutas(r"icono/filtrar.png")
            imagen_pil = Image.open(ruta)
            imagen_resize = imagen_pil.resize((30, 30))
            imagen_tk = ImageTk.PhotoImage(imagen_resize)
            
            # Botón para aplicar el filtro
            btn_filtrar = tk.Button(filtro_frame, text="Filtrar", font="sans 12 bold", bg="#FFFFFF", command=filtrar_ventas)  # Cambiar el tamaño de la fuente del botón
            btn_filtrar.config(image=imagen_tk, compound="left", padx=10)
            btn_filtrar.image = imagen_tk
            btn_filtrar.grid(row=0, column=2, padx=5)

            tree_frame = tk.Frame(ventana_ventas, bg="gray")  
            tree_frame.pack(padx=10, pady=10)

            tree = ttk.Treeview(tree_frame, columns=("Factura", "Cliente", "Producto", "Precio", "Cantidad", "Total", "Fecha", "Hora"), show="headings")
            tree.heading("Factura", text="Factura")
            tree.heading("Cliente", text="Cliente")
            tree.heading("Producto", text="Producto")
            tree.heading("Precio", text="Precio")
            tree.heading("Cantidad", text="Cantidad")
            tree.heading("Total", text="Total")
            tree.heading("Fecha", text="Fecha")
            tree.heading("Hora", text="Hora")

            for col in ("Factura", "Cliente", "Producto", "Precio", "Cantidad", "Total", "Fecha", "Hora"):
                tree.column(col, width=150)
                tree.column(col, anchor="center")  
            scrollbar_y = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
            scrollbar_y.pack(side="right", fill="y")

            scrollbar_x = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
            scrollbar_x.pack(side="bottom", fill="x")

            tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

            # Mostrar todas las ventas al inicio
            for venta in ventas:
                venta = list(venta)
                venta[3] = "{:,.0f} ".format(venta[3])  # Precio
                venta[5] = "{:,.0f} ".format(venta[5])  # Total
                venta[6] = datetime.datetime.strptime(venta[6], "%Y-%m-%d").strftime("%d-%m-%Y")  # Fecha
                tree.insert("", "end", values=venta)

            tree.pack()

        except sqlite3.Error as e:
            print("Error al obtener las ventas:", e)

#Funcion actualizar 
    def actualizar_stock(self, event=None):
        producto_seleccionado = self.entry_codigo_barra.get()

        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT stock FROM inventario WHERE codigo_barra=?", (producto_seleccionado,))
            stock = c.fetchone()[0]
            conn.close()

            self.label_stock.config(text=f"Stock: {stock}")
        except sqlite3.Error as e:
            print("Error al obtener el stock del producto:", e)
      
    def actualizar_fecha_y_hora(self):
        # Obtener la fecha y hora actual
        fecha_actual = datetime.datetime.now().strftime("%d-%m-%Y")
        hora_actual = datetime.datetime.now().strftime("%H:%M:%S")

        # Actualizar las etiquetas de fecha y hora
        self.label_fecha.config(text=fecha_actual)
        self.label_hora.config(text=hora_actual)

        # Llamar a este método nuevamente 
        self.after(1000, self.actualizar_fecha_y_hora)