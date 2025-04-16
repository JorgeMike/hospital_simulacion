# Simulacion de tiempo, 1 segundo = 10 minutos
import asyncio
import random
from datetime import datetime
from logger_datos import guardar_log

# Función para clasificar la prioridad médica según el texto del diagnóstico
def clasificar_prioridad(diagnostico: str) -> str:
    if "hipertensión" in diagnostico.lower() or "reacción alérgica" in diagnostico.lower():
        return "Alta"
    elif "estrés" in diagnostico.lower():
        return "Media"
    elif "no se detectan anomalías" in diagnostico.lower():
        return "Baja"
    else:
        return "Media"

# Generador de diagnóstico en función de los síntomas
def generar_diagnostico(sintomas: str) -> str:
    sintomas = sintomas.lower()
    if "tos" in sintomas or "fiebre" in sintomas:
        return "Posible infección respiratoria leve. Reposo y líquidos."
    elif "dolor de cabeza" in sintomas or "presión" in sintomas:
        return "Signos de hipertensión. Requiere revisión médica."
    elif "estrés" in sintomas or "ansiedad" in sintomas or "mareo" in sintomas:
        return "Síntomas de estrés agudo. Recomendada consulta psicológica."
    elif "alérgica" in sintomas or "ronchas" in sintomas:
        return "Observación por posible reacción alérgica."
    elif "sin síntomas" in sintomas or sintomas.strip() == "":
        return "No se detectan anomalías inmediatas."
    else:
        # Diagnóstico aleatorio si no hay coincidencia
        return random.choice([
            "Posible infección respiratoria leve. Reposo y líquidos.",
            "Signos de hipertensión. Requiere revisión médica.",
            "No se detectan anomalías inmediatas.",
            "Síntomas de estrés agudo. Recomendada consulta psicológica.",
            "Observación por posible reacción alérgica."
        ])

# Función principal asincrónica de diagnóstico
async def diagnosticar(paciente):
    hora_inicio = datetime.now()
    print(f"[DiagnosticoInicio][{hora_inicio.strftime('%H:%M:%S')}] - {paciente.nombre} está en diagnóstico...")

    duracion = random.uniform(0.5, 1.0)
    await asyncio.sleep(duracion)

    diagnostico = generar_diagnostico(paciente.sintomas)
    prioridad = clasificar_prioridad(diagnostico)
    hora_fin = datetime.now()

    print(f"[DiagnosticoFin][{hora_fin.strftime('%H:%M:%S')}] - Diagnóstico para {paciente.nombre}:\n{diagnostico} (Prioridad: {prioridad})\n")

    diagnostico_info = {
        "nombre": paciente.nombre,
        "hora_inicio": hora_inicio,
        "hora_fin": hora_fin,
        "duracion": duracion,
        "diagnostico": diagnostico,
        "prioridad": prioridad
    }

    guardar_log("diagnostico", {
        "nombre": paciente.nombre,
        "hora_inicio": hora_inicio.strftime('%H:%M:%S'),
        "hora_fin": hora_fin.strftime('%H:%M:%S'),
        "duracion": round(duracion, 2),
        "diagnostico": diagnostico,
        "prioridad": prioridad
    }, columnas=["nombre", "hora_inicio", "hora_fin", "duracion", "diagnostico", "prioridad"])

    return diagnostico_info
