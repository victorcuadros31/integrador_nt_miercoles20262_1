import random
import uuid
import pandas as pd
from faker import Faker

# 1. Escoger el pais y lenguaje para simular el usuario
fake = Faker('es_CO')

# 2. Sembrar semillas
Faker.seed(42)
random.seed(42)

# Solo hay 10 categorias reales base
CATEGORIAS = [
    "Logística", "Tecnología", "Finanzas", "Recursos Humanos", 
    "Operaciones", "Marketing", "Ventas", "Atención al Cliente", 
    "Legal", "Mantenimiento"
]

AREAS = [
    "Torre de Control", "Despachos", "Riesgos", "Soporte Técnico", 
    "Administración", "Calidad"
]

FILAS = 250

# Función para aplicar las variantes exactas descritas en la historia de usuario
def variar_escritura(texto):
    if not isinstance(texto, str):
        return texto
    
    # Quitamos tildes temporalmente para jugar con las variantes si es necesario, 
    # o usamos las variantes específicas solicitadas:
    base = texto.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
    
    opcion = random.randint(1, 4)
    if opcion == 1:
        return base.capitalize()        # Ejemplo: 'Logistica'
    elif opcion == 2:
        return texto.upper()            # Ejemplo: 'LOGÍSTICA' o 'LOGISTICA'
    elif opcion == 3:
        return f" {base.lower()} "      # Ejemplo: ' logistica ' (con espacios)
    else:
        return texto                    # Ejemplo: 'logística' (original con tilde)

# 3. Construir función generadora de datos base
def generar_datos_categoria(numero_registros=FILAS):
    filas = []
    for _ in range(numero_registros):
        filas.append({
            "id": str(uuid.uuid4()),
            "nombre": random.choice(CATEGORIAS),
            "descripcion": fake.sentence(nb_words=8),
            "area_responsable": random.choice(AREAS),
        })
    return filas    

# 7.1. Generar muestra aleatoria
def generar_muestra(datos, porcentaje):
    return datos.sample(frac=porcentaje, random_state=random.randint(1, 1000)).index

# 7.2. Función que ensucia los datos según los criterios
def ensuciar(datos_df):
    datos_df = datos_df.copy()
    
    # Se ensucia `descripcion`: 15% en None (nulos).
    subconjunto_descripcion = generar_muestra(datos_df, 0.15)
    datos_df.loc[subconjunto_descripcion, "descripcion"] = None

    # Se ensucia `area_responsable`: 10% en None.
    subconjunto_area = generar_muestra(datos_df, 0.10)
    datos_df.loc[subconjunto_area, "area_responsable"] = None

    # Se ensucia `nombre`: 30% con variantes de escritura.
    subconjunto_nombre = generar_muestra(datos_df, 0.30)
    datos_df.loc[subconjunto_nombre, "nombre"] = (
        datos_df.loc[subconjunto_nombre, "nombre"].apply(variar_escritura)
    )

    # 8% de las filas repetidas tal cual (duplicados exactos). 
    duplicados = datos_df.loc[generar_muestra(datos_df, 0.08)]
    datos_df = pd.concat([datos_df, duplicados], ignore_index=True)
    
    return datos_df

# 8. Todo se arma en una función `generar_categorias(n=250)` que devuelve el DataFrame (`return df`)
def generar_categorias(n=FILAS):
    tabla_ordenada_categorias = pd.DataFrame(generar_datos_categoria(n))
    df = ensuciar(tabla_ordenada_categorias)
    return df

# El bloque `if __name__ == "__main__":` imprime las revisiones solicitadas
if __name__ == "__main__":
    df = generar_categorias(250)
    print("--- SHAPE ---")
    print(df.shape)
    print("\n--- HEAD ---")
    print(df.head())
    print("\n--- ISNA SUM ---")
    print(df.isna().sum())