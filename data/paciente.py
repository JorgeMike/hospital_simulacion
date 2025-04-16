from dataclasses import dataclass, field
from typing import List
from uuid import uuid4

@dataclass
class Paciente:
    nombre: str
    genero: str
    edad: int
    raza: str
    altura: float
    peso: float
    habitos_alimenticios: str
    antecedentes_medicos: List[str]
    sintomas: str 
    registrado: bool = False
    id: str = field(default_factory=lambda: str(uuid4()))
