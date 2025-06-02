import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from PIL import Image, ImageTk
import sys
import os
from openpyxl import Workbook
from tkinter import filedialog

class Inventario(tk.Frame):
    db_name = "database.db"
    
    def __init__(self,padre):
        super().__init__(padre)
        self.widgets()
        self.mostrar()
        self.calcular_costo_total()
        
    def rutas(self,ruta):
        try:
            rutabase=sys.__MEIPASS
        except Exception:
            rutabase=os.path.abspath(".")
        return os.path.join(rutabase,ruta)
       
    def eje_consulta(self,consulta,parametros=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(consulta,parametros)
            conn.commit()
        return result
    
    def validacion(self, name, prov, precio, costo, stock, codigo_barra):
        return len(name)>0 and len(prov)>0 and len(precio)>0 and len(costo)>0 and len(stock)>0 and len(codigo_barra)>0 # validar los datos recuperados
    
    def mostrar(self): # mostrar en el Treeview
        consulta = "SELECT * FROM inventario ORDER BY id DESC"
        result = self.eje_consulta(consulta)
        for elem in result:
            precio_cop = "{:,.0f} ".format(elem[3]) if elem[3] else ""
            costo_cop = "{:,.0f} ".format(elem[4]) if elem[4] else ""  
            self.tre.insert("", 0, text=elem[0], values=(elem[0], elem[1], elem[2], precio_cop, costo_cop, elem[5], elem[6]))
    
    def registrar(self):
        result = self.tre.get_children()
        for i in result:
            self.tre.delete(i)
        name = self.name.get()  
        prov = self.proveedor.get()
        precio = self.precio.get()
        costo = self.costo.get()
        stock = self.stock.get()
        codigo_barra = self.codigo_barra.get()
        if self.validacion(name, prov, precio, costo, stock) and codigo_barra:
            try:
                consulta = "INSERT INTO inventario VALUES(?,?,?,?,?,?,?)"
                parametros = (None, name, prov, precio, costo, stock, codigo_barra)
                self.eje_consulta(consulta, parametros)    
                self.mostrar()
                self.calcular_costo_total()  # Actualizar el costo total después de registrar un nuevo producto
                
                messagebox.showinfo(title="Éxito", message="Producto agregado al inventario correctamente")

                self.name.delete(0, END)
                self.proveedor.delete(0, END)
                self.precio.delete(0, END)
                self.costo.delete(0, END)
                self.stock.delete(0, END)
                self.codigo_barra.delete(0, END)
            except:
                messagebox.showwarning(title="Error", message="Error al registrar el producto")
        else:
            messagebox.showwarning(title="Error", message="Rellene todos los campos")
            self.mostrar()
        
    def widgets(self):

#Frame superior
        frame1 = tk.Frame(self, bg="#BEBEBE",highlightbackground="gray", highlightthickness=1)
        frame1.pack()
        frame1.place(x=0, y=0, width=1100, height=200)
                
        titulo = tk.Label(self, text="INVENTARIOS", font="sans 30 bold", bg="#BEBEBE", anchor="center",)
        titulo.pack()  
        titulo.place(x=5, y=0, width=1090, height=90)
 
#Frame inferior        
        frame2 = tk.Frame(self, bg="#545454",highlightbackground="gray", highlightthickness=1)
        frame2.place(x=0,y=100,width=1100,height=750)
        
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
    
    #LabelFrame Izquierdo    
        labelframe=LabelFrame(frame2,text="Productos", font="sans 22 bold", bg="#BEBEBE")
        labelframe.place(x=20,y=30,width=400,height=600)

        lblcodigo_barra = Label(labelframe, text="Cód. Barra:", font="sans 14 bold", bg="#BEBEBE")
        lblcodigo_barra.place(x=10, y=320)
        self.codigo_barra = ttk.Entry(labelframe, font="sans 14 bold")
        self.codigo_barra.place(x=140, y=320, width=240, height=40)

        lblname=Label(labelframe,text="Nombre: ",font="sans 14 bold",bg="#BEBEBE")
        lblname.place(x=10,y=20)
        self.name=ttk.Entry(labelframe,font="sans 14 bold")
        self.name.place(x=140,y=20,width=240,height=40)
        
        lblproveedor=Label(labelframe,text="Proveedor: ",font="sans 14 bold",bg="#BEBEBE")
        lblproveedor.place(x=10,y=80)
        self.proveedor=ttk.Combobox(labelframe,font="sans 14 bold",state="readonly")
        self.proveedor.place(x=140,y=80,width=240,height=40)
        
        self.cargar_proveedores()

        lblprecio=Label(labelframe,text="Precio: ",font="sans 14 bold",bg="#BEBEBE")
        lblprecio.place(x=10,y=140)
        self.precio=ttk.Entry(labelframe,font="sans 14 bold")
        self.precio.place(x=140,y=140,width=240,height=40)
        
        lblcosto=Label(labelframe,text="Costo: ",font="sans 14 bold",bg="#BEBEBE")
        lblcosto.place(x=10,y=200)
        self.costo=ttk.Entry(labelframe,font="sans 14 bold")
        self.costo.place(x=140,y=200,width=240,height=40)
        
        lblstock=Label(labelframe,text="Stock: ",font="sans 14 bold",bg="#BEBEBE")
        lblstock.place(x=10,y=260)
        self.stock=ttk.Entry(labelframe,font="sans 14 bold")
        self.stock.place(x=140,y=260,width=240,height=40)
        
        ruta=self.rutas(r"icono/ingresara.png")
        imagen_pil = Image.open(ruta)
        imagen_resize = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize)
        
        boton_agregar = tk.Button(labelframe, text="Ingresar", font="sans 14 bold", bg="#FFFFFF", command=self.registrar)
        boton_agregar.config(image=imagen_tk, compound=LEFT, padx=10)
        boton_agregar.image = imagen_tk
        boton_agregar.place(x=80, y=380,width=240,height=40)
        
        ruta=self.rutas(r"icono/editar.png")
        imagen_pil = Image.open(ruta)
        imagen_resize1 = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize1)
        
        boton_editar = tk.Button(labelframe, text="Editar producto", font="sans 14 bold", bg="#FFFFFF", command=self.editar_producto)
        boton_editar.config(image=imagen_tk, compound=LEFT, padx=10)
        boton_editar.image = imagen_tk
        boton_editar.place(x=80, y=440,width=240,height=40)

        # Botón para exportar a Excel
        ruta = self.rutas(r"icono/exportar.png")
        imagen_pil = Image.open(ruta)
        imagen_resize3 = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize3)
        
        btn_exportar = Button(self, text="Exportar a Excel", font="sans 14 bold", bg="#FFFFFF", command=self.exportar_a_excel)
        btn_exportar.config(image=imagen_tk, compound=LEFT, padx=10)
        btn_exportar.image = imagen_tk
        btn_exportar.place(x=820, y=25,width=240,height=40)

#TreeView Tabla
        treFrame=Frame(frame2,bg="white")
        treFrame.place(x=440,y=50,width=620,height=400)

        # Barra de desplazamiento vertical
        scrol_y = ttk.Scrollbar(treFrame)
        scrol_y.pack(side=RIGHT, fill=Y)

        # Barra de desplazamiento horizontal
        scrol_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill=X)

        # Widget Treeview
        self.tre = ttk.Treeview(treFrame, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set, height=40, 
                                columns=("ID", "PRODUCTO", "PROVEEDOR", "PRECIO", "COSTO", "STOCK", "CODIGO BARRA"),show="headings")
        self.tre.pack(expand=True, fill=BOTH)

        scrol_y.config(command=self.tre.yview)
        scrol_x.config(command=self.tre.xview)

        self.tre.heading("ID",text="Id")
        self.tre.heading("CODIGO BARRA", text="Cód. Barra")
        self.tre.heading("PRODUCTO",text="Producto")    
        self.tre.heading("PROVEEDOR",text="Proveedor")
        self.tre.heading("PRECIO",text="Precio")
        self.tre.heading("COSTO",text="Costo")
        self.tre.heading("STOCK",text="Stock")

        self.tre.column("ID",width=70, anchor="center")
        self.tre.column("CODIGO BARRA", width=100, anchor="center")
        self.tre.column("PRODUCTO",width=70, anchor="center")    
        self.tre.column("PROVEEDOR",width=70, anchor="center")
        self.tre.column("PRECIO",width=70, anchor="center")
        self.tre.column("COSTO",width=70, anchor="center")
        self.tre.column("STOCK",width=70, anchor="center")
        
        # Colores de etiqueta
        colores = ("cyan", "gray")
        for color in colores:
            self.tre.tag_configure(color, background=color)
        
        self.lbl_costo_total = Label(frame2, text="Total en Inventario: ", font="sans 14 bold", bg="#545454", fg="#FFFFFF")
        self.lbl_costo_total.place(x=730, y=490)
        
        ruta=self.rutas(r"icono/actualizar.png")
        imagen_pil = Image.open(ruta)
        imagen_resize2 = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize2)
        
        btn_actualizar = Button(frame2, text="Actualizar Inventario", font="sans 14 bold", bg="#FFFFFF", fg="black", command=self.actualizar_inventario)
        btn_actualizar.config(image=imagen_tk, compound=LEFT, padx=10)
        btn_actualizar.image = imagen_tk
        btn_actualizar.place(x=440, y=480, width=260, height=50)
    
#Funciones
    def exportar_a_excel(self):
        try:
            # Crear un nuevo archivo Excel
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Inventario"

            # Agregar encabezados
            encabezados = ["ID", "Producto", "Proveedor", "Precio", "Costo", "Stock"]
            sheet.append(encabezados)

            # Agregar datos desde el Treeview
            for row in self.tre.get_children():
                valores = self.tre.item(row, "values")
                sheet.append(valores)

            # Usar un cuadro de diálogo para guardar el archivo
            archivo = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Archivos Excel", "*.xlsx")],
                title="Guardar archivo como"
            )
        
            if archivo:  # Si el usuario no cancela
                workbook.save(archivo)
                messagebox.showinfo("Exportar a Excel", f"Inventario exportado correctamente a:\n{archivo}")
            else:
                messagebox.showinfo("Exportar a Excel", "Exportación cancelada.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al exportar:\n{e}")
    
    def calcular_costo_total(self):
        consulta = "SELECT SUM(costo * stock) FROM inventario"
        result = self.eje_consulta(consulta)
        costo_total = result.fetchone()[0]
        costo_total_cop = "{:,.0f} ".format(costo_total) if costo_total else "0 "
        self.lbl_costo_total.config(text=f"Total en Inventario: {costo_total_cop}")
    
    def actualizar_inventario(self):
        # Limpiar el Treeview antes de mostrar los datos actualizados
        for item in self.tre.get_children():
            self.tre.delete(item)
        
        # Mostrar los datos actualizados en el Treeview
        self.mostrar()
        self.calcular_costo_total()
        
        messagebox.showinfo("Actualización", "El inventario ha sido actualizado correctamente.")
        
    def editar_producto(self):
        # Obtener el ítem seleccionado en el Treeview
        seleccion = self.tre.selection()
        if not seleccion:
            messagebox.showwarning("Editar Producto", "Seleccione un producto para editar.")
            return
        
        # Obtener los datos del ítem seleccionado
        item_id = self.tre.item(seleccion)["text"]
        item_values = self.tre.item(seleccion)["values"]
        
#Abrir una ventana para editar el producto
        ventana_editar = Toplevel(self)
        ventana_editar.title("Editar Producto")
        ventana_editar.geometry("400x400")
        ventana_editar.config(bg="#BEBEBE")
        
        # Nombre
        lbl_nombre = Label(ventana_editar, text="Nombre:", font="sans 14 bold",bg="#BEBEBE")
        lbl_nombre.grid(row=0, column=0, padx=10, pady=10)
        entry_nombre = Entry(ventana_editar, font="sans 14 bold")
        entry_nombre.grid(row=0, column=1, padx=10, pady=10)
        entry_nombre.insert(0, item_values[1])
        
        # Proveedor
        lbl_proveedor = Label(ventana_editar, text="Proveedor:", font="sans 14 bold",bg="#BEBEBE")
        lbl_proveedor.grid(row=1, column=0, padx=10, pady=10)
        entry_proveedor = Entry(ventana_editar, font="sans 14 bold")
        entry_proveedor.grid(row=1, column=1, padx=10, pady=10)
        entry_proveedor.insert(0, item_values[2])
        
        # Precio
        lbl_precio = Label(ventana_editar, text="Precio :", font="sans 14 bold",bg="#BEBEBE")
        lbl_precio.grid(row=2, column=0, padx=10, pady=10)
        entry_precio = Entry(ventana_editar, font="sans 14 bold")
        entry_precio.grid(row=2, column=1, padx=10, pady=10)
        entry_precio.insert(0, item_values[3].split()[0].replace(",", ""))
        
        # Costo
        lbl_costo = Label(ventana_editar, text="Costo :", font="sans 14 bold",bg="#BEBEBE")
        lbl_costo.grid(row=3, column=0, padx=10, pady=10)
        entry_costo = Entry(ventana_editar, font="sans 14 bold")
        entry_costo.grid(row=3, column=1, padx=10, pady=10)
        entry_costo.insert(0, item_values[4].split()[0].replace(",", ""))
        
        # Stock
        lbl_stock = Label(ventana_editar, text="Stock:", font="sans 14 bold",bg="#BEBEBE")
        lbl_stock.grid(row=4, column=0, padx=10, pady=10)
        entry_stock = Entry(ventana_editar, font="sans 14 bold")
        entry_stock.grid(row=4, column=1, padx=10, pady=10)
        entry_stock.insert(0, item_values[5])
        
        #Codigo Barra
        lbl_codigo_barra = Label(ventana_editar, text="Cód. Barra:", font="sans 14 bold", bg="#BEBEBE")
        lbl_codigo_barra.grid(row=5, column=0, padx=10, pady=10)
        entry_codigo_barra = Entry(ventana_editar, font="sans 14 bold")
        entry_codigo_barra.grid(row=5, column=1, padx=10, pady=10)
        entry_codigo_barra.insert(0, item_values[6])

        # Función para guardar los cambios
        def guardar_cambios():
            nombre = entry_nombre.get()
            proveedor = entry_proveedor.get()
            precio = entry_precio.get()
            costo = entry_costo.get()
            stock = entry_stock.get()
            codigo_barra = entry_codigo_barra.get()
            
            if not (nombre and proveedor and precio and costo and stock):
                messagebox.showwarning("Guardar Cambios", "Rellene todos los campos.")
                return
            
            try:
                precio = float(precio.replace(",", ""))
                costo = float(costo.replace(",", ""))
            except ValueError:
                messagebox.showwarning("Guardar Cambios", "Ingrese valores numéricos válidos para precio y costo.")
                return
            
            # Actualizar los datos en la base de datos
            consulta = "UPDATE inventario SET nombre=?, proveedor=?, precio=?, costo=?, stock=?, codigo_barra=? WHERE id=?"
            parametros = (nombre, proveedor, precio, costo, stock, codigo_barra, item_id)
            self.eje_consulta(consulta, parametros)
            
            # Actualizar el Treeview y el costo total
            self.actualizar_inventario()
            
            # Cerrar la ventana de edición
            ventana_editar.destroy()
        
        ruta=self.rutas(r"icono/guardar.png")
        imagen_pil = Image.open(ruta)
        imagen_resize4 = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize4)
        
        # Botón de guardar cambios
        btn_guardar = Button(ventana_editar, text="Guardar Cambios", font="sans 14 bold", bg="#FFFFFF", command=guardar_cambios)
        btn_guardar.config(image=imagen_tk, compound=LEFT, padx=10)
        btn_guardar.image = imagen_tk
        btn_guardar.place(x=80, y=350,width=240, height=40)
        
    def actualizar_fecha_y_hora(self):
        # Obtener la fecha y hora actual
        fecha_actual = datetime.datetime.now().strftime("%d-%m-%Y")
        hora_actual = datetime.datetime.now().strftime("%H:%M:%S")

        # Actualizar las etiquetas de fecha y hora
        self.label_fecha.config(text=fecha_actual)
        self.label_hora.config(text=hora_actual)

        self.after(1000, self.actualizar_fecha_y_hora)
        
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