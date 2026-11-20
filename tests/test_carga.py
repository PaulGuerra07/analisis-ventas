"""Pruebas unitarias del módulo carga."""

import pytest

from ventas.carga import cargar_ventas, leer_por_bloques


def test_carga_columnas_y_tipos(csv_ventas):
    df = cargar_ventas(csv_ventas)
    assert len(df) == 6
    assert str(df["producto"].dtype) == "category"
    assert str(df["fecha"].dtype).startswith("datetime64")


def test_archivo_inexistente(tmp_path):
    with pytest.raises(FileNotFoundError):
        cargar_ventas(tmp_path / "no_existe.csv")


def test_columnas_faltantes(tmp_path, ventas_crudas):
    ruta = tmp_path / "incompleto.csv"
    ventas_crudas.drop(columns="descuento").to_csv(ruta, index=False)
    with pytest.raises(ValueError, match="descuento"):
        cargar_ventas(ruta)


def test_leer_por_bloques_es_generador(csv_ventas):
    bloques = leer_por_bloques(csv_ventas, tamano_bloque=4)
    tamanos = [len(b) for b in bloques]
    assert tamanos == [4, 2]
