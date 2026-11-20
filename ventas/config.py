"""Rutas y constantes del proyecto, reunidas en un solo lugar."""

from pathlib import Path

RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
RUTA_DATOS = RAIZ_PROYECTO / "data" / "raw" / "ventas.csv"
CARPETA_REPORTES = RAIZ_PROYECTO / "reports"

COLUMNAS_REQUERIDAS = (
    "id_factura", "fecha", "producto", "categoria",
    "region", "cantidad", "precio_unitario", "descuento",
)
TIPOS_COLUMNAS = {
    "id_factura": "string",
    "producto": "category",
    "categoria": "category",
    "region": "string",
    "cantidad": "int32",
    "precio_unitario": "float64",
    "descuento": "float64",
}
REGIONES_VALIDAS = frozenset({"Sierra", "Costa", "Amazonía", "Insular"})
CORRECCIONES_REGION = {"Amazonia": "Amazonía"}
TOP_PRODUCTOS = 5
TAMANO_BLOQUE = 100_000
