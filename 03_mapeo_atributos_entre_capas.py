# ============================================================
# Script 3: Mapeo de Atributos entre Capas
# Tema: 5 Scripts de Python para Limpiar Datos en ArcGIS Pro
# ArcGIS Pro 3.6 / ArcPy
# GeoTech con Josue
# ============================================================

import arcpy

# ============================================================
# CONFIGURACIÓN
# ============================================================

GDB_PATH = r"C:\Tutor\Limpieza_de_Datos\Demo_Automatizacion_Proyectada.gdb"

CAPA_ORIGEN = "LOCALIZACIONES"
CAPA_DESTINO = "LOCALIZACIONES_NUEVAS"

CAMPO_ID = "ID_LOC"

CAMPOS_MAP = {
    "NOM_MUN": "NOM_MUN",
    "DM_MUN": "DM_MUN",
    "NOMBRE_DEV": "NOMBRE_DEV",
    "NOMBRE": "NOMBRE"
}


# ============================================================
# FUNCIÓN PARA DETECTAR VALORES VACÍOS
# ============================================================

def es_valor_vacio(valor):
    """
    Detecta valores vacíos:
    - None
    - texto vacío
    - NULL
    - <NULL>
    - <Null>
    """

    if valor is None:
        return True

    if isinstance(valor, str):
        valor_limpio = valor.strip().upper()

        if valor_limpio in ["", "NULL", "<NULL>"]:
            return True

    return False


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def mapear_atributos():

    arcpy.env.workspace = GDB_PATH

    # ==========================================
    # Crear diccionario desde capa origen
    # ==========================================

    datos_origen = {}

    campos_origen = [CAMPO_ID] + list(CAMPOS_MAP.keys())

    with arcpy.da.SearchCursor(CAPA_ORIGEN, campos_origen) as cursor:

        for row in cursor:
            datos_origen[row[0]] = row[1:]

    print(f"Datos cargados desde capa origen: {len(datos_origen)} registros")

    # ==========================================
    # Actualizar capa destino
    # ==========================================

    campos_destino = [CAMPO_ID] + list(CAMPOS_MAP.values())

    actualizados = 0

    with arcpy.da.UpdateCursor(CAPA_DESTINO, campos_destino) as cursor:

        for row in cursor:

            id_loc = row[0]

            if id_loc in datos_origen:

                valores_origen = datos_origen[id_loc]
                cambio = False

                for i in range(len(valores_origen)):

                    valor_destino = row[i + 1]

                    # Solo actualiza si el campo destino está vacío
                    if es_valor_vacio(valor_destino):

                        row[i + 1] = valores_origen[i]
                        cambio = True

                # Solo guarda la fila si hubo cambios
                if cambio:

                    cursor.updateRow(row)
                    actualizados += 1

    print(f"Registros actualizados: {actualizados}")
    print("Migración completada.")


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":

    mapear_atributos()