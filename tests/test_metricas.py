"""Pruebas unitarias del módulo metricas."""

import pytest

from ventas import metricas
from ventas.limpieza import limpiar_ventas


@pytest.fixture
def ventas(ventas_crudas):
    return metricas.agregar_total(limpiar_ventas(ventas_crudas))


def test_total_aplica_descuento(ventas):
    # F1: 10 unidades x $2.00 con 10 % de descuento = $18.00
    fila = ventas.loc[ventas["id_factura"] == "F1"]
    assert fila["total"].item() == pytest.approx(18.0)


def test_ventas_por_region(ventas):
    por_region = metricas.ventas_por_region(ventas)
    assert por_region.to_dict() == pytest.approx(
        {"Sierra": 38.0, "Insular": 5.0, "Costa": 4.0})
    assert list(por_region.index) == ["Sierra", "Insular", "Costa"]


def test_top_productos(ventas):
    top = metricas.top_productos(ventas, n=2)
    assert list(top.index) == ["Café", "Arroz"]
    assert top.iloc[0] == pytest.approx(25.0)


@pytest.mark.parametrize("n", [0, -3])
def test_top_productos_rechaza_n_invalido(ventas, n):
    with pytest.raises(ValueError):
        metricas.top_productos(ventas, n=n)


def test_ventas_mensuales(ventas):
    mensual = metricas.ventas_mensuales(ventas)
    assert mensual.to_dict() == pytest.approx(
        {"2026-01": 22.0, "2026-02": 25.0})


def test_total_en_bloques_igual_al_total(ventas):
    limpias = ventas.drop(columns="total")
    bloques = (limpias.iloc[i:i + 2] for i in range(0, len(limpias), 2))
    assert metricas.total_en_bloques(bloques) == pytest.approx(47.0)
