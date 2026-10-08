import random
import uuid
import pandas as pd
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

#6. Utilizaremos PANDAS para ordenar los datos simulados en un DATAFRAME
tabla_ordenada_prioridades = pd.DataFrame(generar_datos_prioridades())

#7. Ensuciar los datos (dato sin coerencia)

     #1. Generar una funcion que muestre los datos
def generar_muestra(datos,porcentaje):
    return datos.sample(fraccion = porcentaje,random_state = random.randint(0,9999)).index
     #2. Funcion que ensucia los datos
def ensuciar(datos_df):
    datos_df = datos_df.copy()

    #Se ensucia `nombre`: variantes: 'ALTA', ' alta ', 'Alta'.
    def escribir_mal(texto):
            variantes = [texto.lower(), f" {texto.title()} ", texto.capitalize()]
            return random.choice(variantes)
    subconjunto_datos = generar_muestra(datos_df,0.1)
    datos_df.loc[subconjunto_datos,"nombre"] = datos_df.loc[subconjunto_datos,"nombre"].map(escribir_mal)

    #Se ensucia `nivel`: a veces como TEXTO ('3'), a veces la palabra ('tres')
    def nivel_mal():
        niveles = ['1','uno','2','dos','3','tres']
        return random.choice(niveles)
    subconjunto_datos = generar_muestra(datos_df, 0.14)
    datos_df.loc[subconjunto_datos, "nivel"] = datos_df.loc[subconjunto_datos, "nivel"].map(nivel_mal)

    #Se ensucia `nivel` con el 7% en None.
    subconjunto_datos = generar_muestra(datos_df,0.07)
    datos_df.loc[subconjunto_datos,"nivel"] = None

    #Se ensucia `dias_max_respuesta`: 5% en None 
    subconjunto_datos = generar_muestra(datos_df,0.05)
    datos_df.loc[subconjunto_datos,"dias_max_respuesta"] = None

    #Se ensucia `dias_max_respuesta`: 3% con un valor absurdo (999).
    subconjunto_datos = generar_muestra(datos_df,0.03)
    datos_df.loc[subconjunto_datos,"dias_max_respuesta"] = 999

    #Se ensucia el 8% repitiendo las filas
    filas_repetidas_idx = generar_muestra(datos_df, 0.08)
    filas_repetidas = datos_df.loc[filas_repetidas_idx]
    datos_df = pd.concat([datos_df, filas_repetidas], ignore_index=True)