import tablero

def nuevaJugada(tableroJuego, listaJugadas, blancas, negras):
   
    nuevaJugada = False     # Reiniciamos la variable para pedir una jugada nueva
    
    # A continuación creamos una lista en la que guardaremos información sobre la partida
    # La lista tiene el siguiente formato:
    # datos[0] -> Identificador de la jugada realizada -> T, G o J
    # datos[1] -> Indica si la jugada se ha realizado con éxito
    # Para T, datos[2] = tablas (Si se han aceptado o no las tablas)
    # Para G, datos[2] = guardado (Si se ha guardado y se quiere salir)
    # Para A, datos[2] = abandono (Si se ha abandonado la partida o no)
    # Para J, datos[2] = pieza_capturada (Si se ha capturado una pieza), datos[3] = nombre_pieza (Nombre de la pieza capturada)
    datos = [] 

    # Pedimos una jugada nueva al usuario. Seguirá pidiendo jugadas hasta que se introduzca una válida.
    while not nuevaJugada:            
        
        if(tableroJuego.turn): jugada = input("\nMueven blancas ({name}): ".format(name=blancas))
        else: jugada = input("\nMueven negras ({name}): ".format(name=negras))

        if(jugada == "Tablas"):
            datos = ofrecerTablas()
        elif(jugada == "Abandonar"):
            datos = abandonar()
        elif(jugada == "Guardar"):
            datos = guardarPartida(tableroJuego, listaJugadas, blancas, negras)
        else:
            datos = comprobarJugada(tableroJuego, listaJugadas, jugada)

        nuevaJugada = datos[1]

    return datos      

def ofrecerTablas():
    
    datos = []
    datos.append('T')  # Especificamos el tipo de jugada realizada
    jugada = input("Escribe 'Tablas' de nuevo para confirmar las tablas: ")
    
    # Guardamos el resto de las variables

    if(jugada == "Tablas"): 
        datos.append(True)
        datos.append(True)
    else: 
        print("Se han rechazado las tablas.")
        datos.append(False)
        datos.append(False)

    return datos

def abandonar():

    datos = []
    datos.append('A')  # Especificamos el tipo de jugada realizada
    jugada = input("Escribe 'Abandonar' de nuevo para confirmar el abandono: ")
    
    # Guardamos el resto de las variables

    if(jugada == "Abandonar"): 
        datos.append(True)
        datos.append(True)
    else: 
        print("No se ha abandonado la partida.")
        datos.append(False)
        datos.append(False)

    return datos

def guardarPartida(tableroJuego, listaJugadas, blancas, negras):
    
    datos = []
    datos.append('G')  # Especificamos el tipo de jugada realizada

    nombreArchivo = input("Introduzca el nombre donde va a guardar el archivo (terminado en .txt): ")

    try:  # Guardamos los datos de la partida en un archivo
        f = open(nombreArchivo, 'w')
        f.writelines(tableroJuego.fen() + "\n" + blancas + "\n" + negras + "\n" + str(len(listaJugadas)) + "\n")
        for i in range(len(listaJugadas)):
            f.write("{jugada}\n".format(jugada=listaJugadas[i]))
        f.close()
        intentoGuardado = True
    except OSError as notValid: # Si no se ha podido crear el archivo, lanzamos una excepción
        print("El formato del nombre del archivo no es válido.")

    if(intentoGuardado):        # Si se ha conseguido guardar, preguntamos al usuario si quiere continuar la partida o salir del juego
        jugada = input("La partida ha sido guardada con éxito. ¿Desea continuar jugando? (S/N): ")

        while jugada != 'S' and jugada != 'N':
            print("La instrucción introducida no es válida.\n")
            jugada = input("¿Desea continuar jugando? (S/N): ")
        
        # Guardamos el resto de las variables
        
        if(jugada == 'N'):
            datos.append(True)
            datos.append(True)
        else:
            datos.append(False)
            datos.append(False)
    else:
        datos.append(False)
        datos.append(False)

    return datos
    
def comprobarJugada(tableroJuego, listaJugadas, jugada):
    
    datos = []
    datos.append('J')  # Especificamos el tipo de jugada realizada

    # Definimos los estados base de las variables que vamos a devolver
    es_captura = False 
    nombre = ''
    jugadaRealizada = False

    try:
        movimiento = tableroJuego.parse_san(jugada)    # Comprueba si la jugada es legal y, en caso afirmativo, la convierte en un movimiento
        
        if(tableroJuego.is_capture(movimiento)):
            es_captura = True
            nombre = tablero.piece_name(tableroJuego.piece_type_at(movimiento.to_square))

        tableroJuego.push(movimiento)                  # Realiza el movimiento en el tablero
        jugadaRealizada = True

        if(not tableroJuego.turn):                     # Añadimos la jugada a la lista de movimientos en su posición correspondiente
            listaJugadas.append("{num}. {jugada}".format(num=tableroJuego.fullmove_number, jugada=jugada)) 
        else: listaJugadas[tableroJuego.fullmove_number-2] += "  {jugada}".format(jugada=jugada) 
    except ValueError as noLegal:                 # Si la jugada no es válida por error de sintaxis, lanzamos una excepción
        "La jugada introducida no es válida."
    if(not jugadaRealizada): print("La jugada introducida no es válida.")   # Si la jugada no es legal, pedimos otra jugada
    
    # Guardamos el resto de las variables

    datos.append(jugadaRealizada)
    datos.append(es_captura)
    datos.append(nombre)

    return datos

def final(tableroJuego, blancas, negras, tablas, guardado, abandono):
    print(tableroJuego.unicode(borders=True, empty_square=" "))              # Mostramos el tablero con el resultado final

    if(tableroJuego.is_checkmate and not tablas and not guardado and not abandono):           # Si la partida ha terminado por jaque mate, indica quién es el ganador
        if(not tableroJuego.turn):                                           # Comprobamos qué jugador realizó el jaque mate
            print("\n¡Jaque mate! El ganador ha sido " + blancas) 
        else: print("\n¡Jaque mate! El ganador ha sido " + negras)
    elif(not guardado and not tablas):
        if(not tableroJuego.turn):                                           # Comprobamos qué jugador ha ganado
            print("\nEl ganador ha sido {color} por abandono.".format(color=blancas)) 
        else: print("\nEl ganador ha sido {color} por abandono.".format(color=negras)) 
    elif(not guardado): print("\nLa partida ha terminado en tablas.")   # Si la partida no se guardó, indica que ha terminado en tablas
    else: print("\nSaliendo del programa...")                           # Si la partida no ha terminado y se guardó, sale del programa