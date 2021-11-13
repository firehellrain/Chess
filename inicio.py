import random
import tablero

# Si se ha indicado por el usuario, cargamos la partida del archivo indicado. En caso de que no exista, creamos una nueva.
def cargarPartida():
    
    datos = []
    
    nombreArchivo = input("Introduzca el nombre del archivo con la partida guardada: ")
    try:
        f = open(nombreArchivo, "r")
        if(not f.read(1)):  # Si el archivo está vacío, creamos una partida nueva
            print("No se ha encontrado partida cargada. Creando una nueva en su lugar...\n")
            f.close()
        else:   # Creamos una lista donde guardamos los datos del archivo
            f.seek(0)
            datos = f.readlines()
            f.close()
    except OSError as os:   # Si no existe el archivo, lanzamos una excepción
        print("El formato no es válido o no existe partida guardada con ese nombre. Creando una nueva en su lugar...\n")
    
    return datos

# Si no se ha encontrado partida cargada o se especifica por el usuario, creamos una partida nueva
def crearPartida():

    datos = []
    
    datos.append(tablero.BaseTablero('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'))   # Tablero de ajedrez clásico
    datos.append(input("Introduzca el nombre del primer jugador: "))                               # Nombre del Jugador 1
    datos.append(input("Introduzca el nombre del segundo jugador: "))                             # Nombre del Jugador 2
    datos.append(random.randint(0, 1))                                                           # Num aleatorio para elegir quien empieza

    return datos
