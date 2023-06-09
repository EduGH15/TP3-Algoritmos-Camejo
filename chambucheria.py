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
    
    lista_datos = nuevos_datos.split()
    try:
        archivo = open(nombre_archivo)
    except:
        print("Error al abrir el archivo")
        return
    
    try:
        archivo_auxiliar = open("datos_auxiliares.txt", "a")
    except:
        archivo.close()
        print("error al abrir el archivo auxiliar")
        return

    lector = csv.reader(archivo, delimiter = ";")
    for fila in lector:
        if fila[0] == id:
            print("hola")
            
    """
    for fila in lector:
        print(fila[0])
    """

    """
    escritor = csv.reader(archivo_auxiliar, delimiter=";")
    for lineas in lector:
        if id in lineas:
            escritor.writerow(lista_datos)
            
    """

    archivo.close()
    archivo_auxiliar.close()
    

def main(): 
    """
    if sys.argv[POSICiON_COMANDO] == COMANDO_MODIFICAR and sys.argv[POSICION_ID].isnumeric():
        datos = input("¿Qué desea cambiar?:")
        modificar_reserva(sys.argv, datos, RESERVA)
    """

    if sys.argv[POSICiON_COMANDO] == COMANDO_ELIMINAR and sys.argv[POSICION_ID].isnumeric():
        eliminar_reserva(sys.argv, RESERVA)

if __name__ == "__main__":
    main()