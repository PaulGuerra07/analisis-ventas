"""Pruebas unitarias del módulo limpieza."""

import pandas as pd
import pytest

from ventas.limpieza import limpiar_ventas, normalizar_region


@pytest.mark.parametrize("entrada, esperado", [
    (" sierra", "Sierra"),
    ("COSTA", "Costa"),
    ("Costa ", "Costa"),
    ("amazonia", "Amazonía"),
    ("AMAZONÍA", "Amazonía"),
    ("insular", "Insular"),
])
def test_normalizar_region(entrada, esperado):
    resultado = normalizar_region(pd.Series([entrada]))
    assert resultado.iloc[0] == esperado


def test_elimina_facturas_duplicadas(ventas_crudas):
    limpio = limpiar_ventas(ventas_crudas)
    assert limpio["id_factura"].is_unique


def test_descuento_vacio_se_toma_como_cero(ventas_crudas):
    limpio = limpiar_ventas(ventas_crudas)
    assert limpio["descuento"].notna().all()
    assert limpio.loc[limpio["id_factura"] == "F2", "descuento"].item() == 0


def test_descarta_devoluciones(ventas_crudas):
    limpio = limpiar_ventas(ventas_crudas)
    assert (limpio["cantidad"] > 0).all()
    assert "F3" not in set(limpio["id_factura"])


def test_no_modifica_el_original(ventas_crudas):
    copia = ventas_crudas.copy()
    limpiar_ventas(ventas_crudas)
    pd.testing.assert_frame_equal(ventas_crudas, copia)


def test_dataframe_vacio_no_falla(ventas_crudas):
    vacio = ventas_crudas.iloc[0:0]
    assert limpiar_ventas(vacio).empty


def test_avisa_region_desconocida(ventas_crudas, caplog):
    ventas_crudas.loc[0, "region"] = "Galapagos"
    limpiar_ventas(ventas_crudas)
    assert "Regiones no reconocidas" in caplog.text
