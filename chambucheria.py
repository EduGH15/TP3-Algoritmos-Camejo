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

def asignar_posicion(campo):
    if campo == "nombre":
        return 1
    elif campo == "cant_personas":
        return 2
    elif campo == "tiempo":
        return 3
    elif campo == "ubicacion":
        return 4

def nuevo_id(nombre_archivo):
    archivo = open(nombre_archivo)
    lector = csv.reader(archivo, delimiter=";")
    reservas = list(lector)
    id = reservas[len(reservas) - 1][0]
    return str(int(id) + 1)
    
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
    #posicion_campo_fila = 0
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
            

def main(): 
    if sys.argv[POSICiON_COMANDO] == COMANDO_AGREGAR:
        agregar_reserva(sys.argv, RESERVA)


    if sys.argv[POSICiON_COMANDO] == COMANDO_MODIFICAR and sys.argv[POSICION_ID].isnumeric():
        datos = input("¿Qué desea cambiar?:")
        modificar_reserva(sys.argv, datos, RESERVA)


    if sys.argv[POSICiON_COMANDO] == COMANDO_ELIMINAR and sys.argv[POSICION_ID].isnumeric():
        eliminar_reserva(sys.argv, RESERVA)

if __name__ == "__main__":
    main()