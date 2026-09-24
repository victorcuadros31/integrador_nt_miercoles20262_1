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
#nombre (texto), 
#correo (texto), 
#contrasena_hash (texto), 
#rol (texto), *****************
#activo (booleano), 
#fecha_registro (fecha y hora).

#4. Definir el numero de datos simulados (DATASET)
FILAS=400