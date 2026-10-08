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


#5.construir funcion generadora de datos limpios
def generar_empresas_limpias(n=FILAS):
    filas=[]
    for _ in range(n):
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
    df = pd.DataFrame(filas)
    return df

def generar_datos_empresas(numero_registros=FILAS):
    return generar_empresas_limpias(numero_registros).to_dict(orient="records")


def generar_muestra(datos,porcentaje):
    return datos.sample(frac=porcentaje, random_state=random.randint(0,9999)).index


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
    datos_df.loc[~datos_df.index.isin(subconjunto_datos_nit),"nit"]=datos_df.loc[~datos_df.index.isin(subconjunto_datos_nit),"nit"].apply(lambda x: x.replace("-","")).apply(lambda x: f"{x[:3]}.{x[3:6]}.{x[6:9]}-{x[9:]}")
    datos_df["nit"]=datos_df["nit"].apply(lambda x: x.replace(" ",""))

    #se ensucia sector:variantes del mismo sector: 'Tecnologia', 'TECNOLOGIA', ' tecnologia '.
    subconjunto_datos_sector_mayusculas=generar_muestra(datos_df,0.10)
    subconjunto_datos_sector_espacios=generar_muestra(datos_df,0.10)
    datos_df.loc[subconjunto_datos_sector_mayusculas,"sector"]=datos_df.loc[subconjunto_datos_sector_mayusculas,"sector"].apply(lambda x: x.upper())
    datos_df.loc[subconjunto_datos_sector_espacios,"sector"]=datos_df.loc[subconjunto_datos_sector_espacios,"sector"].apply(lambda x: f" {x.strip().lower()} ")

    #se ensucia "contacto": 8% en None(nulos)
    subconjunto_datos_contacto=generar_muestra(datos_df,0.08)
    datos_df.loc[subconjunto_datos_contacto,"contacto"]=None

    #se ensucia "correo:6% sin la arroba @ (correo invalido)
    subconjunto_datos_correo=generar_muestra(datos_df,0.06)
    datos_df.loc[subconjunto_datos_correo,"correo"]=datos_df.loc[subconjunto_datos_correo,"correo"].apply(lambda x: x.replace("@",""))  

    #Se ensucia `telefono`: tres formatos mezclados: '3001234567', '300 123 4567', '+57 300-123-4567'.
    subconjunto_datos_telefono=generar_muestra(datos_df,0.33)
    datos_df.loc[subconjunto_datos_telefono,"telefono"]=datos_df.loc[subconjunto_datos_telefono,"telefono"].apply(lambda x: f"{x[:3]} {x[3:6]} {x[6:]}")
    #el segundo formato se aplica solo a filas que no recibieron el primero (la mitad del 67% restante = 33%)
    subconjunto_datos_telefono2=generar_muestra(datos_df.drop(subconjunto_datos_telefono),0.50)
    datos_df.loc[subconjunto_datos_telefono2,"telefono"]=datos_df.loc[subconjunto_datos_telefono2,"telefono"].apply(lambda x: f"+57 {x[:3]}-{x[3:6]}-{x[6:]}")


    #Se ensucia `activa`: a veces como texto: 'SI', 'No', '1', '0'.
    subconjunto_datos_activa=generar_muestra(datos_df,0.50)
    datos_df["activa"]=datos_df["activa"].astype(object) #pandas 3 no deja guardar texto en una columna booleana
    datos_df.loc[subconjunto_datos_activa,"activa"]=datos_df.loc[subconjunto_datos_activa,"activa"].apply(lambda x: random.choice(["SI" if x else "No", "1" if x else "0"]))


    #5% de las filas repetidas tal cual (duplicados exactos).
    subconjunto_datos_duplicados=generar_muestra(datos_df,0.05)
    datos_df=pd.concat([datos_df, datos_df.loc[subconjunto_datos_duplicados]], ignore_index=True)

    #3% de los `nit` repetidos entre empresas distintas (el NIT deberia ser unico).
    subconjunto_datos_nit_repetidos=generar_muestra(datos_df,0.03)
    #se copia el nit de otras empresas (filas fuera de la muestra) para que quede repetido
    nits_de_otras_empresas=datos_df.drop(subconjunto_datos_nit_repetidos)["nit"].sample(n=len(subconjunto_datos_nit_repetidos), random_state=random.randint(0,9999)).values
    datos_df.loc[subconjunto_datos_nit_repetidos,"nit"]=nits_de_otras_empresas

    return datos_df


#6.Todo se arma aqui: genera los datos limpios, los ensucia y devuelve el DataFrame
def generar_empresas(n=300):
    df = generar_empresas_limpias(n)
    df = ensuciar_datos(df)
    return df


if __name__ == "__main__":
    df = generar_empresas()
    print(df.shape)
    print(df.head())
    print(df.isna().sum())
