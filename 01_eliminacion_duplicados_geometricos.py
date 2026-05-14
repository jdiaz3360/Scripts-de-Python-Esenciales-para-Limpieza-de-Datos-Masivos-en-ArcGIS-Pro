# ============================================================
# Script 1: Eliminación de Duplicados Geométricos
# Tema: 5 Scripts de Python para Limpiar Datos en ArcGIS Pro
# ArcGIS Pro 3.6 / ArcPy
# GeoTech con Josue
# ============================================================

import arcpy

GDB_PATH = r"C:\Tutor\Automatizacion_ArcGISPro\Demo_Automatizacion.gdb"
CAPA = "Edificaciones"

def eliminar_duplicados_geometricos(gdb_path, capa):
    """
    Elimina entidades duplicadas usando la geometría como criterio.
    Si dos entidades tienen exactamente la misma geometría, una se conserva
    y las demás se eliminan.
    """
    arcpy.env.workspace = gdb_path

    if not arcpy.Exists(capa):
        print(f"No se encontró la capa: {capa}")
        return

    print(f"Analizando duplicados geométricos en: {capa}")

    arcpy.management.DeleteIdentical(
        in_dataset=capa,
        fields=["Shape"]
    )

    print("Duplicados geométricos eliminados.")

if __name__ == "__main__":
    eliminar_duplicados_geometricos(GDB_PATH, CAPA)
