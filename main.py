from imagen_utils import (
    cargar_imagen,
    calcular_posicion_por_zona,
    mostrar_imagen_con_fade
)
from metrics import verificar_actividad_usuario
import tkinter as tk
import threading
import time

def monitorear_usuario_durante(tiempo_visible, usuario_activo_ref):
    fin = time.time() + tiempo_visible
    while time.time() < fin:
        estado = verificar_actividad_usuario(intervalo=1)
        if estado == "Activo":
            usuario_activo_ref[0] = True

# Obtener dimensiones de pantalla
root_temp = tk.Tk()
root_temp.withdraw()
screen_width = root_temp.winfo_screenwidth()
screen_height = root_temp.winfo_screenheight()
root_temp.destroy()

# Cargar imagen
ancho_deseado = 100
imagen, img_width, img_height = cargar_imagen("tshirt.png", ancho_deseado)

# Parámetros de tiempo
fadein = 1
visible = 5
fadeout = 1

# Recorrer zonas 0 a 8
for zona in range(9):
    usuario_activo = [False]  # Variable mutable compartida con el hilo

    # Lanzar hilo de monitoreo durante la visualización
    hilo_monitoreo = threading.Thread(
        target=monitorear_usuario_durante,
        args=(visible + fadein + fadeout, usuario_activo),
        daemon=True
    )
    hilo_monitoreo.start()

    # Mostrar imagen
    x, y = calcular_posicion_por_zona(zona, screen_width, screen_height, img_width, img_height)
    mostrar_imagen_con_fade(
        imagen=imagen,
        img_width=img_width,
        img_height=img_height,
        x=x,
        y=y,
        tiempo_fadein=fadein,
        tiempo_visible=visible,
        tiempo_fadeout=fadeout
    )

    # Esperamos que el hilo termine (por si acaso), aunque ya debe haber terminado
    hilo_monitoreo.join(timeout=0.1)

    # Reportamos el estado
    estado_final = "Activo" if usuario_activo[0] else "Inactivo"
    print(f"[Zona {zona}] Estado: {estado_final}")
