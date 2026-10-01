import random
import uuid
import pandas as pd
from faker import Faker

#1. Escoger el pais y lenguaje para simular los datos
fake=Faker('es_CO')

#2.Sembrar Semillas 
Faker.seed(42)
random.seed(42)

#3.Definir el dato y el tipo a simular
#id (texto (UUID)),
#nombre (texto),
#correo (texto),
#contrasena_hash (texto),
#rol (texto),*****************
#activo (booleano),
#fecha_registro (fecha hora).


#4.Definir numero de datos simulados (DATASET)
FILAS=400

ROLES=["administrador","empresario","profesor"]




#5.construir funcion generadora de datos
def generar_datos_usuarios(numero_registros=FILAS):
    for_in range(numero_registros):
    filas.append({
        "id": str(uuid.uuid4()),
        "nombre": fake.name(),
        "correo":fake.email(),
        "contraseña_hash":fake.sha256(),
        "rol": random.choice(ROLES),
        "activo": random.choice([True, False]),
        "fecha_registro":fake.date_time_between(start_date='-2y', end_date='now').isoformat()



})
return filas    
        

6.#utilizaremos PANDAS para simular los datos ordenados en un DATAFRAME
tabla_ordenada_usuarios=pd.DataFrame(generar_datos_usuarios())   
print(tabla_ordenada_usuarios)     


7.#ensuciar los datos
7.1. #generar un funcion que muestre los datos
def generar_muestra(datos,procentaje):
    return datos.sample(fraccion=porcentaje, random_state=random.randit(0,9999 )).index

7.2. #funcion que ensucia los datos

def ensuciar_datos(datos_df):
    datos_df=datos_df.copy()


    #Para el  atributo nombre generar el 10% de los datos con espacios sobrantes
    subconjunto_datos=generar_muestra(datos_df,0.1)
    datos_df.loc[subconjunto_datos,"nombre"]=" "+datos_df.loc[subconjunto_datos,"nombre"]+" "    

    #Para el atrubuto nombre generar el 8% de los datos en mayusculas
    subconjunto_datos=generar_muestra(datos_df,0.08)
    datos_df.loc[subconjunto_datos,"nombre"]=datos_df.loc[subconjunto_datos,"nombre"].str.upper()


    #para el atributo correo necesito el 12% de los datos en Mayusculas
    subconjunto_datos=generar_muestra(datos_df,0.12)
    datos_df.loc[subconjunto_datos,"correo"]=datos_df.loc[subconjunto_datos,"correo"].str.upper()

    #para el atributo correo necesito el 5% de los datos sin @
    subconjunto_datos=generar_muestra(datos_df,0.05)
    datos_df.loc[subconjunto_datos,"correo"]=datos_df.loc[subconjunto_datos,"correo"].str.replace("@","", regex=False)




    #para el atributo correo necesito el 4% de los datos None
    subconjunto_datos=generar_muestra(datos_df,0.04)
    datos_df.loc[subconjunto_datos,"correo"]=None


    #para el atributo rol para la pálabra administrador y las otras palabras generar
    variantes de Escritura (Mayusculas, capital, espaciado)

    def escribir_mal(text):
        variantes=[text.lower(), f"{text.title()}", f" {text.capitalize()}()"]
        return random.choice(variantes)

    subconjunto_datos=generar_muestra(datos_df,0.15)
    datos_df.loc[subconjunto_datos,"rol"]=datos_df.loc[subconjunto_datos,"rol"].map(escribir_mal)

    
    # Para el atributo fecha_registro: dos formatos mezclados ("2026-03-15 14:30:00" y "15/03/2026 14:30")
    # (si tu fecha es solo fecha, sin hora, usa "%Y-%m-%d" y "%d/%m/%Y")
    iso = datos_df["fecha_registro"].dt.strftime("%Y-%m-%d %H:%M:%S")               
    latino = datos_df["fecha_registro"].dt.strftime("%d/%m/%Y %H:%M")              
    datos_df["fecha_registro"] = iso                                               
    filas_elegidas = generar_muestra(datos_df, 0.40)
    datos_df.loc[filas_elegidas, "fecha_registro"] = latino.loc[filas_elegidas] 


   

)

