import chess
import chess.svg
import typing
from os import system, name

### Overrides y redefiniciones de la librería python-chess ###

RANK_NAMES = ["1", "2", "3", "4", "5", "6", "7", "8"]
PIECE_NAMES = [None, "peón", "caballo", "alfíl", "torre", "reina", "rey"]
PieceType = int
Square = int

def square(file_index: int, rank_index: int) -> Square: return rank_index * 8 + file_index

def piece_name(piece_type: PieceType) -> str:
    return typing.cast(str, PIECE_NAMES[piece_type])

class BaseTablero(chess.Board):

    # Función que muestra por pantalla el tablero con las jugadas realizadas hasta el momento
    def unicode(self, *, invert_color: bool = False, borders: bool = False, empty_square: str = " ") -> str:
    
        builder = []

        for rank_index in range(7, -1, -1):
            if borders:
                builder.append("   ")
                builder.append("-" * 41)
                builder.append("\n")
                if(self.turn):
                    builder.append(RANK_NAMES[rank_index])
                else:
                    builder.append(RANK_NAMES[7-rank_index])
                builder.append("")

            for file_index in range(8):
                if(self.turn):
                    square_index = square(file_index, rank_index)
                else:
                    square_index = square(7-file_index, 7-rank_index)

                if borders:
                    builder.append("  | ")
                elif file_index > 0:
                    builder.append(" ")

                piece = self.piece_at(square_index)
                
                if piece:
                    builder.append(piece.unicode_symbol(invert_color=True))
                else:
                    builder.append(empty_square)

            if borders:
                builder.append("  |")

            if borders or rank_index > 0:
                builder.append("\n")

        if borders:
            builder.append("   ")
            builder.append("-" * 41)
            builder.append("\n")
            if(self.turn):
                builder.append("     a    b    c    d    e    f    g    h")
            else: 
                builder.append("     h    g    f    e    d    c    b    a")
 
        return "".join(builder)

# Función para limpiar la consola y poder actualizar el tablero 
def clear():
    # Limpia la consola de Windows
    if name == 'nt': _ = system('cls')
    
    # Limpia la consola de Mac o Linux
    else: _ = system('clear')
    
# Función que muestra información sobre la situación actual del tablero en la partida
def info(tableroJuego, listaJugadas, pieza_capturada, nombre_pieza):

    print("Escribe 'Guardar', 'Tablas' o 'Abandonar' en cualquier momento si quieres guardar, ofrecer tablas o abandonar la partida.\n")

    print(tableroJuego.unicode(borders=True, empty_square=" ") + "\n")   # Mostramos el tablero con la posición actual

    chess.svg.board(tableroJuego)

    # Si se ha capturado una pieza, muestra por pantalla qué pieza ha sido capturada
    if(pieza_capturada): 
        if(nombre_pieza == "reina"): print("¡Se ha capturado una reina!\n")
        else: print("¡Se ha capturado un {pieza}!\n".format(pieza=nombre_pieza))

    # Muestra la lista con las jugadas realizadas hasta el momento
    for i in range(len(listaJugadas)):
        print(listaJugadas[i])

    if(tableroJuego.is_check()): print("\n¡Jaque!")  # Indica si el jugador se encuentra en jaque

    return False    # Devolvemos la variable para actualizar su estado