# Conciliación bancaria asistida (demo)

Script de ejemplo que compara un **libro contable** contra un **extracto
bancario** (dos archivos Excel) y clasifica cada movimiento automáticamente,
en lugar de cruzarlos fila por fila a mano.

Este repo acompaña el post *"Cómo la IA le ahorra horas a tu área contable:
conciliación bancaria automática"*. Los datos son ficticios (empresa
"Distribuidora El Roble SAS") pero están diseñados para mostrar los 4 casos
que aparecen en cualquier conciliación real.

## Qué hace

`conciliar.py` lee `data/libro_contable.xlsx` y `data/extracto_banco.xlsx`,
y para cada movimiento decide uno de estos 5 estados comparando **fecha +
valor + descripción**:

| Estado | Significado |
|---|---|
| 🟢 Conciliado | El movimiento existe en ambos lados |
| 🟡 Pendiente en banco | Está en libros, el banco aún no lo refleja (ej. cheque no cobrado) |
| 🟠 Pendiente en libros | Está en el banco, nadie lo registró (ej. comisión, rendimientos) |
| 🔴 Revisar diferencia | Mismo movimiento pero con un valor distinto (posible error de digitación) |
| 🔴 Posible duplicado | El banco cobró/registró el mismo movimiento dos veces |

El resultado se exporta a `output/conciliacion_resultado.xlsx` con cada fila
coloreada según su estado, listo para revisar en Excel.

## Cómo correrlo

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python3 generar_datos_ejemplo.py   # crea los Excel de ejemplo en data/
python3 conciliar.py               # genera output/conciliacion_resultado.xlsx
python3 generar_imagenes_post.py   # (opcional) genera las imágenes del post
```

## Cómo funciona el emparejamiento

No usa ningún servicio externo ni API de pago: compara fecha (con una
tolerancia de ±3 días), valor (exacto, o "parecido" dentro de un margen para
detectar errores de digitación) y similitud de texto en la descripción con
`difflib` de la librería estándar de Python.

Es exactamente la misma idea que usan por debajo las herramientas de
conciliación "con IA": si en vez de `difflib` le conectas un modelo de
lenguaje (Claude, GPT, etc.) para comparar las descripciones, el
emparejamiento mejora porque el modelo entiende sinónimos, abreviaturas de
bancos y variaciones de redacción que una comparación de texto literal no
capta.

## Adaptarlo a tus datos reales

1. Reemplaza los archivos en `data/` por tu propio extracto y libro
   contable, respetando las columnas `Fecha`, `Descripcion`, `Valor`.
2. Ajusta las constantes al inicio de `conciliar.py`
   (`FECHA_TOLERANCIA_DIAS`, `VALOR_TOLERANCIA_RELATIVA`) según qué tan
   estricta quieres la coincidencia.
3. Corre `python3 conciliar.py`.

**Nota de privacidad:** si vas a usar datos reales de tu empresa, no subas
el extracto bancario a herramientas de IA públicas sin verificar sus
políticas de datos. Este script corre 100% local, sin enviar información a
ningún servidor.

## Licencia

MIT. Úsalo, adáptalo y compártelo libremente.
