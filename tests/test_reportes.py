"""Pruebas unitarias del módulo reportes."""

import pytest

from ventas.reportes import formatear_moneda


@pytest.mark.parametrize("valor, esperado", [
    (0, "$0.00"),
    (1234.5, "$1,234.50"),
    (579507.824, "$579,507.82"),
])
def test_formatear_moneda(valor, esperado):
    assert formatear_moneda(valor) == esperado
