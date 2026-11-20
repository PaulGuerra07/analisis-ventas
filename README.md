# Análisis de Ventas

Programa en Python que lee el registro de ventas de la empresa, corrige
los datos inconsistentes y genera un reporte con el total vendido, las
ventas por región, los productos más vendidos y la evolución mensual.

Es la versión refactorizada del script `ventas.py` original, que
recorría el archivo fila por fila, repetía código por cada región y
devolvía `TOTAL: nan` cuando un descuento venía vacío.

## Características

- Limpieza automática: facturas duplicadas, descuentos vacíos,
  devoluciones y regiones escritas de distintas formas.
- Cálculos vectorizados con pandas (unas 150 veces más rápido que la
  versión original con 10 000 facturas).
- Lectura por bloques para archivos que no caben en memoria.
- 31 pruebas automáticas con 96 % de cobertura.

## Requisitos

- Python 3.10 o superior
- pandas y NumPy (se instalan con el paso siguiente)

## Instalación

```bash
git clone https://github.com/PaulGuerra07/analisis-ventas.git
cd analisis-ventas
python -m venv .venv
source .venv/bin/activate        # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Uso

```bash
# Generar los datos de ejemplo (data/raw/ventas.csv)
python scripts/generar_datos.py --filas 10000

# Ejecutar el análisis
python main.py --datos data/raw/ventas.csv --salida reports

# Ver mensajes de depuración
python main.py -v
```

Salida esperada:

```text
Total vendido: $579,507.82
  Sierra         $262,566.79
  Costa          $220,625.75
  Amazonía        $66,397.64
  Insular         $29,917.64
```

El reporte completo se guarda en `reports/reporte_ventas.json`.

## Formato del archivo de entrada

| Columna           | Tipo   | Ejemplo      |
|-------------------|--------|--------------|
| `id_factura`      | texto  | F-0000125    |
| `fecha`           | fecha  | 2026-03-14   |
| `producto`        | texto  | Arroz 2 kg   |
| `categoria`       | texto  | Abarrotes    |
| `region`          | texto  | Sierra       |
| `cantidad`        | entero | 12           |
| `precio_unitario` | real   | 2.35         |
| `descuento`       | real   | 0.10         |

## Estructura del proyecto

```text
ventas/       paquete con los módulos (carga, limpieza, métricas, reportes)
tests/        pruebas unitarias, de integración, funcionales y de regresión
scripts/      utilidades: generar datos y medir rendimiento
main.py       punto de entrada
```

## Pruebas

```bash
pytest --cov=ventas      # pruebas y cobertura
ruff check .             # estilo PEP 8 y docstrings PEP 257
```


## Contribución

1. Crea una rama desde `develop`: `git checkout -b feature/nombre`.
2. Escribe o actualiza las pruebas de tu cambio.
3. Verifica que `pytest` y `ruff check .` pasen sin errores.
4. Abre un pull request describiendo qué cambiaste y por qué.

## Licencia

Distribuido bajo la licencia MIT.

## Autor

Paúl Andrés Guerra Vicuña — Ingeniería en Ciencia de Datos e
Inteligencia Artificial, UNACH.
