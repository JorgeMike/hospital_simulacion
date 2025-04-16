import time
import random
from datetime import datetime

from logger_datos import guardar_log

def seguimiento_y_alta(paciente):
    hora_inicio = datetime.now()
    print(f"[ObservacionInicio][{hora_inicio.strftime('%H:%M:%S')}] - {paciente.nombre} está en observación post-consulta...")

    # Simula el tiempo que el paciente permanece bajo observación
    tiempo_observacion = random.uniform(3.0, 5.0)
    time.sleep(tiempo_observacion)

    hora_fin = datetime.now()
    print(f"[Alta][{hora_fin.strftime('%H:%M:%S')}] - {paciente.nombre} ha sido dado de alta tras {tiempo_observacion:.2f} segundos de observación.\n")

    guardar_log("alta", {
        "nombre": paciente.nombre,
        "hora_inicio": hora_inicio.strftime('%H:%M:%S'),
        "hora_fin": hora_fin.strftime('%H:%M:%S'),
        "tiempo_observacion": round(tiempo_observacion, 2)
    }, columnas=["nombre", "hora_inicio", "hora_fin", "tiempo_observacion"])
