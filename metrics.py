import pyautogui
import time

def verificar_actividad_usuario(intervalo=1):
    posicion_anterior = pyautogui.position()
    time.sleep(intervalo)
    posicion_actual = pyautogui.position()

    return "Activo" if posicion_actual != posicion_anterior else "Inactivo"
