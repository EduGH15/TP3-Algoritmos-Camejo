import sys
import csv
import os

RESERVA = "reservas.csv"

POSICiON_COMANDO = 1
POSICION_ID = 2

POSICION_NOMBRE = 3
POSICION_CANTIDAD_PERSONA = 4
POSICION_TIEMPO = 5
POSICION_UBICACION = 6

COMANDO_AGREGAR = "agregar"
COMANDO_MODIFICAR = "modificar"
COMANDO_ELIMINAR = "eliminar"
COMANDO_LISTAR = "listar"

CAMPO_ID = "id"
CAMPO_NOMBRE = "nombre"
CAMPO_CANTIDAD_PERSONAS = "cant_personas"
CAMPO_HORARIO = "horario"
CAMPO_UBICACION = "ubicacion"

def existe_id(id, nombre_archivo):
    existe = False
    archivo = open(nombre_archivo)
    lector = csv.reader(archivo, delimiter=";")
    reservas = list(lector)
    for i in range(len(reservas)):
        if reservas[i][0] == id:
            existe = True
    archivo.close()
    return existe

def imprimir_error_modificar(nombre_archivo):
    if len(sys.argv) != 3:
        print("El nro de argumentos ingresados es incorrecto. ingrese: <archivo> modificar id.")
    elif not(sys.argv[POSICION_ID].isnumeric()):
        print("El id debe ser un número.")
    elif not existe_id(sys.argv[POSICION_ID], nombre_archivo):
        print("No se puede modificar esta reserva porque no existe.")

def imprimir_error_eliminar(nombre_archivo):
    if len(sys.argv) != 3:
        print("El nro de argumentos ingresados es incorrecto. ingrese: <archivo> eliminar id.")
    elif not(sys.argv[POSICION_ID].isnumeric()):
        print("El id debe ser un número.")
    elif not existe_id(sys.argv[POSICION_ID], nombre_archivo):
        print("No se puede eliminar esta reserva porque no existe.")

def asignar_nuevo_formato(campo):
    if campo == CAMPO_ID:
        nuevo_formato = campo.upper()
    elif campo == CAMPO_CANTIDAD_PERSONAS:
        nuevo_formato = "Cantidad de personas"
    else:
        nuevo_formato = campo.capitalize()
    return nuevo_formato

def asignar_posicion(campo):
    if campo == CAMPO_NOMBRE:
        return 1
    elif campo == CAMPO_CANTIDAD_PERSONAS:
        return 2
    elif campo == CAMPO_HORARIO:
        return 3
    elif campo == CAMPO_UBICACION:
        return 4

def nuevo_id(nombre_archivo):
    archivo = open(nombre_archivo)
    lector = csv.reader(archivo, delimiter=";")
    reservas = list(lector)
    if len(reservas) > 1:
        id = reservas[len(reservas) - 1][0]
    else:
        id = "0"
    return str(int(id) + 1)
    archivo.close()
    
def agregar_reserva(argv, nombre_archivo):
    id = nuevo_id(nombre_archivo)
    nombre = argv[2]
    cantidad_personas = argv[3]
    tiempo = argv[4]
    ubicacion = argv[5]
    nueva_linea = [id, nombre, cantidad_personas, tiempo, ubicacion]

    try:
        archivo = open(nombre_archivo, "a")
    except:
        print("Error al abrir el archivo")
        return

    escritor = csv.writer(archivo, delimiter=";")
    escritor.writerow(nueva_linea)
    archivo.close()

def eliminar_reserva(argv, nombre_archivo):
    id = argv[POSICION_ID]

    try:
        archivo = open(nombre_archivo)
    except:
        print("Error al abrir el archivo")
        return
    
    try:
        archivo_auxiliar = open("datos_auxiliares.csv", "w")
    except:
        archivo.close()
        print("error al abrir el archivo auxiliar")
        return
    
    lector = csv.reader(archivo, delimiter=";")
    escritor = csv.writer(archivo_auxiliar, delimiter=";")
    for linea in lector:
        if linea[0] == id:
            continue
        escritor.writerow(linea)

    archivo.close()
    archivo_auxiliar.close()
    
    os.rename("datos_auxiliares.csv", nombre_archivo)

def modificar_reserva(argv, nuevos_datos, nombre_archivo):
    id = argv[POSICION_ID]
    lista_nuevos_datos = nuevos_datos.split()
    campo = lista_nuevos_datos[0]
    valor_campo = lista_nuevos_datos[1]
    posicion_campo_columna = asignar_posicion(campo)
    nueva_linea = []
    try:
        archivo = open(nombre_archivo)
    except:
        print("Error al abrir el archivo")
        return
    
    try:
        archivo_auxiliar = open("datos_auxiliares.csv", "a")
    except:
        archivo.close()
        print("error al abrir el archivo auxiliar")
        return

    lector = csv.reader(archivo, delimiter=";")
    escritor = csv.writer(archivo_auxiliar, delimiter=";")
    reservas = list(lector)

    for i in range(len(reservas)):
        nueva_linea = reservas[i].copy()
        for j in range(len(reservas[i])):
            if reservas[i][0] == id:
                nueva_linea[posicion_campo_columna] = valor_campo

        escritor.writerow(nueva_linea)

    archivo.close()
    archivo_auxiliar.close()
    
    os.rename("datos_auxiliares.csv", nombre_archivo)

def listar_reserva(argv, nombre_archivo):      
    try:
        archivo = open(nombre_archivo)
    except:
        print("Error al abrir el archivo")
        return
    
    lector = csv.reader(archivo, delimiter=";")
    reservas = list(lector)

    
    if len(sys.argv) == 2:
        for i in range(1, len(reservas)):
            for j in range(len(reservas[i])):
                print(f"{asignar_nuevo_formato(reservas[0][j])}: {reservas[i][j]}")
            print("\n")
    elif len(sys.argv) == 4:
        id_inicial = sys.argv[2]
        id_final = sys.argv[3]
        fila_inicial = -1
        fila_final = -1
        for i in range(1, len(reservas)):
            if id_inicial in reservas[i][0]:
                fila_inicial = i
            if id_final in reservas[i][0]:
                fila_final = i
        for i in range(fila_inicial, fila_final + 1):
            for j in range(len(reservas[i])):
                print(f"{asignar_nuevo_formato(reservas[0][j])}: {reservas[i][j]}")
            print("\n")


    archivo.close()

def main(): 
    if sys.argv[POSICiON_COMANDO] == COMANDO_AGREGAR:
        agregar_reserva(sys.argv, RESERVA)


    if sys.argv[POSICiON_COMANDO] == COMANDO_MODIFICAR and len(sys.argv) == 3 and sys.argv[POSICION_ID].isnumeric() and existe_id(sys.argv[POSICION_ID], RESERVA):
        datos = input("¿Qué desea cambiar?:")
        modificar_reserva(sys.argv, datos, RESERVA)
        print("Modificación exitosa.")
    elif sys.argv[POSICiON_COMANDO] == COMANDO_MODIFICAR:
        imprimir_error_modificar(RESERVA)
        return

    if sys.argv[POSICiON_COMANDO] == COMANDO_ELIMINAR and len(sys.argv) == 3 and sys.argv[POSICION_ID].isnumeric() and existe_id(sys.argv[POSICION_ID], RESERVA):
        eliminar_reserva(sys.argv, RESERVA)
    elif sys.argv[POSICiON_COMANDO] == COMANDO_ELIMINAR:
        imprimir_error_eliminar(RESERVA)
        return
    
    if sys.argv[POSICiON_COMANDO] == COMANDO_LISTAR:
        listar_reserva(sys.orig_argv, RESERVA)

if __name__ == "__main__":
    main()