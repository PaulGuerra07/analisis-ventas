"""Pruebas de integración, funcionales y de regresión."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

import main
from main import ejecutar

RAIZ = Path(__file__).resolve().parents[1]


def test_integracion_flujo_completo(csv_ventas, tmp_path):
    """carga -> limpieza -> métricas -> reporte trabajan juntos."""
    reporte = ejecutar(csv_ventas, tmp_path / "salida")
    guardado = json.loads(
        (tmp_path / "salida" / "reporte_ventas.json").read_text("utf-8"))
    assert guardado == reporte
    assert reporte["facturas"] == 4


def test_funcional_linea_de_comandos(csv_ventas, tmp_path):
    """El usuario ejecuta main.py y obtiene el total en pantalla."""
    resultado = subprocess.run(
        [sys.executable, str(RAIZ / "main.py"),
         "--datos", str(csv_ventas), "--salida", str(tmp_path)],
        capture_output=True, text=True, check=False,
    )
    assert resultado.returncode == 0
    assert "Total vendido: $47.00" in resultado.stdout


def test_main_devuelve_cero(csv_ventas, tmp_path, monkeypatch, capsys):
    """main() se ejecuta en el mismo proceso para medir su cobertura."""
    monkeypatch.setattr(sys, "argv", ["main.py", "--datos", str(csv_ventas),
                                      "--salida", str(tmp_path), "-v"])
    assert main.main() == 0
    assert "Sierra" in capsys.readouterr().out


def test_funcional_archivo_inexistente(tmp_path):
    """Con un archivo inexistente el programa termina con código 1."""
    resultado = subprocess.run(
        [sys.executable, str(RAIZ / "main.py"),
         "--datos", str(tmp_path / "nada.csv")],
        capture_output=True, text=True, check=False,
    )
    assert resultado.returncode == 1
    assert "No se encontró el archivo" in resultado.stderr


def test_regresion_resultados_conocidos(csv_ventas, tmp_path):
    """Los valores validados a mano no deben cambiar tras un refactor.

    Antes de la refactorización, el script original devolvía TOTAL: nan
    porque un descuento vacío contaminaba la suma, y contaba dos veces
    la factura F2. Esta prueba evita que esos errores vuelvan.
    """
    reporte = ejecutar(csv_ventas, tmp_path)
    assert reporte["total_general"] == pytest.approx(47.0)
    assert reporte["por_region"]["Costa"] == pytest.approx(4.0)
    assert reporte["top_productos"] == pytest.approx(
        {"Café": 25.0, "Arroz": 18.0, "Leche": 4.0})
