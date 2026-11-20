"""Cálculos agregados sobre las ventas limpias.

Todas las funciones usan operaciones vectorizadas de pandas en lugar
de recorrer el DataFrame fila por fila.
"""

from collections.abc import Iterable

import pandas as pd

from ventas.config import TOP_PRODUCTOS


def agregar_total(df: pd.DataFrame) -> pd.DataFrame:
    """Añade la columna ``total`` = cantidad × precio × (1 − descuento).

    Args:
        df: Ventas limpias con ``cantidad``, ``precio_unitario`` y
            ``descuento``.

    Returns:
        Copia del DataFrame con la columna ``total`` en dólares.
    """
    total = df["cantidad"] * df["precio_unitario"] * (1 - df["descuento"])
    return df.assign(total=total.round(2))


def ventas_por_region(df: pd.DataFrame) -> pd.Series:
    """Suma el total vendido en cada región, de mayor a menor.

    Args:
        df: Ventas con la columna ``total``.

    Returns:
        Serie indexada por región con el total vendido.
    """
    return df.groupby("region")["total"].sum().sort_values(ascending=False)


def top_productos(df: pd.DataFrame, n: int = TOP_PRODUCTOS) -> pd.Series:
    """Obtiene los ``n`` productos con mayor venta.

    Args:
        df: Ventas con la columna ``total``.
        n: Cantidad de productos a devolver.

    Returns:
        Serie indexada por producto, ordenada de mayor a menor.

    Raises:
        ValueError: Si ``n`` no es un entero positivo.
    """
    if n <= 0:
        raise ValueError("n debe ser un entero positivo")
    por_producto = df.groupby("producto", observed=True)["total"].sum()
    return por_producto.nlargest(n)


def ventas_mensuales(df: pd.DataFrame) -> pd.Series:
    """Suma el total vendido por mes (formato AAAA-MM).

    Args:
        df: Ventas con las columnas ``fecha`` y ``total``.

    Returns:
        Serie ordenada cronológicamente.
    """
    meses = df["fecha"].dt.to_period("M").astype(str)
    return df.groupby(meses)["total"].sum().sort_index()


def total_en_bloques(bloques: Iterable[pd.DataFrame]) -> float:
    """Suma el total de ventas recorriendo bloques uno a uno.

    Pensada para archivos que no caben en memoria: recibe cualquier
    iterable (por ejemplo, el generador ``carga.leer_por_bloques``) y
    usa una expresión generadora, así nunca hay más de un bloque cargado.

    Args:
        bloques: Iterable de DataFrames ya limpios.

    Returns:
        Total vendido en dólares.
    """
    return float(sum(agregar_total(b)["total"].sum() for b in bloques))
