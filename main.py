MODO_DIAGNOSTICO = "ia"  # o "ia"

import threading
import asyncio
import multiprocessing
import queue
import time
from datetime import datetime

from data.pacientes import pacientes
from registro import registrar_paciente
from recursos import asignar_recursos
from seguimiento import seguimiento_y_alta

if MODO_DIAGNOSTICO == "ia":
    from diagnostico_ia import diagnosticar
else:
    from diagnostico_mock import diagnosticar

PRIORIDAD_NUMERICA = {
    "Alta": 0,
    "Media": 1,
    "Baja": 2
}

cola_prioritaria = queue.PriorityQueue()

def flujo_paciente(paciente):
    hora_llegada = datetime.now().strftime("%H:%M:%S")
    print(f"[IngresoHospital][{hora_llegada}] - {paciente.nombre} ha ingresado al sistema.\n")

    # Registro (concurrente)
    registrar_paciente(paciente)

    # Diagnóstico (asincrónico)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    diagnostico_info = loop.run_until_complete(diagnosticar(paciente))
    loop.close()

    paciente.prioridad = diagnostico_info["prioridad"]
    prioridad_num = PRIORIDAD_NUMERICA[paciente.prioridad]

    print(f"[DiagnósticoListo] {paciente.nombre} encolado con prioridad {paciente.prioridad}")

    if paciente.prioridad in ["Alta", "Media"]:
        print(f"[Asignación] {paciente.nombre} en atención inmediata.\n")
        asignar_recursos(paciente)
        proceso = multiprocessing.Process(target=seguimiento_y_alta, args=(paciente,))
        proceso.start()
        proceso.join()
        print(f"{paciente.nombre} ha completado su proceso.\n")
    else:    
        print(f"[ConsultaExterna] {paciente.nombre} derivado a consulta. No se asignan recursos.\n")


if __name__ == "__main__":
    print("Simulación del Sistema Hospitalario Iniciada\n")

    hilos = []

    for paciente in pacientes:
        hilo = threading.Thread(target=flujo_paciente, args=(paciente,))
        hilo.start()
        hilos.append(hilo)

    for hilo in hilos:
        hilo.join()

    print("\n[Main] Todos los pacientes han sido atendidos o derivados a consulta externa.")
