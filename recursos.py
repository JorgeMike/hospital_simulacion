import threading
import time
import random
from datetime import datetime

from logger_datos import guardar_log

# Semáforos: definen la cantidad máxima de recursos disponibles
camas_disponibles = threading.Semaphore(10)     # Solo 3 camas disponibles
doctores_disponibles = threading.Semaphore(5)  # Solo 2 doctores disponibles

def asignar_recursos(paciente):
    hora_espera_cama_inicio = time.time()
    print(f"[EsperaCama] - {paciente.nombre} esperando cama...")

    with camas_disponibles:
        hora_entrada_cama = datetime.now()
        espera_cama = time.time() - hora_espera_cama_inicio
        print(f"[AsignacionCama][{hora_entrada_cama.strftime('%H:%M:%S')}] - {paciente.nombre} fue asignado a una cama (esperó {espera_cama:.2f} s).")
        
        tiempo_en_cama = random.uniform(1.5, 3.0)
        time.sleep(tiempo_en_cama)

        hora_espera_doctor_inicio = time.time()
        print(f"[EsperaDoctor] - {paciente.nombre} esperando doctor...")

        with doctores_disponibles:
            hora_atencion_doctor = datetime.now()
            espera_doctor = time.time() - hora_espera_doctor_inicio
            print(f"[ConsultaInicio][{hora_atencion_doctor.strftime('%H:%M:%S')}] - {paciente.nombre} atendido por un doctor (esperó {espera_doctor:.2f} s).")

            tiempo_consulta = random.uniform(2.0, 4.0)
            time.sleep(tiempo_consulta)

            hora_salida = datetime.now()
            print(f"[ConsultaFin][{hora_salida.strftime('%H:%M:%S')}] - {paciente.nombre} terminó su consulta.")

    print(f"[SalidaAreaMedica] - {paciente.nombre} liberó cama y salió del área médica.\n")

    # Guardar log de la consulta
    recursos_info = {
        "nombre": paciente.nombre,
        "hora_cama": hora_entrada_cama,
        "espera_cama": espera_cama,
        "tiempo_en_cama": tiempo_en_cama,
        "hora_doctor": hora_atencion_doctor,
        "espera_doctor": espera_doctor,
        "tiempo_consulta": tiempo_consulta,
        "hora_salida": hora_salida
    }

    guardar_log("recursos", {
        "nombre": recursos_info["nombre"],
        "hora_cama": recursos_info["hora_cama"].strftime('%H:%M:%S'),
        "espera_cama": round(recursos_info["espera_cama"], 2),
        "tiempo_en_cama": round(recursos_info["tiempo_en_cama"], 2),
        "hora_doctor": recursos_info["hora_doctor"].strftime('%H:%M:%S'),
        "espera_doctor": round(recursos_info["espera_doctor"], 2),
        "tiempo_consulta": round(recursos_info["tiempo_consulta"], 2),
        "hora_salida": recursos_info["hora_salida"].strftime('%H:%M:%S')
    }, columnas=[
        "nombre", "hora_cama", "espera_cama", "tiempo_en_cama",
        "hora_doctor", "espera_doctor", "tiempo_consulta", "hora_salida"
    ])
