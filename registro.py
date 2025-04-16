import time
import random
import threading
from datetime import datetime
from queue import Queue
from logger_datos import guardar_log

# Simulamos 5 computadoras disponibles numeradas del 1 al 5
registro_semaforo = threading.BoundedSemaphore(5)
computadoras_disponibles = Queue()
for i in range(1, 6):
    computadoras_disponibles.put(i)

def registrar_paciente(paciente):
    hora_llegada = datetime.now()
    print(f"[RegistroLlegada][{hora_llegada.strftime('%H:%M:%S')}] - {paciente.nombre} llegó al área de registro y está esperando computadora...")

    tiempo_inicio_espera = time.time()

    # Limitar concurrencia a 5 registros simultáneos
    with registro_semaforo:
        computadora_id = computadoras_disponibles.get()

        try:
            tiempo_inicio_registro = time.time()
            espera = tiempo_inicio_registro - tiempo_inicio_espera
            hora_inicio = datetime.now()

            print(f"[RegistroComienzo][{hora_inicio.strftime('%H:%M:%S')}] - {paciente.nombre} comenzó su registro en computadora {computadora_id} (esperó {espera:.2f} s).")

            if paciente.registrado:
                tiempo_registro = random.uniform(0.2, 0.5)  # 2–5 minutos simulados
                tipo_registro = "rápido (recurrente)"
            else:
                tiempo_registro = random.uniform(0.5, 1.0)  # 5–10 minutos simulados
                tipo_registro = "completo (nuevo)"

            time.sleep(tiempo_registro)

            hora_fin = datetime.now()
            duracion_registro = tiempo_registro

            print(f"[RegistroFin] - {paciente.nombre} terminó su registro ({tipo_registro}) en {tiempo_registro:.2f} s en computadora {computadora_id}.")

            # Guardar log
            guardar_log("registro", {
                "nombre": paciente.nombre,
                "hora_llegada": hora_inicio.strftime('%H:%M:%S'),
                "hora_inicio": hora_inicio.strftime('%H:%M:%S'),
                "hora_fin": hora_fin.strftime('%H:%M:%S'),
                "espera": round(espera, 2),
                "duracion_registro": round(duracion_registro, 2),
                "computadora": computadora_id
            }, columnas=["nombre", "hora_llegada", "hora_inicio", "hora_fin", "espera", "duracion_registro", "computadora"])

        finally:
            computadoras_disponibles.put(computadora_id)
