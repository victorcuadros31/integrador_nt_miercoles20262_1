import random
import uuid

from faker import Faker

#1. Escoger el pais y lenguaje para simular los datos
fake=Faker("es_CO")

#2. Sembrar semillas 
Faker.seed(42)
random.seed(42)

#3. Definir el dato y su tipo a simular
#id (texto (UUID)), 
#fecha_registro (fecha y hora),
#observacion (texto)
#estado (texto)
#id_usuario (texto (UUID))
#id_reto (texto (UUID))

#4. Definir el numero de datos simulados (DATASET)
FILAS=800

ESTADOS=["pendiente", "aprobado", "rechazado"]
IDS_USUARIO=["f47ac10b-58cc-4372-a567-0e02b2c3d479", "c9bf9e57-1685-4c89-bafb-ff5af830be8a", "123e4567-e89b-12d3-a456-426614174000"]
IDS_RETO=["e7b8c9d0-1f2a-4b3c-9d8e-5f6a7b8c9d0e", "a1b2c3d4-e5f6-7g8h-9i0j-k1l2m3n4o5p6", "98765432-1abc-4def-5678-90abcdef1234"]

#5. Construir funcion generadora de datos
def generar_datos_usuarios(numero_registros=FILAS):
    filas=[]
    for _ in range(numero_registros):
        filas.append({
            "id": str(uuid.uuid4()),
            "fecha_registro": fake.date_time_between(start_date="-1y", end_date="now"),
            "observacion": fake.sentence(nb_words=10),
            "estado": random.choice(ESTADOS),
            "id_usuario": random.choice(IDS_USUARIO),
            "id_reto": random.choice(IDS_RETO),
        })
        return filas
