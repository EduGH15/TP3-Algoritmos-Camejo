import sys
import csv
import os

RESERVA = "reservas.csv"
AUXILIAR = "datos_auxiliares.csv"

CANTIDAD_ARGUMENTOS_AGREGAR = 6
CANTIDAD_ARGUMENTOS_MODIFICAR = 3
CANTIDAD_ARGUMENTOS_ELIMINAR = 3
CANTIDAD_ARGUMENTOS_MINIMA_LISTAR = 2
CANTIDAD_ARGUMENTOS_MAXIMA_LISTAR = 4
CANTIDAD_ARGUMENTOS_MODIFICAR_CAMPO = 2
CANTIDAD_ARGUMENTOS_INSUFICIENTES = 1

POSICiON_COMANDO = 1
POSICION_ID = 2
POSICION_NOMBRE = 2
POSICION_CANTIDAD_PERSONAS = 3
POSICION_HORARIO = 4
POSICION_UBICACION = 5
POSICION_ID_INICIAL = 2
POSICION_ID_FINAL = 3
POSICION_INVALIDA = -1

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
NUEVO_CANTIDAD_PERSONAS = "Cantidad de personas"

LONGITUD_CAMPO_HORARIO = 5
SIN_RESERVAS = 0
SIN_FORMATO = " "
ID_INICIAL = "1"
LINEA_VACIA = []
DIVISION_HORARIA = ":"
UBICACION_AFUERA = "F"
UBICACION_ADENTRO = "D"

#Pre:El parámetro campo debe ser un string.
#Post: Dado un campo ("nombre" o "cant" u "hora" o "ubicación") le asigna la posición 1 o 2 o 3 o 4 respectivamente. En caso de que el campo no sea el esperado, devuelve -1.
def asignar_posicion(campo):
    nueva_posicion = POSICION_INVALIDA
    if campo == CAMPO_NOMBRE:
        nueva_posicion = POSICION_CAMPO_NOMBRE
    elif campo == CAMPO_CANTIDAD_PERSONAS:
        nueva_posicion = POSICION_CAMPO_CANTIDAD_PERSONAS
    elif campo == CAMPO_HORARIO:
        nueva_posicion = POSICION_CAMPO_HORARIO
    elif campo == CAMPO_UBICACION:
        nueva_posicion = POSICION_CAMPO_UBICACION
    return nueva_posicion

#Pre: El parámetro campo debe de ser válido ("nombre" o "cant" u "hora" o "ubicación").
#Post:Dado un campo ("nombre" o "cant" u "hora" o "ubicación") le asigna un nuevo formato. Si el campo es un id, lo convierte en mayúscula. Si el campo es "cant", el nuevo formato
#será "Cantidad de personas". Para el resto de los campos, su primera letra se transforma en mayúscula.
def asignar_nuevo_formato(campo):
    nuevo_formato = SIN_FORMATO
    if campo == CAMPO_ID:
        nuevo_formato = campo.upper()
    elif campo == CAMPO_CANTIDAD_PERSONAS:
        nuevo_formato = NUEVO_CANTIDAD_PERSONAS
    else:
        nuevo_formato = campo.capitalize()
    return nuevo_formato

#Pre:El parámetro columna debe ser un número entre 0 y 4 (ambos inclusives).
#Post: Dado un número de columna, se devuelve a qué campo corresponde.
def asignar_campo(columna):
    if columna == POSICION_CAMPO_ID:
        return CAMPO_ID.upper()
    if columna == POSICION_CAMPO_NOMBRE:
        return CAMPO_NOMBRE.capitalize()
    elif columna == POSICION_CAMPO_CANTIDAD_PERSONAS:
        return NUEVO_CANTIDAD_PERSONAS
    elif columna == POSICION_CAMPO_HORARIO:
        return CAMPO_HORARIO.capitalize()
    elif columna == POSICION_CAMPO_UBICACION:
        return CAMPO_UBICACION.capitalize()

#Pre: El archivo que se pase por parámetro, debe de existir.
#Post: Dado un archivo, devuelve un nuevo id que es igual al último id + 1. En caso de que el archivo esté vacio, el nuevo id será 1.
def nuevo_id(nombre_archivo):
    try:
        archivo = open(nombre_archivo)
    except:
        return ID_INICIAL

    lector = csv.reader(archivo, delimiter=";")
    reservas = list(lector)
    if len(reservas) != SIN_RESERVAS:
        id = reservas[len(reservas) - 1][0]
    else:
        id = "0"
    archivo.close()
    return str(int(id) + 1)

#----------------------------------------------VALIDACIONES---------------------------------------------
#Pre: El parámetro horario debe ser un string.
#Post Dado un horario, devuelve false si no se encuentra entre las 00:00 y las 23:59 o si contiene letras.
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

#Pre: Ubicacion debe ser un string.
#Post: Devuelve True si la ubicacion es "F" p "D"
def es_ubicacion_valida(ubicacion):
    return ubicacion == UBICACION_AFUERA or ubicacion == UBICACION_ADENTRO

#Pre:cantidad debe ser un string.
#Post: Devuelve True si cantidad no contiene otras letras y si es un número mayor a cero.
def es_cantidad_valida(cantidad):
    return cantidad.isnumeric() and int(cantidad) > 0

#Pre: El parámetro comando debe ser un string.
#Post: Devuelve True si comando es igual a "Agregar", "eliminar", "modificar" o "listar"
def es_comando_valido(comando):
    return comando == COMANDO_AGREGAR or comando == COMANDO_MODIFICAR or comando == COMANDO_ELIMINAR or comando == COMANDO_LISTAR

#------------------------------------------MOSTRAR POR PANTALLA-------------------------------------------

#Pre:Todos los parámetros deben de ser strings
#Post: Imprime un mensaje de error si la cantidad de personas es mayor o igual a cero, o si el horario no está entre las 00:00 y las 23:59, o si la ubicacion no es "D" ni "F"
def imprimir_error_agregar(cantidad_personas, hora, ubicacion):
    if not es_cantidad_valida(cantidad_personas):
        print("La cantidad de personas ingresadas es inválida. Ingrese un número mayor a cero.")
    elif not es_horario_valido(hora):
        print("El horario es inválido. Ingrese un horario entre las 00:00 y las 23:59.")
    elif not es_ubicacion_valida(ubicacion):
        print("La ubicación es inválida. Ingrese D o F.")

#Pre: Todos los parámetros deben ser strings.
#Post: Devuelve un mensaje de error si alguno de los dos no son números o si el primer id es mayor al segundo.
def imprimir_error_listar(id_inicial, id_final):
    if not id_inicial.isnumeric() or not id_final.isnumeric():
        print("Ambos id deben ser números.")
    elif int(id_inicial) > int(id_final):
        print("El primer id debe ser menor al segundo.")

#Pre: El parámetro lista_datos debe de ser un array que solo contenga strings. Lista_datos[0] debe ser un campo y lista_datos[1] debe ser un valor de dicho campo.
#Post: Imprime un mensaje de error si la longitud del array es distinta de 2 o si el campo no es "nombre" o "cant" u "hora" o "ubicacion". También imprime error si el valor del campo
#no es válido.
def imprimir_error_modificar_campo(lista_datos):
    if len(lista_datos) != CANTIDAD_ARGUMENTOS_MODIFICAR_CAMPO:
        print("La cantidad de argumentos es incorrecta. Ingrese: campo nuevo_valor")
    elif lista_datos[POSICION_CAMPO] == CAMPO_CANTIDAD_PERSONAS and not es_cantidad_valida(lista_datos[POSICION_NUEVO_VALOR_CAMPO]):
        print("La cantidad de personas debe ser mayor a cero.")
    elif lista_datos[POSICION_CAMPO] == CAMPO_HORARIO and not es_horario_valido(lista_datos[POSICION_NUEVO_VALOR_CAMPO]):
        print("El horario debe ser entre las 00:00 y las 23:59.")
    elif lista_datos[POSICION_CAMPO] == CAMPO_UBICACION and not es_ubicacion_valida(lista_datos[POSICION_NUEVO_VALOR_CAMPO]):
        print("La ubicación debe ser válida (D o F).")
    else:
        print("El campo que desea cambiar es inválido, ingrese otro campo.")

#----------------------------------------- MODIFICACIONES DE ARCHIVO ---------------------------------------
#Pre: los parámetros nombre, cantidad_personas, hora, ubicacion deben ser strings válidos, y el archivo debe existir.
#Post: Agrega los nuevos datos al final del archivo con un nuevo ID.
def agregar_datos_archivo(id, nombre, cantidad_personas, hora, ubicacion, nombre_archivo):
    try:
        archivo = open(nombre_archivo, "a")
    except:
        print("Error al abrir el archivo.")
        return
    
    nueva_linea = [id, nombre, cantidad_personas, hora, ubicacion]
    escritor = csv.writer(archivo, delimiter=";")
    escritor.writerow(nueva_linea)
    archivo.close()
    print("Se agregó con exito")

#Pre: El parámetro id debe ser un string y el archivo debe existir.
#Post: Dado un id, elimina todos los datos relacionados a ese id. Si el id no existe, imprime un mensaje de error.
def eliminar_datos_archivo(id, nombre_archivo):
    try:
        archivo = open(nombre_archivo)
    except:
        print("Error al abrir el archivo.")
        return
    
    try:
        archivo_auxiliar = open(AUXILIAR, "w")
    except:
        archivo.close()
        print("Error al abrir el archivo auxiliar.")
        return
    
    es_eliminado = False
    lector = csv.reader(archivo, delimiter=";")
    escritor = csv.writer(archivo_auxiliar, delimiter=";")
    for linea in lector:
        if linea[0] != id:
            escritor.writerow(linea)
        else:
            es_eliminado = True

    archivo.close()
    archivo_auxiliar.close()
    os.rename(AUXILIAR, nombre_archivo)
    if es_eliminado:
        print("La reserva fue eliminada exitosamente.")
    else:
        print("La reserva no se pudo eliminar porque el id no existe.")

#Pre: El parámetro id debe ser un string válido, la lista de datos debe ser un array válido y el archivo debe existir.
#Post: Dado un id, un campo y un nuevo valor relacionado a ese campo, modifica el valor de dicho campo relacionado a ese id. Si el id no existe, imprime un
#mensaje de error.
def modificar_datos_archivo(id, lista_datos, nombre_archivo):
    try:
        archivo = open(nombre_archivo)
    except:
        print("Error al abrir el archivo")
        return
    
    try:
        archivo_auxiliar = open(AUXILIAR, "a")
    except:
        archivo.close()
        print("Error al abrir el archivo auxiliar")
        return
    
    campo = lista_datos[POSICION_CAMPO]
    valor_campo = lista_datos[POSICION_NUEVO_VALOR_CAMPO]
    posicion_campo_columna = asignar_posicion(campo)
    nueva_linea = LINEA_VACIA
    es_modificado = False

    lector = csv.reader(archivo, delimiter=";")
    escritor = csv.writer(archivo_auxiliar, delimiter=";")
    reservas = list(lector)

    for i in range(len(reservas)):
        nueva_linea = reservas[i].copy()
        if reservas[i][0] == id and not es_modificado:
            nueva_linea[posicion_campo_columna] = valor_campo
            es_modificado = True
        escritor.writerow(nueva_linea)

    archivo.close()
    archivo_auxiliar.close()
    os.rename(AUXILIAR, nombre_archivo)

    if es_modificado: 
        print("Modificación exitosa.")
    else:
        print("La reserva no pudo ser modificada porque el id no existe.")

#Pre: Los parametros id_inicial e id_final deben ser strings válidos. El archivo debe de existir.
#Post: Dado un id_inicial y un id_final, muestra todas las reservas entre ese rango de id. En caso de que el id_inicial sea mayor al ultimo id del archivo, se
#imprime un mensaje de error.
def listar_rango_datos_archivo(id_inicial, id_final, nombre_archivo):
    try:
        archivo = open(nombre_archivo)
    except:
        print("Error al abrir el archivo.")
        return
    
    es_valido = False      
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
    if int(reservas[len(reservas) - 1][0]) < int(id_inicial):
        print("No se encuentra ninguna reserva dentro de este rango.")
    archivo.close()

#Pre: El parámetro archivo debe existir.
#Post: Dado un archivo, muestra todos las reservas presentes en el archivo. Si está vacio, no muestra nada.
def listar_datos_archivo(nombre_archivo):
    try:
        archivo = open(nombre_archivo)
    except:
        print("Error al abrir el archivo.")
        return
    
    lector = csv.reader(archivo, delimiter=";")
    reservas = list(lector)    
    for i in range(len(reservas)):
        for j in range(len(reservas[i])):
                print(f"{asignar_campo(j)}: {reservas[i][j]}")
        print("\n")
    archivo.close()

#--------------------------------------------PROGRAMAS-----------------------------------------------
#Pre: Los parámetros nombre, cantidad_personas, hora, ubicacion deben ser strings y el archivo debe existir.
#Post: Realiza una reserva con los datos que se le pasen por parámetro. En caso de que sean inválidos, imprime un mensaje de error.
def realizar_reserva(nombre, cantidad_personas, hora, ubicacion, nombre_archivo):
    if es_cantidad_valida(cantidad_personas) and es_horario_valido(hora) and es_ubicacion_valida(ubicacion):
        id = nuevo_id(nombre_archivo)
        agregar_datos_archivo(id, nombre, cantidad_personas, hora, ubicacion, nombre_archivo)
    else:
        imprimir_error_agregar(cantidad_personas, hora, ubicacion)

#Pre: El parámetro id debe ser un string y el archivo debe existir.
#Post: Realiza un cambio en la reserva en caso de que el id sea válido. Si el id es inválido, imprime un mensaje de error.
def cambiar_reserva(id, nombre_archivo):
    es_valido = False
    if id.isnumeric():
        while not es_valido:
            datos = input("¿Qué desea cambiar?:")
            lista_datos = datos.split()
            if len(lista_datos) == CANTIDAD_ARGUMENTOS_MODIFICAR_CAMPO and ((lista_datos[POSICION_CAMPO] == CAMPO_NOMBRE) or (lista_datos[POSICION_CAMPO] == CAMPO_CANTIDAD_PERSONAS and es_cantidad_valida(lista_datos[POSICION_NUEVO_VALOR_CAMPO])) or (lista_datos[POSICION_CAMPO] == CAMPO_HORARIO and es_horario_valido(lista_datos[POSICION_NUEVO_VALOR_CAMPO])) or (lista_datos[POSICION_CAMPO] == CAMPO_UBICACION and es_ubicacion_valida(lista_datos[POSICION_NUEVO_VALOR_CAMPO]))):
                modificar_datos_archivo(id, lista_datos, nombre_archivo)
                es_valido = True
            else:
                imprimir_error_modificar_campo(lista_datos)
    else:
        print("El id debe ser un número.")

#Pre: El parámetro id debe ser un string y el archivo debe existir.
#Post: Realiza una eliminación de la reserva en caso de que el id sea válido. Si el id es inválido, imprime un mensaje de error.
def cancelar_reserva(id, nombre_archivo):
    if id.isnumeric():
        eliminar_datos_archivo(id, nombre_archivo)
    else:
        print("El id debe ser un número")

#Pre: Los parametros id_inicial e id_final deben ser strings y el archivo debe existir.
#Post: Dado un id_inicial y un id_final, muestra todas las reservas en ese intervalo. En caso de que alguno de los id sean inválidos, imprime un mensaje de error.
def mostrar_reservas(id_inicial, id_final, nombre_archivo):
    if (id_inicial.isnumeric() and id_final.isnumeric()) and (id_inicial < id_final):
        listar_rango_datos_archivo(id_inicial, id_final, nombre_archivo)
    else:
        imprimir_error_listar(id_inicial, id_final)

def main():
    if len(sys.argv) == CANTIDAD_ARGUMENTOS_INSUFICIENTES:
        print("Cantidad de argumentos insuficientes.")
        return

    if not es_comando_valido(sys.argv[POSICiON_COMANDO]):
        print(f"{sys.argv[POSICiON_COMANDO]} no es un comando válido.")
        return

    if sys.argv[POSICiON_COMANDO] == COMANDO_AGREGAR and len(sys.argv) == CANTIDAD_ARGUMENTOS_AGREGAR:
        nombre = sys.argv[POSICION_NOMBRE]
        cantidad_personas = sys.argv[POSICION_CANTIDAD_PERSONAS]  
        hora = sys.argv[POSICION_HORARIO]
        ubicacion = sys.argv[POSICION_UBICACION]
        realizar_reserva(nombre, cantidad_personas, hora, ubicacion, RESERVA)
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
        print(f"Cantidad de argumentos insuficientes para el comando: {sys.argv[POSICiON_COMANDO]}.")
        return
    
if __name__ == "__main__":
    main()