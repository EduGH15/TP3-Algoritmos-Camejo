import sys
import csv
import os

RESERVA = "reservas.csv"

POSICiON_COMANDO = 1
POSICION_ID = 2

POSICION_NOMBRE = 2
POSICION_CANTIDAD_PERSONAS = 3
POSICION_HORARIO = 4
POSICION_UBICACION = 5

COMANDO_AGREGAR = "agregar"
COMANDO_MODIFICAR = "modificar"
COMANDO_ELIMINAR = "eliminar"
COMANDO_LISTAR = "listar"

CAMPO_ID = "id"
CAMPO_NOMBRE = "nombre"
CAMPO_CANTIDAD_PERSONAS = "cant"
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

def es_horario_valido(horario):
    es_valido = True
    lista_horario = list(horario)
    i = 0
    while(i < len(lista_horario) and es_valido):
        if len(lista_horario) != 5:
            es_valido = False
        elif i == 2 and lista_horario[i] != ":":
            es_valido = False
        elif i != 2 and not lista_horario[i].isnumeric():
            es_valido = False
        elif i == 0 and int(horario[i])>2:
            es_valido = False
        elif i == 0 and int(horario[i]) == 2 and int(horario[i + 1]) > 3:
            es_valido = False
        elif i == 3 and int(horario[i]) > 5:
            es_valido = False
        i+= 1

    return es_valido   

def es_ubicacion_valida(ubicacion):
    return ubicacion == "F" or ubicacion == "D"

def es_nombre_valido(nombre):
    return nombre.isalpha()

def es_cantidad_valida(cantidad):
    return (not cantidad.isalpha()) and int(cantidad) > 0

def imprimir_error_agregar(argumentos):
    if len(argumentos) != 6:
        print("La cantidad de argumentos ingresado es invalida. Ingrese: <archivo> agrega nombre cant_personas HH:MM ubicacion")
    elif not es_nombre_valido(argumentos[POSICION_NOMBRE]):
        print("el nombre ingresado no es válido. Ingrese un nombre sin números.")
    elif not es_cantidad_valida(argumentos[POSICION_CANTIDAD_PERSONAS]):
        print("La cantidad de personas ingresadas es inválida. Ingrese un número mayor a cero.")
    elif not es_horario_valido(argumentos[POSICION_HORARIO]):
        print("El horario es inválido. Ingrese un horario entre las 00:00 y las 23:59.")
    elif not es_ubicacion_valida(argumentos[POSICION_UBICACION]):
        print("La ubicación es inválida. Ingrese D o F.")

def imprimir_error_modificar(argumentos, nombre_archivo):
    if len(argumentos) != 3:
        print("El nro de argumentos ingresados es incorrecto. ingrese: <archivo> modificar id.")
    elif not(argumentos[POSICION_ID].isnumeric()):
        print("El id debe ser un número.")
    elif not existe_id(argumentos[POSICION_ID], nombre_archivo):
        print("No se puede modificar esta reserva porque no existe.")

def imprimir_error_eliminar(argumentos, nombre_archivo):
    if len(argumentos) != 3:
        print("El nro de argumentos ingresados es incorrecto. ingrese: <archivo> eliminar id.")
    elif not(argumentos[POSICION_ID].isnumeric()):
        print("El id debe ser un número.")
    elif not existe_id(argumentos[POSICION_ID], nombre_archivo):
        print("No se puede eliminar esta reserva porque no existe.")



def imprimir_error_listar(argumentos, nombre_archivo):
    if len(argumentos) == 3:
        print("El número de argumentos no es válido. Ingrese: <archivo> listar id_inicial id_final o <archivo> listar")
    elif not existe_id(argumentos[2], nombre_archivo) or not existe_id(argumentos[3], nombre_archivo):
        print("No se puede listar el archivo porque uno de los dos id no existe")
    elif argumentos[2] < argumentos[3]:
        print("El primer id debe ser mayor al segundo")


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
    
def agregar_reserva(argumentos, nombre_archivo):
    id = nuevo_id(nombre_archivo)
    nueva_linea = [id, argumentos[POSICION_NOMBRE], argumentos[POSICION_CANTIDAD_PERSONAS], argumentos[POSICION_HORARIO], argumentos[POSICION_UBICACION]]
    
    try:
        archivo = open(nombre_archivo, "a")
    except:
        print("Error al abrir el archivo")
        return

    escritor = csv.writer(archivo, delimiter=";")
    escritor.writerow(nueva_linea)
    archivo.close()

def eliminar_reserva(argumentos, nombre_archivo):
    id = argumentos[POSICION_ID]

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

def modificar_reserva(argumentos, lista_datos, nombre_archivo):
    id = argumentos[POSICION_ID]
    #lista_nuevos_datos = nuevos_datos.split()
    campo = lista_datos[0]
    valor_campo = lista_datos[1]
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

def listar_reserva(argumentos, nombre_archivo):      
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
    argumentos = sys.argv.copy()
     
    if argumentos[POSICiON_COMANDO] == COMANDO_AGREGAR and len(argumentos) == 6 and es_nombre_valido(argumentos[POSICION_NOMBRE]) and es_cantidad_valida(argumentos[POSICION_CANTIDAD_PERSONAS]) and es_horario_valido(argumentos[POSICION_HORARIO]) and es_ubicacion_valida(argumentos[POSICION_UBICACION]):
        agregar_reserva(argumentos, RESERVA)
        print("Se agregó con exito")
    elif argumentos[POSICiON_COMANDO] == COMANDO_AGREGAR:
        imprimir_error_agregar(argumentos)
        return
    
    if argumentos[POSICiON_COMANDO] == COMANDO_MODIFICAR and len(argumentos) == 3 and argumentos[POSICION_ID].isnumeric() and existe_id(argumentos[POSICION_ID], RESERVA):
        datos = input("¿Qué desea cambiar?:")
        lista_datos = datos.split()
        if len(lista_datos) == 2 and ((lista_datos[0] == CAMPO_NOMBRE and es_nombre_valido(lista_datos[1])) or (lista_datos[0] == CAMPO_CANTIDAD_PERSONAS and es_cantidad_valida(lista_datos[1])) or (lista_datos[0] == CAMPO_HORARIO and es_horario_valido(lista_datos[1])) or (lista_datos[0] == CAMPO_UBICACION and es_ubicacion_valida(lista_datos[1]))):
            modificar_reserva(sys.argv, lista_datos, RESERVA)
            print("Modificación exitosa.")
    elif sys.argv[POSICiON_COMANDO] == COMANDO_MODIFICAR:
        imprimir_error_modificar(argumentos, RESERVA)
        return
    
    if argumentos[POSICiON_COMANDO] == COMANDO_ELIMINAR and len(argumentos) == 3 and argumentos[POSICION_ID].isnumeric() and existe_id(argumentos[POSICION_ID], RESERVA):
        eliminar_reserva(argumentos, RESERVA)
        print("Se eliminó con éxito")
    elif argumentos[POSICiON_COMANDO] == COMANDO_ELIMINAR:
        imprimir_error_eliminar(argumentos, RESERVA)
        return
    
    """
    if (argumentos[POSICiON_COMANDO] == COMANDO_LISTAR and len(argumentos) == 2) or (argumentos[POSICiON_COMANDO] == COMANDO_LISTAR and len(argumentos) == 4 and (existe_id(argumentos[2], RESERVA) and existe_id(argumentos[3], RESERVA)) and (argumentos[2] > argumentos[3])):
        listar_reserva(argumentos, RESERVA)
    elif argumentos[POSICiON_COMANDO] == COMANDO_LISTAR:
        imprimir_error_listar(RESERVA)
        return
    """

if __name__ == "__main__":
    main()