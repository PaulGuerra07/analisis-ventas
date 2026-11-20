"""Genera un archivo de ventas sintético para probar el proyecto.

El archivo incluye a propósito los problemas que suelen tener los datos
reales: facturas duplicadas, descuentos vacíos, devoluciones (cantidades
negativas) y regiones escritas de distintas formas.
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

PRODUCTOS = {
    "Abarrotes": ["Arroz 2 kg", "Azúcar 1 kg", "Aceite 1 L", "Fideo 400 g",
                  "Atún 180 g", "Harina 1 kg", "Lenteja 500 g"],
    "Lácteos": ["Leche 1 L", "Queso fresco", "Yogur 1 L", "Mantequilla"],
    "Bebidas": ["Agua 625 ml", "Jugo 1 L", "Gaseosa 3 L", "Café 200 g",
                "Té 25 u"],
    "Limpieza": ["Detergente 1 kg", "Cloro 1 L", "Jabón de ropa",
                 "Lavavajillas"],
    "Cuidado personal": ["Shampoo 400 ml", "Pasta dental", "Papel higiénico",
                         "Jabón de tocador", "Desodorante"],
}
REGIONES = ["Sierra", "Costa", "Amazonía", "Insular"]
VARIANTES_REGION = {
    "Sierra": ["sierra", "SIERRA", " Sierra"],
    "Costa": ["costa", "COSTA", "Costa "],
    "Amazonía": ["Amazonia", "amazonia", "AMAZONÍA"],
    "Insular": ["insular", "INSULAR"],
}


def generar_ventas(n_filas: int, semilla: int = 2026) -> pd.DataFrame:
    """Crea un DataFrame de ventas con ``n_filas`` registros y errores típicos.

    Args:
        n_filas: Número de facturas a generar antes de duplicar registros.
        semilla: Semilla del generador aleatorio, para que el resultado
            sea reproducible.

    Returns:
        DataFrame con las columnas que espera el proyecto.
    """
    rng = np.random.default_rng(semilla)
    catalogo = [(cat, prod) for cat, prods in PRODUCTOS.items()
                for prod in prods]
    precios = rng.uniform(0.6, 9.5, size=len(catalogo)).round(2)
    idx = rng.integers(0, len(catalogo), size=n_filas)

    df = pd.DataFrame({
        "id_factura": [f"F-{i:07d}" for i in range(1, n_filas + 1)],
        "fecha": pd.Timestamp("2026-01-01")
        + pd.to_timedelta(rng.integers(0, 304, size=n_filas), unit="D"),
        "producto": [catalogo[i][1] for i in idx],
        "categoria": [catalogo[i][0] for i in idx],
        "region": rng.choice(REGIONES, size=n_filas, p=[.45, .38, .12, .05]),
        "cantidad": rng.integers(1, 25, size=n_filas),
        "precio_unitario": precios[idx],
        "descuento": rng.choice([0, 0.05, 0.10, 0.15], size=n_filas),
    })

    # Errores típicos de los datos reales
    filas = rng.random(n_filas)
    df.loc[filas < 0.015, "descuento"] = np.nan
    df.loc[(filas >= 0.015) & (filas < 0.03), "cantidad"] *= -1
    variantes = rng.random(n_filas) < 0.10
    df.loc[variantes, "region"] = [
        rng.choice(VARIANTES_REGION[r]) for r in df.loc[variantes, "region"]
    ]
    duplicados = df.sample(frac=0.02, random_state=semilla)
    return pd.concat([df, duplicados]).sample(frac=1, random_state=semilla)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--filas", type=int, default=10_000)
    parser.add_argument("--salida", type=Path,
                        default=Path("data/raw/ventas.csv"))
    args = parser.parse_args()
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    generar_ventas(args.filas).to_csv(args.salida, index=False)
    print(f"Archivo generado: {args.salida}")
