import sys
import csv
import os

RESERVA = "reservas.csv"

CANTIDAD_ARGUMENTOS_AGREGAR = 6
CANTIDAD_ARGUMENTOS_MODIFICAR = 3
CANTIDAD_ARGUMENTOS_ELIMINAR = 3
CANTIDAD_ARGUMENTOS_MINIMA_LISTAR = 2
CANTIDAD_ARGUMENTOS_MAXIMA_LISTAR = 4
CANTIDAD_ARGUMENTOS_MODIFICAR_CAMPO = 2

POSICiON_COMANDO = 1
POSICION_ID = 2
POSICION_NOMBRE = 2
POSICION_CANTIDAD_PERSONAS = 3
POSICION_HORARIO = 4
POSICION_UBICACION = 5
POSICION_ID_INICIAL = 2
POSICION_ID_FINAL = 3

POSICION_CAMPO = 0
POSICION_NUEVO_VALOR_CAMPO = 1
POSICION_CAMPO_NOMBRE = 1
POSICION_CAMPO_CANTIDAD_PERSONAS = 2
POSICION_CAMPO_HORARIO = 3
POSICION_CAMPO_UBICACION = 4
POSICION_NO_ENCONTRADA = -1

COMANDO_AGREGAR = "agregar"
COMANDO_MODIFICAR = "modificar"
COMANDO_ELIMINAR = "eliminar"
COMANDO_LISTAR = "listar"

CAMPO_ID = "id"
CAMPO_NOMBRE = "nombre"
CAMPO_CANTIDAD_PERSONAS = "cant"
CAMPO_HORARIO = "hora"
CAMPO_UBICACION = "ubicacion"

LONGITUD_CAMPO_HORARIO = 5
DIVISION_HORARIA = ":"
UBICACION_AFUERA = "F"
UBICACION_ADENTRO = "D"

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
        if len(lista_horario) != LONGITUD_CAMPO_HORARIO:
            es_valido = False
        elif i == 2 and lista_horario[i] != DIVISION_HORARIA:
            es_valido = False
        elif i != 2 and not lista_horario[i].isnumeric():
            es_valido = False
        elif i == 0 and int(horario[i]) > 2:
            es_valido = False
        elif i == 0 and int(horario[i]) == 2 and int(horario[i + 1]) > 3:
            es_valido = False
        elif i == 3 and int(horario[i]) > 5:
            es_valido = False
        i+= 1

    return es_valido   

def es_ubicacion_valida(ubicacion):
    return ubicacion == UBICACION_AFUERA or ubicacion == UBICACION_ADENTRO

def es_nombre_valido(nombre):
    return nombre.isalpha()

def es_cantidad_valida(cantidad):
    return cantidad.isnumeric() and int(cantidad) > 0

def es_comando_valido(comando):
    return comando == COMANDO_AGREGAR or comando == COMANDO_MODIFICAR or comando == COMANDO_ELIMINAR or comando == COMANDO_LISTAR

def imprimir_error_agregar(argumentos):
    if len(argumentos) != CANTIDAD_ARGUMENTOS_AGREGAR:
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
    if len(argumentos) != CANTIDAD_ARGUMENTOS_MODIFICAR:
        print("El nro de argumentos ingresados es incorrecto.")
    elif not(argumentos[POSICION_ID].isnumeric()):
        print("El id debe ser un número.")
    elif not existe_id(argumentos[POSICION_ID], nombre_archivo):
        print("No se puede acceder a esta reserva porque no existe.")

def imprimir_error_eliminar(argumentos, nombre_archivo):
    imprimir_error_modificar(argumentos, nombre_archivo)

def imprimir_error_listar(argumentos, nombre_archivo):
    if len(argumentos) != CANTIDAD_ARGUMENTOS_MINIMA_LISTAR and len(argumentos) != CANTIDAD_ARGUMENTOS_MAXIMA_LISTAR:
        print("El número de argumentos no es válido. Ingrese: <archivo> listar id_inicial id_final o <archivo> listar")
    elif len(argumentos) == CANTIDAD_ARGUMENTOS_MAXIMA_LISTAR and (not existe_id(argumentos[POSICION_ID_INICIAL], nombre_archivo) or not existe_id(argumentos[POSICION_ID_FINAL], nombre_archivo)):
        print("No se puede listar el archivo porque uno de los dos id no existe")
    elif len(argumentos) == CANTIDAD_ARGUMENTOS_MAXIMA_LISTAR and int(argumentos[POSICION_ID_INICIAL]) > int(argumentos[POSICION_ID_FINAL]):
        print("El primer id debe ser menor al segundo")

def imprimir_error_modificar_campo(lista_datos):
    if lista_datos[POSICION_CAMPO] == CAMPO_NOMBRE and not es_nombre_valido(lista_datos[POSICION_NUEVO_VALOR_CAMPO]):
        print("El nombre no debe contener números")
    elif lista_datos[POSICION_CAMPO] == CAMPO_CANTIDAD_PERSONAS and not es_cantidad_valida(lista_datos[POSICION_NUEVO_VALOR_CAMPO]):
        print("La cantidad de personas debe ser mayor a cero.")
    elif lista_datos[POSICION_CAMPO] == CAMPO_HORARIO and not es_horario_valido(lista_datos[POSICION_NUEVO_VALOR_CAMPO]):
        print("El horario debe ser entre las 00:00 y las 23:59.")
    elif lista_datos[POSICION_CAMPO] == CAMPO_UBICACION and not es_ubicacion_valida(lista_datos[POSICION_NUEVO_VALOR_CAMPO]):
        print("La ubicación debe ser válida (D o F).")
    else:
        print("Los campo que desea cambiar es inválido")

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
        return POSICION_CAMPO_NOMBRE
    elif campo == CAMPO_CANTIDAD_PERSONAS:
        return POSICION_CAMPO_CANTIDAD_PERSONAS
    elif campo == CAMPO_HORARIO:
        return POSICION_CAMPO_HORARIO
    elif campo == CAMPO_UBICACION:
        return POSICION_CAMPO_UBICACION

def nuevo_id(nombre_archivo):
    archivo = open(nombre_archivo)
    lector = csv.reader(archivo, delimiter=";")
    reservas = list(lector)
    if len(reservas) > 1:
        id = reservas[len(reservas) - 1][0]
    else:
        id = "0"
    archivo.close()
    return str(int(id) + 1)
        
def agregar_reserva_archivo(argumentos, nombre_archivo):
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

def eliminar_reserva_archivo(argumentos, nombre_archivo):
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

def modificar_reserva_archivo(argumentos, lista_datos, nombre_archivo):
    id = argumentos[POSICION_ID]
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

def listar_reserva_archivo(argumentos, nombre_archivo):      
    try:
        archivo = open(nombre_archivo)
    except:
        print("Error al abrir el archivo")
        return
    
    lector = csv.reader(archivo, delimiter=";")
    reservas = list(lector)

    
    if len(argumentos) == CANTIDAD_ARGUMENTOS_MINIMA_LISTAR:
        for i in range(1, len(reservas)):
            for j in range(len(reservas[i])):
                print(f"{asignar_nuevo_formato(reservas[0][j])}: {reservas[i][j]}")
            print("\n")
    elif len(argumentos) == CANTIDAD_ARGUMENTOS_MAXIMA_LISTAR:
        id_inicial = argumentos[2]
        id_final = argumentos[3]
        fila_inicial = POSICION_NO_ENCONTRADA
        fila_final = POSICION_NO_ENCONTRADA
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

def realizar_reserva(argumentos):
    if argumentos[POSICiON_COMANDO] == COMANDO_AGREGAR and len(argumentos) == CANTIDAD_ARGUMENTOS_AGREGAR and es_nombre_valido(argumentos[POSICION_NOMBRE]) and es_cantidad_valida(argumentos[POSICION_CANTIDAD_PERSONAS]) and es_horario_valido(argumentos[POSICION_HORARIO]) and es_ubicacion_valida(argumentos[POSICION_UBICACION]):
        agregar_reserva_archivo(argumentos, RESERVA)
        print("Se agregó con exito")
    elif argumentos[POSICiON_COMANDO] == COMANDO_AGREGAR:
        imprimir_error_agregar(argumentos)
        return

def cambiar_reserva(argumentos):
    if argumentos[POSICiON_COMANDO] == COMANDO_MODIFICAR and len(argumentos) == CANTIDAD_ARGUMENTOS_MODIFICAR and argumentos[POSICION_ID].isnumeric() and existe_id(argumentos[POSICION_ID], RESERVA):
        datos = input("¿Qué desea cambiar?:")
        lista_datos = datos.split()
        if len(lista_datos) == CANTIDAD_ARGUMENTOS_MODIFICAR_CAMPO and ((lista_datos[POSICION_CAMPO] == CAMPO_NOMBRE and es_nombre_valido(lista_datos[POSICION_NUEVO_VALOR_CAMPO])) or (lista_datos[POSICION_CAMPO] == CAMPO_CANTIDAD_PERSONAS and es_cantidad_valida(lista_datos[POSICION_NUEVO_VALOR_CAMPO])) or (lista_datos[POSICION_CAMPO] == CAMPO_HORARIO and es_horario_valido(lista_datos[POSICION_NUEVO_VALOR_CAMPO])) or (lista_datos[POSICION_CAMPO] == CAMPO_UBICACION and es_ubicacion_valida(lista_datos[POSICION_NUEVO_VALOR_CAMPO]))):
            modificar_reserva_archivo(sys.argv, lista_datos, RESERVA)
            print("Modificación exitosa.")
        else:
            imprimir_error_modificar_campo(lista_datos)
            return
    elif argumentos[POSICiON_COMANDO] == COMANDO_MODIFICAR:
        imprimir_error_modificar(argumentos, RESERVA)
        return

def cancelar_reserva(argumentos):
    if argumentos[POSICiON_COMANDO] == COMANDO_ELIMINAR and len(argumentos) == CANTIDAD_ARGUMENTOS_ELIMINAR and argumentos[POSICION_ID].isnumeric() and existe_id(argumentos[POSICION_ID], RESERVA):
        eliminar_reserva_archivo(argumentos, RESERVA)
        print("Se eliminó con éxito")
    elif argumentos[POSICiON_COMANDO] == COMANDO_ELIMINAR:
        imprimir_error_eliminar(argumentos, RESERVA)
        return 

def mostrar_reservas(argumentos):
    if (argumentos[POSICiON_COMANDO] == COMANDO_LISTAR and len(argumentos) == CANTIDAD_ARGUMENTOS_MINIMA_LISTAR or (len(argumentos) == CANTIDAD_ARGUMENTOS_MAXIMA_LISTAR) and (existe_id(argumentos[POSICION_ID_INICIAL], RESERVA) and existe_id(argumentos[POSICION_ID_FINAL], RESERVA)) and (argumentos[POSICION_ID_INICIAL] < argumentos[POSICION_ID_FINAL])):
        listar_reserva_archivo(argumentos, RESERVA)
    elif argumentos[POSICiON_COMANDO] == COMANDO_LISTAR:
        imprimir_error_listar(argumentos, RESERVA)
        return

def main():
    argumentos = sys.argv.copy()
    if len(argumentos) == 1:
        print("Cantidad de argumentos insuficientes.")
        return

    if not es_comando_valido(argumentos[POSICiON_COMANDO]):
        print(f"{argumentos[POSICiON_COMANDO]} no es un comando válido.")
        return
     
    realizar_reserva(argumentos)
    cambiar_reserva(argumentos)
    cancelar_reserva(argumentos)
    mostrar_reservas(argumentos)
    
if __name__ == "__main__":
    main()