import random
import uuid
from faker import Faker
import pandas as pd



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
SECTORES=["Tecnologia","Salud","Manufactura","Energia"]


#5.construir funcion generadora de datos
def generar_datos_empresas(numero_registros=FILAS):
    filas=[]
    for _ in range(numero_registros):
        filas.append({
            "id": str(uuid.uuid4()),
            "nombre": fake.company(),
            "nit":fake.numerify("#########-#"),
            "sector":random.choice(SECTORES),
            "contacto": fake.name(),
            "correo": fake.company_email(),
            "telefono":fake.numerify("3#########"),
            "activa": random.choice([True, False])                      

 })
        return filas

    tabla_ordenada_usuarios=pd.DataFrame(generar_datos_usuarios())
    print(tabla_ordenada_usuarios) 



def generar_muestra(datos,procentaje):
    return datos.sample(fraccion=porcentaje, random_state=random.randit(0,9999 )).index


def ensuciar_datos(datos_df):
    datos_df=datos_df.copy()

#Se ensucia nombre: 10% con espacios sobrantes al inicio y al final; 15% en MAYUSCULAS.#

subconjunto_datos=generar_muestra(datos_df,0.10)
subconjunto_datos_mayusculas=generar_muestra(datos_df,0.15)
datos_df.loc[subconjunto_datos,"nombre"]=datos_df.loc[subconjunto_datos,"nombre"].apply(lambda x: f" {x} ")
datos_df.loc[subconjunto_datos_mayusculas,"nombre"]=datos_df.loc[subconjunto_datos_mayusculas,"nombre"].apply(lambda x: x.upper())

#se ensucia nit:la mitad con puntos y guiones(900.123.456-7) y la otra mitad sin nada (9001234567).
subconjunto_datos_nit=generar_muestra(datos_df,0.50)
datos_df.loc[subconjunto_datos_nit,"nit"]=datos_df.loc[subconjunto_datos_nit,"nit"].apply(lambda x: x.replace("-","").replace(".",""))
datos_df.loc[~datos_df.index.isin(subconjunto_datos_nit),"nit"]=datos_df.loc[~datos_df.index.isin(subconjunto_datos_nit),"nit"].apply(lambda x: f"{x[:3]}.{x[3:6]}.{x[6:9]}-{x[9:]}")
datos_df["nit"]=datos_df["nit"].apply(lambda x: x.replace(" ",""))

#se ensucia sector:variantes del mismo sector:"Tecnologia",TECNOLOGIA", "tecnologia".
subconjunto_datos_sector=generar_muestra(datos_df,0.20)
subconjunto_datos_sector_mayusculas=generar_muestra(datos_df,0.10)
datos_df.loc[subconjunto_datos_sector,"sector"]=datos_df.loc[subconjunto_datos_sector,"sector"].apply(lambda x: x.lower())
datos_df.loc[subconjunto_datos_sector_mayusculas,"sector"]=datos_df.loc[subconjunto_datos_sector_mayusculas,"sector"].apply(lambda x: x.upper())    

#se ensucia "contacto": 8% en None(nulos)
subconjunto_datos_contacto=generar_muestra(datos_df,0.08)
datos_df.loc[subconjunto_datos_contacto,"contacto"]=None

#se ensucia "correo:6% sin la arroba @ (correo invalido)
subconjunto_datos_correo=generar_muestra(datos_df,0.06)
datos_df.loc[subconjunto_datos_correo,"correo"]=datos_df.loc[subconjunto    _datos_correo,"correo"].apply(lambda x: x.replace("@",""))  

#Se ensucia `telefono`: tres formatos mezclados: '3001234567', '300 123 4567', '+57 300-123-4567'.
subconjunto_datos_telefono=generar_muestra(datos_df,0.33)
datos_df.loc[subconjunto_datos_telefono,"telefono"]=datos_df.loc[subconjunto_datos_telefono,"telefono"].apply(lambda x: f"{x[:3]} {x[3:6]} {x[6:]}")
subconjunto_datos_telefono2=generar_muestra(datos_df,0.33       )
datos_df.loc[subconjunto_datos_telefono2,"telefono"]=datos_df.loc[subconjunto_datos_telefono2,"telefono"].apply(lambda x: f"+57 {x[:3]}-{x[3:6]}-{x[6:]}")


#Se ensucia `activa`: a veces como texto: 'SI', 'No', '1', '0'.
subconjunto_datos_activa=generar_muestra(datos_df,0.50)
datos_df.loc[subconjunto_datos_activa,"activa"]=datos_df.loc[subconjunto_datos_activa,"activa"].apply(lambda x: "SI" if x else "NO") 


#5% de las filas repetidas tal cual (duplicados exactos).
subconjunto_datos_duplicados=generar_muestra(datos_df,0.05)
datos_df=datos_df.append(datos_df.loc[subconjunto_datos_duplicados], ignore_index=True) 

#3% de los `nit` repetidos entre empresas distintas (el NIT deberia ser unico).
subconjunto_datos_nit_repetidos=generar_muestra(datos_df,0.03)
datos_df.loc[subconjunto_datos_nit_repetidos,"nit"]=datos_df.loc[subconjunto_datos_nit_repetidos,"nit"].sample(frac=1).values
