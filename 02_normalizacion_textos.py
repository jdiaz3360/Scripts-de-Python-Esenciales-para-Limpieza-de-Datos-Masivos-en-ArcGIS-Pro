# ============================================================
# Script 2: Normalización de Textos (Mayúsculas Iniciales)
# Tema: 5 Scripts de Python para Limpiar Datos en ArcGIS Pro
# ArcGIS Pro 3.6 / ArcPy
# GeoTech con Josue
# ============================================================

import arcpy

# ============================================================
# CONFIGURACIÓN
# ============================================================

GDB_PATH = r"C:\Tutor\Limpieza_de_Datos\Demo_Automatizacion_Proyectada.gdb"

CAPA = "Vias"

CAMPO_TEXTO = "NOMBRE"


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def normalizar_textos(gdb_path, capa, campo_texto):

    arcpy.env.workspace = gdb_path

    if not arcpy.Exists(capa):
        print(f"No se encontró la capa: {capa}")
        return

    campos = [field.name for field in arcpy.ListFields(capa)]

    if campo_texto not in campos:
        print(f"No se encontró el campo: {campo_texto}")
        return

    print("========================================")
    print("NORMALIZANDO TEXTOS")
    print("========================================")

    print(f"Capa: {capa}")
    print(f"Campo: {campo_texto}")

    actualizados = 0

    with arcpy.da.UpdateCursor(capa, [campo_texto]) as cursor:

        for row in cursor:

            if row[0]:

                texto_original = row[0]

                texto_normalizado = texto_original.title()

                if texto_original != texto_normalizado:

                    row[0] = texto_normalizado

                    cursor.updateRow(row)

                    actualizados += 1

    print("========================================")
    print(f"Registros actualizados: {actualizados}")
    print("Normalización completada.")
    print("========================================")


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":

    normalizar_textos(
        GDB_PATH,
        CAPA,
        CAMPO_TEXTO
    )