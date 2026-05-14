# ============================================================
# Script 5: Validación de Dominios de Geodatabase
# Tema: 5 Scripts de Python para Limpiar Datos en ArcGIS Pro
# ArcGIS Pro 3.6 / ArcPy
# GeoTech con Josue
# ============================================================

import arcpy

# ============================================================
# CONFIGURACIÓN
# ============================================================

GDB_PATH = r"C:\Tutor\Limpieza_de_Datos\Demo_Automatizacion_Proyectada.gdb"

NOMBRE_DOMINIO = "Estado_Revision_DOM"

CAPA = "DIVISIONES"

CAMPO_VALIDAR = "Estado_Revision"


# ============================================================
# FUNCIÓN: LISTAR VALORES DEL DOMINIO
# ============================================================

def listar_valores_dominio(gdb_path, nombre_dominio):
    """
    Lista los valores válidos de un dominio codificado dentro de una geodatabase.
    """

    dominios = arcpy.da.ListDomains(gdb_path)

    for dominio in dominios:

        if dominio.name == nombre_dominio:

            print("========================================")
            print(f"Dominio encontrado: {dominio.name}")
            print("Valores válidos:")
            print("========================================")

            if dominio.domainType == "CodedValue":

                for codigo, descripcion in dominio.codedValues.items():
                    print(f"{codigo} -> {descripcion}")

                return dominio.codedValues

            print("El dominio encontrado no es de tipo CodedValue.")
            return None

    print(f"No se encontró el dominio: {nombre_dominio}")
    return None


# ============================================================
# FUNCIÓN: VALIDAR CAMPO CONTRA DOMINIO
# ============================================================

def validar_campo_contra_dominio(gdb_path, capa, campo_validar, nombre_dominio):
    """
    Valida si los valores de un campo están dentro de los valores permitidos
    por un dominio de geodatabase.
    """

    arcpy.env.workspace = gdb_path

    valores_validos = listar_valores_dominio(gdb_path, nombre_dominio)

    if not valores_validos:
        return

    if not arcpy.Exists(capa):
        print(f"No se encontró la capa: {capa}")
        return

    campos = [field.name for field in arcpy.ListFields(capa)]

    if campo_validar not in campos:
        print(f"No se encontró el campo: {campo_validar}")
        return

    # Como en la tabla se muestran las descripciones:
    # Aprobado, Revisar, Pendiente
    # validamos contra las descripciones del dominio.
    descripciones_validas = set(valores_validos.values())

    print("========================================")
    print(f"Validando campo: {campo_validar}")
    print(f"Capa: {capa}")
    print("========================================")

    errores = 0

    with arcpy.da.SearchCursor(capa, ["OID@", campo_validar]) as cursor:

        for oid, valor in cursor:

            if valor not in descripciones_validas:

                print(f"Valor fuera de dominio | OBJECTID: {oid} | Valor: {valor}")
                errores += 1

    print("========================================")

    if errores == 0:
        print("Todos los valores cumplen con el dominio.")
    else:
        print(f"Total de valores fuera de dominio: {errores}")

    print("Proceso de validación completado.")
    print("========================================")


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":

    validar_campo_contra_dominio(
        GDB_PATH,
        CAPA,
        CAMPO_VALIDAR,
        NOMBRE_DOMINIO
    )