"""Armado y guardado del reporte de ventas."""

import json
from pathlib import Path

import pandas as pd

from ventas import metricas


def formatear_moneda(valor: float) -> str:
    """Da formato de dólares con separador de miles: 1234.5 -> "$1,234.50"."""
    return f"${valor:,.2f}"


def construir_reporte(df: pd.DataFrame) -> dict:
    """Reúne las métricas principales en un diccionario.

    Args:
        df: Ventas limpias con la columna ``total``.

    Returns:
        Diccionario con el total general, las ventas por región, los
        productos más vendidos y la evolución mensual.
    """
    return {
        "total_general": round(float(df["total"].sum()), 2),
        "facturas": int(len(df)),
        "por_region": metricas.ventas_por_region(df).round(2).to_dict(),
        "top_productos": metricas.top_productos(df).round(2).to_dict(),
        "mensual": metricas.ventas_mensuales(df).round(2).to_dict(),
    }


def guardar_reporte(reporte: dict, carpeta: Path) -> Path:
    """Guarda el reporte como JSON y devuelve la ruta del archivo.

    Args:
        reporte: Resultado de ``construir_reporte``.
        carpeta: Carpeta de destino; se crea si no existe.

    Returns:
        Ruta del archivo ``reporte_ventas.json``.
    """
    carpeta = Path(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)
    ruta = carpeta / "reporte_ventas.json"
    with ruta.open("w", encoding="utf-8") as archivo:
        json.dump(reporte, archivo, ensure_ascii=False, indent=2)
    return ruta
