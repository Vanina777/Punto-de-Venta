from tkinter import Tk, Frame
from ttkthemes import ThemedStyle
from login import Login, Registro
from container import Container
import sys
import os

#CONFIGURACIONES INCICIALES DE LA APLICACION
class Manager(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rol_actual = None
        self.title("Punto de Venta UTN")
        self.resizable(False, False)
        self.configure(bg="#BEBEBE")
        self.geometry("1100x650+120+20")
        ruta=self.rutas(r"icono.ico")
        self.iconbitmap(ruta)

        self.container = Frame(self, bg="#BEBEBE")
        self.container.pack(fill="both", expand=True)

        self.frames = {
            Login: None,
            Registro: None,
            Container: None
        }
        
        self.load_frames()

        self.show_frame(Login)

        self.set_theme()
        
    def rutas(self,ruta):
        try:
            rutabase=sys.__MEIPASS
        except Exception:
            rutabase=os.path.abspath(".")
        return os.path.join(rutabase,ruta)

    def set_rol_actual(self, rol):
        self.rol_actual = rol
   
    def load_frames(self):
        for FrameClass in self.frames.keys():
            frame = FrameClass(self.container, self)
            self.frames[FrameClass] = frame

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()

    def set_theme(self):
        style = ThemedStyle(self)
        style.set_theme("breeze")

def main():
    app = Manager()
    app.mainloop()

if __name__ == "__main__":
    main()