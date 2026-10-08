import random 
import uuid 
from datetime import timedelta
import pandas as pd

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
IDS_EMPRESA=[
    "c8f9b7d4-3a2e-4c1f-9b6d-7e5f4a3b2c1d",
    "d9a0c8e5-4b3f-4d20-a7c1-8f6e5b4a3d2c",
    "e0b1d9f6-5c4a-4e31-b8d2-9a7f6c5b4e3d",
    "f1c2e0a7-6d5b-4f42-c9e3-a8b7d6c5f4e0",
    "a2d3f1b8-7e6c-4053-da4f-b9c8e7d6a5f1",
]
IDS_CATEGORIA=[
    "b3e4a2c9-8f7d-4164-eb5a-c0d9f8e7b6a2",
    "c4f5b3d0-9a8e-4275-fc6b-d1e0a9f8c7b3",
    "d5a6c4e1-0b9f-4386-ad7c-e2f1b0a9d8c4",
    "e6b7d5f2-1c0a-4497-be8d-f3a2c1b0e9d5",
]
IDS_PRIORIDAD=[
    "f7c8e6a3-2d1b-45a8-cf9e-a4b3d2c1f0e6",
    "a8d9f7b4-3e2c-46b9-d0af-b5c4e3d2a1f7",
    "b9e0a8c5-4f3d-47ca-e1b0-c6d5f4a3b2e8",
]


def generar_datos_metas(numero_registros=FILAS):

    filas=[]
    for _ in range(numero_registros):
        fecha_inicio = fake.date_between(start_date="-1y", end_date="+3m")
        filas.append({
            "id": str(uuid.uuid4()),
            "nombre": fake.sentence(nb_words=6).rstrip("."),
            "descripcion": fake.sentence(nb_words=12),
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_inicio + timedelta(days=random.randint(15, 180)),
            "estado": random.choice(estados),
            "id_empresa": random.choice(IDS_EMPRESA),
            "id_categoria": random.choice(IDS_CATEGORIA),
            "id_prioridad": random.choice(IDS_PRIORIDAD)
        })
        df = pd.DataFrame(filas)
        df = ensuciar(df)
        return df

# Ensuciar Datos

# 1. Generar funcion que muestre los datos.
def generar_muestra(datos, porcentaje):
    return datos.sample(frac=porcentaje, random_state=random.randint(0, 9999)).index

# 2. Ensuciar los datos/Copiar Informacion.
def ensuciar(datos_df):
    datos_df=datos_df.copy()

    # Para atributo nombre 10% de los datos con espacios sobrantes.
    subconjuto_datos = generar_muestra(datos_df,0.1)
    datos_df.loc[subconjunto_datos,"nombre"] = " "+data_df.loc[subconjunto_datos,"nombre"]+" "

    # Para atributo descripcion 12% de los datos None (nulos).
    subconjuto_datos = generar_muestras(datos_df,0.12)
    datos_df.loc[subconjunto_datos,"descripcion"] = None

    # Para fecha_inicio : dos formatos mezclados : 2026-03-02 y 02/03/2026.
    iso = datos_df["fecha_inicio"].dt.strftime("%Y-%m-%d" "%d%m%Y")
    latino = datos_df["fecha_inicio"].dt.strftime("%d/%m/%Y")
    datos_df["fecha_inicio"]=iso
    filas_elegidas = generar_muestra(datos_df, 0.40)
    datos_df.loc[filas_elegidas, "fecha_inicio"] = latino.loc[filas_elegidas]

    # Se ensucia fecha fin 8% en None y 5% Anterior a fecha_inicio (error logico a detectar).

    # 1. 8% de los datos None
    subconjunto_nulos = generar_muestra(datos_df , 0.08)
    datos_df.loc[subconjunto_nulos, " fecha_fin"] = None

    # 2. 5% de los datos con fecha anterior a fecha inicio
    subconjunto_error = generar_muestra(datos_df, 0.05)
    #Se resta de 1 a 30 dias para garantizar que sea anterior a la fecha.
    datos_df.loc[subconjunto_error, "fecha_fin"] = datos_df.loc[subconjunto_error,"fecha_inicio"] - pd.Timedelta(days=10)

    # Para atributo estado : variantes : en_curso , EN CURSO , Cerrado.
    def escribir_mal(texto):
        variantes = [
            "en_curso",
            "EN CURSO",
            "Cerrado"
        ]
        return random.choice(variantes)

    subconjunto_datos = generar_muestras(datos_df,0.14)
    datos_df.loc[subconjunto_datos,"estado"] = datos_df.loc[subconjunto_datos,"estado"].apply(escribir_mal)

    # 5% de las filas repetidas tal cual (duplicados exactos).
    filas_duplicadas = generar_muestra(datos_df , 0.05)
    datos_df = pd.concat([datos_df, datos_df.loc[filas_duplicadas]],ignore_index=True)



