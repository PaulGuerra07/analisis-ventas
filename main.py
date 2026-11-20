"""Punto de entrada: ejecuta el análisis de ventas de principio a fin.

Uso:
    python main.py --datos data/raw/ventas.csv --salida reports
"""

import argparse
import logging
import sys
from pathlib import Path

from ventas import carga, limpieza, metricas, reportes
from ventas.config import CARPETA_REPORTES, RUTA_DATOS

logger = logging.getLogger("ventas")


def leer_argumentos() -> argparse.Namespace:
    """Define y lee los argumentos de la línea de comandos."""
    parser = argparse.ArgumentParser(description="Análisis de ventas")
    parser.add_argument("--datos", type=Path, default=RUTA_DATOS)
    parser.add_argument("--salida", type=Path, default=CARPETA_REPORTES)
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="muestra mensajes de depuración")
    return parser.parse_args()


def ejecutar(ruta_datos: Path, carpeta_salida: Path) -> dict:
    """Carga, limpia, analiza y guarda el reporte.

    Args:
        ruta_datos: CSV de ventas.
        carpeta_salida: Carpeta donde se guarda el reporte.

    Returns:
        El reporte generado.
    """
    ventas = carga.cargar_ventas(ruta_datos)
    ventas = metricas.agregar_total(limpieza.limpiar_ventas(ventas))
    reporte = reportes.construir_reporte(ventas)
    ruta = reportes.guardar_reporte(reporte, carpeta_salida)
    logger.info("Reporte guardado en %s", ruta)
    return reporte


def main() -> int:
    """Ejecuta el programa y devuelve el código de salida."""
    args = leer_argumentos()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    try:
        reporte = ejecutar(args.datos, args.salida)
    except (FileNotFoundError, ValueError) as error:
        logger.error("No se pudo completar el análisis: %s", error)
        return 1
    total = reportes.formatear_moneda(reporte["total_general"])
    print("Total vendido:", total)
    for region, total in reporte["por_region"].items():
        print(f"  {region:<10}{reportes.formatear_moneda(total):>16}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
