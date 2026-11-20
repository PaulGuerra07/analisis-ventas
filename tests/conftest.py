"""Datos de prueba compartidos por todos los tests."""

import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def ventas_crudas() -> pd.DataFrame:
    """Seis filas pequeñas con los errores típicos del archivo real."""
    return pd.DataFrame({
        "id_factura": ["F1", "F2", "F2", "F3", "F4", "F5"],
        "fecha": pd.to_datetime(["2026-01-05", "2026-01-20", "2026-01-20",
                                 "2026-02-03", "2026-02-10", "2026-02-15"]),
        "producto": ["Arroz", "Leche", "Leche", "Arroz", "Café", "Café"],
        "categoria": ["Abarrotes", "Lácteos", "Lácteos", "Abarrotes",
                      "Bebidas", "Bebidas"],
        "region": [" sierra", "COSTA", "COSTA", "Amazonia", "Sierra",
                   "Insular"],
        "cantidad": [10, 4, 4, -2, 5, 2],
        "precio_unitario": [2.0, 1.0, 1.0, 2.0, 4.0, 5.0],
        "descuento": [0.10, np.nan, np.nan, 0.0, 0.0, 0.5],
    })


@pytest.fixture
def csv_ventas(tmp_path, ventas_crudas):
    """Escribe ``ventas_crudas`` en un CSV temporal y devuelve su ruta."""
    ruta = tmp_path / "ventas.csv"
    ventas_crudas.to_csv(ruta, index=False)
    return ruta
