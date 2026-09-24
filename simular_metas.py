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

# 5 Construir funcion generadora de datos simulados

estados=["pendiente", "en progreso" ,"completada"]
ids_empresa=["Apple", "Microsoft", "Google", "Amazon", "Facebook"]
ids_categoria=["Desarrollo", "Marketing", "Ventas", "Soporte"]
ids_prioridad=["Alta", "Media", "Baja"]


def generar_datos_metas(numero_registros=FILAS):

    filas=[]
    for _ in range(numero_registros):
        filas.append({
            "id": str(uuid.uuid4()),
            "nombre": fake.sentence(nb_words=6).rstrip("."),
            "descripcion": fake.sentence(nb_words=12),
            "fecha_inicio": fake.date_between(start_date="-1y", end_date="+3m"),
            "fecha_fin": fecha_inicio + timedelta(days=random.randint(15, 180)),
            "estado": random.choice(estados),
            "id_empresa":random.choice(ids_empresa),
            "id_categoria": random.choice(ids_categoria),
            "id_prioridad": random.choice(ids_prioridad)
        })
    return filas