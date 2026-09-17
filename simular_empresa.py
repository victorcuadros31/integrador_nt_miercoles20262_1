import random
import uuid

from faker import Faker

#1-Escoger el pais y lenguaje para simular los datos
fake=Faker('es_CO')

#2-Sembrar Semillas
Faker.seed(42)
random.seed(42)

#3.Definir el dato y el tipo a simular  
#id (texto (UUID)), 
#nombre (texto), 
#nit (texto), 
#sector (texto), ****************
#contacto (texto), 
#correo (texto), 
#telefono (texto), 
#activa (booleano).

#4-Definir numero de datos simulados (DATASET)
FILAS=300