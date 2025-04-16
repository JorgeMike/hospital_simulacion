import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def diagnosticar(paciente):
    hora_inicio = datetime.now()
    print(f"[{hora_inicio.strftime('%H:%M:%S')}] {paciente.nombre} está en diagnóstico (OpenAI)...")

    prompt = f"""
Eres un médico de urgencias en un hospital. Realiza un diagnóstico preliminar con base en los siguientes datos del paciente:

- Nombre: {paciente.nombre}
- Edad: {paciente.edad}
- Género: {paciente.genero}
- Raza: {paciente.raza}
- Altura: {paciente.altura} m
- Peso: {paciente.peso} kg
- Hábitos alimenticios: {paciente.habitos_alimenticios}
- Antecedentes médicos: {', '.join(paciente.antecedentes_medicos) or 'Ninguno'}
- Síntomas reportados: {paciente.sintomas}

Proporciona un diagnóstico clínico inicial en lenguaje técnico y profesional. 
Incluye una prioridad de atención (Alta, Media o Baja) y una recomendación inicial de tratamiento.

Responde en este formato:

Diagnóstico: ...
Prioridad: ...
Recomendación: ...
"""

    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un médico de urgencias."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7
        )

        resultado = response.choices[0].message.content.strip()
        hora_fin = datetime.now()

        print(f"[IA] Diagnóstico para {paciente.nombre} ({hora_fin.strftime('%H:%M:%S')}):\n{resultado}\n")

        prioridad = "Media"
        for nivel in ["Alta", "Media", "Baja"]:
            if nivel.lower() in resultado.lower():
                prioridad = nivel
                break

        return {
            "nombre": paciente.nombre,
            "hora_inicio": hora_inicio,
            "hora_fin": hora_fin,
            "duracion": round((hora_fin - hora_inicio).total_seconds(), 2),
            "diagnostico": resultado,
            "prioridad": prioridad
        }

    except Exception as e:
        print(f"[ERROR] Error al diagnosticar a {paciente.nombre}: {e}")
        return {
            "nombre": paciente.nombre,
            "hora_inicio": hora_inicio,
            "hora_fin": datetime.now(),
            "duracion": 0,
            "diagnostico": "Error de diagnóstico",
            "prioridad": "Media"
        }
