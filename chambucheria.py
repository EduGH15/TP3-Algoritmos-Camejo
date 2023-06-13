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
POSICION_CAMPO_ID = 0

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
SIN_RESERVAS = 0
DIVISION_HORARIA = ":"
UBICACION_AFUERA = "F"
UBICACION_ADENTRO = "D"

def id_fuera_rango(id, nombre_archivo):
    esta_fuera_rango = False
    archivo = open(nombre_archivo)
    lector = csv.reader(archivo, delimiter=";")
    reservas = list(lector)
    for i in range(len(reservas)):
        if reservas[len(reservas) - 1][0] < id:
            esta_fuera_rango = True
    archivo.close()
    return esta_fuera_rango

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
    return not nombre.isnumeric()

def es_cantidad_valida(cantidad):
    return cantidad.isnumeric() and int(cantidad) > 0

def es_comando_valido(comando):
    return comando == COMANDO_AGREGAR or comando == COMANDO_MODIFICAR or comando == COMANDO_ELIMINAR or comando == COMANDO_LISTAR


def imprimir_error_agregar(nombre, cantidad_personas, hora, ubicacion):
    if not es_nombre_valido(nombre):
        print("El nombre ingresado no puede ser un número.")
    elif not es_cantidad_valida(cantidad_personas):
        print("La cantidad de personas ingresadas es inválida. Ingrese un número mayor a cero.")
    elif not es_horario_valido(hora):
        print("El horario es inválido. Ingrese un horario entre las 00:00 y las 23:59.")
    elif not es_ubicacion_valida(ubicacion):
        print("La ubicación es inválida. Ingrese D o F.")

def imprimir_error_modificar(id, nombre_archivo):
    if not id.isnumeric():
        print("El id debe ser un número.")
    elif not existe_id(id, nombre_archivo):
        print("No se puede acceder a esta reserva porque no existe.")

def imprimir_error_eliminar(id, nombre_archivo):
    imprimir_error_modificar(id, nombre_archivo)

def imprimir_error_listar(id_inicial, id_final, nombre_archivo):
    if not id_inicial.isnumeric() or not id_final.isnumeric():
        print("Ambos id deben ser números.")
    elif int(id_inicial) > int(id_final):
        print("El primer id debe ser menor al segundo")
    elif id_fuera_rango(id_inicial, nombre_archivo):
        print("No se pueden mostrar las reservas porque los id están fuera de rango.")

def imprimir_error_modificar_campo(lista_datos):
    if len(lista_datos) != 2:
        print("La cantidad de argumentos es incorrecta. Ingrese: campo nuevo_valor")
    elif lista_datos[POSICION_CAMPO] == CAMPO_NOMBRE and not es_nombre_valido(lista_datos[POSICION_NUEVO_VALOR_CAMPO]):
        print("El nombre no debe contener números.")
    elif lista_datos[POSICION_CAMPO] == CAMPO_CANTIDAD_PERSONAS and not es_cantidad_valida(lista_datos[POSICION_NUEVO_VALOR_CAMPO]):
        print("La cantidad de personas debe ser mayor a cero.")
    elif lista_datos[POSICION_CAMPO] == CAMPO_HORARIO and not es_horario_valido(lista_datos[POSICION_NUEVO_VALOR_CAMPO]):
        print("El horario debe ser entre las 00:00 y las 23:59.")
    elif lista_datos[POSICION_CAMPO] == CAMPO_UBICACION and not es_ubicacion_valida(lista_datos[POSICION_NUEVO_VALOR_CAMPO]):
        print("La ubicación debe ser válida (D o F).")
    else:
        print("El campo que desea cambiar es inválido, ingrese otro campo:")


def asignar_nuevo_formato(campo):
    if campo == CAMPO_ID:
        nuevo_formato = campo.upper()
    elif campo == CAMPO_CANTIDAD_PERSONAS:
        nuevo_formato = "Cantidad de personas"
    else:
        nuevo_formato = campo.capitalize()
    return nuevo_formato

def asignar_campo(columna):
    if columna == POSICION_CAMPO_ID:
        return CAMPO_ID.upper()
    if columna == POSICION_CAMPO_NOMBRE:
        return CAMPO_NOMBRE.upper()
    elif columna == POSICION_CAMPO_CANTIDAD_PERSONAS:
        return "Cantidad personas"
    elif columna == POSICION_CAMPO_HORARIO:
        return CAMPO_HORARIO.capitalize()
    elif columna == POSICION_CAMPO_UBICACION:
        return CAMPO_UBICACION.capitalize()

def nuevo_id(nombre_archivo):
    try:
        archivo = open(nombre_archivo)
    except:
        print("Error al abrir el archivo.")

    lector = csv.reader(archivo, delimiter=";")
    reservas = list(lector)
    if len(reservas) > SIN_RESERVAS:
        id = reservas[len(reservas) - 1][0]
    else:
        id = "0"
    archivo.close()
    return str(int(id) + 1)

def agregar_datos_archivo(id, nombre, cantidad_personas, hora, ubicacion, nombre_archivo):
    nueva_linea = [id, nombre, cantidad_personas, hora, ubicacion]
    
    try:
        archivo = open(nombre_archivo, "a")
    except:
        print("Error al abrir el archivo")
        return

    escritor = csv.writer(archivo, delimiter=";")
    escritor.writerow(nueva_linea)
    archivo.close()

def eliminar_datos_archivo(id, nombre_archivo):
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
        if linea[0] != id:
            escritor.writerow(linea)

    archivo.close()
    archivo_auxiliar.close()
    
    os.rename("datos_auxiliares.csv", nombre_archivo)

def modificar_datos_archivo(id, lista_datos, nombre_archivo):
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

def listar_rango_datos_archivo(id_inicial, id_final, nombre_archivo):
    es_valido = False      
    try:
        archivo = open(nombre_archivo)
    except:
        print("Error al abrir el archivo")
        return
    
    lector = csv.reader(archivo, delimiter=";")
    reservas = list(lector)
    
    for i in range(len(reservas)):
        for j in range(len(reservas[i])):
            if int(reservas[i][0]) >= int(id_inicial) and int(reservas[i][0]) <= int(id_final):
                print(f"{asignar_campo(j)}: {reservas[i][j]}")
                es_valido = True
        if es_valido:
            print("\n")
            es_valido = False
    archivo.close()

def listar_datos_archivo(nombre_archivo):
    try:
        archivo = open(nombre_archivo)
    except:
        print("Error al abrir el archivo")
        return
    
    lector = csv.reader(archivo, delimiter=";")
    reservas = list(lector)    
    for i in range(len(reservas)):
        for j in range(len(reservas[i])):
                print(f"{asignar_campo(j)}: {reservas[i][j]}")
        print("\n")
    archivo.close()

def realizar_reserva(nombre, cantidad_personas, hora, ubicacion, nombre_archivo):
    if es_nombre_valido(nombre) and es_cantidad_valida(cantidad_personas) and es_horario_valido(hora) and es_ubicacion_valida(ubicacion):
        id = nuevo_id(nombre_archivo)
        agregar_datos_archivo(id, nombre, cantidad_personas, hora, ubicacion, nombre_archivo)
        print("Se agregó con exito")
    else:
        imprimir_error_agregar(nombre, cantidad_personas, hora, ubicacion)

def cambiar_reserva(id, nombre_archivo):
    es_valido = False
    if id.isnumeric() and existe_id(id, nombre_archivo):
        while(not es_valido):
            datos = input("¿Qué desea cambiar?:")
            lista_datos = datos.split()
            if len(lista_datos) == CANTIDAD_ARGUMENTOS_MODIFICAR_CAMPO and ((lista_datos[POSICION_CAMPO] == CAMPO_NOMBRE and es_nombre_valido(lista_datos[POSICION_NUEVO_VALOR_CAMPO])) or (lista_datos[POSICION_CAMPO] == CAMPO_CANTIDAD_PERSONAS and es_cantidad_valida(lista_datos[POSICION_NUEVO_VALOR_CAMPO])) or (lista_datos[POSICION_CAMPO] == CAMPO_HORARIO and es_horario_valido(lista_datos[POSICION_NUEVO_VALOR_CAMPO])) or (lista_datos[POSICION_CAMPO] == CAMPO_UBICACION and es_ubicacion_valida(lista_datos[POSICION_NUEVO_VALOR_CAMPO]))):
                modificar_datos_archivo(id, lista_datos, nombre_archivo)
                print("Modificación exitosa.")
                es_valido = True
            else:
                imprimir_error_modificar_campo(lista_datos)
    else:
        imprimir_error_modificar(id, RESERVA)

def cancelar_reserva(id, nombre_archivo):
    if id.isnumeric() and existe_id(id, nombre_archivo):
        eliminar_datos_archivo(id, nombre_archivo)
        print("Se eliminó con éxito.")
    else:
        imprimir_error_eliminar(id, nombre_archivo)

def mostrar_reservas(id_inicial, id_final, nombre_archivo):
    if (id_inicial.isnumeric() and id_final.isnumeric()) and (id_inicial < id_final) and not id_fuera_rango(id_inicial, RESERVA):
        listar_rango_datos_archivo(id_inicial, id_final, nombre_archivo)
    else:
        imprimir_error_listar(id_inicial, id_final, nombre_archivo)

def main():
    if len(sys.argv) == 1:
        print("Cantidad de argumentos insuficientes.")
        return

    if not es_comando_valido(sys.argv[POSICiON_COMANDO]):
        print(f"{sys.argv[POSICiON_COMANDO]} no es un comando válido.")
        return

    if sys.argv[POSICiON_COMANDO] == COMANDO_AGREGAR and len(sys.argv) == CANTIDAD_ARGUMENTOS_AGREGAR:
        nombre = sys.argv[POSICION_NOMBRE]
        cant_personas = sys.argv[POSICION_CANTIDAD_PERSONAS]  
        horario = sys.argv[POSICION_HORARIO]
        ubicacion = sys.argv[POSICION_UBICACION]
        realizar_reserva(nombre, cant_personas, horario, ubicacion, RESERVA)
        return
    elif sys.argv[POSICiON_COMANDO] == COMANDO_MODIFICAR and len(sys.argv) == CANTIDAD_ARGUMENTOS_MODIFICAR:
        id = sys.argv[POSICION_ID]
        cambiar_reserva(id, RESERVA)
        return
    elif sys.argv[POSICiON_COMANDO] == COMANDO_ELIMINAR and len(sys.argv) == CANTIDAD_ARGUMENTOS_ELIMINAR:
        id = sys.argv[POSICION_ID]
        cancelar_reserva(id, RESERVA)
        return
    elif sys.argv[POSICiON_COMANDO] == COMANDO_LISTAR and len(sys.argv) == CANTIDAD_ARGUMENTOS_MINIMA_LISTAR:
        listar_datos_archivo(RESERVA)
        return
    elif sys.argv[POSICiON_COMANDO] == COMANDO_LISTAR and len(sys.argv) == CANTIDAD_ARGUMENTOS_MAXIMA_LISTAR:
        id_inicial = sys.argv[POSICION_ID_INICIAL]
        id_final = sys.argv[POSICION_ID_FINAL]
        mostrar_reservas(id_inicial, id_final, RESERVA)
        return
    else:
        print(f"Cantidad de argumentos insuficientes para {sys.argv[POSICiON_COMANDO]}.")
        return
    
if __name__ == "__main__":
    main()