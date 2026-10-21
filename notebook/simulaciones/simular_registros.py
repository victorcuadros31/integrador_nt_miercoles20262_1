"""Simulación y ensuciado de la tabla registros.

Columnas: id, fecha_registro, observacion, estado, id_usuario, id_reto.

Uso:
    python src/simular_registros.py

También se puede importar desde otro script:
    from simular_registros import generar_registros
"""

import random
import uuid

import pandas as pd
from faker import Faker

# ---------------------------------------------------------------------------
# Constantes del proyecto
# ---------------------------------------------------------------------------
ESTADOS = ["pendiente", "aprobado", "rechazado"]

IDS_USUARIO = [
    "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "c9bf9e57-1685-4c89-bafb-ff5af830be8a",
    "123e4567-e89b-12d3-a456-426614174000",
]

# Nota: el segundo id del script original ("...7g8h-9i0j-k1l2...") no era un
# UUID válido (contenía letras fuera de a-f). Aquí se usan UUID válidos.
IDS_RETO = [
    "e7b8c9d0-1f2a-4b3c-9d8e-5f6a7b8c9d0e",
    "a1b2c3d4-e5f6-4a8b-9c0d-e1f2a3b4c5d6",
    "98765432-1abc-4def-8678-90abcdef1234",
]

SEMILLA = 42
FILAS = 800
FILAS2=20

COLUMNAS = ["id", "fecha_registro", "observacion", "estado", "id_usuario", "id_reto"]

# Porcentajes de ensuciado
PCT_FECHA_LATINA = 0.40
PCT_OBSERVACION_NULA = 0.20
PCT_ESTADO_VARIANTE = 0.15
PCT_PAR_REPETIDO = 0.10
PCT_DUPLICADO_EXACTO = 0.05

VARIANTES_ESTADO = ["inscrito", "EN PROCESO", " Finalizado "]

# Semillas globales (requisito del proyecto). Se fijan una sola vez al importar.
Faker.seed(SEMILLA)
random.seed(SEMILLA)


def _validar_uuids(valores):
    """Lanza ValueError si algún texto no tiene formato UUID."""
    for valor in valores:
        uuid.UUID(valor)


_validar_uuids(IDS_USUARIO)
_validar_uuids(IDS_RETO)


def _muestrear(rng, n, porcentaje, excluir=()):
    """Devuelve posiciones (enteros) elegidas de forma determinista.

    Usa un generador local rng, así no se vuelve a tocar la semilla global.
    """
    excluidas = set(excluir)
    candidatas = [i for i in range(n) if i not in excluidas]
    cantidad = round(n * porcentaje)
    return sorted(rng.sample(candidatas, cantidad))


def generar_registros(n=FILAS):
    """Genera n registros y los ensucia de forma determinista.

    Devuelve un DataFrame con las columnas: id, fecha_registro, observacion,
    estado, id_usuario, id_reto.
    """
    # Generadores locales con semilla fija: cada llamada da el mismo muestreo
    # y ensuciado, sin mutar las semillas globales ni depender de llamadas previas.
    rng = random.Random(SEMILLA)
    fake = Faker("es_CO")
    fake.seed_instance(SEMILLA)

    # 1. Datos limpios ------------------------------------------------------
    filas = []
    for _ in range(n):
        filas.append(
            {
                "id": str(uuid.uuid4()),
                "fecha_registro": fake.date_time_between(start_date="-1y", end_date="now"),
                "observacion": fake.sentence(nb_words=10),
                "estado": rng.choice(ESTADOS),
                "id_usuario": rng.choice(IDS_USUARIO),
                "id_reto": rng.choice(IDS_RETO),
            }
        )
    df = pd.DataFrame(filas, columns=COLUMNAS)

    # 2. Ensuciado ----------------------------------------------------------
    # 2.1 Fechas: se pasan a texto y 40 % queda en formato latino.
    fechas = df["fecha_registro"]
    iso = fechas.dt.strftime("%Y-%m-%d %H:%M:%S")
    latino = fechas.dt.strftime("%d/%m/%Y %H:%M")
    df["fecha_registro"] = iso
    pos = _muestrear(rng, n, PCT_FECHA_LATINA)
    df.loc[df.index[pos], "fecha_registro"] = latino.iloc[pos].values

    # 2.2 Observaciones nulas (20 %).
    pos = _muestrear(rng, n, PCT_OBSERVACION_NULA)
    df["observacion"] = df["observacion"].astype(object)
    df.loc[df.index[pos], "observacion"] = None

    # 2.3 Variantes de estado (15 %).
    pos = _muestrear(rng, n, PCT_ESTADO_VARIANTE)
    df.loc[df.index[pos], "estado"] = [rng.choice(VARIANTES_ESTADO) for _ in pos]

    # 2.4 Par id_usuario + id_reto repetido (10 %): cada fila elegida copia el
    # par de otra fila, simulando inscripciones duplicadas (el backend daría 409).
    pos = _muestrear(rng, n, PCT_PAR_REPETIDO)
    for i in pos:
        origen = rng.choice([j for j in range(n) if j != i])
        df.iloc[i, df.columns.get_loc("id_usuario")] = df.iloc[origen]["id_usuario"]
        df.iloc[i, df.columns.get_loc("id_reto")] = df.iloc[origen]["id_reto"]

    # 2.5 Duplicados exactos (5 %): se hace al final para que la copia sea
    # idéntica en todas las columnas. El total sigue siendo n filas.
    destinos = _muestrear(rng, n, PCT_DUPLICADO_EXACTO)
    for i in destinos:
        origen = rng.choice([j for j in range(n) if j not in destinos])
        df.iloc[i] = df.iloc[origen].values

    return df.reset_index(drop=True)


if _name_ == "_main_":
    df = generar_registros()
    print(df.shape)
    print(df.head())
    print(df.isna().sum())