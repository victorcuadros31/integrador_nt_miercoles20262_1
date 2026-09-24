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
#  nombre (texto), 
# descripcion (texto), 
# fecha_inicio (fecha), 
# fecha_fin (fecha), 
# estado (texto), 
# id_empresa (texto (UUID)), 
# id_categoria (texto (UUID)), 
# id_prioridad (texto (UUID)).


#4. Definir el numero de datos simulados (DATASET)
FILAS=500