import random
import uuid

from faker import Faker

#1 Escoger el pais y lenguaje para simular el usuario
fake=Faker('es_CO')

#2 sembrar semillas
Faker.seed(42)
random.seed(42)

#3 Definir el dato y su tipo a simular 
#id (texto (UUID))
#nombre (texto)
#descripcion (texto)
#area_responsable (texto)

#4 Definir el numero de datos simulados (Dataset)
FILAS=400

