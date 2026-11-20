"""Compara el enfoque original (bucles) con el optimizado (vectorizado).

Ejecutar desde la raíz del proyecto:
    python scripts/medir_rendimiento.py
"""

import sys
import time
import tracemalloc

import pandas as pd

from ventas import carga, limpieza, metricas

RUTA = "data/raw/ventas.csv"


def cronometrar(funcion, repeticiones=3):
    """Devuelve el menor tiempo (en segundos) de varias ejecuciones."""
    tiempos = []
    for _ in range(repeticiones):
        inicio = time.perf_counter()
        funcion()
        tiempos.append(time.perf_counter() - inicio)
    return min(tiempos)


def total_con_iterrows(df):
    """Versión original: recorre fila por fila."""
    totales = []
    for _, fila in df.iterrows():
        totales.append(fila["cantidad"] * fila["precio_unitario"]
                       * (1 - fila["descuento"]))
    return totales


def productos_con_bucles(df):
    """Versión original: lista para únicos y bucle anidado por producto."""
    productos = []
    for _, fila in df.iterrows():
        if fila["producto"] not in productos:
            productos.append(fila["producto"])
    resultado = []
    for producto in productos:
        suma = 0
        for _, fila in df.iterrows():
            if fila["producto"] == producto:
                suma += fila["total"]
        resultado.append([producto, suma])
    return sorted(resultado, key=lambda par: par[1], reverse=True)[:5]


def memoria_pico(funcion):
    """Memoria máxima (MB) que usa ``funcion`` mientras se ejecuta."""
    tracemalloc.start()
    funcion()
    _, pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return pico / 1_048_576


def main():
    """Imprime la tabla de comparación."""
    df = metricas.agregar_total(
        limpieza.limpiar_ventas(carga.cargar_ventas(RUTA)))
    print(f"Filas analizadas: {len(df):,}")
    filas = [
        ("Total por fila: iterrows vs vectorizado",
         cronometrar(lambda: total_con_iterrows(df), 1),
         cronometrar(lambda: metricas.agregar_total(df))),
        ("Top 5 productos: bucle anidado vs groupby",
         cronometrar(lambda: productos_con_bucles(df), 1),
         cronometrar(lambda: metricas.top_productos(df))),
    ]
    lista = df["producto"].astype(str).tolist()
    conjunto = set(lista)
    filas.append((
        "Buscar 1 000 productos: lista vs set",
        cronometrar(lambda: [p in lista for p in ["X"] * 1000]),
        cronometrar(lambda: [p in conjunto for p in ["X"] * 1000]),
    ))
    for nombre, antes, despues in filas:
        print(f"{nombre:<45}{antes:>10.4f} s{despues:>10.4f} s"
              f"{antes / despues:>10.0f}x")

    texto = pd.read_csv(RUTA)["producto"]
    categoria = texto.astype("category")
    print(f"Memoria columna producto: object "
          f"{texto.memory_usage(deep=True) / 1024:.0f} KB, category "
          f"{categoria.memory_usage(deep=True) / 1024:.0f} KB")
    pico_lista = memoria_pico(lambda: sum([x * 2 for x in range(10**6)]))
    pico_gen = memoria_pico(lambda: sum(x * 2 for x in range(10**6)))
    print(f"Pico de memoria al sumar 1 millón de valores: lista "
          f"{pico_lista * 1024:,.0f} KB, generador {pico_gen * 1024:.1f} KB")

if __name__ == "__main__":
    sys.exit(main())
