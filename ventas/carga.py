"""Lectura y validación del archivo de ventas."""

from collections.abc import Iterator
from pathlib import Path

import pandas as pd

from ventas.config import COLUMNAS_REQUERIDAS, TAMANO_BLOQUE, TIPOS_COLUMNAS


def validar_columnas(df: pd.DataFrame) -> None:
    """Comprueba que el DataFrame tenga todas las columnas requeridas.

    Args:
        df: Datos recién leídos.

    Raises:
        ValueError: Si falta alguna columna; el mensaje indica cuáles.
    """
    faltantes = set(COLUMNAS_REQUERIDAS) - set(df.columns)
    if faltantes:
        raise ValueError(f"Faltan columnas: {sorted(faltantes)}")


def cargar_ventas(ruta: Path) -> pd.DataFrame:
    """Lee el CSV de ventas con tipos de datos adecuados.

    Solo se leen las columnas necesarias y las de texto repetitivo se
    guardan como ``category``, lo que reduce el uso de memoria.

    Args:
        ruta: Ubicación del archivo CSV.

    Returns:
        DataFrame con las columnas de ``COLUMNAS_REQUERIDAS``.

    Raises:
        FileNotFoundError: Si el archivo no existe.
        ValueError: Si al archivo le faltan columnas.
    """
    ruta = Path(ruta)
    if not ruta.is_file():
        raise FileNotFoundError(f"No se encontró el archivo: {ruta}")
    encabezado = pd.read_csv(ruta, nrows=0)
    validar_columnas(encabezado)
    return pd.read_csv(
        ruta,
        usecols=list(COLUMNAS_REQUERIDAS),
        dtype=TIPOS_COLUMNAS,
        parse_dates=["fecha"],
    )


def leer_por_bloques(
    ruta: Path, tamano_bloque: int = TAMANO_BLOQUE
) -> Iterator[pd.DataFrame]:
    """Genera el archivo por partes para no cargarlo entero en memoria.

    Args:
        ruta: Ubicación del archivo CSV.
        tamano_bloque: Número de filas de cada bloque.

    Yields:
        Un DataFrame por bloque, con los mismos tipos que ``cargar_ventas``.
    """
    lector = pd.read_csv(
        ruta,
        usecols=list(COLUMNAS_REQUERIDAS),
        dtype=TIPOS_COLUMNAS,
        parse_dates=["fecha"],
        chunksize=tamano_bloque,
    )
    with lector:
        yield from lector
