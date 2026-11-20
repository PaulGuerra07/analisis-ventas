"""Corrección de datos inconsistentes antes del análisis."""

import logging

import pandas as pd

from ventas.config import CORRECCIONES_REGION, REGIONES_VALIDAS

logger = logging.getLogger(__name__)


def normalizar_region(regiones: pd.Series) -> pd.Series:
    """Unifica la escritura de las regiones.

    Quita espacios, aplica formato título y corrige tildes, de modo que
    " sierra", "SIERRA" y "Sierra" se cuenten como la misma región.

    Args:
        regiones: Columna de regiones tal como viene en el archivo.

    Returns:
        Serie con las regiones normalizadas.
    """
    limpias = regiones.str.strip().str.title()
    return limpias.replace(CORRECCIONES_REGION)


def limpiar_ventas(df: pd.DataFrame) -> pd.DataFrame:
    """Devuelve una copia limpia de las ventas.

    Reglas aplicadas:
    1. Se elimina cada factura repetida (se conserva la primera).
    2. Las regiones se normalizan con ``normalizar_region``.
    3. Un descuento vacío se toma como 0 y se limita al rango [0, 1].
    4. Se descartan cantidades <= 0 (devoluciones) y precios vacíos.

    Args:
        df: Ventas recién cargadas.

    Returns:
        DataFrame limpio con índice reiniciado. El original no cambia.
    """
    limpio = (
        df.drop_duplicates(subset="id_factura")
        .assign(
            region=lambda d: normalizar_region(d["region"]),
            descuento=lambda d: d["descuento"].fillna(0).clip(0, 1),
        )
        .query("cantidad > 0")
        .dropna(subset=["precio_unitario"])
        .reset_index(drop=True)
    )
    desconocidas = set(limpio["region"].unique()) - REGIONES_VALIDAS
    if desconocidas:
        logger.warning("Regiones no reconocidas: %s", sorted(desconocidas))
    logger.info("Filas: %d leídas, %d válidas", len(df), len(limpio))
    return limpio
