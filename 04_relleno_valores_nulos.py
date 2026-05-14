# ============================================================
# Script 4: Relleno Masivo de Valores Nulos
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

CAMPO = "Estado_Via"

VALOR_RELLENO = "No Evaluado"

# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def rellenar_valores_nulos(gdb_path, capa, campo, valor_relleno):

    arcpy.env.workspace = gdb_path

    # Verificar si la capa existe
    if not arcpy.Exists(capa):
        print(f"No se encontró la capa: {capa}")
        return

    # Verificar si el campo existe
    campos = [field.name for field in arcpy.ListFields(capa)]

    if campo not in campos:
        print(f"No se encontró el campo: {campo}")
        return

    print("========================================")
    print("INICIANDO RELLENO DE VALORES NULOS")
    print("========================================")

    print(f"Capa: {capa}")
    print(f"Campo: {campo}")
    print(f"Valor de reemplazo: {valor_relleno}")

    corregidos = 0

    # ========================================================
    # RECORRER Y ACTUALIZAR REGISTROS
    # ========================================================

    with arcpy.da.UpdateCursor(capa, [campo]) as cursor:

        for row in cursor:

            # Detectar valores NULL
            if row[0] is None:

                # Reemplazar valor
                row[0] = valor_relleno

                # Guardar cambios
                cursor.updateRow(row)

                corregidos += 1

    print("========================================")
    print(f"Valores nulos corregidos: {corregidos}")
    print("Proceso completado correctamente.")
    print("========================================")


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":

    rellenar_valores_nulos(
        GDB_PATH,
        CAPA,
        CAMPO,
        VALOR_RELLENO
    )