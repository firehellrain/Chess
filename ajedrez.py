import tablero
import inicio
import partida

### Variables y funciones para el control del juego ###

tableroJuego = tablero.BaseTablero() # Variable para guardar el tablero con el que se juega y todas las propiedades de su clase
listaJugadas = []       # Lista para guardar la secuencia de jugadas que se hagan durante la partida
datos = []              # Lista para guardar los datos de una partida cargada
blancas = "blancas"     # Variable para guardar el nombre del usuario que juega con blancas
negras = "negras"       # Variable para guardar el nombre del usuario que juega con negras
nombre_pieza = ""       # Variable para guardar el nombre de la pieza que se haya comido en caso de que haya una captura

tablas = False          # Será True cuando la partida acabe en tablas o sean tablas por mútuo acuerdo
abandono = False        # Será True cuando un jugador abandone la partida
guardado = False        # Será True cuando se guarde la partida y se quiera salir del programa. NO será True si se guarda y se sigue jugando
nuevaPartida = True     # Será False cuando se quiera cargar una partida (y se consiga cargar exitosamente)
intentoGuardado = False # Será True cuando se consiga guardar la partida exitosamente
pieza_capturada = False # Será True cuando se haya capturado una pieza en la última jugada

### Inicio del Juego ###

print("\n¡Bienvenido al juego de Ajedrez!\n")

juego = input("¿Desea iniciar una partida nueva o cargar una existente? (N/C): ")
while juego != 'C' and juego != 'N':
    print("La instrucción introducida no es válida.\n")
    juego = input("¿Desea iniciar una partida nueva o cargar una existente? (N/C): ")
tablero.clear()

if(juego == 'C'): 
    # Cargamos los datos del archivo que se ha buscado y los guardamos en sus respectivas variables
    datos = inicio.cargarPartida()
    if(len(datos)!=0):
        tableroJuego = tablero.BaseTablero(datos[0])
        blancas = datos[1].strip()
        negras = datos[2].strip()
        cont = 4    # Quinta posición de nuestra lista de datos, donde están guardadas las jugadas de la partida
        for i in range(int(datos[3])):
            listaJugadas.append(datos[cont].strip())
            cont += 1
if(juego == 'N' or len(datos) == 0): 
    # Cargamos los datos y los guardamos en sus respectivas variables
    datos = inicio.crearPartida()

    tableroJuego = datos[0]

    if(datos[3] == 0):
        blancas = datos[1]      
        negras = datos[2]
    else:
        blancas = datos[2]
        negras = datos[1]

print("{blancas} juega con blancas, {negras} juega con negras.\n".format(blancas=blancas, negras=negras))

# Comienza la partida, la cual continuará mientras hasta que se termine o se quiera salir de ella
while not tableroJuego.is_game_over() and not tablas and not guardado and not abandono:

    # Primero mostramos la situación actual de la partida: Tablero, Jugadas Realizadas, Situación
    pieza_capturada = tablero.info(tableroJuego, listaJugadas, pieza_capturada, nombre_pieza)

    # A continuación pedimos una jugada al usuario
    datos = partida.nuevaJugada(tableroJuego, listaJugadas, blancas, negras)

    if(datos[0] == 'T'):
        tablas = datos[2]
    elif(datos[0] == 'A'):
        abandono = datos[2]
    elif(datos[0] == 'G'):
        guardado = datos[2]
    elif(datos[0] == 'J'):
        pieza_capturada = datos[2]
        nombre_pieza = datos[3]

    tablero.clear() # Limpiamos la consola

partida.final(tableroJuego, blancas, negras, tablas, guardado, abandono)