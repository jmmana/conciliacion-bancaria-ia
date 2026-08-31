"""
Genera dos archivos Excel de ejemplo para demostrar la conciliacion bancaria
asistida por IA:

  - data/libro_contable.xlsx  -> lo que el area contable registro en sus libros
  - data/extracto_banco.xlsx  -> lo que el banco realmente reporta

Los datos son ficticios (empresa "Distribuidora El Roble SAS") pero estan
disenados a proposito para incluir los 4 casos que se encuentran en
cualquier conciliacion real:

  1) Movimientos que coinciden perfectamente          -> "Conciliado"
  2) Un cheque/transferencia registrado en libros que el banco aun no
     ha hecho efectivo                                -> "Pendiente en banco"
  3. Un valor mal digitado en libros (1.205.000 en vez de 1.250.000)
                                                        -> "Revisar diferencia"
  4) Movimientos propios del banco que nadie registro en libros
     (comision, rendimientos) y un cobro duplicado     -> "Pendiente en libros"
                                                           / "Posible duplicado"
"""

import pandas as pd

libro_contable = [
    ("2026-08-01", "Pago factura FE-1002 Cliente Almacenes Rio", 3_500_000),
    ("2026-08-01", "Pago nomina quincena", -8_200_000),
    ("2026-08-02", "Pago proveedor Distribuciones Andina", -2_150_000),
    ("2026-08-03", "Transferencia cliente Supermercado La 80", 1_875_000),
    ("2026-08-04", "Pago servicios publicos", -640_000),
    ("2026-08-05", "Pago factura FE-1010 Cliente Ferreteria Central", 2_300_000),
    ("2026-08-05", "Pago arriendo bodega", -3_000_000),
    ("2026-08-06", "Cheque proveedor Insumos del Valle #4521", -1_250_000),
    ("2026-08-07", "Pago proveedor Papeleria Nacional", -420_000),
    ("2026-08-08", "Transferencia cliente Comercial Rionegro", 1_205_000),  # <- typo, banco dice 1.250.000
    ("2026-08-09", "Pago factura FE-1015 Cliente Hogar y Deco", 980_000),
    ("2026-08-10", "Pago impuestos ICA", -560_000),
    ("2026-08-11", "Pago proveedor Textiles del Norte", -1_730_000),
    ("2026-08-12", "Transferencia cliente Mercados Unidos", 2_640_000),
    ("2026-08-13", "Pago mantenimiento vehiculos", -390_000),
    ("2026-08-14", "Pago factura FE-1022 Cliente Drogueria San Jose", 1_150_000),
    ("2026-08-15", "Pago nomina quincena", -8_350_000),
    ("2026-08-16", "Pago proveedor Suministros Andinos", -875_000),
]

extracto_banco = [
    ("2026-08-01", "TRANSF RECIBIDA ALMACENES RIO", 3_500_000),
    ("2026-08-01", "PAGO NOMINA QUINCENAL", -8_200_000),
    ("2026-08-02", "TRANSF ENVIADA DISTRIB ANDINA", -2_150_000),
    ("2026-08-03", "TRANSF RECIBIDA SUPERMERCADO LA 80", 1_875_000),
    ("2026-08-04", "COMISION MANEJO CUENTA", -35_000),          # <- no esta en libros
    ("2026-08-04", "PAGO SERVICIOS PUBLICOS", -640_000),
    ("2026-08-05", "TRANSF RECIBIDA FERRETERIA CENTRAL", 2_300_000),
    ("2026-08-05", "PAGO ARRIENDO BODEGA", -3_000_000),
    # El cheque #4521 a Insumos del Valle NO aparece todavia (aun no se hace efectivo)
    ("2026-08-07", "PAGO PROVEEDOR PAPELERIA NACIONAL", -420_000),
    ("2026-08-07", "PAGO PROVEEDOR PAPELERIA NACIONAL", -420_000),  # <- cobro duplicado del banco
    ("2026-08-08", "TRANSF RECIBIDA COMERCIAL RIONEGRO", 1_250_000),  # <- valor real (libros dice 1.205.000)
    ("2026-08-09", "TRANSF RECIBIDA HOGAR Y DECO", 980_000),
    ("2026-08-09", "RENDIMIENTOS FINANCIEROS", 4_200),          # <- no esta en libros
    ("2026-08-10", "PAGO IMPUESTOS ICA", -560_000),
    ("2026-08-11", "TRANSF ENVIADA TEXTILES DEL NORTE", -1_730_000),
    ("2026-08-12", "TRANSF RECIBIDA MERCADOS UNIDOS", 2_640_000),
    ("2026-08-13", "PAGO MANTENIMIENTO VEHICULOS", -390_000),
    ("2026-08-14", "TRANSF RECIBIDA DROGUERIA SAN JOSE", 1_150_000),
    ("2026-08-15", "PAGO NOMINA QUINCENAL", -8_350_000),
    ("2026-08-16", "TRANSF ENVIADA SUMINISTROS ANDINOS", -875_000),
]


def guardar(filas, columnas, ruta):
    df = pd.DataFrame(filas, columns=columnas)
    df.to_excel(ruta, index=False)
    print(f"Creado {ruta}  ({len(df)} filas)")


if __name__ == "__main__":
    guardar(libro_contable, ["Fecha", "Descripcion", "Valor"], "data/libro_contable.xlsx")
    guardar(extracto_banco, ["Fecha", "Descripcion", "Valor"], "data/extracto_banco.xlsx")
