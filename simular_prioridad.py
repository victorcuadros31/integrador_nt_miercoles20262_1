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
# nivel (entero)***
# dias_max_respuesta (entero).

#4. Definir el numero de datos simulados(DATASET)
FILAS = 200
NIVELES = [1, 2, 3]
nombre = ["Baja", "Media", "Alta"]
DIAS = [12, 7, 4]
nivel = [1, 2, 3]


#5. Construir funcion generadora de datos
def generar_datos_prioridades(numero_registros = FILAS):

    filas = []
    for _ in range(numero_registros):
        filas.append({
            "id": str(uuid.uuid4()),
            "nombre": random.choice(list(NIVELES.keys())),
            "nivel": NIVELES[nombre],
            "dias_max_respuesta": DIAS[nivel]
        })
    return filas