# TODO
from cs50 import get_int

# ciclo infinito
while True:
    # leer altura de la piramide
    height = get_int("Height: ")
    if height > 0 and height < 9:
        break
# iterar sobre la altura
for row in range(height):
    # impresion de los espacios
    for space in range(height - row - 1, 0, -1):
        print(" ", end="")
    # impresion del hash
    for hash in range(row + 1):
        print("#", end="")
    # salto de linea
    print("\n", end="")