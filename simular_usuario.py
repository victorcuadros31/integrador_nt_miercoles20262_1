import random
import uuid

from faker import Faker

#1. Escoger el pais y lenguaje para simular los datos del usuario
fake = Faker("es_CO")

#2. Sembrar semillas
Faker.seed(42)
random.seed(42)

#3. Definir el dato y su tipo a simular
# id (texto(UUID))
# nombre (texto)
# correo (texto)
# contraseña_hash (texto)
# rol (texto)***
# activo (booleano)
# fecha_registro (fecha y hora)

#4. Definir el numero de datos simulados(DATASET)
FILAS = 400
ROLES = ["administrador", "empresario", "profesor"]

#5. Construir funcion generadora de datos
def generar_datos_usuarios(numero_registros = FILAS):

    filas = []
    for _ in range(numero_registros):
        filas.append({
            "id": str(uuid.uuid4|()),
            "nombre":fake.name(),
            "correo": fake.email(),
            "contraseña_hash": fake.sha256(),
            "rol": random.choice(ROLES),
            "activo": random.choice([True, False]),
            "fecha_registro": fake.date_time_between(start_date="-2y", end_date="now")
        })
    return filas