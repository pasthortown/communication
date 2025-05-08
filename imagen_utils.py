import tkinter as tk
from PIL import Image, ImageTk

def cargar_imagen(path, ancho_deseado):
    original = Image.open(path)
    
    if ancho_deseado > 0:
        relacion = ancho_deseado / original.width
        alto_deseado = int(original.height * relacion)
        imagen_redimensionada = original.resize((ancho_deseado, alto_deseado), Image.Resampling.LANCZOS)
        return imagen_redimensionada, ancho_deseado, alto_deseado
    else:
        return original, original.width, original.height


def calcular_posicion_por_zona(zona, screen_width, screen_height, img_width, img_height):
    if zona not in range(9):
        raise ValueError("Zona debe estar entre 0 y 8")

    fila = zona // 3
    col = zona % 3

    if col == 0:
        x = 0
    elif col == 1:
        x = (screen_width - img_width) // 2
    else:
        x = screen_width - img_width

    if fila == 0:
        y = 0
    elif fila == 1:
        y = (screen_height - img_height) // 2
    else:
        y = screen_height - img_height

    return x, y

def mostrar_imagen_con_fade(imagen, img_width, img_height, x, y, tiempo_fadein=3, tiempo_visible=5, tiempo_fadeout=3):
    root = tk.Tk()
    root.overrideredirect(True)
    root.wm_attributes('-topmost', True)
    root.wm_attributes('-transparentcolor', 'white')
    root.configure(bg='white')
    root.geometry(f"{img_width}x{img_height}+{x}+{y}")

    imagen_tk = ImageTk.PhotoImage(imagen)
    label = tk.Label(root, image=imagen_tk, bg='white', borderwidth=0, highlightthickness=0)
    label.pack()

    pasos = 30
    delay_fadein = int((tiempo_fadein * 1000) / pasos)
    delay_fadeout = int((tiempo_fadeout * 1000) / pasos)
    opacidad = [0.0]

    def realizar_fadein():
        if opacidad[0] < 1.0:
            root.wm_attributes('-alpha', opacidad[0])
            opacidad[0] += 1.0 / pasos
            root.after(delay_fadein, realizar_fadein)
        else:
            root.wm_attributes('-alpha', 1.0)
            root.after(int(tiempo_visible * 1000), realizar_fadeout)

    def realizar_fadeout():
        if opacidad[0] > 0.0:
            opacidad[0] -= 1.0 / pasos
            root.wm_attributes('-alpha', max(opacidad[0], 0.0))
            root.after(delay_fadeout, realizar_fadeout)
        else:
            root.destroy()

    realizar_fadein()
    root.mainloop()
